# 05 · Schematic and PCB conventions

> **Status: early.** Items marked **(proposed)** are defaults until the first board settles them; changing them is a normal handbook PR.

## Schematic

- **Hierarchical sheets follow the architecture document's sheet plan.** One subsystem per sheet; repeated blocks (e.g. Node60's three output switches) are one sheet per instance.
- **Only DropOut library parts.** No KiCad stock symbols except power and graphical symbols.
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
