# 05 · Schematic and PCB conventions

> **Status:** the schematic rules are decided (2026-10-22). Items marked **(proposed)** are defaults until the first board settles them; changing them is a normal handbook PR.

## Schematic

### Where these rules come from

**Decided (2026-10-22).** DropOut adopted the schematic standard in [charlesh97/ee-skills](https://github.com/charlesh97/ee-skills/tree/e45935f58e3915a6fe891818fd0d49ef9114db4f/skills/ee-schematic-rules) (`SKILL.md` and `rules/schematic.md`, as of commit `e45935f`), with the DropOut changes marked **(DropOut)** below. That repo has no license, so nothing here is copied from it: each rule is restated in DropOut's words. The drawing-rule IDs (`D-01`…`D-61`, `O-1`, `O-2`) are the source's, kept so a rule can be traced back and so reviews can cite it. Never renumber a rule; retire one by marking it *(retired)*.

- **Adopted:** everything in the source's `SKILL.md`, and every drawing rule except D-03.
- **Not adopted: D-03** (prefer a few flat sheets; hierarchy two deep is a smell). DropOut boards use one hierarchical sheet per subsystem, and a repeated block is one sheet file placed per instance (below), so a change is made once.
- The `schematic-rules` skill summarises every rule by ID for capture and review.

Where a rule gives a reason, the reason decides the cases the rule didn't foresee.

### Before capture: project questions

Ask these at the start of schematic capture; the answers depend on the board. Record each answer in the board's `CLAUDE.md` (section "Schematic project answers"). If a question with a default isn't answered, take the default and record it **as a default**, not as a decision, so nobody mistakes it for one. Questions 5–7 have no default: capture doesn't start until they are answered. **(DropOut:** recorded in `CLAUDE.md`, not in separate `project.yaml` / `open_items.yaml` files.)

| # | Question | Default |
|---|---|---|
| 1 | Are 0201 passives allowed? | No; 0402 is the smallest |
| 2 | What is a signal test point? | A 1 mm exposed pad (smaller only if density forces it) |
| 3 | Where do 0R debug resistors go? | In every regulator output |
| 4 | Which debug header? | 2×5 1.27 mm Cortex Debug |
| 5 | What ambient temperature range must the end device work over, and to what qualification grade (e.g. AEC-Q100/Q200 Grade 1, −40…+125 °C)? | None: take it from the architecture's requirements, or ask |
| 6 | What environment does the end device live in (enclosure, humidity and condensation, vibration, conformal coating)? | None: ask |
| 7 | Which capacitor dielectrics are allowed (e.g. X7R, X7S, X8R, C0G; is X5R allowed)? | None: chosen from 5 and 6 so the rated temperature range covers the ambient range plus self-heating |

**(DropOut, 2026-10-22)** Questions 5–7 replace the source's fixed dielectric rule: capacitor temperature ratings depend on where the device runs, so each board decides them.

Node60 (2026-10-22): questions 1–4 take the defaults; 5 is Grade 1, −40…+125 °C (architecture requirements); 7: **no X5R**, higher-temperature dielectrics only (exact set to be recorded at capture); 6 not yet asked. Ground test points are probe loops on every board (Design for debug, below).

### Sheet structure

- **Hierarchical sheets follow the architecture document's sheet plan.** One subsystem per sheet; a repeated block (e.g. Node60's three output switches) is **one sheet file placed once per instance**, so a change is made once. Plan the sheet order along the power and signal path (D-02) before parts are placed, since page numbers freeze once they are.
- **Every pin is visible and wired on purpose.** Library symbols never combine pins ([chapter 04](04-library.md)), so each supply and ground pin is connected explicitly, with its own decoupling where the datasheet asks for it.

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
- **Prefixes** (the number part is page × 100 + nn, above):

  | Prefix | Part | Prefix | Part |
  |---|---|---|---|
  | `R` | resistor, including 0R debug links and jumpers | `J` | connector |
  | `RN` | resistor network | `TP` | test point |
  | `C` | capacitor | `SW` | switch |
  | `L` | inductor used for energy storage | `F` | fuse or e-fuse |
  | `FB` | ferrite bead used for filtering | `K` | relay |
  | `D` | any diode: TVS, Schottky, Zener, LED | `MH` | mounting hole |
  | `Q` | transistor | `FID` | fiducial |
  | `U` | IC | `NT` | net tie |
  | `Y` | crystal or oscillator | `AE` | antenna |

  Some splits are on purpose. `FB` and `L` are checked differently (impedance at frequency against saturation current), so a reviewer must tell them apart from the designator. Test points are `TP`, never `J`, so a script can count them. A permitted ground split joins through an `NT`, so the single join point exists as a part. `MH` and `FID` are left out of the BOM and placement files.
- **Designators are stable.** Assigned once and kept; renumbering breaks every review finding and placement note that cites one.
- **Sheets** are named after the block they hold.

### Net naming

**Decided (2026-10-22)**, replacing the proposed `<VOLTAGE>_<DOMAIN>` / `_N` rule.

- **Format:** uppercase letters, digits and underscores only. No hyphens, dots, spaces, or lowercase.
- **Rails are named by voltage**, with no sign and the decimal point written as `V`: `3V3`, `1V8`, `1V5`, `12V`, `0V9`. Add a domain qualifier only when two rails share a voltage (`3V3` and `3V3_ANA`). Never name a rail by function alone.
- **Nets derived from a rail** start with the voltage, then the device, then the pin: `1V8_MCU_VDD`, `3V3_ADC_AVDD`. Voltage first makes every net on a rail sort together and match one prefix.
- **Ground** is one net, `GND`. Split it (`AGND`, `PGND`) only where a part's datasheet requires it, cite that part on the sheet, and join the grounds at exactly one point through a net tie (`NT`). An unjustified split creates return-path problems layout can't fix.
- **Buses:** bus and index, then what the bus is for, then the signal: `I2C0_SENSORS_SDA`, `SPI0_FLASH_SCK`. The middle field is the bus's purpose, not its master, so a multi-drop net keeps one name. A per-device signal on a shared bus adds the device: `SPI0_SENSORS_CS_ADC1`.
- **Active-low signals end in `_L`** (`RESET_L`, `IRQ_L`). **(DropOut:** replaces the earlier proposed `_N`.)
- **`_P` / `_N` are reserved for differential pairs** (`USB_D_P`, `USB_D_N`). KiCad's differential-pair router and DRC find pairs by these suffixes; any other suffix makes their constraints silently do nothing.
- **Existing boards (O-1).** A board may keep the names its architecture already records; renaming touches the schematic and any routed layout. Record the choice in the board's `CLAUDE.md`. **Node60 keeps its Rev A names** (`3V3_MAIN`, `1V5_CORE`, `VDDAU_AON`, `VBAT_PROT`); its new nets follow these rules.

### Every net is named

No net in the netlist keeps a name KiCad made up (`Net-(R201-Pad2)`): every node of a feedback divider, an RC filter, or a chain of series parts gets a label. A net without a name can't be checked against what it should be or classified by layout. A dropped label also shows up as an auto-generated name, so this check catches the failure D-50 describes (O-2). The board's `scripts/check_schematic.py` enforces it ([chapter 06](06-ci-releases.md)).

### Every part is fully specified

- **Only DropOut library parts.** No KiCad stock symbols except power and graphical symbols. The library is the approved-parts list: a part already in it has been used and checked, so prefer it over an equivalent new one even at a slightly higher price.
- **Every part has a real MPN and its full set of descriptors:** manufacturer, MPN, distributor part numbers, package, value, tolerance, voltage rating, dielectric (ceramics), temperature range, and whatever else it was chosen for (tempco, current rating, saturation current, ESR, CTR). "100nF 0402" can't be checked for derating or DC-bias loss. **(DropOut:** distributor fields are `DigiKey_PN` and `Mouser_PN`; [chapters 03](03-part-search.md) and [04](04-library.md).)
- **Never fill an MPN from memory.** A remembered number is a lead until a live distributor lookup or the datasheet confirms it. Leave the field empty and say so.
- **Substitutable or binding.** Commodity passives are chosen on price and may be swapped for an equivalent at purchase. A part chosen for an electrical property (precision, tempco, matching, dielectric) is binding: mark it so the cheapest-part rule doesn't replace it.
- Fewer distinct part numbers usually saves more at assembly than a cheaper line: consolidate nearby values.
- **(DropOut) JLC assembly only:** a board whose `CLAUDE.md` names JLC assembly also fills `LCSC`, prefers JLC basic parts for passives, and marks a part JLC can't supply `LCSC = CONSIGNED` with a `Consigned` field saying who supplies it (D-46).

### Passives and part choice

- **0402 is the default capacitor package**, bypass included, up to 1 µF. Choose the package by search, not by table: the smallest one that meets both the capacitance and the voltage rating after DC-bias derating (a 1 µF 0402 exists at 16 V, not at 50 V).
- **Decoupling uses the smallest package on purpose**, so it sits closer to the pin; layout must follow through.
- **Resistors:** 5 %, 0402, E24 by default; tighter only where the circuit needs it.
- **Dielectric (DropOut):** set per board by project questions 5–7, not by a fixed rule; the part's rated temperature range must cover the board's ambient range ([chapter 03](03-part-search.md) rule 2). On every board: C0G/NP0 where the value sets a timing, filter, or oscillator, and never Y5V or Z5U (they lose most of their capacitance over temperature and bias).
- **Capacitor voltage rating:** at least 2× the working voltage, judged after DC-bias derating.
- **Value format and fields:** D-45, below and in [chapter 04](04-library.md).

### Reference circuits (DropOut)

Lessons from Node60's 10BASE-T1S interface (DEC-012 rev. B, DEC-017; 2026-10-29).

- **Interface circuits follow the IC maker's reference.** Use the application note the data sheet points to (LAN8670 → Microchip AN1718) and the interface standard's reference schematic (OPEN Alliance), and compare part by part, **including the order along the signal path**, not only the values. Node60 first had the T1S choke and DC-block capacitors in the reverse order.
- **Check the maker's evaluation-board schematic as a third source**, but note which circuit variant it uses: Microchip's LAN8670 boards use a demo network the app note reserves for another case. The app note wins over the board.
- **Read the standard's component table, not just its figure.** OPEN Alliance's T1S end termination is two 50 Ω ±1 % legs to a centre tap with 100 nF and 100 kΩ to ground, not one 100 Ω resistor.
- **Record every deviation** from the reference in a decision record, with the reason.

### Switched and configurable hardware (DropOut)

- **A switch in series with a precision element** (termination, divider, gain resistor) adds its on-resistance, and that resistance's drift over temperature and signal level, to the element's tolerance. Its off-state capacitance adds to the node's capacitance budget. Work out both before choosing a switch type: photorelays and analog switches trade low resistance against low capacitance, and single-supply switches clip signals that swing below ground. On a bus line, also check the switch survives the line's fault voltages (short to battery).
- **Settings that must hold while the board sleeps or is unpowered** (bus termination, address or mode selection) use latching or non-volatile parts, never a switch that falls back when its drive is gone. Firmware stores the intended state and re-applies it at every cold boot, because a latching part may ship, or be shocked, into the other state. Document the shipped state on the sheet and choose it as the safe default.

### Derating

Every part carrying voltage, current or power is derated:

| Part | Limit |
|---|---|
| Ceramic capacitor | ≤ 50 % of rated voltage, after DC-bias derating |
| MOSFET | ≤ 80 % of Vds, ≤ 50 % of Id |
| Resistor | ≤ 60 % of rated power |
| Electrolytic or polymer capacitor | ≤ 80 % of rated ripple current |
| Junction temperature **(DropOut)** | ≤ Tj(max) − 25 °C at the board's maximum ambient |
| Inductor | saturation current ≥ peak current (load + half the ripple), not RMS against average |

- **(DropOut)** The junction limit is a margin below each part's own maximum rather than the source's fixed 110 °C, because a board's maximum ambient (project question 5) can be at or above 110 °C; Node60 runs at +125 °C.
- **0R debug resistors are sized for their current**, taken from the power tree (a 0402 0R carries about 1 A).
- Derating applies on bring-up boards too.

### Design for debug

- **Test points** on every rail, on every bus and key GPIO used for bring-up (clock, SPI, I²C, MDIO), on reset, interrupt lines, and boot straps. Signal test points take the form the board's project answers give.
- **Ground test points are probe loops**, not flat pads, so a scope ground spring fits.
- **0R resistors in regulator outputs** (or where the project answers say), so a rail can be opened and its current measured.
- **Every board has a debug header** chosen for the board; not Tag-Connect.
- A power LED and an MCU heartbeat LED are good practice where area and power allow.
- **Document reset/default states** for control lines (chip selects, enables, fault inputs) on the sheet.
- **Expose the nets the architecture document lists** for each sheet at its interface.
- **Mark unverified items** (unconfirmed package ball maps, unverified sequencing, unmated connectors) with a visible note: they are release-blocking until closed.

### Drawing rules

**Flow and sheets**

- **D-01** In a sheet, signals flow left to right, power comes in from the top, ground goes to the bottom.
- **D-02** Sheets are ordered along the power and signal path. **(DropOut:** this sets the sheet plan's order before parts are placed; afterwards page numbers don't change.)
- **D-04** At most three wires meet at a junction; draw two offset tees instead of a four-way dot.

**Clusters**

- **D-10** Each function is one cluster: the IC with its decoupling, pull-ups, and series parts.
- **D-11** Clusters form a left-to-right band along the signal path.
- **D-12** Repeated circuits are drawn the same way and lined up, so a difference stands out.
- **D-13** Each cluster sits in a dashed grey box with a bold title at its top left saying what it does and its main designator. A box edge never crosses a symbol, label, or text; wires may cross it.
- **D-14 (DropOut)** A large MCU symbol is split into units by the datasheet's function groups (ports, supplies, ADC, debug, …) **in the shared library**, because library symbols don't know which board uses them ([chapter 04](04-library.md)). On the sheet, each unit sits in its own D-13 box whose title and a short note give the board-specific use: which peripheral and client, alternate-function numbers, boot-time catches the firmware must know.

**Wires and labels**

- **D-20** Inside a cluster, connect with wires; labels are for connections between clusters and sheets.
- **D-21** A local label names a wire once; two stubs with the same label in place of a visible wire are not allowed.
- **D-22** Series and pull-up resistors are drawn in the path they sit in, between the nodes they connect.
- **D-23** A decoupling capacitor is wired to the pin it serves and joins the rail with a junction.
- **D-24** A column of parts hanging off rail symbols with labels is allowed only for multi-drop nets (e.g. I²C pull-ups), placed beside the cluster that owns the net.
- **D-25** A net that stays on one sheet uses a local label on its wire. **(DropOut:** a net that leaves a sheet uses a hierarchical label and sheet pin, which is how each sheet exposes its interface; a global label only for a net with no sheet-pin path.) Check the netlist for which sheets a name appears on rather than judging from the drawing.

**Power symbols**

- **D-30** One rail symbol per cluster, shared through junctions, not one per pin.
- **D-31** A supply symbol may be turned horizontal to feed a horizontal inline part, pointing away from it; `GND` is always upright.
- **D-32** Each rail entering from a connector or through a passive gets a `PWR_FLAG`, grouped in one block.

**Symbols and text**

- **D-40** A part's orientation follows its path: horizontal inline, vertical in a pull-up column.
- **D-41** Field text turns with the symbol; set field positions so reference and value never overlap.
- **D-42** Values are visible.
- **D-43** Connectors face into the sheet with pin 1 at the top.
- **D-44** Nothing overlaps (symbols, labels, text); everything is on the 1.27 mm grid.
- **D-47** A box symbol is tall enough that no pin name runs into another. A library rule: [chapter 04](04-library.md).
- **D-48** An optional circuit is drawn complete with every part DNP, plus a fitted 0R bypass where the path must still conduct; the box title says `NOSTUFF` and a note says what is fitted, what is lost, and how to swap.

**Values and part fields**

- **D-45** One value format: capacitors `22pF`, `100nF`, `1uF`, `4.7uF`; inductors `100nH`, `2.2uH`; resistors `0R`, `22R`, `4.7k`, `10k`, `1M`, `10mR`; ferrite beads `600R@100MHz`. The number is 1–999 with the largest prefix that keeps it there, a decimal point (never `4k7`), ASCII `u` for micro, and every value ends in a letter. Voltage, tolerance, dielectric and power go in their own fields (`Voltage`, `Tolerance`, `Dielectric`, `Power`), never in the value. For DropOut library passives these are set in the library ([chapter 04](04-library.md)).
- **D-46 (DropOut)** Every part that reaches the BOM (all but `MH`, `FID`, `TP`, `NT`, power symbols and parts excluded from the BOM) carries `Manufacturer`, `MPN`, `DigiKey_PN` and `Mouser_PN`, from a live lookup, never from memory; DNP parts too. DropOut library symbols already carry them. On JLC-assembled boards only, add `LCSC` (whose MPN must match the symbol's) or `CONSIGNED` with a `Consigned` field; a blank `LCSC` never means consigned.

**Process**

- **D-50** After redrawing or restructuring a schematic, diff the netlist against the previous revision and account for every change. A tidy page can still swap two connector pins.
- **D-51** Render every sheet and look at it; ERC passes a page with one part drawn over another.
  - **(DropOut)** KiCad mirrors a mirrored symbol's field justification too: a field justified right on a symbol with `(mirror y)` renders left-justified. Check the reference and value of every mirrored symbol on the rendered sheet, whether it was placed by hand or by a script.
- **D-52** ERC is zero before handoff, or each remaining item has a written justification ([chapter 06](06-ci-releases.md)). Correct the design rather than downgrading the ERC rule.

**File hygiene**

- **D-60** Never copy a `.kicad_pro` from another project (stale root sheet name and UUID make KiCad re-key the file on first save).
- **D-61** Generated symbol instances include `(body_style 1)` and `(in_pos_files yes)`, so KiCad's first save changes nothing.

### Open

- **Thermistor prefix.** The adopted prefix list has none; Node60 uses `TH`. Undecided.

## PCB (proposed defaults)

- **Stackup:** 4 layers minimum for any board with a high-speed bus or a switching regulator; 2 oz outer copper for high-current paths. Final stackup per board in the architecture document.
- **Rules:** start from the chosen fab house's standard capability; record the fab house and its rule set in the board's `CLAUDE.md` and `.kicad_dru`.
- **High-current paths:** every path above ~3 A gets its copper width, thickness, and via count calculated and noted on the PCB or in `docs/`.
- **Exposed pads:** follow each datasheet's thermal-via recommendation.
- **Return paths:** keep high di/dt loops away from analog sense, clock, and network lines; describe the ground strategy in the architecture document.
- **Silkscreen:** reference designators readable after assembly; connector pin 1 and polarity marked; board name, revision, and DropOut on the top side.
