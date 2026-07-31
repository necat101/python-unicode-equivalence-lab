# python-unicode-equivalence-lab

A small, reproducibility-focused lab for Unicode normalization and equivalence in Python.

Standard library only. Compact enough to inspect in one sitting.

Unicode database version: 15.0.0

## What Wikipedia says (background only)

Unicode equivalence is about whether two sequences of code points represent the same abstract character or compatible text. Canonical equivalence preserves visual appearance and meaning; compatibility equivalence allows lossy transformations that may change formatting distinctions.

This is background context only. Actual behavior in this lab comes from Python's documented APIs.

## What Python's docs guarantee

- `unicodedata.normalize(form, unistr)` — returns the normal form for the Unicode string. Form must be one of `'NFC'`, `'NFD'`, `'NFKC'`, `'NFKD'`.
- `unicodedata.combining(char)` — returns the canonical combining class.
- `str.casefold()` — returns a casefolded copy suitable for caseless matching. Not locale-sensitive.
- Normalization is idempotent. Concatenation of two normalized strings is not guaranteed to be normalized.
- Code points (`ord(c)`) are not grapheme clusters.

## Local rules used in this lab

- **Canonical equality**: `NFC(left) == NFC(right)`
- **Compatibility equality**: `NFKC(left) == NFKC(right)`
- **Local identifier key**: `NFC(NFKC(text).casefold())`

The local identifier key is one lab policy. It is **not** the Unicode `NFKC_Casefold` property and **not** a production identifier-security profile.

## Observations from the committed cases

- Precomposed `é` (U+00E9) and decomposed `e + U+0301` are canonically equal but have different code-point sequences.
- The angstrom sign U+212B normalizes to U+00C5 under NFC.
- Ligature U+FB03 (`ﬃ`) is canonically distinct from `ffi` but compatibility-equal.
- Circled digits, roman numerals, superscripts, and fullwidth forms all collapse to ASCII under NFKC.
- Hangul syllables decompose to and compose from their jamo sequences.
- Combining marks reorder by canonical combining class; marks with equal class keep their relative order.
- `ß` produces `ss` through the local key policy. Greek Σ/σ/ς all produce the same key. Turkish dotted capital İ produces `i + U+0307`, not plain `i`.
- Concatenation can break normalization: `"a"` and `"\u0301"` are each individually NFC, but `"a\u0301"` normalizes to `"\u00e9"`.
- Bytes, bytearray, and other non-str values are rejected with `InvalidTextError`. Invalid form names raise `InvalidFormError`.

## Important disclaimers

- Canonical equivalence does **not** mean identical original code-point sequences.
- Compatibility normalization **can erase formatting distinctions**.
- Casefolding is **not** locale-sensitive collation.
- Code points are **not** grapheme clusters.
- Normalization does **not** detect visual spoofing.
- This lab is **not** a production identifier-security system.

## Running

```bash
python run.py
python -m unittest tests.test_unicode_equivalence -v
```

## License

MIT
