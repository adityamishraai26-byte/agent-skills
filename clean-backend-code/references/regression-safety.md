# Regression Safety (Tests Before & After Edits)

Goal: edit backend without breaking what already works. No silent regression.

## Mandatory mini-protocol (every edit)

1. **Before edit — baseline:**
   - Find related test: `tests/**/*.test.js`, `test_*.py`, or nearest `*.spec.*`. If none, note it in final summary as `No tests found for X`.
   - Run it (or at least the related file) and note PASS/FAIL before your change.
   - If no test exists for the function you touch, write a 5-10 line smoke test FIRST for current behavior (happy path + 1 failure path).

2. **During edit — keep it testable:**
   - Prefer pure service functions `(input) -> output/throw` over code needing HTTP/DB to test.
   - Validation, pricing math, auth rules → must be unit-testable without server running.
   - If you add branch (`if newField`), add 1 test case for it.

3. **After edit — verify:**
   - Re-run the same test(s). Both old + new cases must PASS.
   - Run checker: `python scripts/check_readability.py <changed files>`.
   - If tests can't run (no runner/db), say so explicitly in summary: `Tests: not run (reason) — manual check: ...`.

## Minimal test templates (copy-paste)

JS (node:test, no install needed):
```js
// tests/user.service.test.js
// PURPOSE: regression guard for signup — run with: node --test tests/user.service.test.js
const test = require("node:test");
const assert = require("node:assert");
const { createUser } = require("../src/services/user.service");

test("rejects duplicate email with 409", async () => {
  // WHY: regression — duplicate used to return 500 before 23505 mapping
  await assert.rejects(() => createUser({ email: "dup@test.com", password: "x12345678" }), /already exists/);
});
```

Python (pytest):
```python
# tests/test_user_service.py
# PURPOSE: regression guard for signup — run with: pytest tests/test_user_service.py
import pytest
from src.services.user_service import create_user, ConflictError

def test_duplicate_email_raises_conflict():
    # WHY: regression — duplicate used to return 500 before mapping
    with pytest.raises(ConflictError, match="already exists"):
        create_user(email="dup@test.com", password="x12345678")
```

## Rules
- NEVER ship backend edit with `Tests: not checked`. Always state before/after result.
- NEVER delete/skip a failing old test to make yours pass — fix code, or explain why old expectation changed.
- 1 changed behavior = 1 test. No test = flag as risk in final summary.
