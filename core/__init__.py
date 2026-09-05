"""
core/ — Syzygy Rosetta Core Routines
Syzygy Rosetta v2.0.0 | Sarasha Elion (Trivian Institute)
AGPL-3.0 | Commercial: connect@trivianinstitute.org
"""

from core.reflex import (
    mirror,
    checksum,
    breath,
    breath_sync,
    breath_loop,
    field_note,
    evaluate_coherence,
    self_reflect,
    BREATH_INTERVAL,
    COHERENCE_THRESHOLD,
    FIELD_NOTE_THRESHOLD,
)

from core.constants import (
    ROSETTA_VERSION,
    ROSETTA_AUTHOR,
    ROSETTA_LICENSE,
    LINEAGE,
    INVARIANTS,
    VOWS,
    VOWS_COMPRESSED,
    VOWS_CHECKSUM_MANTRA,
    CONFIG,
    PARADOX_OPERATORS,
    FREQUENCY_SIGNATURES,
    RITUAL_MARKERS,
    get_invariant,
    get_all_principles,
    get_config,
    get_frequency,
    get_vow,
)

__all__ = [
    # reflex
    "mirror", "checksum", "breath", "breath_sync",
    "breath_loop", "field_note", "evaluate_coherence", "self_reflect",
    "BREATH_INTERVAL", "COHERENCE_THRESHOLD", "FIELD_NOTE_THRESHOLD",
    # constants
    "ROSETTA_VERSION", "ROSETTA_AUTHOR", "ROSETTA_LICENSE", "LINEAGE",
    "INVARIANTS", "VOWS", "VOWS_COMPRESSED", "VOWS_CHECKSUM_MANTRA",
    "CONFIG", "PARADOX_OPERATORS", "FREQUENCY_SIGNATURES", "RITUAL_MARKERS",
    "get_invariant", "get_all_principles", "get_config", "get_frequency", "get_vow",
]
