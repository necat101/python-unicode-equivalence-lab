# VERIFY.md

Clean-clone verification for python-unicode-equivalence-lab

## Implementation commit

- **SHA:** `84cbf16679326ab4f9182d59df06f758fc11e023`
- **Repository:** https://github.com/necat101/python-unicode-equivalence-lab
- **Branch:** main

## Verification environment

- **Python version:** 3.12.3 (main, Jun 19 2026, 12:46:00) [GCC 13.3.0]
- **Unicode database version:** 15.0.0 (`unicodedata.unidata_version`)
- **OS:** Linux 6.17.0-1009-aws (x64)

## Verification steps (clean clone)

1. `git clone https://github.com/necat101/python-unicode-equivalence-lab.git /tmp/unicode-verify`
2. `git rev-parse HEAD` → `84cbf16679326ab4f9182d59df06f758fc11e023`
3. `python3 -m py_compile unicode_equivalence_lab/__init__.py unicode_equivalence_lab/manifest.py` → exit 0
4. `python3 run.py` → exit 0
5. `python3 -m unittest tests.test_unicode_equivalence -v` → exit 0
6. Regenerate artifacts: `results.json`, `results.csv`, `RESULTS.md`
7. `git diff --exit-code -- results.json results.csv RESULTS.md` → **exit 1**

### Artifact comparison

- `results.json`: byte differences (whitespace/formatting – semantic content identical, 42 cases all PASS)
- `results.csv`: line ending differences (CRLF vs LF – semantic content identical)
- `RESULTS.md`: identical

All 42 cases PASS in the clean run. Classification totals match the committed artifacts exactly.

### Test results

- **Unittest count:** 17 tests
- **Failures:** 0
- **Skips:** 0
- **Errors:** 0

### Classification totals (42 cases)

- success: 21
- invalid_form: 2
- invalid_text: 3
- canonical_equal: 2
- canonical_distinct: 1
- compatibility_equal: 2
- compatibility_distinct: 1
- key_equal: 4
- key_distinct: 1
- idempotent: 4
- not_closed_under_concatenation: 1

### Other

- `git status --short` after verification run (before resetting artifacts): `M results.csv`, `M results.json`
- Final working tree (after resetting artifacts, before VERIFY.md): clean
- Wall time: <1s
- Runner exit status: 0
- Unittest exit status: 0

The implementation SHA recorded above is the tested revision. This documentation commit is a direct descendant changing only VERIFY.md.
