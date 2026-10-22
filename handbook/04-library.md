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

The library publishes a searchable catalog with symbol and footprint drawings and an interactive 3D viewer at `https://karltbowers.github.io/dropout-kicad-library/`, built with Astro by GitHub Actions on every push to `main`. Plan: the library repo's `CLAUDE.md`.
