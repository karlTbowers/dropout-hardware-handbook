---
name: find-part
description: Find, compare, and select electronic parts the DropOut way (DigiKey, Mouser, and Newark APIs, web search, manufacturer datasheets), with dated price/stock observations and a recorded decision. Use when asked to find a part, suggest alternatives or second sources, check stock, pricing, or lifecycle, or re-source a BOM.
---

# Find and select a part

Policy and tool choices are in `../../handbook/03-part-search.md` (relative to this skill's base directory). Read it if anything below is unclear; it wins on conflict.

## 0. Check the tools (once per session)

- `DIGIKEY_CLIENT_ID`, `MOUSER_SEARCH_API_KEY`, and `NEWARK_SEARCH_API_KEY` must be set (exported by `~/Dev/dropout-kicad-library/scripts/vendor-env.sh`). If not, say so and stop; don't fall back to scraping distributor sites.
- The kicad-happy `digikey`, `mouser`, and `element14` skills are the way to call the APIs.

## 1. Pin down the requirement

Write the requirement as a short list of hard limits before searching: function, key electrical limits, package constraints, qualification grade (from the board's requirements; automotive = AEC-Q100/Q101/Q200 at the stated grade), interface, and budget. Ask the user only for limits you can't get from the architecture document.

## 2. Discover candidates

1. **DigiKey parametric search** via the `digikey` skill, using the hard limits as filters, in-stock first.
2. **Manufacturer selection guides / parametric tables** via web search when DigiKey's categories don't fit, or to catch parts DigiKey doesn't stock.
3. Narrow to 2–5 candidates. Never propose a part from memory without confirming it exists and is active.

## 3. Verify each candidate

For each:
- **Datasheet:** open the manufacturer PDF and check every hard limit against it. Distributor summaries don't count.
- **Exact orderable MPN** including packaging suffix.
- **DigiKey and Mouser:** PN, price at 1 and 1,000, stock, lifecycle; **Newark** as a third check.
- **Second source:** a drop-in or near-drop-in alternative, or "none found".
- Gated documents (reference manuals, pinout spreadsheets) through the user's Chrome, signing in with the matching lines from the credentials file only if needed.

## 4. Recommend and record

Present a comparison table with: MPN, why it fits, the limiting spec, price @1 / @1k, stock at DigiKey / Mouser / Newark, lifecycle, second source, and the risk. **Date every price and stock figure** ("observed YYYY-MM-DD").

Then:
- Give one recommendation with its main trade-off.
- Once the user picks, update the board's architecture document: the selection, the numbers that justify it, and the **rejected candidates with reasons**.
- If the part isn't in `dropout-kicad-library` yet, offer to add it with the library repo's `add-part` skill.

## Re-sourcing an existing BOM

Use the kicad-happy `bom` skill to extract MPNs, then refresh every line's stock, price, and lifecycle. Report: zero-stock lines, lifecycle changes, and price changes over 20% since the last recorded observation. Propose second sources for every zero-stock or end-of-life line.
