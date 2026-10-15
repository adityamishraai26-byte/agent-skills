# Documentation: README + Decisions

Goal: human understands project in 5 min without reading all code. Code comments explain lines, README explains system.

## 1. README (update on every feature/folder change)
Keep root or `src/README.md` short — max 1 page, these 5 sections only:
```md
## What (1 line)
Signup/login API — Express + Postgres.
## Run
cp .env.example .env && npm i && npm run dev
## Structure
routes/ controllers/ services/ repositories/ (see references/backend-layout.md)
## Important flows
- POST /users -> controller.create -> service.createUser -> repo.create
- Auth: middleware/requireAuth checks JWT, see DEBUG tags there
## Change guide
- Add field: schema + service + repo + test
- Debug 500: grep "TO CHANGE|DEBUG|IMPORTANT" then check [Service] logs
```

Rules: commands must be copy-paste runnable. No stale port/commands. If you change setup, env var, or folder structure → update README in same edit.

## 2. Decisions (WHY that is not in code)
If you choose library/number/pattern that future dev might question, leave 2-3 lines either as `// WHY:` in code (preferred for local choice) or in `DECISIONS.md` (for global choice):
```md
- 2026-10-15: bcrypt 12 rounds (not argon2) — team knows bcrypt, 300ms ok on t3.micro.
- 2026-10-15: Postgres 23505 -> 409 mapping in service (not repo) — so repo stays ORM-swappable.
```

## 3. What NOT to document
- Don't paste full code in README. Link file + function name.
- Don't document obvious (`npm install installs deps`). Document non-obvious (which migration must run first, which ENV is required in prod).
- Stale doc = bug. If behavior changed and doc didn't → fix doc before finishing (same rule as stale comments).
