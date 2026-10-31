# Changelog

Every change to a DropOut rule, by plugin version (`.claude-plugin/plugin.json`).

## 0.11.0 — 2026-10-30

- **New `enclosure-drawing` skill**: a board's dimensioned enclosure drawing is generated, not drawn: a board-independent engine (`scripts/enclosure_drawing.py`, Python standard library only) draws third-angle SVG views, a cutout details sheet and a JSON for the docs table from a geometry spec (`references/spec.md`). Each board writes a small adapter, `scripts/enclosure_geometry.py`, that builds the spec from its own placement data, so moving a connector moves its cutout. `--check` fails on a cutout or seal area leaving its face or overlapping another. Engine 1.1 draws stepped tops (`raised` regions: hoods or a raised T over tall parts), staggers colliding labels, and turns a raised region's label up the region (or onto two lines) when it is too narrow for one line. Engine 1.2 draws board notches and further boards (a stacked second board). Includes a STEP-slicing helper for connector heights the manufacturer drawing doesn't give, and the docs components and page template. Extracted from Node60's enclosure work (DEC-020, DEC-021), which is the worked example. No rule change.

## 0.10.1 — 2026-10-29

- Chapter 05: Node60's answers to project questions 6 (environment) and 7 (dielectrics) recorded in the worked example. No rule change.

## 0.10.0 — 2026-10-29

Lessons from Node60's schematic work (DEC-012 rev. B, DEC-016, DEC-017).

- **Reference circuits** (chapter 05): interface circuits follow the IC maker's application note and the interface standard's reference schematic, compared part by part *including order along the signal path*. Evaluation boards are a third source but may use another variant; read the standard's component table, not just its figure; record deviations in a decision.
- **Switched and configurable hardware** (chapter 05): a series switch's on-resistance and drift count against a precision element's tolerance, and its off-capacitance against the node's budget; check signal swing and fault voltages too. Settings that must hold through sleep or power-off use latching or non-volatile parts, firmware re-applies the stored state at cold boot, and the shipped state is the documented safe default.
- **Mirrored symbols mirror field justification** (chapter 05, under D-51): check reference and value placement on the rendered sheet.
- **Temperature range for parts without AEC qualification** (chapter 03, rule 2): connectors, relays and terminals still need a rated range covering the board's ambient; most small signal relays stop at +85 °C.
- **After a library update** (chapter 02): add new libraries to `sym-lib-table`/`fp-lib-table`, refresh placed symbols whose library fields changed, and re-pin from a library PR's head to its merge commit before the board PR merges.

## 0.9.0 — 2026-10-28

- **Konnect (KiCad MCP) removed from the toolchain** (chapter 07; `new-board`): no longer installed or registered when setting up a Mac, and listed under "Considered and rejected". `new-board` asks the user to create the KiCad project instead of creating it through Konnect.

## 0.8.0 — 2026-10-22

- **Schematic standard adopted** from [charlesh97/ee-skills](https://github.com/charlesh97/ee-skills/tree/e45935f58e3915a6fe891818fd0d49ef9114db4f/skills/ee-schematic-rules) `ee-schematic-rules`, restated in DropOut's words (the source has no license) with its rule IDs kept (chapter 05; new `schematic-rules` skill). All of its `SKILL.md` and drawing rules D-01…D-61 except D-03. DropOut changes: rails named by voltage, with existing names kept per board (O-1; Node60 keeps its Rev A names); active-low suffix `_L` (replaces the proposed `_N`; `_P`/`_N` reserved for differential pairs); distributor fields stay `DigiKey_PN`/`Mouser_PN`, with `LCSC`, JLC-basic preference and `CONSIGNED` only on JLC-assembled boards; junction temperature ≤ Tj(max) − 25 °C; the source's fixed dielectric rule (X7R to 1 µF, X5R from 1 µF) replaced by three more project questions (ambient range and grade, environment, allowed dielectrics), so capacitor temperature ratings are set per board (Node60: no X5R); the seven project questions recorded in the board's `CLAUDE.md`; D-14 MCU units split by datasheet function group in the library; D-25 uses hierarchical labels and sheet pins for off-sheet nets.
- **Fully specified parts, never from memory** (chapter 03); **D-45 passive value format and fields, D-14 and D-47 as library rules** (chapter 04).
- **Every net is named, enforced in CI (O-2)** and **ERC zero or justified before handoff (D-52)** (chapter 06). Board template: `check_schematic.py` fails on `Net-(…)` names and on `unconnected-(…)` pins without a no-connect flag; `CLAUDE.md.template` gains "Schematic project answers".

## 0.7.0 — 2026-10-22

- **Never combine pins on a symbol** (chapters 04, 05; `dropout-standards`): every package pin gets its own visible pin, including repeated power and ground pins. No KiCad native pin stacks and no hidden stacked pins, even where KLC S4.3 allows them. Stricter than KLC; enforced by library CI (`check_pin_pad_match.py`). In schematics, every supply and ground pin is wired explicitly.

## 0.6.0 — 2026-10-22

- **Vendor sites through Claude Code's built-in browser** (chapters 03, 07; `find-part`): it keeps the user's vendor sign-ins. Claude in Chrome becomes the fallback. Claude never types passwords; the user signs in once per site.
- **Private `dropout-vendor-docs` repo** (chapters 00, 02, 03): every manufacturer document a part or board was built from is archived there by default (Git LFS, index with revision, source, SHA-256). Public repos link to documents, never copy them; symbols get an optional `Reference_Manual` link field. Check document revisions: distributor mirrors go stale.
- **Library part pipeline** (chapter 04): `distributor_lookup.py`, `generate_footprint.py` (specs in `generators/`), `pintables/` + `symbolgen.py` (`parts/<MPN>/`), `check_pin_pad_match.py` in CI; KLC results are FAIL / WARN / WAIVED, with each WARN explained in the PR. Second-source pin cross-check and a visual review of every unit are required.
- **Setting up a new Mac** (chapter 07): every tool in order: Homebrew `gh`, `uv`, `poppler`, `git-lfs`, `d2`, `node`; KiCad 10; repo clones; plugins; credentials; the library's `setup_tools.sh`; Konnect; vendor sign-ins; checks.

## 0.5.0 — 2026-10-22

- **Library catalog in its own repo** (chapters 00, 02, 04, 07, 08): `dropout-library-catalog`, live at `https://karltbowers.github.io/dropout-library-catalog/`. The library repo holds only parts and their checks, so boards mounting it as a submodule don't carry the site. The catalog rebuilds on a `library-updated` dispatch from library CI and nightly.

## 0.4.0 — 2026-10-22

- **Schematic sheet files** (chapter 05): root sheet `<board>.kicad_sch` at the repo root as a page-1 index; every other sheet flat in `sheets/`, named by subsystem; a repeated block is one file placed per instance.
- **Page numbers**: integers 1–99, unique, root = 1, frozen once a sheet has parts.
- **Reference designators**: page × 100 + 01…99 (`R201`, `C1101`), via KiCad's "first free after sheet number × 100" set in the project file. Limits: 99 pages, 99 parts of one prefix per page.
- Board template: `scripts/check_schematic.py` and a CI step enforcing all three; `sheets/` folder. CI runs DRC, PCB outputs, and `rev-*` releases only once the board has an Edge.Cuts outline. `new-board` sets the annotation method.

## 0.3.0 — 2026-10-21

- **Board template ships a Starlight starter** in `templates/board/docs/`, extracted from the Node60 architecture port (labelled Rev C at the time; renumbered Rev A on 2026-10-22): config, content-collection schemas with build-time reference checks, rendering components, empty data files, page skeletons, power/signals D2 skeletons, and `docs.yml`. The single-file `ARCHITECTURE.md` outline is removed; `new-board` installs and builds the site (chapter 08 "Template").

## 0.2.0 — 2026-10-21

- **Architecture and board documents are Astro Starlight sites** in each board repo's `docs/`, published to GitHub Pages (new chapter 08). Single-file HTML documents are retired; existing ones are kept frozen.
- Facts as data with IDs (requirements, decisions, parts, gates), with traceability enforced by the build.
- Diagrams as code with **D2** (decided). Every architecture has two views, **power** and **signals** (digital + analog), with drawing conventions. Both views left-to-right; power view uses the dagre engine, signals view uses ELK. Mermaid proposed for sequences and state machines.
- Architecture revisions tagged `arch-rev-<letter>`; new `docs.yml` CI.

## 0.1.0 — 2026-10-21

Initial handbook, seeded from decisions made while setting up Node60 and the DropOut library:
- Design process with stage gates; architecture-document pattern from Node60 (then labelled Rev C, now Rev A).
- Repository layout, library submodule at `lib/dropout-kicad-library`, `rev-*` release tags, `~/Dev` working copies.
- Part search and selection: DigiKey → Mouser → Newark via kicad-happy skills and official APIs; datasheet is the authority; dated observations; second sources; considered-and-rejected tools.
- Library: KLC in full plus `klc-exceptions.yml`; atomic parts; DropOut fields.
- Schematic/PCB conventions (early; several items proposed).
- CI and releases; tools; credentials handling.
- Skills: `dropout-standards`, `find-part`, `new-board`; board template.
