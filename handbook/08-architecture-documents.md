# 08 · Architecture and board documentation

**Decision (2026-10-21):** every DropOut device documents its architecture, and its other design documents, as an **Astro Starlight** site in the board repo, published to GitHub Pages. Hand-written single-file HTML documents are no longer used. Existing ones are kept as frozen records.

## What makes a good architecture document

1. **Lead with the decision.** The chosen architecture in one paragraph, the primary release blocker, and a status grid (locked / risk / blocked per subsystem).
2. **Facts live once, as data.** Requirements, parts, decisions, and verification gates are structured data files with IDs. Pages render them, so a number is never typed twice and can't drift.
3. **Every decision has a record.** Context, the choice, **rejected alternatives with reasons**, and consequences. Superseded decisions are marked, never deleted.
4. **Traceability.** Requirement → decision → part → gate → test result, all linked by ID. The build fails on a reference to an ID that doesn't exist.
5. **Numbers justify choices.** Show the calculation (dissipation, margins, resolution), not just the conclusion.
6. **Sourcing is dated.** Price and stock are observations with a date and source ([chapter 03](03-part-search.md)).
7. **Diagrams are code.** Diagram sources are text, diffable in PRs, and every block links to its section.
8. **Layered for the reader.** One-page overview → system view → one page per subsystem → data tables.
9. **Git is the revision history.** Each architecture revision is a tag; changes are reviewable diffs, with a revision-history page summarizing them.

## Site layout in a board repo

The whole `docs/` folder is the Starlight project:

```
docs/
  package.json, astro.config.mjs          Starlight site; base "/<board>-hw"
  src/content/docs/
    index.mdx                             decision overview + status grid (from data)
    requirements.mdx                      rendered from data/requirements.yaml
    system.mdx                            system block diagram + partitioning
    subsystems/<name>.mdx                 one page per subsystem
    decisions/                            index + one page per decision (from data)
    components.mdx                        component baseline (from data/parts.yaml)
    interfaces.mdx                        schematic sheet plan and nets each sheet exposes
    verification.mdx                      gates and status (from data/gates.yaml)
    calculations/, bring-up/, validation/ other design documents
    sources.mdx                           source register
    revisions.mdx                         revision history
  src/data/
    requirements.yaml                     REQ-<AREA>-<NNN>
    parts.yaml                            role, MPN, dated observations, second source, library ref
    gates.yaml                            GATE-<AREA>-<NN>
    decisions/DEC-<NNN>-<slug>.md         one file per decision (frontmatter + reasoning)
  src/diagrams/                           *.d2 and *.mmd sources
  src/components/                         StatusGrid, RequirementTable, PartTable, GateList, Ref…
  public/legacy/                          frozen pre-Starlight documents (served as-is)
```

### IDs and data

| Kind | ID format | Key fields |
|---|---|---|
| Requirement | `REQ-PWR-003` | text, value/limit, rationale, `verified_by: [GATE-…]` |
| Decision | `DEC-007` | title, status (proposed / accepted / superseded), date, revision, `supersedes`, `requirements`, `parts`, rejected alternatives |
| Part | MPN | role, subsystem, manufacturer, `observations: [{date, source, price_1, price_1k, stock}]`, second source, `DropOut_<Lib>:<Symbol>` reference |
| Gate | `GATE-THM-01` | evidence required, what it blocks, status, link to result |

Astro content collections validate the data (schemas with references). A broken ID or missing field fails the build, and CI runs the build.

Parts that exist in `dropout-kicad-library` link to their page in the library catalog (`https://karltbowers.github.io/dropout-library-catalog/parts/<Library>/<Symbol>/`: symbol, footprint, 3D viewer).

## Diagrams

**Decided (2026-10-21):** D2 for architecture diagrams. Every architecture has **two system views**:

| View | Shows | Conventions |
|---|---|---|
| **Power** | Source → input protection → protected bus → always-on supplies, switched rails, switched loads; what each rail feeds | Line weight shows current: thick = high-current battery path, medium = protected-bus branches, thin = regulated rails; dashed = enable/supervision. Collapse series chains (e.g. TVS → FETs → shunt → FETs) into one block with the chain in its label, and use a bus node where one supply fans out, so the diagram stays a few columns deep. |
| **Signals** (digital and analog) | Buses and signals between the controller and everything it talks to | Inputs on one side, controller in the middle, controlled devices on the other. Solid = digital (network in its own colour), dashed = analog into an ADC. Undirected analog lines with "→ ADC" in the label keep the layout one-sided. |

Rules for both:
- Colours by domain, consistent across the site: battery, always-on, compute, network, measurement, switched loads.
- **Every block links to its subsystem page.** Every connection is labelled.
- Enables that would add extra layout depth (e.g. a PHY INH pin enabling a regulator) are written in the block label ("EN ← LAN8670 INH") rather than drawn as an edge.
- Don't mix D2 grid layouts with the automatic layout; edges get routed through blocks.
- **Direction: left-to-right** for both views (`direction: right`).
- **Layout engine per view**, set inside each `.d2` file so no command-line flag is needed:
  - Power view: **dagre** (curved lines; reads like a power tree).
  - Signals view: **ELK** (right-angle lines; the controller becomes a tall block that signals enter and leave like pins).
  ```d2
  vars: {
    d2-config: {
      layout-engine: elk   # dagre for the power view
    }
  }
  ```
- Keep each view about five columns deep so left-to-right stays readable at page width (decided 2026-10-21 after comparing all eight direction/engine combinations on Node60).
- **Mermaid** (proposed) for sequences and state machines, such as a power-state cycle, and for small diagrams in READMEs and PRs.
- Diagrams render at build time (the `d2` binary is installed in CI), never in the reader's browser.

## Revisions

- Architecture revisions are lettered (Rev A, B, C…) and tagged in git as `arch-rev-<letter>`. (Board fab revisions use `rev-<letter>`; the two series are independent.)
- `revisions.mdx` lists what changed in each revision and why, linking the decisions added or superseded.
- The published site always shows `main`. A past revision is read from its tag.

## Publishing

A `docs.yml` workflow in the board repo builds the site (Node + `d2`) on every push to `main` and deploys it to GitHub Pages: `https://karltbowers.github.io/<board>-hw/`. Pull requests build it without deploying, so broken references fail the PR. In the repo's **Settings → Pages**, set the source to **GitHub Actions**.

## Template

The board template (`templates/board/docs/`) is a ready Starlight starter, extracted from the Node60 port (2026-10-21): config with the `/<board>-hw` base, content-collection schemas, the data layer that fails the build on unknown IDs, the rendering components (`StatusGrid`, `RequirementTable`, `PartTable`, `GateList`, `DecisionList`, `SourceList`, `Metrics`, `Ref`, `D2Diagram`, `MermaidDiagram`), empty data files with commented examples, page skeletons, power and signals D2 skeletons with this chapter's conventions, and `.github/workflows/docs.yml`. The `new-board` skill installs it. Node60's site is the worked example.
