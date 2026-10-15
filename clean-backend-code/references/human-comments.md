# Human-Style Comments Guide

Goal: write like a senior dev leaving notes for a junior — short, honest, useful. Only on important lines.

## Density rule
- ~1 comment per 10-20 lines + header + hotspot tags.
- 100-line backend file = 5-10 comments max. More = noise, less = no guidance.
- NEVER comment syntax (`// loop`, `// function`, `// return true`). Comment intent.

## The 4 tags (use exactly these so grep works)

| Tag | When | Example |
|-----|------|---------|
| `IMPORTANT:` | breaking this breaks feature/security/money | `// IMPORTANT: order matters — charge BEFORE creating DB row, else free orders on crash` |
| `WHY:` | non-obvious choice, number, workaround | `// WHY: 12 rounds = ~300ms, 14 rounds = 2s — tested on t3.micro` |
| `TO CHANGE:` | future edit point | `// TO CHANGE: to support phone login, add phone lookup here + validator` |
| `DEBUG:` | where to look when it fails | `// DEBUG: 500 here = usually DB_URL wrong or migration missing, check [UserRepo] logs` |

Grep-friendly: teammate can run `grep -rn "TO CHANGE\|DEBUG\|IMPORTANT" src/` and instantly map the codebase. Tell user this in final summary.

## File header template (copy-paste, fill it)

JS:
```js
// FILE: <name>
// PURPOSE: <one line, no jargon>
// IMPORTANT: <which function is critical + who calls it>
// TO CHANGE: <most likely future change + where>
// DEBUG: <first log tag / check on failure>
```

Python:
```python
# FILE: <name>
# PURPOSE: <one line>
# IMPORTANT: <critical function>
# TO CHANGE: <edit point>
# DEBUG: <check>
```

## Hotspot checklist — each MUST have comment + log
- [ ] auth/permission check → `// IMPORTANT: ...` + 401/403 handling
- [ ] input validation → `// WHY: strict because ...`
- [ ] DB query → `// DEBUG: ...` + error log `[RepoName.method]`
- [ ] external API/payment/email → `// WHY: retry/timeout choice` + `// DEBUG:`
- [ ] `throw` → comment what user sees vs what is logged
- [ ] env/config read → `// TO CHANGE: set via ENV in prod`

## Good vs bad — learn the tone

BAD (robotic / useless):
```js
// function to create user
// get email from request
// hash password
// save to db
```

GOOD (human):
```js
// PURPOSE: signup logic — called only by auth.controller
// WHY: we hash here (not controller) so no plain password ever leaves service layer
const hash = await bcrypt.hash(password, BCRYPT_ROUNDS);

// IMPORTANT: check duplicate BEFORE hash to save ~300ms on repeat signups
const existing = await userRepo.findByEmail(email);
```

BAD Python:
```python
# loop through users
for u in users:  # get u
```

GOOD Python:
```python
# WHY: batch 500 at a time — full table load OOMs on 100k users (seen in prod 2024)
for batch in chunked(users, 500):
```

## Language tweaks
- Keep comments in English (code-readable globally).
- One line preferred. Two lines max. If needs paragraph → it should be a docstring/README, not inline.
- Update comment when you change code. Stale comment is worse than no comment.
