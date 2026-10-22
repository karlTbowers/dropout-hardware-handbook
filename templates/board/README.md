# {{BOARD_TITLE}}

{{DESCRIPTION}}

Open hardware by DropOut, designed in KiCad 10 following the [DropOut Hardware Handbook](https://github.com/karlTbowers/dropout-hardware-handbook).

**Status:** requirements and architecture.

## Cloning

The DropOut part library is a git submodule, so clone recursively:

```bash
git clone --recursive https://github.com/karlTbowers/{{BOARD}}-hw.git
```

Already cloned without it? Run `git submodule update --init`.

## Layout

```
{{BOARD}}.kicad_pro / .kicad_sch / .kicad_pcb   KiCad 10 project
sym-lib-table, fp-lib-table                     point into lib/
lib/dropout-kicad-library/                      submodule: symbols, footprints, 3D models
docs/architecture/                              architecture document
docs/                                           calculations, test plans, bring-up, validation
.github/workflows/ci.yml                        ERC/DRC on every push; fab outputs on rev-* tags
```

## Releases

Board revisions are git tags (`rev-a`, `rev-b`, …). Pushing one makes CI attach the fabrication package (Gerbers, drill, positions, BOM, schematic PDF, STEP) to a GitHub Release.

## License

TBD — to be chosen before the first public release.
