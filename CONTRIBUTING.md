# Contributing to CS423 Color Segmentation Project

This repository is the team's single working source of truth for the CS423/523 Computer Vision project.

All human contributors and all AI tools must follow these rules strictly. These rules are intentionally conservative because the project will be developed collaboratively and every result must remain reproducible, reviewable, and safe to merge.

## 1. Core Policy

- No direct pushes to `main`.
- No work is considered complete until required local validation passes.
- No Pull Request may be opened, updated, or merged unless all required GitHub Actions checks pass.
- No contributor may bypass validation gates using `--no-verify`, disabled hooks, ignored failures, or weakened lint/test rules.
- No contributor may silently rewrite or delete another person's work without explicit agreement.
- No contributor may claim an experiment result unless it can be reproduced from the repository.

## 2. Branching Strategy

- `main` is the protected release branch.
- All work must happen on short-lived feature branches.
- Branch naming should use one of these prefixes:
  - `feature/...`
  - `fix/...`
  - `refactor/...`
  - `docs/...`
  - `test/...`
  - `chore/...`
- One branch should address one logical task only.

## 3. Required Workflow

Every change must follow this order:

1. Understand the existing repository state before editing.
2. Define or update the relevant test cases first when behavior changes.
3. Implement the smallest correct change.
4. Run the full required local validation suite.
5. Open or update a Pull Request only after local validation is green.
6. Merge only after GitHub Actions is green.

## 4. Quality Philosophy

- Untested behavioral changes are not allowed.
- Incomplete validation is treated as failure.
- Broken `main` is unacceptable.
- Fast local iteration is good; skipping safety checks is not.
- Reproducibility matters as much as correctness.

## 5. Local Validation Requirements

Before every push intended for review, the contributor must run the repository validation suite locally.

Until project tooling is finalized, the expected validation categories are:

1. Formatting check
2. Lint check
3. Unit/integration tests
4. Smoke test on at least one sample image or dataset slice
5. Build/package validation if the repository adds a build step

When repository scripts are added, the minimum standard command set should be:

- `make install-dev`
- `make format-check`
- `make lint`
- `make test`
- `make smoke-test`
- `make validate-pr`

If a `Makefile` is not yet present, the equivalent project-native commands must be used instead.

## 5.1 Development Setup

- Install Python 3.9 or newer.
- Run `make install-dev` before starting development.
- Do not commit without hooks installed and working.
- If you use OpenCode, this repository includes a project-level `opencode.json` so the shared `superpowers` plugin is discovered automatically.

## 6. Pull Request Rules

- Every code change must come through a Pull Request.
- PRs must be small enough to review carefully.
- PRs must describe:
  - what changed
  - why it changed
  - what was validated locally
  - any dataset, threshold, metric, or experiment impact
- PRs must not mix unrelated work.
- PR authors must list exact validation commands run.
- PRs must be up to date with the base branch before merge.
- If GitHub Actions is red, the PR is not ready.

## 7. Mandatory Tests

The following expectations apply whenever the repository contains the relevant code.

### 7.1 Unit Tests

Required for:

- color space conversion helpers
- threshold selection helpers
- morphology utilities
- contour or connected-component counting utilities
- metric calculation code
- file/metadata parsing

### 7.2 Integration Tests

Required for:

- full RGB pipeline on representative sample input
- full HSV pipeline on representative sample input
- batch evaluation flow that reads metadata and produces metrics

### 7.3 Smoke Tests

Required for:

- running the main pipeline entrypoint against a known sample image
- verifying that output artifacts are written to expected paths
- verifying that the process exits successfully

### 7.4 Regression Tests

Required when fixing a bug. The failing scenario must be captured by a test first, then fixed.

## 8. Experiment and Data Rules

- Raw data must remain unchanged once committed unless the team agrees on a replacement.
- Metadata files must be version-controlled.
- Ground-truth counts must be reviewable and traceable.
- Any change that affects thresholds, masks, counts, or metrics must document the reason.
- Results used in the report must be reproducible from repository scripts, not manual notebook-only execution.
- Generated outputs should go to stable, documented directories.

## 9. Commit Standards

- Use atomic commits.
- Use Conventional Commits.
- Valid prefixes include:
  - `feat:`
  - `fix:`
  - `refactor:`
  - `test:`
  - `docs:`
  - `chore:`
- Commit messages must explain the purpose of the change, not just the files touched.

## 10. Prohibited Shortcuts

The following are forbidden unless explicitly approved by the team in writing:

- `--no-verify`
- disabling git hooks
- weakening lint rules to make failing code pass
- weakening test thresholds to make failing code pass
- deleting tests to unblock a merge
- committing broken generated outputs to hide failures
- force-pushing shared branches without team agreement
- editing results tables manually when they should be script-generated
- claiming a bug is fixed without a reproducer and validation

## 11. AI Tool Policy

These rules apply equally to human contributors and AI assistants used through OpenCode, Claude Code, Cursor, Gemini, Copilot, or any other tool.

- AI-generated code is not trusted by default.
- AI-generated changes must be reviewed like any other contribution.
- AI tools must follow repository docs before making edits.
- AI tools must not bypass tests, hooks, lint, or review.
- AI tools must prefer minimal, targeted changes over speculative rewrites.
- AI tools must not invent experimental results, metrics, or dataset facts.
- AI tools must not fabricate successful validation.

## 12. Documentation Rules

- Keep operational rules in this file and `AGENTS.md`.
- Avoid duplicating the same rule text in multiple files.
- Tool-specific files should point back to the authoritative documents.
- Update documentation when behavior, structure, or commands change.

## 13. Repository Protection Settings

When the GitHub repository is created, configure these protections immediately:

1. Protect `main`.
2. Disable direct pushes to `main`.
3. Require Pull Requests before merging.
4. Require at least one approval before merge.
5. Require status checks to pass before merge.
6. Require branches to be up to date before merge.
7. Dismiss stale approvals when new commits are pushed.
8. Disable force pushes to protected branches.
9. Disable branch deletion for protected branches.

## 14. Definition of Done

A task is done only if all of the following are true:

1. The change is implemented.
2. Required tests exist and pass.
3. Local validation is green.
4. Documentation is updated if needed.
5. The Pull Request clearly explains the change.
6. GitHub Actions is green.
7. Review feedback is resolved.

Failure to follow these rules should block merge approval.
