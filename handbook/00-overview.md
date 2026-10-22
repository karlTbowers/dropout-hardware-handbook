# DropOut Hardware Handbook: Overview

This handbook is how DropOut designs hardware. Every device follows it, whoever (or whatever) is doing the work: a person, or Claude via this repo's Claude Code plugin.

## Principles

1. **Open hardware by default.** Board and library repos are public. Never commit credentials, NDA material, or files whose license forbids redistribution. Manufacturer documents go in the one private repo, `dropout-vendor-docs`, and public repos link to them.
2. **The manufacturer's datasheet is the authority.** Distributor pages, aggregator models, and AI-extracted data are checks, never sources.
3. **Decisions are written down with their reason.** Architecture choices, rejected alternatives, rule exceptions, and tool choices all live in a document with a date.
4. **Machines enforce rules; people review judgment.** Anything checkable (fields, KLC, ERC, DRC) runs in CI. Reviews cover what scripts can't.
5. **Everything is reproducible.** Board revisions pin the library and handbook versions they were designed under. A tagged revision rebuilds its fab outputs identically.
6. **Sourcing is a design input, not an afterthought.** Availability, lifecycle, and second sources are checked when a part is chosen, not at BOM lock.

## The repositories

| Repo | Purpose | Visibility |
|---|---|---|
| [`dropout-hardware-handbook`](https://github.com/karlTbowers/dropout-hardware-handbook) | This handbook, board template, and the Claude Code plugin | Public |
| [`dropout-kicad-library`](https://github.com/karlTbowers/dropout-kicad-library) | Company-wide symbols, footprints, 3D models, and their checks only; boards mount it as a submodule | Public |
| [`dropout-library-catalog`](https://github.com/karlTbowers/dropout-library-catalog) | Browsable catalog of the library ([site](https://karltbowers.github.io/dropout-library-catalog/)) | Public |
| [`dropout-vendor-docs`](https://github.com/karlTbowers/dropout-vendor-docs) | Archive of every manufacturer document a part or board was built from (datasheets, reference manuals, package drawings, design packages), Git LFS | **Private** |
| `<board>-hw` (e.g. [`node60-hw`](https://github.com/karlTbowers/node60-hw)) | One per device: KiCad project, docs, CI | Public |
| `<board>-fw` (future) | Firmware per device | TBD |

## Chapters

| # | Chapter | Covers |
|---|---|---|
| 01 | [Design process](01-design-process.md) | Stages and gates from requirements to release |
| 02 | [Repositories and workflow](02-repositories.md) | Repo layout, submodules, branches, tags, versioning |
| 03 | [Part search and selection](03-part-search.md) | How parts are found, verified, and chosen, and with which tools |
| 04 | [Library](04-library.md) | How the shared KiCad library works |
| 05 | [Schematic and PCB conventions](05-schematic-pcb.md) | Sheets, nets, test points, layout defaults |
| 06 | [CI and releases](06-ci-releases.md) | Checks on every push; what a release contains |
| 07 | [Tools and credentials](07-tools.md) | The toolchain, what was rejected and why, credentials handling, setting up a new Mac |
| 08 | [Architecture and board documentation](08-architecture-documents.md) | Starlight docs sites, data-driven architecture, diagrams, decision records |

## Changing the handbook

The handbook changes through pull requests, like code. Each merged change that alters a rule bumps the plugin version in `.claude-plugin/plugin.json` and adds a line to [`CHANGELOG.md`](../CHANGELOG.md). Board repos record the handbook version they follow, so a rule change never silently rewrites how an existing board should have been done.
