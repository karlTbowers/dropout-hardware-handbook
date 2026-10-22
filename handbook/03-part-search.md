# 03 · Part search and selection

How DropOut finds, verifies, and chooses parts, and which tool is used for each job. Claude follows this through the `find-part` skill.

## Which tool for which job

| Job | Primary tool | Fallback | Never |
|---|---|---|---|
| **Discover candidates** ("a 40 V Grade 1 buck, ≤ 2 µA Iq, QFN") | DigiKey API keyword + parametric search (kicad-happy `digikey`) | Web search of manufacturer parametric tables and selection guides | Rely on memory for what exists |
| **Exact part data** (MPN with packaging suffix, distributor PNs, price breaks, stock, lifecycle) | DigiKey API and Mouser API (kicad-happy `digikey`, `mouser`) | Newark/element14 API (kicad-happy `element14`) | Copy numbers from a distributor web page without the date |
| **Third-source check** (availability spread) | Newark/element14 API | — | |
| **Datasheet** | Manufacturer site (direct PDF, e.g. `ti.com/lit/gpn/...`), fetched in Claude Code's built-in browser; DigiKey API returns the link. Check the revision | Distributor-hosted copy *to read* only, and re-check against the manufacturer's current revision (mirrors go stale) | Commit PDFs to any public repo |
| **Gated manufacturer files** (reference manuals, pinout spreadsheets, IBIS, design files) | Manufacturer site in Claude Code's **built-in browser**, which keeps the user's vendor sign-ins | Claude in Chrome; or ask the user to download | Bypass a login, NDA, CAPTCHA, or export-control step; have Claude type a password |
| **Symbol pinout** | Generated from the datasheet pin table (or manufacturer pinout spreadsheet) | — | Use an aggregator's symbol as the source |
| **Footprint** | kicad-library-tools generators fed the datasheet's recommended land pattern | Hand-drawn per KLC for non-standard packages | Commit aggregator footprints |
| **3D model** | kicad-library-tools 3D generators | Manufacturer STEP whose license allows redistribution | Commit SnapMagic / Ultra Librarian / SamacSys models |
| **Cross-check** of pinout and land pattern | A second manufacturer source (a datasheet figure, the vendor's own CAD in a design package); SnapMagic, Ultra Librarian (TI's official CAD source), SamacSys via the built-in browser | — | Treat aggregators as authoritative |
| **Archiving documents** | Every manufacturer document used goes in the private `dropout-vendor-docs` repo with an index row, by default | — | Commit it to a public repo |
| **Product change / EOL notices** | DigiKey Product Information API (product change notifications) | Manufacturer PCN pages | |

## Distributor priority

1. **DigiKey**: primary for prototypes and the main API for search.
2. **Mouser**: second source and price/stock comparison.
3. **Newark / element14**: third check.

JLCPCB/LCSC are not in the default flow. If a board uses JLC assembly, that board's `CLAUDE.md` says so and adds LCSC part numbers.

## Selection rules

A part is acceptable only when all of these hold, or the exception is written into the architecture document:

1. **Datasheet verified.** Every number used in the design comes from the manufacturer datasheet, not a distributor summary.
2. **Qualification matches the requirement.** Automotive designs require AEC-Q100 (ICs), AEC-Q101 (discretes), or AEC-Q200 (passives) at the grade the requirements state (Node60: Grade 1, −40…+125 °C).
3. **Active lifecycle.** Not obsolete, NRND, or last-time-buy.
4. **Orderable now.** Stock at DigiKey or Mouser, or a known lead time that fits the schedule. Zero-stock parts are flagged as procurement risks in the architecture status grid.
5. **Second source considered.** For each key part, record a drop-in or near-drop-in alternative, or state that none exists.
6. **Exact orderable MPN.** Including packaging suffix (`TPS2HCS08AQPWPRQ1`, not `TPS2HCS08-Q1`).

## Recording what was found

- Every price or stock figure is an **observation with a date** ("$5.43 @1, 32,413 DigiKey, observed 2026-10-13"), never a quote.
- Rejected candidates go in the architecture document with the reason, so the search isn't repeated.
- Distributor PNs go into the symbol's `DigiKey_PN` and `Mouser_PN` fields when the part is added to the library.
- Re-check stock and lifecycle at BOM lock and again before ordering.

## Tools in use

| Tool | What it is | Used for |
|---|---|---|
| **kicad-happy** (Claude Code plugin) | Skills: `digikey`, `mouser`, `element14`, `kicad`, `bom`, `spice`, `emc`, … | Distributor APIs, design analysis, pin-level review |
| **DigiKey Product Information API v4** | Official API; 2-legged OAuth; 120 req/min, 1,000/day | Search, product details, datasheet links, change notifications |
| **Mouser Search API** | Official API key | Product data, second source |
| **Newark / element14 Product Search API** | Official API key | Third source |
| **Web search** | General search | Discovery, manufacturer selection guides, app notes |
| **Built-in browser** (Claude Code desktop app) | A browser pane with a persistent profile, signed in once by the user to each vendor site | NXP, TI, Ultra Librarian, SnapMagic, Newark, and other sign-in-gated sites; downloads land in `~/Downloads` |
| **Claude in Chrome** | The user's Chrome with saved sign-ins | Fallback when the built-in browser can't reach a site |
| **`distributor_lookup.py`** (library repo) | One command over the DigiKey, Mouser, and Newark APIs | Exact-MPN data for a library part |
| **poppler** (`pdftotext`, `pdftoppm`, `pdfdetach`, `pdfinfo`) | PDF command-line tools | Reading datasheets, rendering drawings, extracting spreadsheets attached to reference manuals |
| **kicad-library-tools** | KiCad library team's generators and KLC checkers | Footprints, 3D models, KLC compliance |

### Considered and not used

| Tool | Why not |
|---|---|
| pcbparts-mcp | Parametric search covers JLCPCB/LCSC only; DigiKey/Mouser lookups are by part number only; shared quota. Revisit if a board uses JLC assembly. |
| Nexar / Octopart MCP | Multi-distributor and lifecycle data are useful, but the free tier is limited. Candidate for later lifecycle checks. |
| Sheetsdata / Whatic datasheet MCPs | AI-extracted pinouts can't be the source; the datasheet is read directly. |
| kistack `kicad-footprint` skill | DropOut builds its own `add-part` skill on kicad-library-tools directly. |
| easyeda2kicad, JLC2KiCadLib | LCSC-centric importers; redistribution terms unclear. |

## Manufacturer documents

- **Get them in the built-in browser.** Scripted downloads are blocked by some vendors (nxp.com) and distributor fetchers return stale copies. Claude uses the built-in browser without asking which browser to use.
- **Sign-ins are the user's.** If a site asks for a password, the user signs in in the browser pane once; the sign-in persists. Claude never types passwords, even though they're stored in the credentials file (Claude's own safety rules forbid it).
- **Check the revision.** Read the revision and date off the document; a distributor's mirror can be several revisions old (S32K3xx data sheet: Newark Rev. 12, NXP Rev. 14).
- **Archive every document used** in `dropout-vendor-docs` under `<Manufacturer>/<family>/` (package drawings under `<Manufacturer>/packages/`), original file name, with an index row: revision, source URL, sign-in needed, date retrieved, SHA-256 prefix, and what it was used for. Never overwrite a revision a released part used.
- **Public repos link, never copy.** Symbols carry the manufacturer `Datasheet` URL and, for a gated document the part was built from, a `Reference_Manual` URL plus a `Notes` line naming the exact attachment or sheet.

## Credentials

API keys and site logins live only in `~/.local/share/dropout/vendor-logins` on the Mac, outside every repo. API keys reach the environment through `dropout-kicad-library/scripts/vendor-env.sh`. See [chapter 07](07-tools.md#credentials).
