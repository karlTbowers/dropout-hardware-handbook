# 07 · Tools and credentials

## Toolchain

| Tool | Role |
|---|---|
| **KiCad 10** | Schematic, PCB, library editing; `kicad-cli` for exports and checks |
| **Claude Code** on the Mac, in `~/Dev` | The main way Claude works on DropOut hardware: direct file access, no network allowlist |
| **dropout-hardware-handbook** plugin (this repo) | Skills: `dropout-standards`, `find-part`, `new-board` |
| **kicad-happy** plugin | Distributor APIs (`digikey`, `mouser`, `element14`), design analysis (`kicad`, `bom`, `spice`, `emc`) |
| **Konnect** (KiCad 10 MCP, installed on the Mac) | Live KiCad project and board edits through KiCad's IPC API; needs KiCad running |
| **Claude in Chrome** | Sign-in-gated manufacturer and CAD sites, using the user's Chrome |
| **kicad-library-tools** | Footprint and 3D generators, KLC checkers (pinned in the library repo) |
| **GitHub** + **Actions** | Repos, PRs, CI, releases, GitHub Pages |
| **Astro** + Pagefind | Library catalog site |
| **Astro Starlight** | Architecture and board documentation sites ([chapter 08](08-architecture-documents.md)) |
| **D2** | System and block diagrams (text source, clickable blocks) |
| **Mermaid** | Sequence and state diagrams; diagrams in READMEs and PRs |
| **claude.ai project** "Automotive Power Distribution Unit KiCAD project" | Architecture discussions and documents; not the place for file work |

## Considered and rejected

| Tool | Decision |
|---|---|
| KiCAD-Prism | Reviewed by the user; not used. The catalog site is built with Astro. |
| kistack | Not used; DropOut writes its own skills. |
| Hugo, Jekyll, seite | Astro chosen for data-driven pages and the interactive 3D viewer. |
| Hand-written single-file HTML architecture documents | Replaced by Starlight sites (2026-10-21): not diffable, raster diagrams, facts duplicated, no traceability. |
| pcbparts-mcp, Nexar, datasheet MCPs | See [chapter 03](03-part-search.md#considered-and-not-used). |

## Credentials

All site logins and API keys live in **one file on the Mac**:

```
~/.local/share/dropout/vendor-logins        (mode 600, outside ~/Dev)
```

- It holds `<VENDOR>_USER` / `<VENDOR>_PASSWORD` pairs (NXP, TI, Ultra Librarian, SnapMagic, DigiKey, Mouser, Newark) and the API keys `DIGIKEY_CLIENT_ID`, `DIGIKEY_CLIENT_SECRET`, `MOUSER_SEARCH_API_KEY`, `NEWARK_SEARCH_API_KEY`.
- **API keys** reach every shell (and Claude Code) through `~/.zshrc`:
  ```bash
  eval "$("$HOME/Dev/dropout-kicad-library/scripts/vendor-env.sh")"
  ```
  The script parses the file, never sources it, and exports only API keys, plus alias names for tools that expect different variable names.
- **Passwords** are read from the file only when a browser sign-in is needed.

Rules for Claude:
- Never print, log, echo, commit, or copy values from this file.
- Never `source` it; passwords contain shell metacharacters.
- New credentials: the user edits the file directly. Avoid pasting secrets into chat, where they stay in the conversation history.
- A new API key that a tool expects under a different variable name gets an alias in `vendor-env.sh`'s `EXPORTS` list, not a duplicate entry in the file.
