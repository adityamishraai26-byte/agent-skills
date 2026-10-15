# Backend Layout (Where Code Goes)

Use this for Node/Express/Fastify/Python-FastAPI/Django — same idea, names may vary.

## Allowed tree (small backend)
```
src/
  routes/        # URL only: router.post("/users", controller.create)
  controllers/   # req/res, validation, status codes (max 100 lines/file)
  services/      # business logic (no req/res, no SQL)
  repositories/  # DB queries only (one file per table/model)
  middlewares/   # auth, errorHandler, rateLimit
  utils/         # pure helpers: validateEmail, hash, chunked
  config.js      # env read ONCE, export typed config
  app.js         # wire-up only, no logic
```

Large backend: add `jobs/`, `webhooks/`, `db/migrations/`.

## File responsibilities with example

**routes/user.routes.js** — only wiring:
```js
// FILE: user.routes.js
// PURPOSE: map /users URLs to controller (no logic here)
// TO CHANGE: add new endpoint -> add line here + controller method
router.post("/users", validate(signupSchema), userController.create);
```

**controllers/user.controller.js** — HTTP only:
```js
// FILE: user.controller.js
// PURPOSE: HTTP layer for users — parse req, call service, send res
async function create(req, res, next) {
  try {
    // WHY: validate at boundary so service stays pure/testable
    const data = signupSchema.parse(req.body);
    const user = await userService.createUser(data);
    res.status(201).json(user);
  } catch (err) { next(err); } // DEBUG: 400 = validation, 409 = duplicate, 500 = see [UserService] logs
}
```

**services/user.service.js** — rules:
```js
// FILE: user.service.js
// PURPOSE: signup/login rules (no req/res, no SQL)
async function createUser({ email, password }) { ... }
```

**repositories/user.repo.js** — SQL/ORM only:
```js
// FILE: user.repo.js
// PURPOSE: users table queries only — no business rules
async function findByEmail(email) { ... } // DEBUG: returns null if not found, never throws
```

## Import rule (prevents cycles/spaghetti)
`routes -> controllers -> services -> repositories -> db`
`utils` and `config` can be imported anywhere. Never reverse (service must NOT import controller).

## When to create new file
- New table/model → new `repositories/<name>.repo.js`.
- New feature area (payments, notifications) → new `services/<name>.service.js`.
- Shared by 2+ files → move to `utils/`.
- File hits 200 lines → split by function group.
