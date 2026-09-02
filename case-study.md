# AI Email Assistant: Automated Inbox Triage & Draft Replies
### Built three ways — Python, no-code AI agent (Cowork), and no-code automation (Zapier)

## The Problem

Busy professionals lose significant time each day reading through unread emails, deciding how to categorize them, and writing replies — especially for repetitive or routine messages. Manually triaging an inbox is one of the most common productivity drains in any small business or freelance operation.

## The Solution

I built an AI-powered email assistant that connects securely to Gmail and automatically:

- **Reads** recent unread emails
- **Classifies** each one (Urgent, Billing, Support, Sales, Spam, Personal, Other)
- **Drafts a reply** in the user's own voice, tailored to the specific email
- **Saves the draft directly into Gmail** — nothing is ever sent automatically

The user stays in full control: every draft is reviewed and approved by a human before it goes out.

To demonstrate range, I implemented the same solution three different ways, each suited to a different kind of client:

## Version 1: Python + Anthropic API + Gmail API

A custom script for clients who want full control, version-controlled code, and the ability to extend the logic freely (custom rules, integrations with other internal systems, scheduled runs, etc.). Best fit: technical teams or clients with an in-house developer who will maintain it long-term.

## Version 2: Claude Cowork (AI agent, no code)

The same workflow, run by an AI agent through plain-language instructions instead of code, with the process packaged into a reusable Skill. Best fit: solo professionals or small teams who want something running today, fully customizable through conversation, with no code to maintain.

## Version 3: Zapier (no-code automation, no code)

A visual, three-step automation (Gmail trigger → Claude drafts a reply → Gmail saves the draft) built entirely through Zapier's interface. Best fit: clients who want a standard, easy-to-hand-off automation tool that their own team can view and adjust without technical help — and that runs continuously in the background without any app needing to stay open.

## How It Works (all three versions)

1. Connect to Gmail (OAuth or one-click login — no passwords handled directly)
2. New/unread email content is sent to Claude with instructions to draft a reply *as the recipient*, not as a generic assistant or as the sender
3. Claude classifies the message and writes a short, professional reply in the user's voice
4. The reply is saved as a Gmail draft in the correct thread — never sent automatically

## Result

- **Minutes saved per inbox pass** — no more reading and re-reading routine emails
- **Zero risk of accidental sends** — everything lands as a draft, human review required
- **Consistent, professional tone** across every reply
- **Delivered in the format that fits the client** — code, AI agent, or no-code automation

## Tech Stack

- Python, Gmail API (OAuth 2.0), Anthropic Claude API
- Claude Cowork (AI agent platform, Anthropic)
- Zapier (no-code automation platform)

## Availability

This workflow adapts to any inbox-heavy business — customer support teams, sales reps, solo consultants, agencies managing multiple client inboxes. Categories, tone, and business rules are fully customizable per client, and I can deliver in whichever format (code, AI agent, or no-code) best fits how the client's team works.

---
*Interested in a similar automation for your inbox or workflow? Let's talk about what's eating up your time.*
