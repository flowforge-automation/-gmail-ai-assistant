# MEMORY — persistent state for the Gmail Triage Agent

This is the agent's long-term memory. It is a plain file, not magic: the
agent is instructed (in `CLAUDE.md`) to read it at the start of every
session and append to it at the end. Because it's a file in this repo
(not a chat), it works the same whether you run the agent from the CLI,
from Claude Code on the web, or from a scheduled trigger — and it survives
across sessions, machines, and people.

Keep entries short and dated. Never delete a past entry — mark it
superseded instead, so the history stays auditable.

## Mailboxes this agent has run against

This agent isn't tied to one inbox. Each mailbox gets its own taxonomy below
because the mail mix is completely different (freelance/business inbox vs.
personal inbox). When starting a run, check which mailbox is connected
before applying a taxonomy.

### `thanostonia86@gmail.com` — freelance/business inbox
Original design target (Upwork job alerts, client mail). Categories:
`Urgent, Billing, Support, Sales, Spam, Personal, Other` (kept in sync with
`../gmail_agent.py`).

### `kyratzis7@gmail.com` — personal inbox
Added 2026-09-17. Mostly retail/marketing noise, not client work. Draft
replies are **not** appropriate here (almost everything is no-reply/automated) —
this mailbox only gets categorized + labeled, never drafted, unless the human
asks otherwise for a specific thread. Gmail labels used (create if missing,
`list_labels` first to get IDs — 4 already existed as user labels before this
agent touched the mailbox, 4 were created):

| Label | Sender pattern (domain/address) |
|---|---|
| `Αγορές/Προσφορές` (existing→reused: no; created) | `*.aliexpress.com` (selections/newarrival/mail/promotion subdomains, **not** `notice.aliexpress.com` or `safetyprotection@`), `*.temuemail.com`, `m1.email.samsung.com`, `mail.adobe.com`, `nedm.asus.com`, `*.nespresso.com`, `vendora.gr`, `pulze.gr`, `info.skroutz.gr` (newsletter@, **not** bare `skroutz.gr`), `coffeeisland.gr` |
| `Παραγγελίες` (created) | `orders.temu.com`, `notice.aliexpress.com`, `ecommerce-support@skroutz.gr`, `noreply@skroutz.gr` (bare domain = order/review, not marketing), `bestprice.gr`, `boxnow.gr` |
| `Αποδεικτικά` (existing, reused) | `klarna.gr`, `tbibank.eu`, `mail.anthropic.com`, `googleplay-noreply@google.com` |
| `Ασφάλεια` (created) | `github.com`, `transactional.n8n.io`, `account.temu.com` (verification codes), `accounts.google.com` / `noreply-accounts@google.com` (account/OAuth notices), `safetyprotection@aliexpress.com` |
| `Εργασία` (existing, reused) | `notify-noreply@google.com` (Jooble/Jobfind job alerts), `alerts@mail.zapier.com` (⚠️ "held tasks" = a real Zap may be broken — flag to human, don't just file away), `notifications.freelancer.com` |
| `Ενημερωτικά` (created) | `pinterest.com` (all recommendations@ subdomains), `quora.com`, `email.openai.com`, `learn@send.zapier.com` / `updates@send.zapier.com` |
| `Ταξίδι` (existing, reused) | `marketing.ryanairemail.com`, `news.ferryhopper.com`, `info.wise.com` |
| `Προσωπικό` (existing, reused) | `thanostonia86@gmail.com` (see Known contacts below) — genuine correspondence, never auto-file without reading first |

Notes for the next run on this mailbox:
- `temu.com` has multiple purposes by subdomain: `eu.temuemail.com` /
  `eu-shop.temuemail.com` / `info.temuemail.com` = marketing;
  `orders.temu.com` / `notice@orders.temu.com` = real order updates;
  `account.temu.com` = verification codes. Don't lump them together.
- `skroutz.gr` similarly splits: `info.skroutz.gr` (newsletter@) = marketing,
  bare `skroutz.gr` (ecommerce-support@, noreply@) = real order/review flow.
- `google.com` sends three unrelated things from this one domain:
  `notify-noreply@` = job alerts (Εργασία), `noreply-accounts@` /
  `no-reply@accounts.google.com` = account security notices (Ασφάλεια),
  `googleplay-noreply@` = billing receipts (Αποδεικτικά). Match on full
  address, not just domain.
- Scope any bulk run to a bounded window (e.g. `newer_than:45d`) and check
  `list_labels` → `UNREAD.threadsUnread` first — this mailbox had 6,219
  unread threads going back to 2022 when first touched; don't assume
  "is:unread" is a small number.
- Marking-as-read at scale (hundreds+) is not practical via one-by-one API
  calls — point the human at Gmail's own bulk UI ("select all N matching" +
  mark as read) instead of trying to loop it yourself.

## Sender preferences

<!-- Format: - **sender/domain** — rule — (date added) -->
- *(none yet for thanostonia86@gmail.com — will fill in as corrections happen)*
- See the `kyratzis7@gmail.com` taxonomy table above for that mailbox's
  sender→category routing (added 2026-09-17).

## Category corrections

<!-- When the human re-categorizes a draft the agent got wrong, record
     the pattern here so it isn't repeated. -->
- *(none yet)*

## Tone / voice rules

<!-- e.g. "with client X, always sign off with first name only" -->
- *(none yet)*

## Known contacts

<!-- Recurring senders worth remembering context about. -->
- **thanostonia86@gmail.com** ↔ **kyratzis7@gmail.com** — these are the same
  person's two mailboxes. `thanostonia86` already has its own automation
  running (sends "Morning Brief" digests to `kyratzis7` daily) and has been
  asked, in a real thread, to search for a house listing in Chania
  (budget €160,000, standalone house). Don't treat cross-mailbox mail
  between these two as external correspondence — (added 2026-09-17).

## Deliverables this agent can produce (beyond drafts/labels)

- **Excel export** of a categorization run: one sheet per category + one
  combined sheet, columns `Ημερομηνία (ΗΗ-ΜΜ-ΕΕ), Αποστολέας, Θέμα,
  Gmail Link (hyperlink) + Gmail URL (plain text, for viewers that don't
  render hyperlinks)`. Built with `openpyxl` (see repo xlsx skill). Requested
  ad hoc by the human on 2026-09-17 for the `kyratzis7@gmail.com` run —
  worth offering proactively after a bulk categorization, not just waiting
  to be asked.

## Session log

<!-- One line per run: date, how many emails processed, anything notable. -->
- 2026-09-12 — memory file initialized, no runs yet.
- 2026-09-17 — first real run, on `kyratzis7@gmail.com` (not the original
  `thanostonia86` target). Categorized ~336 unread threads from the last 45
  days into 8 Gmail labels (4 new, 4 reused from the human's existing
  labels) — no drafts written (human said not to). Flagged 3 things for the
  human: a stuck Zapier automation ("held tasks"), a rejected tbi bank
  financing application, and a live house-search thread with
  `thanostonia86`. Human then bulk-marked the mailbox as read via Gmail's
  own UI (6,219 → 0 unread over a few iterations) and asked for an Excel
  export of the categorization, which was built and delivered, then
  revised twice on request (added plain-text URL column; date format
  changed to ΗΗ-ΜΜ-ΕΕ).
