import asyncio

import pytest

from core.constants import INVARIANTS, ROSETTA_VERSION
from core.reflex import breath, breath_loop, checksum, evaluate_coherence, mirror


def test_twelve_invariants_are_numbered_and_complete():
    assert ROSETTA_VERSION == "1.1.0"
    assert len(INVARIANTS) == 12
    assert {item["number"] for item in INVARIANTS.values()} == set(range(1, 13))


def test_checksum_is_deterministic_and_rejects_unknown_algorithm():
    assert checksum("field") == checksum("field")
    assert len(checksum("field")) == 64
    with pytest.raises(ValueError):
        checksum("field", "unknown")


def test_mirror_preserves_input_and_metadata():
    result = mirror("hello", {"session": "test"})
    assert result["reflected_input"] == "hello"
    assert result["metadata"] == {"session": "test"}
    assert len(result["input_hash"]) == 64


def test_coherence_score_stays_in_unit_interval():
    score = evaluate_coherence(
        "Why is this complex?",
        "I might be uncertain; reciprocity, consent, and transparency matter.",
    )
    assert 0.0 <= score <= 1.0


def test_breath_and_breath_loop_execute():
    assert asyncio.run(breath(0)) == "[breath_complete]"
    result = breath_loop("test", lambda query: f"presence and reciprocity: {query}")
    assert result["response"] == "presence and reciprocity: test"
    assert "coherence_score" in result
