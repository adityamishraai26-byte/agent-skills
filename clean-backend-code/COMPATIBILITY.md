# COMPATIBILITY — where `clean-backend-code` works (as of 2026-10-15)

This skill follows the Agent Skills open standard (`SKILL.md` + `references/` + `scripts/`).
Any agent in Table 1 loads it natively. Others (Table 2) can still use it by pasting
`SKILL.md` + the relevant `references/` file into context.

## Table 1 — Skill-compatible (native `SKILL.md` support, verified)

| Agent | Type | Install this skill |
|-------|------|--------------------|
| OpenCode | terminal (open-source) | `.opencode/skills/clean-backend-code` (project) or `~/.config/opencode/skills/` (global) |
| Claude Code (Anthropic) | terminal | `.claude/skills/clean-backend-code` (project) or `~/.claude/skills/` (global) |
| OpenAI Codex (CLI / IDE / cloud) | terminal + IDE | `.agents/skills/clean-backend-code` (project) or `~/.agents/skills/` (global) |
| Cursor | IDE + CLI | skills dir (Agent Skills standard) |
| GitHub Copilot (CLI / VS Code) | terminal + IDE | skills dir (Agent Skills standard) |
| VS Code agent mode | IDE | skills dir (Agent Skills standard) |
| Gemini CLI (Google) | terminal | skills dir (Agent Skills standard) |
| Windsurf | IDE | skills dir (Agent Skills standard) |
| Goose (Block) | terminal/desktop | skills dir (Agent Skills standard) |
| Roo Code | VS Code ext. | skills dir (Agent Skills standard) |
| Trae | IDE | skills dir (Agent Skills standard) |

Invoke: `@clean-backend-code` (ChatGPT/Codex style `$clean-backend-code`, Claude `/clean-backend-code`).
Agent auto-loads it on backend tasks via the `description` field.

## Table 2 — Other major public agents (no native skill dir confirmed; use manually)

| Agent | Type | How to use this skill |
|-------|------|-----------------------|
| Cline (VS Code ext., open-source) | IDE | paste `SKILL.md` + `references/` into chat / project rules |
| Kilo Code (Cline/Roo fork) | IDE | same as above |
| Aider (open-source, git-native) | terminal | paste `SKILL.md` in chat or `CONVENTIONS.md` |
| OpenHands (open-source) | terminal/cloud | repo `microagents` / paste skill |
| Qwen Code (Alibaba) | terminal | paste skill (CLI agent) |
| Crush (Charm) | terminal | paste skill |
| Pi (terminal minimalist) | terminal | paste skill |
| Devin (Cognition) | autonomous cloud | paste `SKILL.md` in task instructions |
| Manus | autonomous web | paste skill in task prompt |
| ChatGPT Agent mode | autonomous web | upload/paste skill |
| Gemini Agent / Deep Research (Google) | autonomous web | paste skill |
| Replit Agent | web IDE | paste skill in prompt |
| Bolt / Lovable / v0 (builders) | web vibe-coding | paste `SKILL.md` step 3–4 (comments + structure) |
| Microsoft Copilot Studio / Agentforce / ServiceNow | enterprise | import as instruction set |

## Notes
- "Har ek" exhaustive list is impossible — hundreds of thin wrappers exist. Above are the major public ones as of 2026-10-15.
- Model-agnostic open-source harnesses (OpenCode, Cline, Aider, Roo/Kilo, OpenHands, Goose) work with any provider model (Claude, GPT, Gemini).
- Verify: `python scripts/check_readability.py examples/after-clean.js` must print `RESULT: PASS`.
