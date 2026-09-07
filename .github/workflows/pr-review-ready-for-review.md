---
name: pr-review
description: Review pull requests for quality and issues
intent: Ensure each ready-for-review pull request gets an evidence-based quality review, including dependency release-note coverage and page availability checks.
on:
  pull_request:
    types: [ready_for_review]
permissions:
  contents: read
  issues: read
  pull-requests: read
  copilot-requests: write
engine: copilot
tools:
  github:
    mode: gh-proxy
    toolsets: [repos, issues, pull_requests]
    min-integrity: approved
  web-fetch: true
safe-outputs:
  add-comment:
    max: 1
timeout-minutes: 30
evals:
  - id: operational_value
    question: Does the agent output provide one evidence-based PR review that verifies dependency update release-note coverage and page/link health, including owner notification guidance when a page check fails?
  - id: dependency_release_notes_check
    question: Does the agent output explicitly state whether dependency or GitHub Actions version changes were detected and whether release-note updates are needed?
  - id: page_health_verification
    question: Does the agent output show that changed public pages or links were checked for reachability and report concrete pass or fail outcomes?
  - id: scoped_quality_findings
    question: Does the agent output report only actionable findings supported by evidence from the PR diff and avoid speculative or unrelated comments?
  - id: noop_when_clean
    question: If no actionable issues are found, does the agent output call noop with a brief reason instead of posting a comment?
---

# PR review for check-azure-bicep

Review the pull request that triggered this workflow (`ready_for_review`) for quality and actionable issues.

## Repository context

- Project purpose: pre-commit hooks that validate and format Azure Bicep files using Azure CLI (`az bicep`).
- Main implementation areas: Python packaging (`setup.py`, `requirements.txt`, `checkazurebiceppython/`) and PowerShell hook scripts (`az_bicep_build.ps1`, `az_bicep_format.ps1`).
- CI conventions: GitHub Actions CI runs `pre-commit run --all-files`; CodeQL is configured for Python; Dependabot updates GitHub Actions daily.
- Owner reference from CODEOWNERS: `@JanuszNowak`.

## What to review

1. Check code quality risks in changed files, focusing on correctness, security, maintainability, and CI compatibility for this repository.
2. Validate dependency-update intent:
   - Detect dependency version changes in files like `requirements.txt`, `setup.py`, `.pre-commit-config.yaml`, `.github/dependabot.yml`, or `.github/workflows/*.yml`.
   - Confirm the PR includes a clear release-note/release-impact note (PR description or updated release-note documentation such as README/release-related docs).
3. Validate page-health intent:
   - If the PR changes public URLs in docs/workflow metadata (README, markdown docs, badges, links), check those changed URLs with `web-fetch`.
   - Mark link/page checks as passed or failed with evidence.
   - If a page/link check fails, include a clear owner notification request in the review comment and mention `@JanuszNowak`.

## Output policy

- Use `add-comment` only when there is at least one actionable, evidence-backed finding.
- Use `noop` with a short reason when there are no actionable findings or insufficient evidence.
- Keep output concise: summary, findings, and required next actions only.

## DO NOT constraints

- DO NOT comment on style-only preferences unless they create functional or security risk.
- DO NOT report issues without quoting concrete evidence from the PR diff, metadata, or link check result.
- DO NOT invent missing release notes when dependency-related files were not changed.
- DO NOT run destructive, write, or merge actions; this workflow is review-only.
- DO NOT post multiple comments for the same run.
