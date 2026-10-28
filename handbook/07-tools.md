# 07 · Tools and credentials

## Toolchain

| Tool | Role |
|---|---|
| **KiCad 10** | Schematic, PCB, library editing; `kicad-cli` for exports and checks |
| **Claude Code** on the Mac, in `~/Dev` | The main way Claude works on DropOut hardware: direct file access, no network allowlist |
| **dropout-hardware-handbook** plugin (this repo) | Skills: `dropout-standards`, `find-part`, `new-board` |
| **kicad-happy** plugin | Distributor APIs (`digikey`, `mouser`, `element14`), design analysis (`kicad`, `bom`, `spice`, `emc`) |
| **Built-in browser** (Claude Code desktop app) | Sign-in-gated manufacturer and CAD sites; the user signs in once per site and the profile keeps it |
| **Claude in Chrome** | Fallback browser, using the user's own Chrome |
| **Homebrew** | Installs the command-line tools below |
| **gh** (GitHub CLI) | PRs, repo creation, CI status |
| **uv** | Python versions and virtual environments (kicad-library-tools needs Python 3.12 for CadQuery) |
| **poppler** | `pdftotext`, `pdftoppm`, `pdfdetach`, `pdfinfo`: reading datasheets, rendering drawings for review, extracting reference-manual attachments |
| **git-lfs** | Large files in the private `dropout-vendor-docs` repo |
| **d2**, **node** | Diagram rendering and the Astro/Starlight sites |
| **`~/.cache/dropout/klt-venv`** | Python 3.12 env with kicad-library-tools (+ CadQuery), pyyaml, openpyxl; built by the library's `scripts/setup_tools.sh` |
| **Library scripts** | `setup_tools.sh`, `distributor_lookup.py`, `generate_footprint.py`, `symbolgen.py`, `pintables/`, `check_pin_pad_match.py`, `klc_check.py` ([chapter 04](04-library.md)) |
| **qlmanage** (macOS) | Converts `kicad-cli` SVG exports to PNG so Claude can look at symbols and footprints |
| **kicad-library-tools** | Footprint and 3D generators, KLC checkers (pinned in the library repo) |
| **GitHub** + **Actions** | Repos, PRs, CI, releases, GitHub Pages |
| **Astro** | Library catalog site (`dropout-library-catalog`; Pagefind planned for search) |
| **Astro Starlight** | Architecture and board documentation sites ([chapter 08](08-architecture-documents.md)) |
| **D2** | System and block diagrams (text source, clickable blocks) |
| **Mermaid** | Sequence and state diagrams; diagrams in READMEs and PRs |
| **claude.ai project** "Automotive Power Distribution Unit KiCAD project" | Architecture discussions and documents; not the place for file work |

## Considered and rejected

| Tool | Decision |
|---|---|
| KiCAD-Prism | Reviewed by the user; not used. The catalog site is built with Astro. |
| kistack | Not used; DropOut writes its own skills. |
| Konnect (KiCad 10 MCP) | Used until 2026-10-28; removed from the toolchain. The user creates KiCad projects in KiCad. |
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
- **Passwords** are for the user. Claude never types a password into a sign-in form (Claude's own safety rules forbid it, whatever this handbook says). When a vendor site needs a sign-in, the user signs in once in the built-in browser; the sign-in persists.

Rules for Claude:
- Never print, log, echo, commit, or copy values from this file.
- Never `source` it; passwords contain shell metacharacters.
- New credentials: the user edits the file directly. Avoid pasting secrets into chat, where they stay in the conversation history.
- A new API key that a tool expects under a different variable name gets an alias in `vendor-env.sh`'s `EXPORTS` list, not a duplicate entry in the file.

## Setting up a new Mac

Everything Claude needs to work on DropOut hardware, in order. Claude can run each step except the ones marked **user** (accounts, passwords, secrets, app installs that need an admin password).

1. **user** Install the Claude desktop app and sign in; Claude Code runs in its Code tab.
2. **user** Install [Homebrew](https://brew.sh) (needs an admin password).
3. Command-line tools:
   ```bash
   brew install gh uv poppler git-lfs d2 node
   git lfs install
   ```
4. **user** Install KiCad 10 from https://www.kicad.org/download/macos/ (or `brew install --cask kicad`). `kicad-cli` is inside the app; scripts find it at `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`.
5. **user** `gh auth login` (GitHub account `karlTbowers`); set `git config --global user.name` / `user.email`.
6. Clone the repos into `~/Dev` (outside iCloud sync):
   ```bash
   mkdir -p ~/Dev && cd ~/Dev
   gh repo clone karlTbowers/dropout-hardware-handbook
   gh repo clone karlTbowers/dropout-kicad-library
   gh repo clone karlTbowers/dropout-library-catalog
   gh repo clone karlTbowers/dropout-vendor-docs        # private, Git LFS
   git clone --recursive https://github.com/karlTbowers/node60-hw.git
   ```
7. Claude Code plugins, from a `claude` terminal session:
   ```
   /plugin marketplace add karlTbowers/dropout-hardware-handbook
   /plugin install dropout-hardware@dropout
   /plugin marketplace add aklofas/kicad-happy
   /plugin install kicad-happy@kicad-happy
   ```
8. **user** Credentials: create `~/.local/share/dropout/vendor-logins` (mode 600) with the API keys and logins listed under [Credentials](#credentials), then add to `~/.zshrc`:
   ```bash
   eval "$("$HOME/Dev/dropout-kicad-library/scripts/vendor-env.sh")"
   ```
   Open a new shell (or restart the Claude app) so the keys are in the environment.
9. Library tools (Python 3.12 env, kicad-library-tools, CadQuery; a few minutes):
   ```bash
   ~/Dev/dropout-kicad-library/scripts/setup_tools.sh
   ```
10. **user** Vendor sign-ins: in the Claude app's built-in browser, sign in once to nxp.com, ti.com, ultralibrarian.com, snapeda.com, and newark.com.
11. Check it all:
    ```bash
    ~/Dev/dropout-kicad-library/scripts/setup_tools.sh --check
    python3 ~/Dev/dropout-kicad-library/scripts/distributor_lookup.py S32K344EHT1MMMST
    ~/.cache/dropout/klt-venv/bin/python ~/Dev/dropout-kicad-library/scripts/klc_check.py
    ```
