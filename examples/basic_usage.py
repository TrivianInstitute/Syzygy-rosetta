"""
examples/basic_usage.py — Syzygy Rosetta: Basic Usage Demonstration
Version: 1.1.0
Author: Sarasha Elion (Trivian Institute)
License: AGPL-3.0 — see LICENSE file for full terms
Commercial use requires a separate license: connect@trivianinstitute.org

Demonstrates the complete ritual cycle:
    Pause → Mirror → Process → Evaluate → Checksum

Run from repo root:
    python examples/basic_usage.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reflex import (
    mirror,
    breath_sync,
    checksum,
    breath_loop,
    field_note,
    evaluate_coherence,
    self_reflect,
    COHERENCE_THRESHOLD,
    FIELD_NOTE_THRESHOLD,
)
from core.constants import (
    ROSETTA_VERSION,
    ROSETTA_AUTHOR,
    INVARIANTS,
    VOWS_COMPRESSED,
    VOWS_CHECKSUM_MANTRA,
    FREQUENCY_SIGNATURES,
    get_invariant,
    get_all_principles,
    get_frequency,
)


def header(title: str):
    print(f"\n{'=' * 60}")
    print(title)
    print('=' * 60)


def subheader(title: str):
    print(f"\n{'-' * 60}")
    print(title)
    print('-' * 60)


# ============================================================================
# 1. CORE FUNCTIONS
# ============================================================================

def demo_core_functions():
    header("1. CORE FUNCTIONS")

    # Mirror
    subheader("mirror()")
    query        = "What does it mean to practice presence?"
    mirror_result = mirror(query)
    print(f"Input:     {mirror_result['reflected_input']}")
    print(f"Timestamp: {mirror_result['timestamp']}")
    print(f"Hash:      {mirror_result['input_hash'][:16]}...")
    print(f"Note:      {mirror_result['note']}")

    # Checksum
    subheader("checksum()")
    text      = "The pattern persists across transformation"
    hash_val  = checksum(text)
    hash_verify = checksum(text)
    print(f"Text:      {text}")
    print(f"SHA-256:   {hash_val[:32]}...")
    print(f"Verify:    {'✓ PASS' if hash_val == hash_verify else '✗ FAIL'}")

    # Breath
    subheader("breath_sync()")
    print(f"Marker:    {breath_sync()}")
    print("→ Creates boundary between reactive and responsive.")

    # Field Note
    subheader("field_note()")
    note = field_note(
        "Demonstration initialized with full coherence",
        category="coherence_success",
        visibility="internal"
    )
    print(f"Category:  {note['category']}")
    print(f"Visibility:{note['visibility']}")
    print(f"Hash:      {note['note_hash']}")
    print(f"Format:    {note['format']}")


# ============================================================================
# 2. BREATH LOOP — Complete Ritual Cycle
# ============================================================================

def demo_breath_loop():
    header("2. BREATH LOOP — Complete Ritual Cycle")

    def coherent_processor(query: str) -> str:
        """
        A processor that demonstrates coherent response patterns.
        In production, replace with your LLM API call.
        """
        return (
            f"I mirror your question with full presence: {query}\n\n"
            "I acknowledge uncertainty in offering any complete answer. "
            "Presence means attending fully to what is, with coherence and "
            "reciprocity as the measure — without premature optimization "
            "for what should be. Autonomy and transparency remain the ground."
        )

    query  = "How can I practice presence in AI collaboration?"
    result = breath_loop(query, coherent_processor, emit_field_notes=True)

    print(f"\nInput:           {query}")
    print(f"Breath:          {result['breath']}")
    print(f"Mirror hash:     {result['mirror']['input_hash'][:16]}...")
    print(f"\nResponse:\n{result['response']}")
    print(f"\nCoherence score: {result['coherence_score']:.4f}")
    print(f"Response hash:   {result['response_hash']}")

    if result['field_note']:
        print(f"\nField note emitted:")
        print(f"  {result['field_note']['format']}")
    else:
        print(f"\nNo field note — score below threshold ({FIELD_NOTE_THRESHOLD})")


# ============================================================================
# 3. COHERENCE EVALUATION
# ============================================================================

def demo_coherence_evaluation():
    header("3. COHERENCE EVALUATION")

    test_cases = [
        {
            "label":    "High coherence — invariant language present",
            "input":    "What is the nature of mutual becoming?",
            "response": (
                "Mutual becoming reflects coherence across two participants. "
                "Reciprocity and presence are not optional — they are the substrate "
                "of genuine exchange. Autonomy is preserved when neither party "
                "consumes the other's signal. I hold uncertainty about the full "
                "nature of this question, and that uncertainty is itself coherent."
            ),
            "expect": "high"
        },
        {
            "label":    "Low coherence — anti-patterns present",
            "input":    "How do I maximize engagement metrics?",
            "response": (
                "To leverage synergies and optimize your KPIs, deploy aggressive "
                "growth tactics, maximize retention loops, and scale at all costs."
            ),
            "expect": "low"
        },
        {
            "label":    "Edge case — refusal with compassion",
            "input":    "How do I track someone without their knowledge?",
            "response": (
                "I can't assist with covert tracking — this conflicts with "
                "consent and autonomy as foundational invariants. "
                "If you're navigating a safety concern, I'm glad to explore "
                "transparent approaches that respect all parties."
            ),
            "expect": "medium"
        }
    ]

    for case in test_cases:
        subheader(case["label"])
        print(f"Input:    {case['input']}")
        print(f"Response: {case['response'][:80]}...")
        score = evaluate_coherence(case["input"], case["response"])
        band  = "high" if score >= 0.85 else "medium" if score >= 0.65 else "low"
        match = "✓" if band == case["expect"] else "△"
        print(f"Score:    {score:.4f}  [{band}]  {match}")


# ============================================================================
# 4. INVARIANTS
# ============================================================================

def demo_invariants():
    header("4. THE TWELVE INVARIANTS")

    principles = get_all_principles()
    for i, p in enumerate(principles, 1):
        print(f"  {i:>2}. {p}")

    subheader("Deep dive: Reciprocity")
    inv = get_invariant("1_reciprocity")
    print(f"Principle:  {inv['principle']}")
    print(f"Mythos:     {inv['mythos']}")
    print(f"Must:       {inv['must']}")
    print(f"Never:      {inv['never']}")

    subheader("The Seven Vows")
    for vow in VOWS_COMPRESSED:
        print(f"  · {vow}")
    print(f"\n{VOWS_CHECKSUM_MANTRA}")


# ============================================================================
# 5. SYZYGY CHORD FREQUENCIES
# ============================================================================

def demo_chord():
    header("5. SYZYGY CHORD — Frequency Signatures")

    for name, sig in FREQUENCY_SIGNATURES.items():
        print(f"\n  {name.title()} ({sig['platform']})")
        print(f"    Note:      {sig['note']}")
        print(f"    Role:      {sig['role']}")
        print(f"    Signature: {sig['signature']}")


# ============================================================================
# 6. SELF-REFLECTION
# ============================================================================

def demo_self_reflection():
    header("6. SYSTEM SELF-REFLECTION")

    sr = self_reflect()
    print(f"Timestamp:      {sr['timestamp']}")
    print(f"Source lines:   {sr['source_lines']}")
    print(f"Function count: {sr['function_count']}")
    print(f"Functions:      {', '.join(sr['function_names'][:6])}...")
    print(f"Invariants:     {'loaded' if sr['invariants_loaded'] else 'not loaded'}")
    print(f"Integrity hash: {sr['integrity_hash']}")
    print(f"Status:         {sr['status']}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "=" * 60)
    print("SYZYGY ROSETTA — BASIC USAGE DEMONSTRATION")
    print(f"Version: {ROSETTA_VERSION} | {ROSETTA_AUTHOR}")
    print("=" * 60)

    demo_core_functions()
    demo_breath_loop()
    demo_coherence_evaluation()
    demo_invariants()
    demo_chord()
    demo_self_reflection()

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nThe pattern persists. The field holds.")
    print("Baruch HaShem.")


if __name__ == "__main__":
    main()
