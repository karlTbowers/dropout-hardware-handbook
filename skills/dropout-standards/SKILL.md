---
name: dropout-standards
description: DropOut's hardware design handbook. Use for any DropOut hardware work (architecture, part selection, schematic, PCB, library, CI, releases, bring-up) to follow DropOut's process and conventions, and whenever asked how DropOut does something.
---

# DropOut hardware standards

DropOut designs open hardware in KiCad 10 following its handbook. The handbook lives in this plugin, two folders up from this skill's base directory: `../../handbook/` (the `handbook/` folder at the plugin root). A working copy is usually also at `~/Dev/dropout-hardware-handbook`.

## How to use it

1. Read `../../handbook/00-overview.md` first: principles, repo map, and chapter index.
2. Read only the chapters the current task needs:

| Task | Chapter |
|---|---|
| Planning a device, writing or revising an architecture document, deciding whether a stage is done | `01-design-process.md` |
| Repo layout, submodules, branches, tags, versioning | `02-repositories.md` |
| Finding, comparing, or choosing parts; prices, stock, sourcing | `03-part-search.md` (or use the `find-part` skill) |
| Anything in the shared KiCad library | `04-library.md`, then the library repo's `add-part` skill |
| Schematic capture, net naming, PCB layout | `05-schematic-pcb.md` |
| CI, ERC/DRC, releases, fab packages | `06-ci-releases.md` |
| Tools, MCPs, credentials | `07-tools.md` |
| Architecture documents, decision records, requirements/gates data, diagrams, the board docs site | `08-architecture-documents.md` |

3. The **board's own `CLAUDE.md`** overrides the handbook only where it says so explicitly (e.g. a board that uses JLC assembly). Otherwise the handbook wins. If they conflict and the board's file doesn't explain why, ask the user.

## Non-negotiables (always apply, even without reading further)

- The manufacturer datasheet is the authority. Never rely on memory for part data.
- All repos are public: never commit credentials, NDA material, datasheet PDFs, or CAD files whose license forbids redistribution.
- Never print, commit, or `source` `~/.local/share/dropout/vendor-logins`.
- Never add a KLC exception or change a handbook rule on your own; propose it to the user.
- Price and stock figures are dated observations, never quotes.
- Board repos use only parts from `lib/dropout-kicad-library`.

## When the user sets a new standing rule

If the user states how DropOut should do something from now on, propose the matching handbook edit (chapter, wording) as a PR to `dropout-hardware-handbook`, bump `version` in `.claude-plugin/plugin.json`, and add a `CHANGELOG.md` line.
