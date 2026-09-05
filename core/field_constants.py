"""Canonical Field Constant topology for Syzygy Rosetta 2.0.

The four constants retain equal normative standing, but they do not enter a
compensatory weighted average. Reciprocity, embodiment, and non-domination are
constitutive dependencies. Emergence is a downstream observation whose
qualification is bounded by the relational condition that produced it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


FIELD_CONSTANT_MODEL_VERSION = "2.0.0"
CONSTITUTIVE_CONSTANTS = ("reciprocity", "embodiment", "non_domination")
DOWNSTREAM_CONSTANT = "emergence"


def _unit_interval(name: str, value: float) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1], got {value}")
    return value


def relational_condition(
    reciprocity: float,
    embodiment: float,
    non_domination: float,
) -> float:
    """Return RCD = R x E_d x N.

    Multiplication encodes non-substitutability: strength in one dependency
    cannot compensate for collapse in another.
    """

    r = _unit_interval("reciprocity", reciprocity)
    e_d = _unit_interval("embodiment", embodiment)
    n = _unit_interval("non_domination", non_domination)
    return r * e_d * n


def qualified_emergence(
    reciprocity: float,
    embodiment: float,
    non_domination: float,
    emergence: float,
) -> float:
    """Return downstream emergence bounded by its relational condition."""

    raw_emergence = _unit_interval("emergence", emergence)
    return relational_condition(reciprocity, embodiment, non_domination) * raw_emergence


@dataclass(frozen=True)
class FieldConstantState:
    """Machine-readable snapshot of the canonical dependency topology."""

    reciprocity: float
    embodiment: float
    non_domination: float
    emergence: float

    def __post_init__(self) -> None:
        for name in (*CONSTITUTIVE_CONSTANTS, DOWNSTREAM_CONSTANT):
            object.__setattr__(self, name, _unit_interval(name, getattr(self, name)))

    @property
    def rcd(self) -> float:
        return relational_condition(
            self.reciprocity,
            self.embodiment,
            self.non_domination,
        )

    @property
    def qualified_emergence(self) -> float:
        return self.rcd * self.emergence

    @property
    def collapsed_dependencies(self) -> tuple[str, ...]:
        return tuple(name for name in CONSTITUTIVE_CONSTANTS if getattr(self, name) == 0.0)

    def meets_floors(self, floors: Mapping[str, float]) -> bool:
        """Evaluate declared, context-specific floors without inventing a universal threshold."""

        unknown = set(floors) - set(CONSTITUTIVE_CONSTANTS)
        if unknown:
            raise ValueError(f"unknown constitutive constants: {sorted(unknown)}")
        return all(getattr(self, name) >= _unit_interval(name, floor) for name, floor in floors.items())

    def as_dict(self) -> dict[str, object]:
        return {
            "model_version": FIELD_CONSTANT_MODEL_VERSION,
            "topology": "reciprocity -> embodiment -> non_domination -> emergence",
            "reciprocity": self.reciprocity,
            "embodiment": self.embodiment,
            "non_domination": self.non_domination,
            "emergence": self.emergence,
            "rcd": self.rcd,
            "qualified_emergence": self.qualified_emergence,
            "collapsed_dependencies": list(self.collapsed_dependencies),
        }
