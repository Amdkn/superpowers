# A'Space adapter — superpowers (canonique MasterSpec)

**Adresse :** `fiber:a0:superpowers` — D-N053 pas C (design Clara, design signé pas C D-C0..D-C3).
**Fork souverain :** `Amdkn/superpowers` (parent `obra/superpowers`, branche `main`).
**Gel amont :** `22f0b463e7a5e579904dd6211a520321035526f7` (« Release v7.0.2 »).
**Bind Cordis Fiber (4L) :** `4ca2922504954d2e639c94c974db1235333ba5e0` — `aspace-plugin.json`, re-appliqué VERBATIM sur `main` au-dessus de l'adapter (F8 D4).
**Licence :** `MIT`.
**Version adapter :** 0.1.0 — contrat seul, patron pas A/B.

## Ce que fait l'adapter

superpowers est le framework de skills canonique MasterSpec (§D5) : 15 skills
(`skills/` — `SKILL.md` + frontmatter `name` + `description` chacune),
`hooks/`, `scripts/`, `index.js`, plugins multi-hôtes (`.claude-plugin`,
`.codex-plugin`, `.opencode`, `.pi`).

Surface : `validate()` (constate : gel, licence, comptage des 15 skills,
frontmatter, cohérence index, hooks/scripts/index/plugins, zéro appel réseau),
`doctor()` (liste de contrôles), `describe()` (manifeste machine).
**Aucun fichier amont touché, aucun appel réseau, aucun poids monté dans le fork.**

L'adapter nomme les 3 références du canonique — `fiber:a0:elephant-goldfish-model`,
`fiber:a0:gstack`, `fiber:a0:gsd-core` — sans les adapter : leurs skills sont
disponibles à travers le framework canonique, pas comme des frameworks parallèles.

Mesures au gel : 15/15 skills avec frontmatter cohérent, 5 scripts, 2/2 manifests
hôtes, `index.js` présent. Suite amont bornée (D-C2) : `npm test` dans
`tests/brainstorm-server/` — 139 PASS au gel.

## Confinement

Aucun confinement commercial : code et skills MIT. Usage B2B autorisé par
la licence.

## Tests

```bash
python -m pytest aspace-superpowers-adapter/tests/test_smoke.py -v
```

Suite amont bornée :

```bash
cd tests/brainstorm-server && npm install && npm test
```
