// FILE: user.service.js
// PURPOSE: User signup business logic (no HTTP, no raw SQL in handler)
// IMPORTANT: createUser() is called by auth.controller — breaking it breaks signup/login
// TO CHANGE: to add phone field, update validateSignup + userRepo.create + schema
// DEBUG: if signup returns 500, check logs [UserService.createUser] then DB_URL/migration

const bcrypt = require("bcrypt");
const logger = require("../utils/logger");
const { ConflictError, DbError } = require("../utils/errors");
const userRepo = require("../repositories/user.repo");

// WHY: 12 rounds = ~300ms on t3.micro, 14 rounds = 2s — tested, security vs speed tradeoff
const BCRYPT_ROUNDS = 12;

async function createUser({ email, password }) {
  // IMPORTANT: check duplicate BEFORE expensive hash to save ~300ms on repeat signups
  const existing = await userRepo.findByEmail(email); // DEBUG: returns null if not found, never throws
  if (existing) throw new ConflictError("email already exists"); // TO CHANGE: allow re-invite -> return invite instead of throw

  // WHY: hash here (not controller) so plain password never leaves service layer
  const hash = await bcrypt.hash(password, BCRYPT_ROUNDS);

  try {
    // DEBUG: 500 here = usually DB_URL wrong or migration missing, check [UserRepo] logs
    const user = await userRepo.create({ email, hash });
    return user;
  } catch (err) {
    // IMPORTANT: 23505 = unique violation = duplicate email, not generic 500
    if (err.code === "23505") throw new ConflictError("email already exists");
    logger.error("[UserService.createUser] DB failed: email=%s code=%s", email, err.code);
    throw new DbError("create user failed");
  }
}

module.exports = { createUser };

// AFTER SUMMARY (what skill forces agent to output):
// Files: services/user.service.js (logic) + repositories/user.repo.js (SQL) + controllers/user.controller.js (HTTP)
// Important lines: duplicate-check (race condition), BCRYPT_ROUNDS (perf), 23505 mapping (correct 409 vs 500)
// To change email rules: edit validateSignup + this file
// To debug: grep "TO CHANGE|DEBUG|IMPORTANT" or check [UserService.createUser] logs
