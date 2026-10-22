# {{BOARD_TITLE}} documentation

This folder is the {{BOARD_TITLE}} documentation site ([Astro Starlight](https://starlight.astro.build/), DropOut Hardware Handbook chapter 08), published at **https://karltbowers.github.io/{{BOARD}}-hw/**.

| Document | Status |
|---|---|
| Architecture Rev A | In progress |
| Calculations | Open |
| Bring-up checklist | Open |
| Validation results | Open |

## Layout

```
src/content/docs/        pages (MDX): overview, requirements, system, subsystems/, decisions, components, …
src/data/                facts with IDs: requirements.yaml, parts.yaml, gates.yaml, decisions/DEC-NNN-*.md,
                         status.yaml (overview grid), sources.yaml
src/content.config.ts    schemas; every cross-reference is checked at build time
src/diagrams/            power.d2 (dagre), signals.d2 (ELK), *.mmd (Mermaid)
src/components/          StatusGrid, RequirementTable, PartTable, GateList, DecisionList, Ref, D2Diagram, …
public/legacy/           frozen pre-Starlight documents, served as-is
```

## Build locally

Needs Node 22+ and the [`d2`](https://d2lang.com/) binary (`brew install node d2`).

```bash
cd docs
npm install
npm run dev        # renders diagrams, then serves http://localhost:4321/{{BOARD}}-hw/
npm run build      # renders diagrams, validates data, builds dist/
```

To change a fact, edit its data file, not the page. A reference to an ID that doesn't exist fails the build (`<Ref id="DEC-001" />` in pages, `verified_by`, `parts`, `gates`, … in data).

Datasheets are linked from each symbol's `Datasheet` field rather than stored here.
