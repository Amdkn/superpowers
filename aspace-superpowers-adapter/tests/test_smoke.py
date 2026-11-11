"""Smoke tests de l'adapter superpowers (D-N053 pas C).

Roulés avec le venv du pas : `python -m pytest aspace-superpowers-adapter/tests/test_smoke.py -v`.
Ne touchent pas l'amont, ne font aucun appel réseau. La validation complète
de la suite est celle de la suite amont (`npm test` dans
tests/brainstorm-server/, 139 PASS au gel) ; le smoke vérifie les constantes,
les comptages mesurés par l'adapter et le rôle canonique (§D5).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import aspace_superpowers_adapter as adapter  # noqa: E402


def test_constants():
    assert re.fullmatch(r"[0-9a-f]{40}", adapter.PINNED_UPSTREAM_COMMIT)
    assert adapter.FIBER_ADDRESS == "fiber:a0:superpowers"
    assert adapter.LICENSE == "MIT"
    assert adapter.FORK == "Amdkn/superpowers"
    assert adapter.UPSTREAM_REPO == "obra/superpowers"
    assert adapter.ADAPTER_VERSION == "0.1.0"
    assert adapter.BIND_COMMIT == "4ca2922504954d2e639c94c974db1235333ba5e0"
    assert adapter.BIND_LAYER == "4L"


def test_validate_counts():
    v = adapter.validate()
    assert v["pinned_commit_is_40_hex"] is True
    assert v["license_file_present"] is True
    assert v["skill_dirs_total"] == 15
    assert v["skills_with_skill_md"] == 15
    assert v["skills_missing"] == []
    assert v["skills_unexpected"] == []
    assert v["missing_skill_md"] == []
    assert len(v["frontmatter_ok"]) == 15
    assert v["frontmatter_bad"] == []
    assert v["name_mismatch"] == []
    assert v["hooks_present"] is True
    assert v["hooks_cursor_present"] is True
    assert v["index_js_present"] is True
    assert v["host_plugins_missing"] == []
    assert len(v["scripts_present"]) == 5
    assert v["adapter_network_calls"] == 0
    assert v["confinement"]


def test_validate_coherent():
    v = adapter.validate()
    assert v["inventory_coherent"] is True
    assert v["canonical"] == "fiber:a0:superpowers"
    assert v["references"] == [
        "fiber:a0:elephant-goldfish-model",
        "fiber:a0:gstack",
        "fiber:a0:gsd-core",
    ]


def test_doctor_all_pass():
    checks = adapter.doctor()
    assert checks, "doctor() vide"
    failed = [c for c in checks if not c["ok"]]
    assert not failed, failed


def test_no_network_import_in_adapter():
    src = (Path(adapter.__file__).parent / "__init__.py").read_text()
    for banned in ("requests", "httpx", "urllib", "socket", "huggingface_hub", "aiohttp"):
        assert banned not in src, banned


def test_describe():
    d = adapter.describe()
    assert d["fiber"] == "fiber:a0:superpowers"
    assert d["pinned_upstream_commit"] == adapter.PINNED_UPSTREAM_COMMIT
    assert d["license"] == "MIT"
    assert d["canonical_role"] == "canonique MasterSpec (§D5)"
    assert d["references"] == list(adapter.REFERENCE_MODULES)
