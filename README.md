# Gmail AI Assistant

An AI-powered agent that reads unread Gmail messages, classifies them, and drafts context-aware replies directly into Gmail Drafts — **never sends anything automatically**. Every reply is reviewed and approved by a human before going out.

## What it does

- Connects to Gmail via official Google OAuth
- Fetches recent unread emails
- Uses Claude (Anthropic) to:
  - Categorize each email (`Urgent`, `Billing`, `Support`, `Sales`, `Spam`, `Personal`, `Other`)
  - Draft a reply written in the recipient's voice
- Saves the draft into the correct Gmail thread

See [`case-study.md`](./case-study.md) for the full write-up of the problem this solves and the results.

## Setup

### 1. Requirements

- Python 3.10+
- A Google Cloud project with the Gmail API enabled, and an OAuth `credentials.json` file
- An Anthropic API key

### 2. Install dependencies

```bash
pip install anthropic google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 3. Set your Anthropic API key

**Windows (cmd):**
```cmd
setx ANTHROPIC_API_KEY "your-key-here"
```

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 4. Add your Gmail credentials

Place your `credentials.json` (from Google Cloud Console) in the project root. **Never commit this file** — see `.gitignore`.

### 5. Run it

```bash
python gmail_agent.py
```

The first run opens a browser window for you to authorize Gmail access. After that, a `token.json` is saved locally so you won't need to log in again.

## Configuration

- `MAX_EMAILS` in `gmail_agent.py` controls how many unread emails are processed per run (default: 5)

## Security notes

- No credentials, tokens, or API keys are stored in this repository
- The agent only ever **creates drafts** — it never sends email on its own
- Gmail access uses the `gmail.modify` scope (read + create drafts), not full account access

## License

MIT (or update as needed)
