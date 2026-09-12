# Example run — first time, no memory yet

**Session prompt (human → agent):**
> Process my unread emails and update memory with anything you learn.

**Agent's actual steps:**

1. Reads `MEMORY.md` → all sections empty ("none yet"). No prior rules to
   apply.
2. Runs the triage flow (`gmail_agent.py` / Gmail tools) on the unread
   emails.
3. Finds 3 unread emails, classifies and drafts replies for each:
   - `billing@vendor.com` → category `Billing`, draft saved.
   - `jane@client.com` → category `Sales`, draft saved.
   - `no-reply@newsletter.com` → category `Other`, draft saved (a generic
     "thanks, noted" reply — turns out to be wrong, see next example).
4. Appends to `MEMORY.md` → **Session log**:
   ```
   - 2026-09-13 — processed 3 emails (Billing, Sales, Other). No corrections yet.
   ```

**Result:** nothing "learned" yet — this run just establishes a baseline.
Memory becomes useful once a human reviews the drafts and corrects one,
as in `example-correction.md`.
