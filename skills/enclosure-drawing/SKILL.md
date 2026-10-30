---
name: enclosure-drawing
description: Make or update a dimensioned enclosure drawing for a DropOut board (panel cutouts for every connector, outside size, board position, third-angle views) that is generated from the board's PCB placement and shown on its docs site, so it redraws itself when connectors or enclosure assumptions change. Use whenever the user wants an enclosure, panel, case or box drawing, connector cutout positions or sizes for a wall or lid, a mechanical drawing for the architecture docs, or to update one after moving connectors, even if they don't say "drawing".
---

# Enclosure drawing

A board's enclosure drawing is **generated**, never drawn by hand: connectors move, enclosures get chosen, and a hand drawing goes stale silently. Three pieces, all in the board repo:

| File | Role |
|---|---|
| `scripts/enclosure_geometry.py` | The board's adapter. `spec()` returns the geometry spec, built from the board's own placement data and named enclosure assumptions |
| `scripts/enclosure_drawing.py` | The engine, copied from this skill (`scripts/enclosure_drawing.py`). Board-independent |
| docs page | `Drawing` and `EnclosureTable` components and an MDX page; `npm run drawings` regenerates the SVGs and JSON at every docs build |

Read `references/spec.md` before writing the adapter: it defines the frame, the faces and the cutout types. Node60 (`node60-hw`, DEC-020) is the worked example: its adapter derives everything from `scripts/place_connectors.py` and handles a board mounted component side down.

## 1. Collect

Ask only for what the repo doesn't already say (architecture decisions, `CLAUDE.md`, the PCB):

- **Which connector goes on which face**, and which face is the front. A sketch from the user is enough; read positions off it as proportions, then check them against the PCB.
- **How the board mounts**: component side up or down, and what fixes its height (standoffs, connectors screwed to a wall, terminals screwed through a lid). This sets `z` for the board and each cutout's `near_edge`.
- **The enclosure assumptions** while no enclosure is chosen: wall thickness, gaps from board edges to walls, clearance to floor and lid. Name each one in the adapter; they will change.
- **Whether the top is stepped.** When lid-mounted parts need a lower panel than the tall headers allow, raise the top only over the headers (`raised` regions, e.g. a T over a row of outputs and a pair on another wall) and derive each region's edges from the header bodies plus a clearance, so they follow the layout.
- **Where positions come from**: a placement script if the board has one, otherwise the `.kicad_pcb` (the adapter template parses footprints and the Edge.Cuts outline without KiCad).

## 2. Get each connector's cutout from its manufacturer

Use the **recommended panel cutout** on the manufacturer's drawing; never invent one. Archive the drawing in `dropout-vendor-docs` (handbook chapter 03) and cite drawing and revision next to each value in the adapter.

- Render the drawing to read it: `pdftotext -bbox` finds "PANEL CUTOUT" on the page, then `pdftoppm -r 260 -x … -y … -W … -H …` crops that view.
- Cutouts are usually dimensioned from the PCB surface: the near edge's height and the mating axis (where the screw holes are). In the spec, `near` = axis height − near-edge height.
- **If the drawing gives no height above the board**, measure it from the part's STEP model in the library: `~/.cache/dropout/klt-venv/bin/python scripts/measure_step.py MODEL.step --y0 … --y1 …` slices the mating shroud; its centre is the axis. Say in the sources that the value was measured, not drawn.
- Note the seal or flange area (the flat panel area the gasket needs): the engine checks it against face edges and neighbours.
- A lid or wall receptacle (SurLok and similar) usually has a round cutout and screws on a square; its catalog's "panel layout" table gives both.

## 3. Write the adapter

Start from `assets/enclosure_geometry.py` (replace `{{BOARD}}`, `{{BOARD_TITLE}}` and every EXAMPLE value). Rules that keep it trustworthy:

- **Derive positions, don't copy numbers.** Import the placement script's constants or read the PCB, so moving a connector moves its cutout.
- Convert KiCad coordinates (y down, seen from the component side) into the enclosure frame once, in two small functions (`ex`, `ey`). **A board mounted component side down is mirrored**: KiCad's top view looks at the component side, which then faces the floor, so left and right swap against the outside view.
- The cutout centre is the connector's mating axis: usually the pin-pair centre, not the footprint origin (pin 1). Take the offset from the footprint.
- Put board-specific values the docs page should print (assumptions, derived distances) in extra top-level keys; they are copied to `enclosure.json`.

## 4. Install the engine and check

```bash
cp <this skill>/scripts/enclosure_drawing.py scripts/
python3 scripts/enclosure_drawing.py scripts/enclosure_geometry.py --check
```

The engine is copied, not linked, because the docs CI has no plugin. Its `ENGINE_VERSION` names the spec format; to update a board, copy the new engine over and rerun `--check`. Fix every problem `--check` reports: a seal area leaving its face or two overlapping means the enclosure or the layout is wrong, not the drawing.

## 5. Put it on the docs site

In the board's `docs/` (the handbook's board template, chapter 08):

- `package.json`: add `"drawings": "python3 ../scripts/enclosure_drawing.py ../scripts/enclosure_geometry.py src/diagrams/build"` (paths from `docs/`), and run it in `dev` and `build` after `diagrams`. Generated files land in the gitignored `src/diagrams/build/`.
- Copy `assets/Drawing.astro` and `assets/EnclosureTable.astro` into `src/components/` (replace `{{BOARD}}`).
- Copy `assets/enclosure.mdx` to `src/content/docs/subsystems/enclosure.mdx`; fill in the intro paragraph and the sources and assumptions list. Add it to the sidebar in `astro.config.mjs` next to the connector and harness page, and link it from the decision that fixes the enclosure.
- `src/styles/custom.css`: `.diagram.drawing .diagram-scroll > svg { width: 100%; margin: 0 auto; }`. Diagrams sit on a white panel in both themes, so the engine's fixed dark ink reads in dark mode too.

## 6. Verify

- `npm run build` in `docs/` passes and lists the views.
- Open the page in the browser (the docs dev server) in light and dark: every view fits the column, no labels overlap, cutouts face the right way (a key toward the floor on a board mounted component side down).
- Spot-check two numbers against the PCB: one cutout centre and the outside size.
- Record in the board's `CLAUDE.md` which files hold the positions and the assumptions, and that the SVGs are generated.

## Updating later

Moving a connector or changing an assumption needs nothing here: edit the placement or the adapter, rebuild the docs. Re-run `--check` in the same change. New cutout shapes go into the engine in this skill (and `references/spec.md`, bumping `ENGINE_VERSION` if the format changes), then into each board by copying.
