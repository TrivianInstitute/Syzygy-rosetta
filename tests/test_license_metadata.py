import json
from pathlib import Path

from core.constants import ROSETTA_LICENSE


def test_current_metadata_matches_license():
    root = Path(__file__).resolve().parents[1]
    assert "PolyForm" in (root / "LICENSE").read_text()
    assert "PolyForm-Noncommercial-1.0.0" in ROSETTA_LICENSE
    data = json.loads((root / "core/invariants.json").read_text())
    assert "AGPL-3.0" not in json.dumps(data)
    for folder in ("core", "adapters", "evaluation", "examples"):
        for path in (root / folder).glob("*.py"):
            assert "AGPL-3.0" not in path.read_text(), path
