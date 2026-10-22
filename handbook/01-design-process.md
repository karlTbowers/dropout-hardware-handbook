# 01 · Design process

Every device moves through these stages. Each ends at a **gate**: a list of evidence that must exist before the next stage starts. Gates can be passed with open items only when each open item is written down with an owner and a stage by which it must close.

## Stage 1 · Requirements

Write down what the device must do, in measurable terms: electrical (voltages, currents, accuracy, resolution), environmental (temperature range, qualification grade), interfaces (connectors, buses, wire count), and constraints (cost, size, power budget in each state).

**Gate:** a requirements table in the architecture document, every line testable.

## Stage 2 · Architecture

Choose the system structure and the key parts. The architecture is documented as a **Starlight site** in the board repo's `docs/` (format, data files, and diagrams in [chapter 08](08-architecture-documents.md)). Its content follows the Node60 pattern:

- **Decision overview:** the chosen architecture in one paragraph, plus the primary release blocker if there is one.
- **Status grid:** each subsystem with its state (locked, risk, blocked).
- **One section per subsystem:** what was chosen, why, the numbers that justify it, and **rejected alternatives with the reason**.
- **Component baseline:** every key part with price and stock *observations, dated*. These are snapshots, never quotes.
- **Schematic-capture interfaces:** the sheet plan and the nets each sheet must expose.
- **Verification and release gates:** what must be proven, and what each unproven item blocks.
- **Source register:** every datasheet and reference used.

Revisions are lettered (Rev A, B, C…), tagged `arch-rev-<letter>`, and each states what changed and why.

**Gate:** architecture reviewed; every key part has a datasheet-verified selection and a sourcing check ([chapter 03](03-part-search.md)); release blockers are named.

## Stage 3 · Library

Every part the schematic will use exists in `dropout-kicad-library`, added through the `add-part` skill and merged ([chapter 04](04-library.md)). Missing parts are added *before* they are placed, never as placeholders.

**Gate:** all parts merged; the board repo's library submodule updated to include them.

## Stage 4 · Schematic capture

Follow the sheet plan from the architecture document and the conventions in [chapter 05](05-schematic-pcb.md).

**Gate:** ERC clean in CI; schematic review done (pin-level check of every IC against its datasheet, using the kicad-happy `kicad` skill as a first pass, then human review); BOM exported and sourcing re-checked.

## Stage 5 · PCB layout

**Gate:** DRC clean with schematic parity in CI; layout review (power paths, thermal, return paths, sensitive nets); 3D view checked for mechanical fit.

## Stage 6 · Release for fabrication

Tag `rev-<letter>`. CI builds the fab package and attaches it to a GitHub Release ([chapter 06](06-ci-releases.md)). Final sourcing check against live distributor stock before ordering.

**Gate:** release exists; BOM orderable; fab and assembly order placed.

## Stage 7 · Bring-up

Follow a written bring-up checklist in `docs/`: power-up sequence, rail-by-rail checks, then each subsystem in dependency order. Record every deviation as an issue in the board repo.

**Gate:** every subsystem functional or its failure recorded as an issue.

## Stage 8 · Validation

Run the verification gates from the architecture document. Results, with data, go in `docs/`. A claim (e.g. "10 A continuous") is not made until its gate passes.

**Gate:** all release-blocking gates passed, or the product claim is reduced to what was proven.
