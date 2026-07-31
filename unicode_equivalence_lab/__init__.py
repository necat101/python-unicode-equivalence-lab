"""python-unicode-equivalence-lab

Small reproducibility lab for Unicode normalization and equivalence.
Standard library only.
"""

import unicodedata

__version__ = "0.1.0"

_VALID_FORMS = {"NFC", "NFD", "NFKC", "NFKD"}


class InvalidFormError(ValueError):
    """Normalization form was not one of NFC, NFD, NFKC, NFKD."""


class InvalidTextError(TypeError):
    """A text argument was not a Python str."""


def _check_form(form):
    if not isinstance(form, str) or form not in _VALID_FORMS:
        raise InvalidFormError("form must be one of NFC, NFD, NFKC, NFKD")


def _check_text(text):
    if not isinstance(text, str):
        raise InvalidTextError("text must be str")


def normalize_text(form, text):
    """Normalize text using the given form."""
    _check_form(form)
    _check_text(text)
    return unicodedata.normalize(form, text)


def codepoints(text):
    """Return code points as U+XXXX tuples."""
    _check_text(text)
    return tuple(f"U+{ord(char):04X}" for char in text)


def canonical_equal(left, right):
    """Canonical equality: NFC(left) == NFC(right)."""
    _check_text(left)
    _check_text(right)
    return normalize_text("NFC", left) == normalize_text("NFC", right)


def compatibility_equal(left, right):
    """Compatibility equality: NFKC(left) == NFKC(right)."""
    _check_text(left)
    _check_text(right)
    return normalize_text("NFKC", left) == normalize_text("NFKC", right)


def local_identifier_key(text):
    """Local identifier key: NFC(NFKC(text).casefold()).
    
    This is one lab policy, not the Unicode NFKC_Casefold property
    and not a production identifier-security profile.
    """
    _check_text(text)
    return normalize_text("NFC", normalize_text("NFKC", text).casefold())


def is_normalized(form, text):
    """Check if text is already normalized in the given form."""
    _check_form(form)
    _check_text(text)
    return normalize_text(form, text) == text


def concatenation_preserves_form(form, left, right):
    """True if left, right are individually normalized and their
    concatenation is also normalized. False otherwise.
    
    Exceptions are only raised for invalid form or text types,
    not for normalization non-closure.
    """
    _check_form(form)
    _check_text(left)
    _check_text(right)
    if not is_normalized(form, left):
        return False
    if not is_normalized(form, right):
        return False
    return is_normalized(form, left + right)


__all__ = [
    "InvalidFormError",
    "InvalidTextError",
    "normalize_text",
    "codepoints",
    "canonical_equal",
    "compatibility_equal",
    "local_identifier_key",
    "is_normalized",
    "concatenation_preserves_form",
]
