# Anti-Spaghetti Rules (Backend)

These are MUST rules. If you break one, refactor before finishing.

## 1. Limits
- File: max 200 lines (hard fail at 250). Split by responsibility.
- Function: max 30 lines (hard fail at 50). If longer, extract helper.
- Params: max 4. If more, pass object: `createUser({email, hash, role})`.
- Nesting: max 3 levels. Level 4 = refactor with early return or helper.

Good (early return):
```js
if (!user) throw new NotFoundError("user not found");
if (!user.isActive) throw new ForbiddenError("inactive");
return doWork(user);
```

Bad (pyramid):
```js
if (user) {
  if (user.isActive) {
    if (role) {
      if (...) { ... }
    }
  }
}
```

## 2. Layer separation (backend only)
```
route (URL + method only)
 -> controller (req/res, validation, status codes — NO SQL, NO business math)
 -> service (business logic, rules — NO req/res, NO raw SQL)
 -> repository (DB queries only — NO business rules, NO HTTP)
```

Violation example (NEVER):
```js
// route handler doing everything — SPAGHETTI
app.post("/users", async (req, res) => {
  const hash = await bcrypt.hash(req.body.pw, 10);
  const r = await db.query(`INSERT ... ${req.body.email}`); // SQL injection + mixed layers
  if (...) { ... } else { ... } // 80 lines...
  res.json(r);
});
```

Fixed: split into 3 files as per `backend-layout.md`.

## 3. Naming
- Functions = verb + object: `createUser`, `validateEmail`, `chargePayment`.
- Variables = full words: `existingUser`, not `eu`, `d`, `tmp`.
- Booleans: `isValid, hasToken, shouldRetry`.
- Constants: `UPPER_SNAKE`: `MAX_LOGIN_ATTEMPTS = 5`.
- Errors: specific classes: `NotFoundError, ValidationError, ConflictError` — never generic `throw "err"`.

## 4. No magic values
Bad: `if (role === 2)`, `setTimeout(..., 86400000)`, `hash(pw, 10)`.
Good:
```js
const ADMIN_ROLE_ID = 2;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;
const BCRYPT_ROUNDS = 12; // WHY: see human-comments.md
```

Env-only values: `PORT, DATABASE_URL, JWT_SECRET, STRIPE_KEY, REDIS_URL`. Read once in `config.js`, import from there.

## 5. Error handling (explicit, never silent)
Every `await` on I/O (DB, API, file, queue) must be in try/catch or let caller handle with documented throw.

```js
try {
  const user = await userRepo.create(data);
  return user;
} catch (err) {
  // IMPORTANT: unique-violation = duplicate email, not generic 500
  if (err.code === "23505") throw new ConflictError("email exists");
  logger.error("[UserService.createUser] DB failed:", err);
  throw new DbError("create user failed");
}
```

NEVER: empty catch, `console.log(err)`, bare `except: pass`.

## 6. No duplication (DRY at 3 lines)
If same 3+ lines appear twice, extract: `validateEmail()`, `requireAuth()`, `handleDbError()`.
Duplicated validation/DB-error mapping is the #1 spaghetti source in vibe code.

## 7. Async discipline
- JS: `async/await` only. No nested `.then().then()`. Always `await` or `return` promise with comment why.
- Parallel independent calls: `Promise.all([...])` with comment.
- Timeouts/retries on external calls: `fetchWithRetry(url, {retries: 3})`.
