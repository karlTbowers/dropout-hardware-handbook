---
name: schematic-rules
description: DropOut's schematic standard (net and designator naming, fully specified parts, passives, derating, design for debug, and the D-xx drawing rules). Load at the start of any DropOut schematic work and keep it loaded - capturing or drawing a sheet, choosing parts for a schematic, making symbols, or reviewing a schematic - and whenever the question is how to name a net or rail, which package or dielectric, how much margin, whether something needs a test point, or how a sheet should look.
---

# DropOut schematic rules

The full rules, with reasons, are in chapter 05 of the handbook: `../../handbook/05-schematic-pcb.md` (relative to this skill's base directory). Read it before drawing or reviewing a sheet; this file is the checklist. Where a rule gives a reason, the reason decides the cases the rule didn't foresee.

Adopted 2026-10-22 from charlesh97/ee-skills (`ee-schematic-rules`), restated in DropOut's words with DropOut changes. The `D-` and `O-` IDs are the source's; cite them in reviews and never renumber them. D-03 is not adopted.

The board's own `CLAUDE.md` overrides these only where it says so (e.g. JLC assembly, or net names kept under O-1).

## Start of capture

Ask the project questions and record the answers in the board's `CLAUDE.md` ("Schematic project answers"). An unanswered question with a default takes it and is written down **as a default**. Questions 5-7 have no default: don't start capture until they are answered.

1. 0201 passives allowed? Default no (0402 minimum).
2. Signal test point form? Default 1 mm exposed pad.
3. 0R debug resistors where? Default every regulator output.
4. Debug header? Default 2x5 1.27 mm Cortex Debug.
5. Ambient temperature range and qualification grade of the end device? From the architecture's requirements, or ask.
6. Environment (enclosure, humidity/condensation, vibration, conformal coating)? Ask.
7. Allowed capacitor dielectrics (X7R, X7S, X8R, C0G; is X5R allowed)? Chosen from 5 and 6: rated range covers ambient plus self-heating.

## Sheets and designators

- One hierarchical sheet per subsystem, per the architecture's sheet plan; a repeated block is one file placed per instance; files flat in `sheets/`; root `<board>.kicad_sch` is page 1.
- Page numbers 1-99, frozen once a sheet has parts. Designators are prefix + page x 100 + 01..99 (`R201`, `C1101`), stable once assigned.
- Prefixes: `R` (incl. 0R, jumpers), `RN`, `C`, `L` (energy storage), `FB` (ferrite), `D` (all diodes, LEDs), `Q`, `U`, `Y`, `J`, `TP`, `SW`, `F` (fuse, e-fuse), `K`, `MH`, `FID`, `NT`, `AE`. No thermistor prefix is decided yet (Node60 uses `TH`): ask if one is needed.
- Every pin is visible and wired on purpose; every supply pin gets the decoupling its datasheet asks for.

## Net naming

- Uppercase, digits, underscores only.
- Rails by voltage, no sign: `3V3`, `1V8`, `12V`. Domain qualifier only when two rails share a voltage (`3V3_ANA`). Never a rail named only by function.
- Rail-derived nets: voltage, device, pin: `1V8_MCU_VDD`.
- One `GND`. A split only where a datasheet requires it, cited on the sheet, joined once through an `NT`.
- Buses: bus+index, purpose, signal: `I2C0_SENSORS_SDA`, `SPI0_SENSORS_CS_ADC1`.
- Active low: `_L` suffix (`RESET_L`). `_P`/`_N` only for differential pairs.
- O-1: a board may keep names its architecture already records; Node60 keeps `3V3_MAIN`, `1V5_CORE`, `VDDAU_AON`, `VBAT_PROT`.
- **Every net is named** (O-2): no `Net-(...)` in the netlist, including divider, filter and series-chain nodes. `scripts/check_schematic.py` fails on it.

## Parts

- Only DropOut library parts (KiCad stock power and graphical symbols excepted). Prefer an existing library part over an equivalent new one.
- Fully specified: Manufacturer, MPN, `DigiKey_PN`, `Mouser_PN`, package, value, tolerance, voltage, dielectric, temperature range, and whatever it was chosen for. Never fill an MPN or distributor number from memory: live lookup or datasheet, or leave it empty and say so.
- Commodity passives are substitutable; parts chosen for an electrical property are binding and marked so. Consolidate nearby values.
- JLC-assembled boards only (named in the board's `CLAUDE.md`): `LCSC` field from a live lookup, JLC basic passives preferred, `CONSIGNED` plus a `Consigned` field for parts JLC can't supply (D-46).
- Capacitors: 0402 default through 1 uF; smallest package meeting capacitance and voltage after DC bias; dielectrics per the board's answer to question 7, C0G/NP0 for timing/filter/oscillator values, never Y5V/Z5U; rating at least 2x working voltage after DC bias. The temperature range must meet the board's grade.
- Resistors: 5 %, 0402, E24 unless the circuit needs better.

## Derating

Ceramic caps <= 50 % rated V after DC bias; MOSFETs <= 80 % Vds, <= 50 % Id; resistors <= 60 % power; electrolytic/polymer <= 80 % ripple current; junction <= Tj(max) - 25 C at the board's maximum ambient (question 5; Node60 +125 C); inductors on saturation current vs peak current (load + half ripple). Size 0R debug resistors for their current (0402 ~1 A). No relaxing on bring-up boards.

## Design for debug

Test points on every rail, bring-up buses and key GPIO, reset, interrupts, boot straps; ground test points are probe loops. 0R in regulator outputs. A debug header on every board (not Tag-Connect). Power and heartbeat LEDs where they fit. Document reset/default states of control lines; expose the architecture's interface nets; mark unverified items with a visible release-blocking note.

## Drawing rules

- D-01 Inputs left, outputs right, power from top, ground to bottom.
- D-02 Sheet order follows the power and signal path (set in the sheet plan before parts are placed).
- D-04 No four-way junctions; use two offset tees.
- D-10 One cluster per function: IC + decoupling + pull-ups + series parts.
- D-11 Clusters in a left-to-right band along the signal path.
- D-12 Repeated circuits drawn identically and aligned.
- D-13 Each cluster in a dashed grey box with a bold title (function + main designator); no box edge through a symbol, label or text.
- D-14 Large MCU symbols are split into units by datasheet function group in the library; on the sheet each unit gets its own box with the board-specific peripheral use and firmware notes.
- D-20 Wires inside a cluster; labels only between clusters and sheets.
- D-21 A local label appears once, on a wire; no same-name stubs instead of a wire.
- D-22 Series and pull-up resistors drawn inline in their path.
- D-23 Decoupling cap wired to its pin, joined to the rail with a junction.
- D-24 Rail-symbol columns with labels only for multi-drop nets (e.g. I2C pull-ups), beside the owning cluster.
- D-25 One-sheet nets get local labels; off-sheet nets use hierarchical labels and sheet pins; global labels only where there is no sheet-pin path. Use the netlist to tell which sheets a name reaches.
- D-30 One rail symbol per cluster, shared through junctions.
- D-31 Supply symbols may turn horizontal for an inline part; `GND` always upright.
- D-32 `PWR_FLAG` on each rail entering via a connector or passive, grouped together.
- D-40 Orientation follows the path.
- D-41 Field text rotates with the symbol; reference and value never overlap.
- D-42 Values visible.
- D-43 Connectors face into the sheet, pin 1 at top.
- D-44 Nothing overlaps; 1.27 mm grid.
- D-45 Values: `22pF`, `100nF`, `1uF`, `2.2uH`, `0R`, `120R`, `4.7k`, `1M`, `10mR`, `600R@100MHz`; ASCII `u`; voltage/tolerance/dielectric/power in their own fields.
- D-46 Every BOM part has Manufacturer, MPN, DigiKey_PN, Mouser_PN from a live lookup (plus LCSC on JLC boards); DNP parts too.
- D-47 (library) Box symbols sized so no pin name overprints another.
- D-48 Optional circuits drawn complete, DNP, with a 0R bypass where the path must conduct; `NOSTUFF` in the box title plus a population note.
- D-50 After a redraw or restructure, diff the netlist against the previous revision and explain every change.
- D-51 Render every sheet and look at it.
- D-52 ERC zero at every severity before handoff and before a `rev-*` tag, or each item excluded with a written reason. Correct the design rather than downgrading the ERC rule.
- D-60 Never copy a `.kicad_pro` from another project.
- D-61 Generated symbol instances carry `(body_style 1)` and `(in_pos_files yes)`.

## Reviewing

Grade a sheet against these IDs, citing the ID in each finding. Also run `python3 scripts/check_schematic.py <board>` and ERC, and render every sheet (D-51).
