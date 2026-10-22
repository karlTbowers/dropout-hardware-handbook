# DropOut Hardware Handbook — instructions for Claude

This repo is DropOut's hardware design handbook **and** the `dropout-hardware` Claude Code plugin (marketplace `dropout`). It is **public**.

## When editing it

- The handbook is the rulebook for every DropOut device. Rule changes need the user's agreement; propose them, don't decide them.
- Any change that alters a rule: bump `version` in `.claude-plugin/plugin.json` (semver: patch = wording, minor = new or changed rule, major = restructure) and add a `CHANGELOG.md` entry.
- Keep chapters factual and short. Record decisions with their reason and date; record rejected alternatives.
- Part-level library rules belong in `dropout-kicad-library` (`docs/CONTRIBUTING.md`, `klc-exceptions.yml`, `add-part` skill). Chapter 04 only summarizes and links them; don't duplicate them.
- Skills reference handbook chapters by path relative to the skill's base directory (`../../handbook/...`) so they work wherever the plugin is installed.
- `templates/board/` is copied into new board repos by the `new-board` skill. Its `CLAUDE.md` is stored as `CLAUDE.md.template` on purpose. Placeholders: `{{BOARD}}`, `{{BOARD_TITLE}}`, `{{DESCRIPTION}}`, `{{HANDBOOK_VERSION}}`, `{{DATE}}`.
- Never put credentials or anything from `~/.local/share/dropout/vendor-logins` in this repo.
- After changing plugin files, validate the plugin with Claude Code's plugin validation (`claude plugin validate .`) if available.
