// BEFORE (typical vibe-coded spaghetti — DO NOT DO THIS)
// Problems: no header, cryptic names, 3 layers mixed, SQL injection,
// deep nesting, magic 86400000, silent-ish error handling, zero guidance
// for change/debug.

const db = require('./db');
const bcrypt = require('bcrypt');

async function getU(req, res) {
  const x = req.body;
  if (x) {
    if (x.email) {
      if (x.pw) {
        const d = await db.query(`SELECT * FROM users WHERE email='${x.email}'`);
        if (d.rows.length > 0) {
          res.json({ err: "exists" });
        } else {
          bcrypt.hash(x.pw, 10).then(h => {
            db.query(`INSERT INTO users VALUES ('${x.email}', '${h}')`).then(r => {
              setTimeout(() => {}, 86400000);
              res.json(r);
            }).catch(e => { console.log(e); });
          });
        }
      }
    }
  }
}
module.exports = { getU };
