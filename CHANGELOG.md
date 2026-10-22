# Changelog

Every change to a DropOut rule, by plugin version (`.claude-plugin/plugin.json`).

## 0.2.0 — 2026-10-21

- **Architecture and board documents are Astro Starlight sites** in each board repo's `docs/`, published to GitHub Pages (new chapter 08). Single-file HTML documents are retired; existing ones are kept frozen.
- Facts as data with IDs (requirements, decisions, parts, gates), with traceability enforced by the build.
- Diagrams as code with **D2** (decided). Every architecture has two views, **power** and **signals** (digital + analog), with drawing conventions. Direction and layout engine pending; Mermaid proposed for sequences and state machines.
- Architecture revisions tagged `arch-rev-<letter>`; new `docs.yml` CI.

## 0.1.0 — 2026-10-21

Initial handbook, seeded from decisions made while setting up Node60 and the DropOut library:
- Design process with stage gates; architecture-document pattern from Node60 Rev C.
- Repository layout, library submodule at `lib/dropout-kicad-library`, `rev-*` release tags, `~/Dev` working copies.
- Part search and selection: DigiKey → Mouser → Newark via kicad-happy skills and official APIs; datasheet is the authority; dated observations; second sources; considered-and-rejected tools.
- Library: KLC in full plus `klc-exceptions.yml`; atomic parts; DropOut fields.
- Schematic/PCB conventions (early; several items proposed).
- CI and releases; tools; credentials handling.
- Skills: `dropout-standards`, `find-part`, `new-board`; board template.
