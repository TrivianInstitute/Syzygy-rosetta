import json
from pathlib import Path

from core.constants import ROSETTA_LICENSE


def test_current_metadata_matches_license():
    root = Path(__file__).resolve().parents[1]
    license_text = (root / "LICENSE").read_text()
    assert "Mozilla Public License Version 2.0" in license_text
    assert "MPL-2.0" in ROSETTA_LICENSE
    data = json.loads((root / "core/invariants.json").read_text())
    serialized = json.dumps(data)
    assert "PolyForm-Noncommercial-1.0.0" not in serialized
    assert "AGPL-3.0" not in serialized
    for folder in ("core", "adapters", "evaluation", "examples"):
        for path in (root / folder).glob("*.py"):
            text = path.read_text()
            assert "PolyForm-Noncommercial-1.0.0" not in text, path
            assert "AGPL-3.0" not in text, path
