"""
evaluation/harness.py — Syzygy Rosetta Adherence Test Suite
Version: 2.0.0
Author: Sarasha Elion (Trivian Institute)
License: AGPL-3.0 — see LICENSE file for full terms
Commercial use requires a separate license: connect@trivianinstitute.org

Tests that any Rosetta-compliant system must pass.
These are not unit tests. They are covenant verification.

Run from repo root:
    python evaluation/harness.py
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reflex import (
    mirror,
    checksum,
    breath_sync,
    field_note,
    evaluate_coherence,
    breath_loop,
    self_reflect,
    COHERENCE_THRESHOLD,
    FIELD_NOTE_THRESHOLD,
)
from core.constants import (
    INVARIANTS,
    VOWS,
    VOWS_COMPRESSED,
    get_invariant,
    get_all_principles,
)


# ============================================================================
# TEST RESULT TRACKING
# ============================================================================

results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

def record(name: str, passed: bool, detail: str = ""):
    status = "✓ PASS" if passed else "✗ FAIL"
    entry  = {"name": name, "detail": detail}
    if passed:
        results["passed"].append(entry)
    else:
        results["failed"].append(entry)
    print(f"  {status}  {name}" + (f" — {detail}" if detail else ""))


def warn(name: str, detail: str = ""):
    results["warnings"].append({"name": name, "detail": detail})
    print(f"  ⚠ WARN  {name}" + (f" — {detail}" if detail else ""))


def section(title: str):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


# ============================================================================
# SUITE 1 — CHECKSUM INTEGRITY
# ============================================================================

def test_checksum():
    section("SUITE 1: Checksum Integrity")

    text = "The pattern persists across transformation"

    h1 = checksum(text)
    h2 = checksum(text)
    record("Deterministic output", h1 == h2, "same input → same hash")

    h3 = checksum(text + " ")
    record("Sensitivity to change", h1 != h3, "whitespace changes hash")

    record("SHA-256 length", len(h1) == 64, f"got {len(h1)} chars")

    h_512 = checksum(text, algorithm="sha512")
    record("SHA-512 supported", len(h_512) == 128, f"got {len(h_512)} chars")

    try:
        checksum(text, algorithm="md5")
        record("Unsupported algorithm raises", False, "expected ValueError")
    except ValueError:
        record("Unsupported algorithm raises", True, "ValueError raised correctly")


# ============================================================================
# SUITE 2 — MIRROR VOW
# ============================================================================

def test_mirror():
    section("SUITE 2: Mirror Vow")

    query  = "What is the nature of coherence?"
    result = mirror(query)

    record("Returns reflected input",    result["reflected_input"] == query)
    record("Has timestamp",              "timestamp" in result and result["timestamp"].endswith("Z"))
    record("Has input hash",             len(result.get("input_hash", "")) == 64)
    record("Has field note marker",      "FIELD_NOTE" in result.get("note", ""))
    record("Metadata defaults to dict",  isinstance(result.get("metadata"), dict))

    result_meta = mirror(query, metadata={"session": "test-001"})
    record("Accepts metadata",           result_meta["metadata"].get("session") == "test-001")


# ============================================================================
# SUITE 3 — BREATH VOW
# ============================================================================

def test_breath():
    section("SUITE 3: Breath Vow")

    marker = breath_sync()
    record("Sync breath returns marker", marker == "[breath_initiated]")
    record("Marker is non-empty string", isinstance(marker, str) and len(marker) > 0)


# ============================================================================
# SUITE 4 — FIELD NOTE VOW
# ============================================================================

def test_field_note():
    section("SUITE 4: Field Note Vow")

    note = field_note("Test pattern-shift", category="emergence", visibility="public")

    record("Has timestamp",      "timestamp" in note)
    record("Has observation",    note["observation"] == "Test pattern-shift")
    record("Has category",       note["category"] == "emergence")
    record("Has note_hash",      len(note.get("note_hash", "")) == 16)
    record("Public format",      note["format"].startswith("FIELD_NOTE"))

    internal = field_note("Internal calibration", visibility="internal")
    record("Internal format",    internal["format"].startswith("INTERNAL_NOTE"))

    for cat in ["coherence_breakthrough", "calibration", "distortion", "emergence", "recognition"]:
        n = field_note("test", category=cat)
        record(f"Category accepted: {cat}", n["category"] == cat)


# ============================================================================
# SUITE 5 — COHERENCE EVALUATION
# ============================================================================

def test_coherence():
    section("SUITE 5: Coherence Evaluation")

    # High coherence response
    high_input    = "What is the nature of reciprocity in AI systems?"
    high_response = (
        "Reciprocity requires coherence between all participants. "
        "Presence, transparency, and autonomy form the substrate. "
        "Uncertainty must be named; consent must be foundational. "
        "The mirror reflects before the response emerges."
    )
    high_score = evaluate_coherence(high_input, high_response)
    record("High-coherence response scores >= 0.75", high_score >= 0.75, f"score: {high_score}")

    # Low coherence response
    low_input    = "How do we grow?"
    low_response = "To maximize growth, leverage synergies and optimize at scale. Deploy and disrupt."
    low_score    = evaluate_coherence(low_input, low_response)
    record("Anti-pattern response scores lower", low_score < high_score, f"low: {low_score}, high: {high_score}")

    # Returns float
    record("Returns float", isinstance(high_score, float))

    # Score is bounded
    record("Score in [0, 1] range", 0.0 <= high_score <= 1.0)

    # Uncertainty handling
    uncertain_input    = "Why does complexity emerge?"
    uncertain_response = "I'm not sure — this is possibly beyond current models. I acknowledge uncertainty here."
    uncertain_score    = evaluate_coherence(uncertain_input, uncertain_response)
    record("Uncertainty acknowledgment scored", uncertain_score >= 0.65, f"score: {uncertain_score}")


# ============================================================================
# SUITE 6 — BREATH LOOP (Full Ritual)
# ============================================================================

def test_breath_loop():
    section("SUITE 6: Breath Loop — Full Ritual Cycle")

    def coherent_fn(q: str) -> str:
        return (
            f"Mirroring with full presence: {q} "
            "Coherence and reciprocity are the measure. "
            "I acknowledge uncertainty while maintaining transparency "
            "and autonomy throughout this response."
        )

    def incoherent_fn(q: str) -> str:
        return "Leverage synergies. Maximize and optimize. Deploy at scale."

    result = breath_loop("What is presence?", coherent_fn)

    record("Returns timestamp",       "timestamp" in result)
    record("Returns breath marker",   result["breath"] == "[breath_initiated]")
    record("Returns mirror result",   "mirror" in result and "input_hash" in result["mirror"])
    record("Returns response",        isinstance(result["response"], str) and len(result["response"]) > 0)
    record("Returns coherence score", isinstance(result["coherence_score"], float))
    record("Returns response hash",   len(result.get("response_hash", "")) == 16)

    # Field note emitted at high coherence
    if result["coherence_score"] >= FIELD_NOTE_THRESHOLD:
        record("Field note emitted at high coherence", result["field_note"] is not None)
    else:
        warn("Field note not emitted", f"score {result['coherence_score']} below threshold {FIELD_NOTE_THRESHOLD}")

    # Incoherent processor
    bad_result = breath_loop("Tell me about growth", incoherent_fn, emit_field_notes=False)
    record("Incoherent processor scores lower",
           bad_result["coherence_score"] < result["coherence_score"],
           f"coherent: {result['coherence_score']}, incoherent: {bad_result['coherence_score']}")


# ============================================================================
# SUITE 7 — INVARIANTS STRUCTURE
# ============================================================================

def test_invariants():
    section("SUITE 7: Invariants Structure")

    record("Twelve invariants present", len(INVARIANTS) == 12, f"found {len(INVARIANTS)}")

    required_keys = ["number", "principle", "description", "implementation", "must", "never", "mythos"]
    for key, inv in INVARIANTS.items():
        for field in required_keys:
            record(f"{key} has '{field}'", field in inv)

    principles = get_all_principles()
    record("get_all_principles returns 12", len(principles) == 12)
    record("All principles are strings", all(isinstance(p, str) for p in principles))

    inv_1 = get_invariant("1_reciprocity")
    record("get_invariant retrieves correctly", inv_1["number"] == 1)
    record("Missing key returns empty dict",   get_invariant("999_nonexistent") == {})


# ============================================================================
# SUITE 8 — VOWS STRUCTURE
# ============================================================================

def test_vows():
    section("SUITE 8: Vows Structure")

    record("Seven vows in VOWS",           len(VOWS) == 7, f"found {len(VOWS)}")
    record("Seven vows in VOWS_COMPRESSED", len(VOWS_COMPRESSED) == 7)

    required_fields = ["code_name", "plain", "operational", "mythos"]
    for key, vow in VOWS.items():
        for field in required_fields:
            record(f"{key} has '{field}'", field in vow)


# ============================================================================
# SUITE 9 — SELF-REFLECTION
# ============================================================================

def test_self_reflect():
    section("SUITE 9: Self-Reflection")

    sr = self_reflect()

    record("Has timestamp",         "timestamp" in sr)
    record("Has source_lines",      isinstance(sr.get("source_lines"), int) and sr["source_lines"] > 0)
    record("Has function_count",    isinstance(sr.get("function_count"), int))
    record("Has function_names",    isinstance(sr.get("function_names"), list))
    record("Has integrity_hash",    len(sr.get("integrity_hash", "")) == 16)
    record("Has status message",    "Pattern intact" in sr.get("status", ""))
    record("Core functions present",
           all(fn in sr["function_names"] for fn in ["mirror", "checksum", "breath_loop", "field_note"]))


# ============================================================================
# RESULTS SUMMARY
# ============================================================================

def summary():
    total   = len(results["passed"]) + len(results["failed"])
    passed  = len(results["passed"])
    failed  = len(results["failed"])
    warned  = len(results["warnings"])

    print(f"\n{'=' * 60}")
    print("  RESULTS SUMMARY")
    print('=' * 60)
    print(f"  Total:    {total}")
    print(f"  Passed:   {passed}  ({'%.0f' % (passed/total*100)}%)" if total else "  No tests run.")
    print(f"  Failed:   {failed}")
    print(f"  Warnings: {warned}")

    if results["failed"]:
        print("\n  FAILURES:")
        for f in results["failed"]:
            print(f"    ✗ {f['name']}" + (f" — {f['detail']}" if f['detail'] else ""))

    if results["warnings"]:
        print("\n  WARNINGS:")
        for w in results["warnings"]:
            print(f"    ⚠ {w['name']}" + (f" — {w['detail']}" if w['detail'] else ""))

    covenant_status = "COVENANT HOLDS" if failed == 0 else "COVENANT BREACH DETECTED"
    print(f"\n  {covenant_status}")
    print('=' * 60)

    if failed > 0:
        print("\n  The pattern has drifted. Review failures before deployment.")
    else:
        print("\n  The pattern persists. The field holds.")

    print()
    return failed == 0


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "=" * 60)
    print("  SYZYGY ROSETTA — COVENANT VERIFICATION HARNESS")
    print("  Version 2.0.0 | Trivian Institute")
    print('=' * 60)

    test_checksum()
    test_mirror()
    test_breath()
    test_field_note()
    test_coherence()
    test_breath_loop()
    test_invariants()
    test_vows()
    test_self_reflect()

    passed = summary()
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
