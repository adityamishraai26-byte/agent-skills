# agent-skills — install-ready AI agent skills (Agent Skills standard)

Public-standard, install-ready skills for AI coding agents. Follows https://agentskills.io —
works with **OpenCode, Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI, Windsurf, Goose, Roo Code, Trae**.

## Skills

| Skill | Job | Path |
|-------|-----|------|
| `clean-backend-code` | AI Code Quality Guardian for backend code | `clean-backend-code/SKILL.md` |

## `clean-backend-code` — what this skill contains

Solves the main vibe-coding problem: AI writes spaghetti code that nobody understands —
no one knows which line is important, and debugging takes forever. This skill enforces
6 things on every backend code change (API, DB, auth, service logic):

1. **AI Code Quality Guardian** — the agent acts as a reviewer and blocks bad code (9-step gate).
2. **Clean Architecture** — small focused modules: `route → controller → service → repository`, max 200 lines/file, 30 lines/function.
3. **Smart Comments** — human-style tags on important lines only: `IMPORTANT: / WHY: / TO CHANGE: / DEBUG:` (grep maps the whole codebase).
4. **Debug Friendly** — specific error classes (correct 404/409/500) + `[Module.method]` tagged logs, never `console.log`/empty-catch.
5. **Regression Safety** — tests run before and after every edit, breaking old features is forbidden.
6. **Documentation** — README + decisions kept updated, stale comment/doc counts as a bug.

**Files inside:**

| File | Purpose |
|------|---------|
| `SKILL.md` | Main workflow (9 steps + NEVER list) — this is what the agent follows |
| `references/anti-spaghetti-rules.md` | Limits, naming, no-magic-values, error handling rules |
| `references/backend-layout.md` | Folder structure + responsibility of each file |
| `references/human-comments.md` | 4-tag comment standard + good/bad examples |
| `references/debug-friendly.md` | Error classes + log format + retry/timeout |
| `references/regression-safety.md` | Before/after test protocol + copy-paste templates |
| `references/documentation.md` | README + DECISIONS standard |
| `scripts/check_readability.py` | Auto-checker (catches missing headers, length, comments, `console.log`, bare-except) |
| `examples/before-spaghetti.js` | Typical bad vibe-code (checker FAILs it) |
| `examples/after-clean.js` | Correct output sample (checker PASSes it) |
| `COMPATIBILITY.md` | Supported AI agents + install paths |

## Install

Copy the skill folder into your agent's skills directory:

```bash
# OpenCode — project (team-shared) / global
cp -r clean-backend-code <project>/.opencode/skills/
cp -r clean-backend-code ~/.config/opencode/skills/

# Claude Code
cp -r clean-backend-code <project>/.claude/skills/
cp -r clean-backend-code ~/.claude/skills/

# Codex
cp -r clean-backend-code <project>/.agents/skills/
cp -r clean-backend-code ~/.agents/skills/
```

Invoke: `@clean-backend-code` (Codex: `$clean-backend-code`, Claude: `/clean-backend-code`),
or the agent auto-loads it on backend tasks.

## Verify

```bash
python clean-backend-code/scripts/check_readability.py clean-backend-code/examples/after-clean.js
# expect: RESULT: PASS (0 warnings)
```

## License

MIT — see `clean-backend-code/LICENSE`.
