#!/usr/bin/env python3
"""Runner for python-unicode-equivalence-lab."""

import json
import csv
import unicodedata
from unicode_equivalence_lab import (
    normalize_text, codepoints, canonical_equal, compatibility_equal,
    local_identifier_key, is_normalized, concatenation_preserves_form,
    InvalidFormError, InvalidTextError,
)
from unicode_equivalence_lab.manifest import CASES

def escape_str(s):
    if not isinstance(s, str):
        return repr(s)
    return s.encode("unicode_escape").decode("ascii")

def get_codepoints(s):
    if not isinstance(s, str):
        return ()
    return codepoints(s)

def combining_classes(s):
    if not isinstance(s, str):
        return ()
    return tuple(unicodedata.combining(ch) for ch in s)

def run_case(case):
    cid = case["id"]
    op = case["operation"]
    expected_exception = case.get("expect_exception")
    classification = case["classification"]
    observation = case["observation"]

    actual_output = None
    actual_bool = None
    exception_name = ""
    form = case.get("form", "")
    inputs_escaped = ""
    cp_left = ()
    cp_right = ()
    comb_classes = ""

    try:
        if op == "normalize_text":
            if case.get("all_forms"):
                text = case["text"]
                inputs_escaped = f"text={escape_str(text)}"
                cp_left = get_codepoints(text)
                results = {}
                for f in ("NFC", "NFD", "NFKC", "NFKD"):
                    results[f] = normalize_text(f, text)
                actual_output = results
                expected = case["expected_output"]
            else:
                form = case["form"]
                text = case["text"]
                inputs_escaped = f"form={form} text={escape_str(text)}"
                cp_left = get_codepoints(text) if isinstance(text, str) else ()
                actual_output = normalize_text(form, text)
                expected = case["expected_output"]
                if isinstance(text, str):
                    comb_classes = ",".join(str(x) for x in combining_classes(text))
        elif op == "codepoints":
            text = case["text"]
            inputs_escaped = f"text={escape_str(text) if isinstance(text, str) else repr(text)}"
            cp_left = get_codepoints(text) if isinstance(text, str) else ()
            actual_output = codepoints(text)
            expected = case["expected_output"]
        elif op == "canonical_equal":
            left = case["left"]
            right = case["right"]
            inputs_escaped = f"left={escape_str(left)} right={escape_str(right)}"
            cp_left = get_codepoints(left)
            cp_right = get_codepoints(right)
            actual_bool = canonical_equal(left, right)
            expected = case["expected_bool"]
        elif op == "compatibility_equal":
            left = case["left"]
            right = case["right"]
            inputs_escaped = f"left={escape_str(left)} right={escape_str(right)}"
            cp_left = get_codepoints(left)
            cp_right = get_codepoints(right)
            actual_bool = compatibility_equal(left, right)
            expected = case["expected_bool"]
        elif op == "local_identifier_key":
            text = case["text"]
            inputs_escaped = f"text={escape_str(text) if isinstance(text, str) else repr(text)}"
            cp_left = get_codepoints(text) if isinstance(text, str) else ()
            actual_output = local_identifier_key(text)
            expected = case["expected_output"]
        elif op == "local_identifier_key_equal":
            left = case["left"]
            right = case["right"]
            inputs_escaped = f"left={escape_str(left)} right={escape_str(right)}"
            cp_left = get_codepoints(left)
            cp_right = get_codepoints(right)
            k1 = local_identifier_key(left)
            k2 = local_identifier_key(right)
            actual_bool = (k1 == k2)
            actual_output = k1
            expected = case["expected_bool"]
        elif op == "is_normalized":
            form = case["form"]
            text = case["text"]
            inputs_escaped = f"form={form} text={escape_str(text)}"
            cp_left = get_codepoints(text)
            actual_bool = is_normalized(form, text)
            expected = case["expected_bool"]
        elif op == "concatenation_preserves_form":
            form = case["form"]
            left = case["left"]
            right = case["right"]
            inputs_escaped = f"form={form} left={escape_str(left)} right={escape_str(right)}"
            cp_left = get_codepoints(left)
            cp_right = get_codepoints(right)
            actual_bool = concatenation_preserves_form(form, left, right)
            expected = case["expected_bool"]
        else:
            raise RuntimeError(f"unknown operation {op}")

    except Exception as e:
        exception_name = type(e).__name__
        expected = None
        actual_output = None
        actual_bool = None

    # Check pass/fail
    passed = False
    if expected_exception:
        passed = (exception_name == expected_exception)
    else:
        if op in ("canonical_equal", "compatibility_equal", "is_normalized", "concatenation_preserves_form", "local_identifier_key_equal"):
            passed = (actual_bool == expected)
        else:
            passed = (actual_output == expected)

    # Verify codepoints match actual strings
    if op == "normalize_text" and not case.get("all_forms") and isinstance(case.get("text"), str) and exception_name == "":
        actual_cps = get_codepoints(case["text"])
        if "codepoints_input" in case:
            assert actual_cps == case["codepoints_input"], f"{cid} input codepoints mismatch"
    
    row = {
        "case_id": cid,
        "operation": op,
        "classification": classification,
        "form": form,
        "inputs_escaped": inputs_escaped,
        "codepoints_left": "|".join(cp_left),
        "codepoints_right": "|".join(cp_right),
        "expected_output": json.dumps(expected, ensure_ascii=False) if expected is not None and not isinstance(expected, bool) else (str(expected) if expected is not None else ""),
        "actual_output": json.dumps(actual_output, ensure_ascii=False) if actual_output is not None and not isinstance(actual_output, bool) else (str(actual_output) if actual_output is not None else ""),
        "expected_bool": "" if case.get("expected_bool") is None else str(case["expected_bool"]),
        "actual_bool": "" if actual_bool is None else str(actual_bool),
        "exception": exception_name,
        "combining_classes": comb_classes,
        "observation": observation,
        "pass": "PASS" if passed else "FAIL",
    }
    return row, passed

def main():
    rows = []
    for case in CASES:
        row, passed = run_case(case)
        rows.append(row)

    # validations
    assert len(rows) == 42, f"expected 42 rows, got {len(rows)}"
    case_ids = [r["case_id"] for r in rows]
    assert len(set(case_ids)) == 42, "duplicate case ids"
    
    recognized_ops = {"normalize_text", "codepoints", "canonical_equal", "compatibility_equal", "local_identifier_key", "local_identifier_key_equal", "is_normalized", "concatenation_preserves_form"}
    for r in rows:
        assert r["operation"] in recognized_ops, f"unrecognized op {r['operation']}"
    
    recognized_classes = {"success", "invalid_form", "invalid_text", "canonical_equal", "canonical_distinct", "compatibility_equal", "compatibility_distinct", "key_equal", "key_distinct", "idempotent", "not_closed_under_concatenation"}
    for r in rows:
        assert r["classification"] in recognized_classes, f"unrecognized classification {r['classification']}"

    # totals
    from collections import Counter
    totals = Counter(r["classification"] for r in rows)
    assert sum(totals.values()) == 42

    # all rows must PASS
    fails = [r["case_id"] for r in rows if r["pass"] != "PASS"]
    assert not fails, f"failing cases: {fails}"

    # write results.json
    with open("results.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(rows, f, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        f.write("\n")

    # write results.csv
    fieldnames = ["case_id","operation","classification","form","inputs_escaped","codepoints_left","codepoints_right","expected_output","actual_output","expected_bool","actual_bool","exception","combining_classes","observation","pass"]
    with open("results.csv", "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)

    # write RESULTS.md
    with open("RESULTS.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("# Results\n\n")
        f.write(f"Total cases: {len(rows)}\n\n")
        f.write("## Classification totals\n\n")
        for cls in sorted(recognized_classes):
            f.write(f"- {cls}: {totals.get(cls, 0)}\n")
        f.write("\n## Cases\n\n")
        f.write("| case_id | operation | classification | pass |\n")
        f.write("|---|---|---|---|\n")
        for r in rows:
            f.write(f"| {r['case_id']} | {r['operation']} | {r['classification']} | {r['pass']} |\n")
        f.write("\n")

    # terminal totals
    print(f"Total: {len(rows)} cases")
    for cls in sorted(recognized_classes):
        print(f"  {cls}: {totals.get(cls, 0)}")
    print(f"Failures: {len(fails)}")

    return 0 if not fails else 1

if __name__ == "__main__":
    raise SystemExit(main())
