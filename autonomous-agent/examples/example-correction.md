# Example run — a human correction becomes permanent memory

**Context:** after `example-run-1.md`, the human opens Gmail Drafts and
notices the draft to `no-reply@newsletter.com` was mis-categorized as
`Other` — it's actually a newsletter that should always be `Spam` and
never get a drafted reply at all.

**Session prompt (human → agent):**
> Emails from no-reply@newsletter.com are newsletters — always categorize
> them as Spam and skip drafting a reply. Remember this for next time.

**Agent's actual steps:**

1. Reads `MEMORY.md` (current state from the previous run).
2. Appends a new entry under **Sender preferences**:
   ```
   - **no-reply@newsletter.com** — always categorize as Spam, do not draft a reply — (2026-09-13)
   ```
3. Appends a new entry under **Category corrections**:
   ```
   - Newsletter senders (no-reply@*) mis-classified as "Other" by default
     — corrected to "Spam", no draft — (2026-09-13)
   ```
4. Appends to **Session log**:
   ```
   - 2026-09-13 — recorded correction: no-reply@newsletter.com → Spam, no draft.
   ```

**Next run, weeks later, in a brand-new session with zero chat history:**

The new session's `CLAUDE.md` tells it to read `MEMORY.md` first. It sees
the `no-reply@newsletter.com` rule, applies it automatically — categorizes
that sender as `Spam` and skips the draft — **without the human repeating
the instruction**. This is the whole point of the pattern: the correction
survives the end of the conversation because it lives in a file, not in
chat memory.
