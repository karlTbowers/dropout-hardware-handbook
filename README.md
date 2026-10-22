# DropOut Hardware Handbook

How DropOut designs open hardware: the process, the conventions, how parts are found and chosen, and the tools. It is also a **Claude Code plugin**, so Claude follows the same process on every DropOut device.

## Read it

Start with [handbook/00-overview.md](handbook/00-overview.md).

| # | Chapter |
|---|---|
| 00 | [Overview](handbook/00-overview.md): principles, repositories |
| 01 | [Design process](handbook/01-design-process.md): stages and gates |
| 02 | [Repositories and workflow](handbook/02-repositories.md) |
| 03 | [Part search and selection](handbook/03-part-search.md): APIs, web search, skills, MCPs |
| 04 | [Library](handbook/04-library.md) |
| 05 | [Schematic and PCB conventions](handbook/05-schematic-pcb.md) |
| 06 | [CI and releases](handbook/06-ci-releases.md) |
| 07 | [Tools and credentials](handbook/07-tools.md) |

## Install the Claude Code plugin

In Claude Code:

```
/plugin marketplace add karlTbowers/dropout-hardware-handbook
/plugin install dropout-hardware@dropout
```

Skills it provides:

| Skill | Use |
|---|---|
| `dropout-standards` | The handbook itself: Claude reads the relevant chapter for any DropOut hardware task |
| `find-part` | Find, compare, and select parts through the DigiKey, Mouser, and Newark APIs, with dated observations |
| `new-board` | Create a new `<board>-hw` repo from the board template |

It works alongside the **kicad-happy** plugin (distributor APIs, design analysis) and the library repo's own **`add-part`** skill.

## Layout

```
.claude-plugin/     plugin.json (version) and marketplace.json
handbook/           the chapters
skills/             Claude Code skills
templates/board/    files for a new board repo
CHANGELOG.md        every rule change, by plugin version
```

## Changing the handbook

Open a pull request. If it changes a rule, bump `version` in `.claude-plugin/plugin.json` and add a line to `CHANGELOG.md`. Board repos record the handbook version they follow.

## License

TBD — CC-BY-4.0 proposed for the handbook text.
