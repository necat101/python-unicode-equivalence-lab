import unittest
import unicodedata
from unicode_equivalence_lab import (
    normalize_text, codepoints, canonical_equal, compatibility_equal,
    local_identifier_key, is_normalized, concatenation_preserves_form,
    InvalidFormError, InvalidTextError,
)

class TestUnicodeEquivalence(unittest.TestCase):

    def test_all_four_forms(self):
        text = "A\u00e9"
        for form in ("NFC", "NFD", "NFKC", "NFKD"):
            out = normalize_text(form, text)
            self.assertIsInstance(out, str)
            # direct unicodedata check
            self.assertEqual(out, unicodedata.normalize(form, text))

    def test_codepoints_format(self):
        self.assertEqual(codepoints("A\u00e9"), ("U+0041", "U+00E9"))
        self.assertEqual(codepoints(""), ())

    def test_canonical_compose_decompose(self):
        self.assertEqual(normalize_text("NFD", "\u00e9"), "e\u0301")
        self.assertEqual(normalize_text("NFC", "e\u0301"), "\u00e9")

    def test_compatibility_changes(self):
        # ligature
        self.assertEqual(normalize_text("NFKC", "\ufb03"), "ffi")
        # circled digit
        self.assertEqual(normalize_text("NFKC", "\u2460"), "1")
        # roman numeral
        self.assertEqual(normalize_text("NFKC", "\u2168"), "IX")
        # superscript
        self.assertEqual(normalize_text("NFKC", "\u2075"), "5")
        # fullwidth
        self.assertEqual(normalize_text("NFKC", "\uff21"), "A")

    def test_hangul(self):
        decomposed = normalize_text("NFD", "\uac00")
        self.assertEqual(decomposed, "\u1100\u1161")
        composed = normalize_text("NFC", "\u1100\u1161")
        self.assertEqual(composed, "\uac00")

    def test_combining_reorder(self):
        # different classes: U+0301 (230), U+0327 (202)
        # NFD should reorder to lower class first
        out = normalize_text("NFD", "a\u0301\u0327")
        self.assertEqual(out, "a\u0327\u0301")

    def test_combining_equal_class_stable(self):
        # both 230, order preserved
        out = normalize_text("NFD", "x\u0300\u0301")
        self.assertEqual(out, "x\u0300\u0301")

    def test_idempotence(self):
        for form in ("NFC", "NFD", "NFKC", "NFKD"):
            s = normalize_text(form, "Hello \u00e9 \ufb03")
            self.assertTrue(is_normalized(form, s))
            self.assertEqual(normalize_text(form, s), s)

    def test_concatenation_non_closure(self):
        left = "a"
        right = "\u0301"
        self.assertTrue(is_normalized("NFC", left))
        self.assertTrue(is_normalized("NFC", right))
        self.assertFalse(is_normalized("NFC", left + right))
        self.assertFalse(concatenation_preserves_form("NFC", left, right))

    def test_canonical_vs_compatibility(self):
        # canonically equal
        self.assertTrue(canonical_equal("\u00e9", "e\u0301"))
        self.assertTrue(canonical_equal("\u212b", "\u00c5"))
        # canonically distinct but compat equal
        self.assertFalse(canonical_equal("\ufb03", "ffi"))
        self.assertTrue(compatibility_equal("\ufb03", "ffi"))
        # compat distinct
        self.assertFalse(compatibility_equal("\u00e9", "e"))

    def test_sharp_s_sigma_dotted_i_fullwidth(self):
        # ß → ss
        key = local_identifier_key("\u00df")
        self.assertEqual(key, "ss")
        # Σ / σ same key
        k1 = local_identifier_key("\u03a3")
        k2 = local_identifier_key("\u03c3")
        self.assertEqual(k1, k2)
        # final sigma / sigma same key
        k1 = local_identifier_key("\u03c2")
        k2 = local_identifier_key("\u03c3")
        self.assertEqual(k1, k2)
        # Turkish İ → i + U+0307
        key = local_identifier_key("\u0130")
        self.assertEqual(key, "i\u0307")
        self.assertEqual(codepoints(key), ("U+0069", "U+0307"))
        # fullwidth Ａ and a same key
        k1 = local_identifier_key("\uff21")
        k2 = local_identifier_key("a")
        self.assertEqual(k1, k2)

    def test_key_pipeline_exact_order(self):
        # verify NFKC → casefold → NFC
        text = "Stra\u00dfe"
        step1 = unicodedata.normalize("NFKC", text)
        step2 = step1.casefold()
        step3 = unicodedata.normalize("NFC", step2)
        self.assertEqual(local_identifier_key(text), step3)
        self.assertEqual(step3, "strasse")

    def test_type_validation(self):
        with self.assertRaises(InvalidFormError):
            normalize_text("nfc", "x")
        with self.assertRaises(InvalidFormError):
            normalize_text("NFQ", "x")
        with self.assertRaises(InvalidTextError):
            normalize_text("NFC", b"x")
        with self.assertRaises(InvalidTextError):
            codepoints(b"x")
        with self.assertRaises(InvalidTextError):
            local_identifier_key(bytearray(b"x"))

    def test_validation_precedence(self):
        # normalize_text: form first, then text
        with self.assertRaises(InvalidFormError):
            normalize_text("bad", b"x")
        # is_normalized: form first
        with self.assertRaises(InvalidFormError):
            is_normalized("bad", b"x")
        # concatenation_preserves_form: form, left, right
        with self.assertRaises(InvalidFormError):
            concatenation_preserves_form("bad", b"l", "r")
        with self.assertRaises(InvalidTextError):
            concatenation_preserves_form("NFC", b"l", "r")
        with self.assertRaises(InvalidTextError):
            concatenation_preserves_form("NFC", "l", b"r")
        # canonical_equal: left, then right
        with self.assertRaises(InvalidTextError):
            canonical_equal(b"l", "r")
        with self.assertRaises(InvalidTextError):
            canonical_equal("l", b"r")
        # compatibility_equal: left, then right
        with self.assertRaises(InvalidTextError):
            compatibility_equal(b"l", "r")

    def test_nul_zwj_regional(self):
        # embedded NUL
        s = "a\0b"
        self.assertEqual(normalize_text("NFC", s), s)
        # ZWJ emoji codepoints
        cps = codepoints("\U0001f469\u200d\U0001f52c")
        self.assertEqual(cps, ("U+1F469", "U+200D", "U+1F52C"))
        # regional indicators
        cps = codepoints("\U0001f1fa\U0001f1f8")
        self.assertEqual(cps, ("U+1F1FA", "U+1F1F8"))

    def test_caller_strings_unchanged(self):
        left = "e\u0301"
        right = "\u00e9"
        _ = canonical_equal(left, right)
        self.assertEqual(left, "e\u0301")
        self.assertEqual(right, "\u00e9")
        text = "Stra\u00dfe"
        _ = local_identifier_key(text)
        self.assertEqual(text, "Stra\u00dfe")

    def test_manifest_independent_reconstruction(self):
        # At least one case per classification, reconstructed independently
        # success
        self.assertEqual(normalize_text("NFC", ""), "")
        # invalid_form
        with self.assertRaises(InvalidFormError):
            normalize_text("nfc", "x")
        # invalid_text
        with self.assertRaises(InvalidTextError):
            codepoints(b"x")
        # canonical_equal
        l = unicodedata.normalize("NFC", "\u00e9")
        r = unicodedata.normalize("NFC", "e\u0301")
        self.assertEqual(l, r)
        # canonical_distinct
        l = unicodedata.normalize("NFC", "\ufb03")
        r = unicodedata.normalize("NFC", "ffi")
        self.assertNotEqual(l, r)
        # compatibility_equal
        l = unicodedata.normalize("NFKC", "\u2460")
        r = unicodedata.normalize("NFKC", "1")
        self.assertEqual(l, r)
        # compatibility_distinct
        l = unicodedata.normalize("NFKC", "\u00e9")
        r = unicodedata.normalize("NFKC", "e")
        self.assertNotEqual(l, r)
        # key_equal
        k1 = unicodedata.normalize("NFC", unicodedata.normalize("NFKC", "\u03a3").casefold())
        k2 = unicodedata.normalize("NFC", unicodedata.normalize("NFKC", "\u03c3").casefold())
        self.assertEqual(k1, k2)
        # key_distinct
        k1 = unicodedata.normalize("NFC", unicodedata.normalize("NFKC", "\u0131").casefold())
        k2 = unicodedata.normalize("NFC", unicodedata.normalize("NFKC", "i").casefold())
        self.assertNotEqual(k1, k2)
        # idempotent
        s = unicodedata.normalize("NFC", "test")
        self.assertEqual(unicodedata.normalize("NFC", s), s)
        # not_closed_under_concatenation
        left, right = "a", "\u0301"
        self.assertEqual(unicodedata.normalize("NFC", left), left)
        self.assertEqual(unicodedata.normalize("NFC", right), right)
        self.assertNotEqual(unicodedata.normalize("NFC", left + right), left + right)


if __name__ == "__main__":
    unittest.main()
