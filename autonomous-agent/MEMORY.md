# MEMORY — persistent state for the Gmail Triage Agent

This is the agent's long-term memory. It is a plain file, not magic: the
agent is instructed (in `CLAUDE.md`) to read it at the start of every
session and append to it at the end. Because it's a file in this repo
(not a chat), it works the same whether you run the agent from the CLI,
from Claude Code on the web, or from a scheduled trigger — and it survives
across sessions, machines, and people.

Keep entries short and dated. Never delete a past entry — mark it
superseded instead, so the history stays auditable.

## Sender preferences

<!-- Format: - **sender/domain** — rule — (date added) -->
- *(none yet — will fill in as corrections happen)*

## Category corrections

<!-- When the human re-categorizes a draft the agent got wrong, record
     the pattern here so it isn't repeated. -->
- *(none yet)*

## Tone / voice rules

<!-- e.g. "with client X, always sign off with first name only" -->
- *(none yet)*

## Known contacts

<!-- Recurring senders worth remembering context about. -->
- *(none yet)*

## Session log

<!-- One line per run: date, how many emails processed, anything notable. -->
- 2026-09-12 — memory file initialized, no runs yet.
