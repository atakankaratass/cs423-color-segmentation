# Agent Protocol

This document defines mandatory repository behavior for all AI agents working on this project.

Read this file and `CONTRIBUTING.md` before making changes.

Agents must also follow the repository AI workflow described in `docs/ai-tooling.md`.

## 1. Scope

These rules apply to all AI agents and AI-assisted editors, including OpenCode, Claude Code, Cursor, Gemini, Copilot, and similar systems.

## 2. Non-Negotiable Rules

- Before any coding, planning, debugging, or refactoring work, read `CONTRIBUTING.md`, `AGENTS.md`, and `docs/ai-tooling.md`.
- Do not start editing before examining the repository state.
- Do not assume architecture, commands, or file locations without checking.
- Do not bypass validation gates.
- Do not weaken lint, test, or CI rules to make failures disappear.
- Do not fabricate outputs, metrics, counts, screenshots, or test results.
- Do not mark work complete before validation actually passes.
- Do not rewrite unrelated files as a side effect of the task.
- Do not modify or revert user work you did not create unless explicitly instructed.

## 3. Exploration First

Before changing code:

1. Inspect the relevant files and repository structure.
2. Search before broad reading when possible.
3. Read only the files needed for the task.
4. Understand existing conventions before introducing new ones.

Preferred search/navigation order:

1. `rg` / repository search
2. `sg` / `ast-grep` for structural search and rewrite when applicable
3. LSP-based symbol navigation when available
4. targeted file reads

## 3.1 Mandatory AI Workflow

All AI tools, whether or not they support the OpenCode `superpowers` plugin directly, must follow the equivalent workflow below.

1. Read repository rules before acting.
2. Inspect the relevant code and current state.
3. Write or update tests first when behavior changes.
4. Make the smallest correct implementation change.
5. Validate locally before claiming success.
6. Report results truthfully.

OpenCode users should use `superpowers` skills directly when available. Cursor, Claude Code, and other AI tools must still follow the same workflow even if they cannot load the plugin itself.

## 4. Editing Rules

- Make the smallest correct change.
- Preserve existing naming and structure unless change is justified.
- Avoid adding abstractions unless reuse or complexity clearly requires them.
- Keep behavior explicit and reviewable.
- Do not add compatibility layers unless there is a real compatibility requirement.
- Add brief comments only where code would otherwise be hard to parse.

## 5. Testing Rules

If behavior changes, tests must change too.

Required agent behavior:

1. Add or update a failing test first when fixing a bug.
2. Add or update tests when introducing a feature.
3. Run the required local validation suite before claiming success.
4. Report validation truthfully, including failures and limitations.

Minimum test expectations for this project:

- unit tests for reusable image-processing helpers
- integration tests for RGB and HSV pipelines
- smoke tests for end-to-end sample execution
- regression tests for fixed bugs

## 6. Reproducibility Rules

- Do not claim experiment improvements without reproducible commands.
- Do not hand-edit result tables that should be produced by code.
- Keep output paths stable and documented.
- If a change affects metrics, counts, masks, thresholds, or runtime, state that clearly.

## 7. Git and PR Rules

- Never commit unless explicitly asked.
- Never push unless explicitly asked.
- Never open or update a PR until required local validation passes.
- Never suggest that CI can replace local validation.
- Keep branches focused on one logical task.

## 8. Tooling Safety Rules

- Never use `--no-verify`.
- Never add ignore directives just to silence real failures.
- Never lower coverage or lint standards to get green checks.
- Never replace missing validation with verbal assurance.
- Never hide failing tests by skipping or deleting them without explicit approval and justification.

## 9. Documentation Duties

Update docs when any of the following change:

- repository commands
- project structure
- experiment workflow
- output locations
- validation steps
- contributor expectations

## 10. Completion Standard

An agent may only present work as complete if:

1. Implementation is done.
2. Relevant tests were added or updated.
3. Required local validation ran successfully.
4. Any important caveats are explicitly stated.

If any of those are missing, say so directly.
