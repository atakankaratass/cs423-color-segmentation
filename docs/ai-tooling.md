# AI Tooling Setup

This repository supports multiple AI tools, but all of them must follow the same repository rules.

No AI tool may skip this document at the start of a task.

## Shared Rule Files

- `CONTRIBUTING.md`: human and team workflow policy
- `AGENTS.md`: mandatory AI-agent operating rules
- `CLAUDE.md`: Claude-specific entry instructions
- `.cursor/rules/project-rules.mdc`: Cursor-specific entry instructions

## OpenCode Superpowers

This repository includes a project-level `opencode.json` with the shared `superpowers` plugin:

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"]
}
```

That means OpenCode users working from this repository should automatically pick up the plugin without doing a separate global-only install.

Recommended OpenCode skills for this project:

- `writing-plans`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`

## Mandatory AI Workflow For All Tools

The workflow below is mandatory even for tools that cannot load the OpenCode plugin directly.

1. Read `CONTRIBUTING.md`, `AGENTS.md`, and this file first.
2. Inspect repository state before editing.
3. Search before broad reading.
4. Add or update tests before changing behavior.
5. Make the smallest correct change.
6. Run the required local validation suite.
7. Report results truthfully.

This means Cursor, Claude Code, Gemini, Copilot, and any other AI assistant must behave as if the `superpowers` workflow is active, even when the plugin itself is unavailable.

## Husky and Lint-Staged

- `husky` manages local git hooks.
- `pre-commit` runs `lint-staged` for fast checks on staged files only.
- `pre-push` runs the full validation suite.

This means contributors get:

1. fast formatting and staged-file cleanup before commit
2. strict full validation before push

Important:

- `git commit` does not currently run the full test suite.
- `git push` does run the full validation gate through the `pre-push` hook.
- GitHub Actions reruns the same categories in CI.

## GitHub Actions

The repository CI workflow mirrors the local validation suite.

Local validation remains mandatory. GitHub Actions is the second gate, not the first one.

## Current Implementation Scope

The repository now contains a small but real baseline implementation:

- RGB thresholding pipeline
- HSV thresholding pipeline
- binary morphology cleanup
- connected-component counting
- dataset evaluation CLI
- versioned profile loading
- structured dataset metadata with scene labels
- bundled sample dataset for reproducible smoke tests

This baseline is intentionally small so the team can extend it safely during the project.
