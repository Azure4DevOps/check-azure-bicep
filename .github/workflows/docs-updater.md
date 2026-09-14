---
name: Documentation Drift Updater
description: Detect outdated documentation after recent code changes and open a draft PR with updates.
on:
  schedule:
    - cron: "17 3 * * *"
  workflow_dispatch:
  skip-if-match: 'is:pr is:open in:title "[docs] "'
permissions:
  contents: read
  issues: read
  pull-requests: read
  copilot-requests: write
strict: true
network:
  allowed: [defaults, github]
tools:
  github:
    mode: gh-proxy
    toolsets: [default]
safe-outputs:
  create-pull-request:
    title-prefix: "[docs] "
    draft: true
    protected-files: allowed
    allowed-files:
      - "*.md"
      - "**/*.md"
---

# Documentation Drift Updater

Review code changes merged in the last 24 hours and identify documentation that is now out of sync.

Prioritize updates to user-facing Markdown documentation such as:
- repository Markdown guides and examples
- Markdown files under `/.github/`

Update only documentation files needed to reflect current behavior, commands, configuration, and examples.

Create one draft pull request summarizing:
- Which documentation files were updated
- Which recent code changes required each update
- Any areas that still need human follow-up

If no documentation updates are needed, call `noop` with a short reason.
