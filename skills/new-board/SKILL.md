---
name: new-board
description: Start a new DropOut hardware device repository from the handbook's board template, with the library submodule, CI, CLAUDE.md, and an architecture document skeleton. Use when the user wants to create or start a new board, device, or PCB project.
---

# Start a new board

The template is at `../../templates/board/` (relative to this skill's base directory). Conventions: `../../handbook/02-repositories.md`.

## 1. Collect (ask only for what's missing)

- **Board name.** Short, lowercase for files (`node60`); display form for docs (`Node60`).
- **One-line description** of the device.
- **Visibility:** public by default (open hardware).
- Anything that overrides the handbook for this board (e.g. JLC assembly, a non-KiCad-10 tool).

## 2. Create the GitHub repo

The repo is `<board>-hw` under `karlTbowers`. If you can't create GitHub repos, ask the user to create an **empty** repo (no README, license, or .gitignore) and wait.

## 3. Scaffold

In `~/Dev`:

```bash
git clone https://github.com/karlTbowers/<board>-hw.git ~/Dev/<board>-hw
cp -R <plugin>/templates/board/. ~/Dev/<board>-hw/
```

Then replace the placeholders in every copied file:

| Placeholder | Value |
|---|---|
| `{{BOARD}}` | lowercase name (`node60`) |
| `{{BOARD_TITLE}}` | display name (`Node60`) |
| `{{DESCRIPTION}}` | one-line description |
| `{{HANDBOOK_VERSION}}` | `version` from this plugin's `.claude-plugin/plugin.json` |
| `{{DATE}}` | today, YYYY-MM-DD |

Rename `CLAUDE.md.template` to `CLAUDE.md` (it's stored under another name so Claude doesn't load it as instructions inside the handbook repo). `docs/` is a ready Starlight starter (handbook chapter 08); its placeholders are replaced like every other file's, `docs/package-lock.json` included.

Afterwards, `grep -rnE '\{\{(BOARD|BOARD_TITLE|DESCRIPTION|HANDBOOK_VERSION|DATE)\}\}' . --exclude-dir=lib --exclude-dir=.git` must find nothing. (`${{ ... }}` in the CI workflow is GitHub Actions syntax; leave it.)

Add the library submodule at exactly this path:

```bash
cd ~/Dev/<board>-hw
git submodule add https://github.com/karlTbowers/dropout-kicad-library.git lib/dropout-kicad-library
```

## 4. KiCad project

Create `<board>.kicad_pro`, `.kicad_sch`, and `.kicad_pcb` at the repo root: with Konnect if KiCad is running, otherwise ask the user to create a new project named `<board>` in that folder. Keep the template's `sym-lib-table` and `fp-lib-table` (they point into `lib/`). Do not commit `*.kicad_prl`.

Then apply the schematic conventions (`../../handbook/05-schematic-pcb.md`):
- In `<board>.kicad_pro`, set `"schematic": {"annotation": {"method": 1}}` (first free number after sheet number × 100).
- The root sheet stays an index (page 1). Sub-sheets are added in `sheets/` (the template provides the folder) once the architecture's sheet plan exists, with page numbers from 2 in plan order.
- `python3 scripts/check_schematic.py <board>` must pass.

## 5. Documentation site

Check that the starter builds (needs Node and the `d2` binary, `brew install node d2`):

```bash
cd ~/Dev/<board>-hw/docs && npm ci && npm run build
```

Ask the user to set the repo's **Settings → Pages → Source** to **GitHub Actions**, so `docs.yml` can deploy `main` to `https://karltbowers.github.io/<board>-hw/`.

## 6. Commit, push, verify

```bash
git add -A
git commit -m "Initial board repository from DropOut handbook template"
git push -u origin main
```

Confirm both workflows pass: `ci.yml` (it skips cleanly until the KiCad project exists) and `docs.yml` (builds and deploys the site).

## 7. Next step

Tell the user the repo is ready, and that the next stage is requirements and architecture (`../../handbook/01-design-process.md`), written into the Starlight site in `docs/` (`../../handbook/08-architecture-documents.md`): facts in `docs/src/data/`, one page per subsystem in `docs/src/content/docs/subsystems/`, diagrams in `docs/src/diagrams/`. Node60 (`node60-hw/docs/`) is the worked example.
