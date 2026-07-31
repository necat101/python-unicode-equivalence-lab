# Results

Total cases: 42

## Classification totals

- canonical_distinct: 1
- canonical_equal: 2
- compatibility_distinct: 1
- compatibility_equal: 2
- idempotent: 4
- invalid_form: 2
- invalid_text: 3
- key_distinct: 1
- key_equal: 4
- not_closed_under_concatenation: 1
- success: 21

## Cases

| case_id | operation | classification | pass |
|---|---|---|---|
| c01_empty_nfc | normalize_text | success | PASS |
| c02_ascii_all_forms | normalize_text | success | PASS |
| c03_e_acute_decompose | normalize_text | success | PASS |
| c04_e_acute_compose | normalize_text | success | PASS |
| c05_angstrom_sign_nfc | normalize_text | success | PASS |
| c06_ring_a_decompose | normalize_text | success | PASS |
| c07_ligature_ffi_canonical_distinct | canonical_equal | canonical_distinct | PASS |
| c08_ligature_ffi_compat_equal | compatibility_equal | compatibility_equal | PASS |
| c09_circled_one | normalize_text | success | PASS |
| c10_roman_nine | normalize_text | success | PASS |
| c11_superscript_five | normalize_text | success | PASS |
| c12_fullwidth_a | normalize_text | success | PASS |
| c13_hangul_decompose | normalize_text | success | PASS |
| c14_hangul_compose | normalize_text | success | PASS |
| c15_combining_reorder | normalize_text | success | PASS |
| c16_combining_equal_class_stable | normalize_text | success | PASS |
| c17_bytes_reject_normalize | normalize_text | invalid_text | PASS |
| c18_embedded_nul | normalize_text | success | PASS |
| c19_zwj_emoji | codepoints | success | PASS |
| c20_regional_indicators | codepoints | success | PASS |
| c21_sharp_s_key | local_identifier_key | success | PASS |
| c22_greek_sigma_key_equal | local_identifier_key_equal | key_equal | PASS |
| c23_greek_final_sigma_key_equal | local_identifier_key_equal | key_equal | PASS |
| c24_turkish_dotted_i | local_identifier_key | success | PASS |
| c25_fullwidth_key_equal | local_identifier_key_equal | key_equal | PASS |
| c26_e_acute_canonical_equal | canonical_equal | canonical_equal | PASS |
| c27_angstrom_canonical_equal | canonical_equal | canonical_equal | PASS |
| c28_ligature_codepoints | codepoints | success | PASS |
| c29_ffi_codepoints | codepoints | success | PASS |
| c30_circled_one_compat_equal | compatibility_equal | compatibility_equal | PASS |
| c31_e_acute_compat_distinct | compatibility_equal | compatibility_distinct | PASS |
| c32_strasse_key_equal | local_identifier_key_equal | key_equal | PASS |
| c33_dotless_i_key_distinct | local_identifier_key_equal | key_distinct | PASS |
| c34_nfc_idempotent | is_normalized | idempotent | PASS |
| c35_nfd_idempotent | is_normalized | idempotent | PASS |
| c36_nfkc_idempotent | is_normalized | idempotent | PASS |
| c37_nfkd_idempotent | is_normalized | idempotent | PASS |
| c38_concat_not_closed | concatenation_preserves_form | not_closed_under_concatenation | PASS |
| c39_lowercase_nfc_reject | normalize_text | invalid_form | PASS |
| c40_unknown_form_reject | normalize_text | invalid_form | PASS |
| c41_codepoints_bytes_reject | codepoints | invalid_text | PASS |
| c42_key_bytearray_reject | local_identifier_key | invalid_text | PASS |

