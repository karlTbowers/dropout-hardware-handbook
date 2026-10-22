# 06 · CI and releases

## Library repo CI (every push and PR)

| Check | What fails it |
|---|---|
| Required symbol fields | A missing or blank DropOut/KLC field |
| KLC (with DropOut exceptions) | Any KLC violation not waived by `klc-exceptions.yml`; also a self-test proving the waivers are exact |
| KiCad 10 can load every library | A library that doesn't parse |

## Board repo CI (`templates/board/.github/workflows/ci.yml`)

Runs in the official `kicad/kicad:10.0` container (`--user root`), with the library submodule checked out.

- **Every push and PR:** ERC (errors fail), DRC with schematic parity (errors fail), and the full output set (PDF, BOM, Gerbers, drill, positions, STEP), uploaded as a workflow artifact.
- **Skips cleanly** until `<board>.kicad_pro` exists.

## Releases

A board revision is released by pushing a tag:

```bash
git tag rev-a && git push origin rev-a
```

CI then attaches the fab package to a GitHub Release:

- schematic PDF
- BOM CSV, grouped by MPN, with Manufacturer, MPN, DigiKey, Mouser, and quantity columns, DNP parts excluded
- Gerbers and drill files
- pick-and-place position file (CSV, mm, both sides)
- STEP model of the assembled board

Before tagging: ERC/DRC clean, BOM re-sourced against live stock ([chapter 03](03-part-search.md)), reviews done ([chapter 01](01-design-process.md)).

## CI conventions

- Run KiCad CI jobs in `kicad/kicad:10.0` with `options: --user root`. The image's default user can't write the Actions workspace.
- When a CI step's logs aren't accessible, report problems with `::error::`/`::notice::` annotations, which are always readable through the API.
- Pin third-party tools (e.g. kicad-library-tools) to a commit, and add a self-test when a wrapper depends on another tool's output format.
