"""
GMAIL AGENT: Reads your recent unread emails, uses Claude to classify them
and draft a reply, then saves the reply as a DRAFT in your Gmail
(does NOT send anything). You review and approve/send from your phone
or computer, just like any normal Gmail draft.

First run will open a browser window asking you to log in and approve
access -- that's normal, it's Google confirming YOU are authorizing this.

Run it with:  python gmail_agent.py
"""

import os
import base64
import json
from email.mime.text import MIMEText

import anthropic
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail permissions we're requesting: read emails + create drafts.
# "modify" scope includes both reading and creating drafts (but not
# permanently deleting anything).
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# How many recent unread emails to process each time you run this.
MAX_EMAILS = 5


def get_gmail_service():
    """Handles Google login. First time: opens a browser to approve access
    and saves a token.json file so you don't have to log in every time."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def get_email_body(payload):
    """Gmail stores email content in a nested structure -- this digs out
    the plain text part."""
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data", "")
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    else:
        data = payload["body"].get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    return "(no readable text content)"


def classify_and_draft(client, subject, sender, body):
    """Asks Claude to read the email and write a category + draft reply."""
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""You are drafting a reply on behalf of ME, the person who RECEIVED this email
in my own inbox. I am the recipient, not the sender. Write the reply in MY voice,
as if I am personally responding to the sender below -- do not take on the sender's
role, perspective, or goals (e.g. if they are trying to sell me something or ask me
something, reply as the person being asked/sold to, not as them).

Read this email and respond with ONLY a raw JSON object.
No markdown, no backticks, no explanation. Two fields:
- "category": one of Urgent, Billing, Support, Sales, Spam, Personal, Other
- "draft_reply": a short, professional reply (2-4 sentences), written as MY reply to the sender

From: {sender}
Subject: {subject}
Body: {body[:2000]}"""
            }
        ]
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def create_draft_reply(service, gmail_message, reply_text, subject, sender):
    """Creates a Gmail draft reply in the same thread as the original email."""
    thread_id = gmail_message["threadId"]
    to_address = sender

    reply_subject = subject if subject.lower().startswith("re:") else f"Re: {subject}"

    message = MIMEText(reply_text)
    message["to"] = to_address
    message["subject"] = reply_subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    draft_body = {
        "message": {
            "raw": raw,
            "threadId": thread_id
        }
    }
    service.users().drafts().create(userId="me", body=draft_body).execute()


def main():
    print("Connecting to Gmail...")
    gmail = get_gmail_service()
    claude = anthropic.Anthropic()

    print(f"Fetching up to {MAX_EMAILS} recent unread emails...")
    results = gmail.users().messages().list(
        userId="me", labelIds=["INBOX", "UNREAD"], maxResults=MAX_EMAILS
    ).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No unread emails found.")
        return

    for msg_meta in messages:
        msg = gmail.users().messages().get(userId="me", id=msg_meta["id"], format="full").execute()
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        subject = headers.get("Subject", "(no subject)")
        sender = headers.get("From", "(unknown sender)")
        body = get_email_body(msg["payload"])

        print(f"\nProcessing: {subject} (from {sender})")
        result = classify_and_draft(claude, subject, sender, body)
        print(f"  Category: {result['category']}")

        create_draft_reply(gmail, msg, result["draft_reply"], subject, sender)
        print("  Draft reply saved to your Gmail Drafts folder.")

    print("\nDone. Open Gmail (phone or computer) and check your Drafts folder to review.")


if __name__ == "__main__":
    main()
