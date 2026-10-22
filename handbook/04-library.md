# 04 · Library

All DropOut boards use one shared library: [`dropout-kicad-library`](https://github.com/karlTbowers/dropout-kicad-library). Its own `docs/CONTRIBUTING.md` and `klc-exceptions.yml` are the authority for part-level rules; this chapter is the summary.

## Rules in brief

- **KLC in full** (https://klc.kicad.org/), except the approved deviations in `klc-exceptions.yml`. CI runs the official KLC checker from kicad-library-tools and waives only those.
- **Fully specified (atomic) parts:** one symbol = one orderable MPN, footprint linked. No generic symbols, including passives.
- **DropOut fields** on every symbol: `Manufacturer`, `MPN`, `DigiKey_PN`, `Mouser_PN`, in addition to KLC's fields.
- **Library names** `DropOut_<Category>`, an approved exception so they never collide with KiCad's stock libraries.
- **3D model paths** `${KIPRJMOD}/lib/dropout-kicad-library/3dmodels/...`, an approved exception that keeps models pinned per board revision.
- **Never silently change a released land pattern.**

## Adding a part

Use the library repo's `add-part` skill (Claude Code in `~/Dev/dropout-kicad-library`). In order: find the exact part ([chapter 03](03-part-search.md)), generate the footprint and 3D model with kicad-library-tools, build the symbol from the datasheet pin table, run the field and KLC checks, cross-check pins, and open a PR titled `Add <MPN>`.

## Exceptions

New KLC exceptions are proposed to the user, never added on Claude's own initiative. Each goes in its own PR, as one entry in `klc-exceptions.yml` with the rule ID, scope, a narrow `match` regex, reason, and date.

## Catalog site

**Decided (2026-10-22):** the catalog lives in its **own repo**, [`dropout-library-catalog`](https://github.com/karlTbowers/dropout-library-catalog), published at `https://karltbowers.github.io/dropout-library-catalog/`. The library repo holds only parts and their checks, because every board mounts it as a submodule and none of them needs the site.

- The catalog is built with Astro by GitHub Actions from the library's `main`: symbol and footprint drawings, every field, distributor links, and (planned) an interactive 3D viewer.
- It rebuilds when the library's CI sends a `library-updated` repository dispatch after a push to `main` passes the checks (library secret `CATALOG_DISPATCH_TOKEN`: a fine-grained token with Contents: read and write on the catalog repo only), and nightly as a fallback.
- Nothing is edited in the catalog to add a part: add it to the library. Plan and status: the catalog repo's `CLAUDE.md`.
