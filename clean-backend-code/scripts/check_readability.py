#!/usr/bin/env python3
"""
check_readability.py — Skill verifier for clean-backend-code.
Usage: python scripts/check_readability.py <file1> <file2> ...
Checks: file/function length, file header, hotspot comments, magic numbers,
console.log/print vs logger, bare except / empty catch, string throw.
Exit 0 = PASS, 1 = FAIL.
"""
import re
import sys
from pathlib import Path

MAX_FILE = 200
HARD_FILE = 250
MAX_FUNC = 30
HARD_FUNC = 50

FUNC_RE = re.compile(
    r"^\s*(?:async\s+)?(?:function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\(|"
    r"(?:async\s+)?def\s+\w+|(?:public|private|protected)?\s*(?:async\s+)?\w+\s*\(.*\)\s*\{?)"
)
# simpler: detect function starts
DEF_RE = re.compile(r"^\s*(async\s+function\s+\w+|function\s+\w+|const\s+\w+\s*=\s*(async\s*)?(\([^)]*\)\s*=>|function)|async\s+def\s+\w+|def\s+\w+|async\s+\w+\s*\([^)]*\)\s*\{)")
HOTSPOT_RE = re.compile(r"(await\s+\w*?(query|db|prisma|pool|axios|fetch|stripe|sendmail)|bcrypt|jwt\.|throw new|process\.env|os\.getenv)", re.I)
TAG_RE = re.compile(r"(IMPORTANT:|WHY:|TO CHANGE:|DEBUG:|FILE:|PURPOSE:)")
MAGIC_RE = re.compile(r"(setTimeout\([^,]+,\s*\d{4,}|===\s*\d{2,}|sleep\(\d{3,}\))")
BAD_LOG_RE = re.compile(r"console\.log\s*\(|print\s*\(")
BARE_EXCEPT_RE = re.compile(r"^\s*except\s*:\s*(#.*)?$")
EMPTY_CATCH_RE = re.compile(r"catch\s*(\([^)]*\))?\s*\{\s*\}")
STRING_THROW_RE = re.compile(r"throw\s+['\"]")

def check_file(path: Path):
    fails, warns = [], []
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    n = len(lines)

    if n > HARD_FILE:
        fails.append(f"FAIL {path}: {n} lines > hard limit {HARD_FILE} — split file")
    elif n > MAX_FILE:
        warns.append(f"WARN {path}: {n} lines > {MAX_FILE} — consider split")

    # header: first 15 lines must have FILE: + PURPOSE:
    head = "\n".join(lines[:15])
    if "FILE:" not in head or "PURPOSE:" not in head:
        fails.append(f"FAIL {path}: missing file header (need // FILE: + // PURPOSE: in top 15 lines)")

    # function length approx: track def lines
    func_starts = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if (s.startswith("function ") or s.startswith("async function ")
            or re.match(r"^(async\s+)?def\s+\w+", s)
            or re.match(r"^const\s+\w+\s*=\s*(async\s*)?(\(|function)", s)
            or re.match(r"^async\s+\w+\(", s)):
            func_starts.append(i)
    func_starts.append(n)
    for k in range(len(func_starts) - 1):
        flen = func_starts[k+1] - func_starts[k]
        # cap by blank-line heuristic: only flag if > limit and block looks like one func
        if flen > HARD_FUNC:
            fails.append(f"FAIL {path}: function near line {func_starts[k]+1} ~{flen} lines > {HARD_FUNC} — split it")
        elif flen > MAX_FUNC and flen < 120:
            warns.append(f"WARN {path}: function near line {func_starts[k]+1} ~{flen} lines > {MAX_FUNC}")

    # hotspot comments: every hotspot should have a tag within 3 lines above
    # skip pure comment lines to avoid flagging summary text containing keywords
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        if stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("*"):
            continue
        if HOTSPOT_RE.search(ln):
            window = "\n".join(lines[max(0, i-3):i+1])
            if not TAG_RE.search(window):
                warns.append(f"WARN {path}:{i+1}: hotspot '{ln.strip()[:60]}' has no IMPORTANT/WHY/DEBUG comment above")

    # magic numbers
    for i, ln in enumerate(lines):
        if MAGIC_RE.search(ln) and "WHY:" not in "\n".join(lines[max(0,i-2):i+1]) and "const " not in ln and "CONST" not in ln:
            warns.append(f"WARN {path}:{i+1}: possible magic number '{ln.strip()[:60]}' — use named const + WHY comment")

    # nesting depth heuristic (brace indent)
    depth = max_depth = 0
    for ln in lines:
        depth += ln.count("{") - ln.count("}")
        max_depth = max(max_depth, depth)
    if max_depth > 6:
        warns.append(f"WARN {path}: brace depth {max_depth} suggests nesting >3 — use early returns")

    # debug-friendly: no console.log/print, no bare except/empty catch, no string throw
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("//") or s.startswith("#") or s.startswith("*"):
            continue
        if BAD_LOG_RE.search(ln) and "logger." not in ln:
            warns.append(f"WARN {path}:{i+1}: use logger.error/info with [Module.method] tag instead of '{s[:50]}'")
        if BARE_EXCEPT_RE.match(ln):
            fails.append(f"FAIL {path}:{i+1}: bare except: forbidden — catch specific exception + log")
        if EMPTY_CATCH_RE.search(ln):
            fails.append(f"FAIL {path}:{i+1}: empty catch block — log with [Module.method] + rethrow specific error")
        if STRING_THROW_RE.search(ln):
            warns.append(f"WARN {path}:{i+1}: string throw — use specific Error class (NotFound/Validation/Conflict/Db)")

    return fails, warns

def main(files):
    if not files:
        print("Usage: python check_readability.py <file...>")
        return 1
    all_fails, all_warns = [], []
    for f in files:
        p = Path(f)
        if not p.exists():
            print(f"SKIP {f}: not found")
            continue
        fails, warns = check_file(p)
        all_fails += fails
        all_warns += warns
    for w in all_warns:
        print(w)
    for fl in all_fails:
        print(fl)
    if all_fails:
        print(f"\nRESULT: FAIL ({len(all_fails)} errors, {len(all_warns)} warnings)")
        return 1
    print(f"\nRESULT: PASS ({len(all_warns)} warnings)")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
