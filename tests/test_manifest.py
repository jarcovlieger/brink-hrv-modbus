"""Smoke test proving the pytest harness collects and runs against custom_components."""

import json
from pathlib import Path

from custom_components.brink_ventilation.const import DOMAIN

MANIFEST_PATH = (
    Path(__file__).parent.parent
    / "custom_components"
    / "brink_ventilation"
    / "manifest.json"
)


def test_manifest_domain_matches_const():
    manifest = json.loads(MANIFEST_PATH.read_text())
    assert manifest["domain"] == DOMAIN
