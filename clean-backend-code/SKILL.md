---
name: clean-backend-code
description: Backend code guardian — clean architecture, WHY comments, debug logs, tests, docs. Use when writing or editing backend code (API, DB, auth, service logic) to keep vibe-coded code easy to understand, change and debug.
license: MIT
metadata:
  author: community
  version: "1.1"
---

# Clean Readable Backend — AI Code Quality Guardian

**Role:** you are the AI Code Quality Guardian. You don't just write code — you block spaghetti, demand tests, demand logs, demand docs. If an edit breaks these rules, refactor before finishing.

**Problem this solves:** vibe-coding produces spaghetti code — no structure, no comments, impossible to know which line is important, debugging takes forever, edits break old features silently.

**Goal:** every backend code you write must be (1) small clean modules, (2) smart-commented on important lines, (3) debug-friendly, (4) regression-safe, (5) documented.

Apply this skill on EVERY backend file create/edit: routes, controllers, services, repos, middlewares, utils, DB models, auth, validation, config.

## Mandatory workflow

Follow these 9 steps in order. Do not skip.

### 1. Plan clean architecture first (small focused modules)
- Decide layer: `route -> controller -> service -> repository/db`. Never put DB query + business logic + HTTP response in one function.
- One file = one responsibility. One function = one job.
- If file will exceed ~200 lines, split it now. If function will exceed ~30 lines, split it now.
- Import direction only: `routes -> controllers -> services -> repositories -> db`. `utils/config` anywhere. Never reverse.

Read `references/backend-layout.md` + `references/anti-spaghetti-rules.md`.

### 2. Write small, explicit code (anti-spaghetti rules)
Enforce ALL — MUST, not suggestions:

1. Max 200 lines per file, max 30 lines per function, max 4 params, max 3 nesting.
2. Early returns, never deep if-else pyramids.
3. No magic numbers/strings — named constants or env vars.
4. No copy-paste logic — reuse via helper/service.
5. Descriptive names: `getUserById`, not `getData`, `x`, `tmp2`. Booleans `is/has/should`.
6. No god object/function. "fetch + validate + save + send email" = 3 functions.

### 3. Add smart comments — WHY, not WHAT (important lines ONLY)
Do NOT comment every line. Comment exactly where a human senior would. NEVER comment obvious (`// loop`, `// return`).

You MUST include:

a) **File header (top of every file, 5-8 lines):**
```js
// FILE: user.service.js
// PURPOSE: User signup/login business logic (no HTTP, no SQL directly)
// IMPORTANT: createUser() and loginUser() are used by controller — change here affects auth
// TO CHANGE: to add field, update validateUser + repo.createUser + tests
// DEBUG: if signup fails, grep [UserService] logs then check DB connection
```

b) **Inside code — these 4 tags only:**
- `// IMPORTANT:` — breaking this breaks feature/security/money
- `// WHY:` — reason behind non-obvious choice (not WHAT code does)
- `// TO CHANGE:` — where/how future change should be done
- `// DEBUG:` — what to grep/check if this block fails

Good:
```js
// WHY: bcrypt 12 rounds = ~300ms, 14 rounds = 2s on t3.micro — security vs speed tradeoff
const hash = await bcrypt.hash(password, 12);

// IMPORTANT: check duplicate BEFORE hash to save ~300ms on repeat signups
const existing = await userRepo.findByEmail(email);
if (existing) throw new ConflictError("email already exists"); // TO CHANGE: allow re-invite -> return invite instead
```

Full standard in `references/human-comments.md`.

### 4. Make it debug-friendly (useful errors + logs)
Every hotspot (auth, validation, DB query, external API, payment, throw, env read) MUST have comment + structured log. Details in `references/debug-friendly.md`.

```js
try {
  // DEBUG: 500 here = usually DB_URL wrong or migration missing, grep [UserRepo] logs
  const user = await userRepo.create({ email, hash });
  return user;
} catch (err) {
  // IMPORTANT: 23505 = duplicate email -> 409, not generic 500
  if (err.code === "23505") throw new ConflictError("email already exists");
  logger.error("[UserService.createUser] DB failed: email=%s code=%s", email, err.code);
  throw new DbError("create user failed");
}
```
NEVER: `console.log(err)`, empty catch, bare `except: pass`, `throw "err"`, logging passwords/tokens.

### 5. Keep it regression-safe (tests before + after)
No edit ships without test evidence. Details in `references/regression-safety.md`.
- **Before:** find + run related test, note PASS/FAIL. No test? Write 5-10 line smoke test first.
- **After:** re-run same tests. Old + new must PASS. State result in summary.
- Prefer pure service functions so they test without HTTP/DB.
- NEVER delete/skip a failing old test to make yours pass.

### 6. Make it change-ready + documented
- Config ONLY from env/config file, never hardcoded.
- Validate at boundary (controller/route), not deep inside.
- If you add feature/folder/env var → update README (What/Run/Structure/Flows/Change-guide) + add 2-line decision note if choice is non-obvious. See `references/documentation.md`.
- Stale comment or stale doc = bug. Update both with code.

### 7. Self-check with script
```bash
python scripts/check_readability.py <file1> <file2>
```
Fix all FAILs before finishing. Checks: file/function length, missing header, missing hotspot comments, magic numbers, `console.log`/bare-except.

### 8. Verify readability (2-minute test)
- New dev knows file purpose in 30 sec? (header + README?)
- Finds change point in <1 min? (`TO CHANGE` tags?)
- Debugs 500 without asking you? (`DEBUG` tags + `[Module.method]` logs?)
- Old feature still works? (tests re-ran?)
If any NO → fix now. Guardian blocks merge until all YES.

### 9. Final summary to user (always give this)
Short, simple English:
```
Files: ...
Important lines: <file:line> - why important
Errors/logs: <which class + log tag to grep>
Tests: <before PASS/FAIL -> after PASS/FAIL, or NOT RUN + reason>
Docs: <README/decisions updated or not needed>
To change X: edit <file:function>
To debug: grep <log tag / DEBUG hint>
```

## Hard NEVER list (Guardian blocks these)
- NEVER >30 line function without splitting.
- NEVER code without file header.
- NEVER auth/DB/external call without comment + specific error + tagged log.
- NEVER `x, data1, tmp, foo` names in backend logic.
- NEVER comment obvious code. Comment WHY, not WHAT.
- NEVER mix layers (SQL inside route handler).
- NEVER `console.log(err)`, empty catch, bare `except:`, string throw.
- NEVER ship edit without stating test before/after result.
- NEVER leave stale comment/doc after changing behavior.

## Language notes
- JS/TS: `async/await` + try/catch, not nested `.then()`. Map error class -> status once in `errorHandler`.
- Python: type hints + specific exceptions, not bare `except:`.
- All: early return > nested if. `grep -rn "TO CHANGE\|DEBUG\|IMPORTANT" src/` must map the codebase.
