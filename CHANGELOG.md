# Changelog

Every change to a DropOut rule, by plugin version (`.claude-plugin/plugin.json`).

## 0.1.0 — 2026-10-21

Initial handbook, seeded from decisions made while setting up Node60 and the DropOut library:
- Design process with stage gates; architecture-document pattern from Node60 Rev C.
- Repository layout, library submodule at `lib/dropout-kicad-library`, `rev-*` release tags, `~/Dev` working copies.
- Part search and selection: DigiKey → Mouser → Newark via kicad-happy skills and official APIs; datasheet is the authority; dated observations; second sources; considered-and-rejected tools.
- Library: KLC in full plus `klc-exceptions.yml`; atomic parts; DropOut fields.
- Schematic/PCB conventions (early; several items proposed).
- CI and releases; tools; credentials handling.
- Skills: `dropout-standards`, `find-part`, `new-board`; board template.
