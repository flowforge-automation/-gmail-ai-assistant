# Autonomous Agent Template (with persistent memory)

This folder is a minimal, working example of the pattern requested: an
agent that (a) runs on its own instructions, isolated from any other
chat/conversation, and (b) keeps memory across runs in a plain file
instead of in chat history.

```
autonomous-agent/
├── CLAUDE.md     ← the agent's instructions ("constitution"), auto-loaded
├── MEMORY.md     ← the agent's persistent memory (it reads + updates this)
├── examples/     ← sample runs showing the pattern in action
└── README.md     ← this file (for humans)
```

## Why this makes the agent "autonomous with its own memory"

- **Isolation from other conversations.** Claude Code loads `CLAUDE.md`
  from whatever folder a session is started in. A session started here
  only ever sees *this* file — never anything said in an unrelated chat
  about a different project. That's what "δικό του, ανεπηρέαστο" means
  in practice: scope by folder, not by memory magic.
- **Memory that isn't the chat.** By default an LLM agent remembers
  nothing once a session ends. `MEMORY.md` is the fix: `CLAUDE.md`
  instructs the agent to read it before acting and write to it after.
  A plain markdown file in git is enough — no database or vector store
  needed to start.
- **Auditable.** Because memory is a file, you can read it, diff it,
  review it in a pull request, and roll it back with `git revert` if the
  agent learns something wrong.

## How to run this agent

### Option A — Claude Code CLI (local)

```bash
cd autonomous-agent
claude
```

Claude Code automatically loads `CLAUDE.md` from the current directory.
Ask it to do its job, e.g.: *"Process unread emails and update memory."*
It will read `MEMORY.md`, run `../gmail_agent.py` (or call Gmail tools if
connected), then append what it learned back into `MEMORY.md`.

### Option B — Claude Code on the web / GitHub

1. Push this repo to GitHub (already done if you're reading this from
   the repo).
2. Start a new session on [claude.ai/code](https://claude.ai/code)
   pointed at this repository, and set the working directory (or just
   ask Claude to `cd autonomous-agent`) so it picks up this `CLAUDE.md`.
3. Each new session is isolated — it has no memory of any other chat you've
   had, only what's written in `MEMORY.md` in this folder.

### Option C — scheduled / recurring

Use a cron trigger or the `/loop` skill to run this agent on an interval
(e.g. every morning). Every run: read memory → act → write memory. No
human needs to repeat context between runs.

## Building your own agent from this template

1. Copy this folder, rename it for your use case.
2. Rewrite `CLAUDE.md`: role, hard rules (what it must never do), the
   read-memory → act → write-memory workflow, and style/output rules.
3. Replace `MEMORY.md`'s sections with whatever your agent actually needs
   to remember (preferences, decisions, known entities, a running log —
   whatever changes run to run and should persist).
4. Add 1-2 `examples/` transcripts once you've run it, so future-you (or
   a teammate) can see the intended pattern at a glance.
5. Commit everything except secrets (`credentials.json`, `token.json`,
   API keys — see the repo's `.gitignore`). The agent's *instructions*
   and *memory* are safe to commit; its *credentials* never are.

## Local vs. GitHub

Both work with this exact structure:

- **Local only:** keep the folder on your machine, run `claude` in it.
  Memory persists as long as the file stays on disk.
- **GitHub (recommended):** push the repo. Now the agent's brain
  (`CLAUDE.md` + `MEMORY.md`) is versioned, backed up, shareable, and
  usable from Claude Code on the web or from any machine that clones the
  repo — the memory travels with the repo, not with a device.
