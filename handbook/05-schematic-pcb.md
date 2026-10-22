# 05 · Schematic and PCB conventions

> **Status: early.** Items marked **(proposed)** are defaults until the first board settles them; changing them is a normal handbook PR.

## Schematic

- **Hierarchical sheets follow the architecture document's sheet plan.** One subsystem per sheet; a repeated block (e.g. Node60's three output switches) is **one sheet file placed once per instance**, so a change is made once.

### Sheet files

**Decided (2026-10-22).**

- The **root sheet** is `<board>.kicad_sch` at the repo root, beside `<board>.kicad_pro` and `<board>.kicad_pcb`. It is page 1, an index: hierarchical sheet symbols, title block, and notes only, no circuit.
- **Every other sheet** lives in `sheets/`, **flat** (no subfolders, even for nested hierarchy), named after its subsystem in lowercase with hyphens: `sheets/power-entry.kicad_sch`, `sheets/output-switch.kicad_sch`. File names carry no page number, so adding a sheet never renames files.
- KiCad stores a sheet's file path relative to the **parent** sheet's folder: the root refers to `sheets/power-entry.kicad_sch`; a sheet inside `sheets/` refers to its child by bare name (`mcu-clocks.kicad_sch`). When adding a sheet in KiCad, save the new file into `sheets/`.
- CI fails if a `.kicad_sch` other than the root sits outside `sheets/`, or if a file in `sheets/` isn't used by the hierarchy.

### Page numbers

**Decided (2026-10-22).**

- **Every sheet has a page number**: a plain integer, unique, from 1 to 99. The root is page 1; the others follow the sheet plan's order from page 2. Each placement of a repeated sheet gets its own page (Node60's output switch is pages 6, 7, 8).
- A page number is **not changed once the sheet has parts**, because the reference designators carry it. A new sheet takes the next unused page number rather than renumbering the others; tidy the order only before parts are placed.
- The architecture document's sheet plan lists each sheet's page number.

### Reference designators

**Decided (2026-10-22).**

- A designator is **prefix + page number + a two-digit index**: page × 100 + 01…99. The first two resistors on page 2 are `R201`, `R202`; capacitors on page 11 are `C1101`, `C1102`, … Never `R1`, `R2`.
- Set it once per project: in `<board>.kicad_pro`, `"schematic": {"annotation": {"method": 1}}`, which is **Tools → Annotate → "Use first free number after sheet number × 100"**. KiCad 10 then uses it for the Annotate dialog and when annotating parts as they are placed, taking the number from the sheet's printed page number.
- Parts on a repeated sheet are numbered per placement (`R601` / `R701` / `R801` for the same resistor on pages 6–8).
- CI fails on any designator that doesn't match its sheet's page, or that is left unannotated.
- **Limits:** this works for up to 99 pages and up to 99 parts of one prefix on a page. If a board outgrows either, change this rule (e.g. to sheet number × 1000) before going past it.
- **Only DropOut library parts.** No KiCad stock symbols except power and graphical symbols.
- **Every pin is visible and wired on purpose.** Library symbols never combine pins ([chapter 04](04-library.md)), so each supply and ground pin is connected explicitly, with its own decoupling where the datasheet asks for it.
- **Name every net that leaves a sheet or matters for review.** Unnamed nets are acceptable only for purely local connections.
- **Net naming (proposed):** uppercase with underscores; rails as `<VOLTAGE>_<DOMAIN>` (`3V3_MAIN`, `1V5_CORE`, `VBAT_PROT`); active-low signals with a `_N` suffix (`RESET_N`, `IRQ_N`), unless the datasheet name is kept for a single-pin net.
- **Expose the nets the architecture document lists** for each sheet at its interface.
- **Document reset/default states** for control lines (chip selects, enables, fault inputs) on the sheet.
- **Test points on every rail and on every bus used for bring-up** (clock, SPI, I²C, MDIO, reset, interrupt lines).
- **Mark unverified items** (unconfirmed package ball maps, unverified sequencing, unmated connectors) with a visible note: they are release-blocking until closed.

## PCB (proposed defaults)

- **Stackup:** 4 layers minimum for any board with a high-speed bus or a switching regulator; 2 oz outer copper for high-current paths. Final stackup per board in the architecture document.
- **Rules:** start from the chosen fab house's standard capability; record the fab house and its rule set in the board's `CLAUDE.md` and `.kicad_dru`.
- **High-current paths:** every path above ~3 A gets its copper width, thickness, and via count calculated and noted on the PCB or in `docs/`.
- **Exposed pads:** follow each datasheet's thermal-via recommendation.
- **Return paths:** keep high di/dt loops away from analog sense, clock, and network lines; describe the ground strategy in the architecture document.
- **Silkscreen:** reference designators readable after assembly; connector pin 1 and polarity marked; board name, revision, and DropOut on the top side.
