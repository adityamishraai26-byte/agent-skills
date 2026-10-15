# Debug-Friendly Errors & Logs

Goal: when production gives 500, human finds cause in <2 min from logs alone.

## 1. Error shape (always specific, never generic)
Bad: `throw "err"`, `throw new Error("failed")`, `res.status(500).json({error: "err"})`
Good:
```js
// IMPORTANT: specific class decides HTTP status in errorHandler — generic Error always becomes 500
throw new NotFoundError("user 123 not found");      // -> 404
throw new ValidationError("email invalid");          // -> 400
throw new ConflictError("email already exists");     // -> 409
throw new DbError("create user failed");             // -> 500 + alert
```

Python:
```python
# WHY: specific exception -> specific status, bare Exception hides root cause
raise NotFoundError(f"user {user_id} not found")
```

Map once in `middlewares/errorHandler.js` — controller never writes status for domain errors manually.

## 2. Log format (grep-able, with context)
Template: `[Module.method] what + key ids, never passwords/tokens`
```js
logger.error("[UserService.createUser] DB failed: email=%s code=%s", email, err.code);
logger.info("[UserService.createUser] created: id=%s email=%s", user.id, email);
logger.warn("[AuthMiddleware] invalid token: reason=%s ip=%s", reason, req.ip);
```

Rules:
- Every `catch` MUST log with `[File.function]` tag + relevant id (userId, email, orderId) + original `err`.
- NEVER `console.log(err)` / `print(err)` / empty catch. Use `logger.error/warn/info`.
- NEVER log secrets: password, token, card, JWT_SECRET.
- Log at creation point (service/repo), not only at top middleware — else context is lost.
- Include `// DEBUG:` comment above every try/catch telling human which log tag to grep:
```js
// DEBUG: 500 here = usually DB_URL wrong or migration missing, grep [UserRepo] logs
```

## 3. Fail fast + fail loud
- Validate at boundary (controller/route) → return 400 with field name, don't let bad data reach DB.
- External calls (DB, Stripe, email, queue) MUST have timeout + retry comment:
```js
// WHY: 3 retries with 2s timeout — Stripe p99 is 800ms, avoids hanging requests
const charge = await stripeWithRetry(payload, { retries: 3, timeoutMs: 2000 });
// DEBUG: Stripe fail -> grep [PaymentService.charge], check STRIPE_KEY + dashboard
```
- Don't swallow: `catch (err) { /* ignore */ }` is FORBIDDEN. Either rethrow specific error or log + throw.
