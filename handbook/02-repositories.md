# 02 · Repositories and workflow

## Where things live on the Mac

```
~/Dev/
  dropout-hardware-handbook/      this handbook (also installed as a Claude Code plugin)
  dropout-kicad-library/          librarian working copy: parts are added here
  dropout-library-catalog/        catalog site for the library
  dropout-vendor-docs/            private archive of manufacturer documents (Git LFS)
  <board>-hw/                     one per device
    lib/dropout-kicad-library/    pinned copy of the library (git submodule)
```

`~/Dev` is outside iCloud Desktop & Documents sync on purpose: iCloud can evict files and race with git.

## Board repository layout

Created from [`templates/board`](../templates/board) by the `new-board` skill.

```
<board>.kicad_pro / .kicad_sch / .kicad_pcb    KiCad project, named after the board in lowercase;
                                                <board>.kicad_sch is the root sheet (page 1, index)
sheets/                                         every other schematic sheet, flat (chapter 05)
scripts/check_schematic.py                      CI check: sheet files, page numbers, reference designators
sym-lib-table, fp-lib-table                     point only into lib/
lib/dropout-kicad-library/                      library submodule
docs/                                           Starlight documentation site: architecture, calculations,
                                                test plans, bring-up, validation (chapter 08)
.github/workflows/ci.yml                        ERC/DRC on push; fab package on rev-* tags
CLAUDE.md                                       board-specific facts only; points to this handbook
```

Naming: repo `<board>-hw` in lowercase (`node60-hw`); KiCad project `<board>` (`node60`).

## The library submodule

Every board mounts the library at exactly `lib/dropout-kicad-library`. Footprints reference 3D models through that path, so it must not change.

- **Clone a board:** `git clone --recursive <url>` (or `git submodule update --init` afterwards).
- **Pick up library changes:** deliberately, never automatically:
  ```bash
  git -C lib/dropout-kicad-library pull origin main
  git add lib/dropout-kicad-library && git commit -m "Update DropOut library"
  ```
- A board revision ships with whatever library commit was pinned when it was tagged. Old revisions keep opening correctly forever.

## Branches, pull requests, tags

- `main` is always in a state that passes CI.
- Changes go through a branch and a pull request: `add/<MPN>` in the library, `<topic>` in board repos. Small doc fixes may go straight to `main`.
- Board fab revisions are tags `rev-a`, `rev-b`, …; architecture revisions are tags `arch-rev-a`, `arch-rev-b`, …. Tags are never moved or deleted.
- Commits made with Claude carry a `Co-Authored-By` trailer.

## Recording the handbook version

Each board's `CLAUDE.md` records the handbook version it follows (the `version` in `.claude-plugin/plugin.json` here). When the handbook changes a rule, a board adopts the new version explicitly, the same way it updates the library.

## Licenses

To be chosen before the first public release. Candidates: CERN-OHL-S-2.0 for boards; CERN-OHL-P-2.0 or CC-BY-SA-4.0 for the library; CC-BY-4.0 for this handbook.
