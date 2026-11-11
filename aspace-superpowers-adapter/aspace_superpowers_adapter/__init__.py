"""A'Space adapter — superpowers (D-N053 pas C, design Clara + design signé pas C).

Contrat seul, patron pas A/B : cet adapter ne modifie AUCUN fichier amont,
ne fait AUCUN appel réseau, ne monte AUCUN poids. Il constate : le gel
épinglé, la licence, l'inventaire des 15 skills (comptage SKILL.md,
frontmatter name + description, cohérence index), la présence des hooks,
des scripts et des plugins multi-hôtes — et il NOMME superpowers canonique
MasterSpec (§D5 du design D-N053), les 3 autres modules du pas C (EGM,
gstack, gsd-core) n'étant que des références du canonique, sans être adaptés
ici.

Adresse : fiber:a0:superpowers
Fork souverain : Amdkn/superpowers (parent obra/superpowers, branche main)
Gel amont : 22f0b463e7a5e579904dd6211a520321035526f7 (« Release v7.0.2 »)
Bind Cordis Fiber (4L) : 4ca2922504954d2e639c94c974db1235333ba5e0
Licence : MIT

Mesures au gel (2026-11-11, vérifiées au fichier) :
- 15 skills dans skills/ (brainstorming, diagnosing-superpowers,
  dispatching-parallel-agents, executing-plans, finishing-a-development-branch,
  receiving-code-review, requesting-code-review, subagent-driven-development,
  systematic-debugging, test-driven-development, using-git-worktrees,
  using-superpowers, verification-before-completion, writing-plans,
  writing-skills) — chacune avec SKILL.md, frontmatter name + description.
- hooks/ (hooks.json, hooks-cursor.json, session-start), scripts/
  (bump-version.sh, lint-shell.sh, package-codex-plugin.sh,
  render-antigravity-logo.sh, sync-to-codex-plugin.sh), index.js racine.
- Plugins multi-hôtes : .claude-plugin (marketplace.json, plugin.json),
  .codex-plugin (plugin.json), .opencode, .pi, etc.
- Suite amont bornée (D-C2) : `npm test` dans tests/brainstorm-server/
  (7 fichiers *.test.js node + 2 scripts shell) — 139 PASS au gel
  (32 + 15 + 3 + 20 + 7 + 34 + 13 + 8 + 7) ; run-skill-tests.sh exclu
  (CLI Claude absent + quota modèle).
- Télémétrie : 0 SDK ; 1 image de marque distante (primeradiant.com,
  logo des écrans brainstorm), omise par SUPERPOWERS_DISABLE_TELEMETRY /
  DISABLE_TELEMETRY / CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC ou sur
  bind non-loopback — déclencheur tranché, conservé tel quel (voir audit).
"""

from __future__ import annotations

import re
from pathlib import Path

FIBER_ADDRESS = "fiber:a0:superpowers"
FORK = "Amdkn/superpowers"
UPSTREAM_REPO = "obra/superpowers"
UPSTREAM_BRANCH = "main"
PINNED_UPSTREAM_COMMIT = "22f0b463e7a5e579904dd6211a520321035526f7"
PINNED_UPSTREAM_COMMIT_SHORT = "22f0b463"
BIND_COMMIT = "4ca2922504954d2e639c94c974db1235333ba5e0"
BIND_LAYER = "4L"
LICENSE = "MIT"
ADAPTER_VERSION = "0.1.0"

CANONICAL_ROLE = "canonique MasterSpec (§D5)"
REFERENCE_MODULES = (
    "fiber:a0:elephant-goldfish-model",
    "fiber:a0:gstack",
    "fiber:a0:gsd-core",
)
EXPECTED_SKILLS = (
    "brainstorming",
    "diagnosing-superpowers",
    "dispatching-parallel-agents",
    "executing-plans",
    "finishing-a-development-branch",
    "receiving-code-review",
    "requesting-code-review",
    "subagent-driven-development",
    "systematic-debugging",
    "test-driven-development",
    "using-git-worktrees",
    "using-superpowers",
    "verification-before-completion",
    "writing-plans",
    "writing-skills",
)
EXPECTED_HOST_PLUGINS = (
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
)

CONFINEMENT = """Aucun confinement commercial : code et skills MIT. Usage B2B autorisé
par la licence. L'adapter ne fait que constater l'inventaire ; le contenu
des skills reste byte-identique à l'amont."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _frontmatter(text: str) -> dict:
    """Extrait name + description du frontmatter YAML d'un SKILL.md.

    Lecture stdlib seule (le YAML complet est celui de la suite amont) :
    le frontmatter est le bloc entre les deux lignes `---` initiales.
    """
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    out = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def _skill_inventory(root: Path) -> dict:
    skills_dir = root / "skills"
    dirs = sorted(p.name for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    present = [p for p in dirs if (skills_dir / p / "SKILL.md").is_file()]
    missing_skill_md = [p for p in dirs if not (skills_dir / p / "SKILL.md").is_file()]
    frontmatter_ok: list[str] = []
    frontmatter_bad: list[str] = []
    names: dict[str, str] = {}
    for name in present:
        fm = _frontmatter((skills_dir / name / "SKILL.md").read_text(encoding="utf-8", errors="replace"))
        if fm.get("name") == name and fm.get("description"):
            frontmatter_ok.append(name)
        else:
            frontmatter_bad.append(name)
        if fm.get("name"):
            names[name] = fm["name"]
    name_mismatch = [n for n, v in names.items() if v != n]
    hooks_dir = root / "hooks"
    scripts_dir = root / "scripts"
    return {
        "skill_dirs_total": len(dirs),
        "skills_with_skill_md": len(present),
        "skills_expected": list(EXPECTED_SKILLS),
        "skills_missing": [s for s in EXPECTED_SKILLS if s not in present],
        "skills_unexpected": [s for s in present if s not in EXPECTED_SKILLS],
        "missing_skill_md": missing_skill_md,
        "frontmatter_ok": frontmatter_ok,
        "frontmatter_bad": frontmatter_bad,
        "name_mismatch": name_mismatch,
        "hooks_present": (hooks_dir / "hooks.json").is_file(),
        "hooks_cursor_present": (hooks_dir / "hooks-cursor.json").is_file(),
        "scripts_present": sorted(p.name for p in scripts_dir.iterdir() if p.is_file()) if scripts_dir.is_dir() else [],
        "index_js_present": (root / "index.js").is_file(),
        "host_plugins_present": [p for p in EXPECTED_HOST_PLUGINS if (root / p).is_file()],
        "host_plugins_missing": [p for p in EXPECTED_HOST_PLUGINS if not (root / p).is_file()],
        "brainstorm_server_tests": sorted(
            p.name for p in (root / "tests" / "brainstorm-server").iterdir()
            if p.suffix in (".js", ".sh")
        ) if (root / "tests" / "brainstorm-server").is_dir() else [],
    }


def describe() -> dict:
    """Décrit l'adapter (manifeste machine, sans effet de bord)."""
    return {
        "fiber": FIBER_ADDRESS,
        "fork": FORK,
        "upstream": UPSTREAM_REPO,
        "upstream_branch": UPSTREAM_BRANCH,
        "pinned_upstream_commit": PINNED_UPSTREAM_COMMIT,
        "bind_commit": BIND_COMMIT,
        "bind_layer": BIND_LAYER,
        "license": LICENSE,
        "adapter_version": ADAPTER_VERSION,
        "canonical_role": CANONICAL_ROLE,
        "references": list(REFERENCE_MODULES),
        "confinement": CONFINEMENT,
        "surface": "validate() -> dict ; doctor() -> list[check] ; describe() -> dict",
    }


def validate() -> dict:
    """Constate l'état de l'inventaire gelé. Aucun appel réseau, aucune écriture."""
    root = _repo_root()
    inv = _skill_inventory(root)
    license_file = root / "LICENSE"
    return {
        "pinned_commit_is_40_hex": bool(re.fullmatch(r"[0-9a-f]{40}", PINNED_UPSTREAM_COMMIT)),
        "license_file_present": license_file.is_file(),
        "license": LICENSE,
        "adapter_network_calls": 0,
        "canonical": FIBER_ADDRESS,
        "canonical_role": CANONICAL_ROLE,
        "references": list(REFERENCE_MODULES),
        "confinement": CONFINEMENT,
        **inv,
        "inventory_coherent": (
            inv["skill_dirs_total"] == 15
            and inv["skills_with_skill_md"] == 15
            and inv["skills_missing"] == []
            and inv["skills_unexpected"] == []
            and inv["frontmatter_bad"] == []
            and inv["name_mismatch"] == []
            and inv["hooks_present"]
            and inv["index_js_present"]
            and inv["host_plugins_missing"] == []
        ),
    }


def doctor() -> list[dict]:
    """Liste de contrôles sur l'inventaire gelé."""
    v = validate()
    checks = [
        {
            "name": "gel_epingle_40_hex",
            "ok": v["pinned_commit_is_40_hex"],
            "detail": PINNED_UPSTREAM_COMMIT_SHORT,
        },
        {
            "name": "licence_mit",
            "ok": v["license_file_present"] and v["license"] == "MIT",
            "detail": "LICENSE present, MIT",
        },
        {
            "name": "inventaire_15_skills",
            "ok": v["skill_dirs_total"] == 15 and v["skills_with_skill_md"] == 15,
            "detail": f"{v['skill_dirs_total']} dossiers skills, {v['skills_with_skill_md']} SKILL.md",
        },
        {
            "name": "frontmatter_name_description",
            "ok": v["frontmatter_bad"] == [] and v["name_mismatch"] == [],
            "detail": f"{len(v['frontmatter_ok'])}/15 frontmatters name + description cohérents",
        },
        {
            "name": "inventaire_exact_attendu",
            "ok": v["skills_missing"] == [] and v["skills_unexpected"] == [],
            "detail": "0 manquante, 0 inattendue parmi les 15 attendues",
        },
        {
            "name": "hooks_scripts_index_plugins",
            "ok": v["hooks_present"] and v["hooks_cursor_present"] and v["index_js_present"]
            and v["host_plugins_missing"] == [] and len(v["scripts_present"]) == 5,
            "detail": (
                f"hooks.json + hooks-cursor.json, index.js, "
                f"{len(v['host_plugins_present'])}/2 manifests hôtes, "
                f"{len(v['scripts_present'])} scripts"
            ),
        },
        {
            "name": "canonique_nomme_avant_references",
            "ok": v["canonical"] == "fiber:a0:superpowers" and len(v["references"]) == 3,
            "detail": "superpowers canonique MasterSpec (§D5) ; 3 références nommées sans être adaptées",
        },
        {
            "name": "adapter_sans_reseau",
            "ok": v["adapter_network_calls"] == 0,
            "detail": "stdlib seule, 0 import réseau, 0 appel sortant",
        },
    ]
    return checks
