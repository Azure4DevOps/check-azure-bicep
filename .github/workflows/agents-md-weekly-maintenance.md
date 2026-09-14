---
name: Weekly AGENTS.md Maintenance
description: Weekly maintenance of AGENTS.md from merged pull requests and source updates.
intent: Keep AGENTS.md accurate by reviewing merged pull requests and source file updates since the previous successful run, then propose only necessary AGENTS.md updates.
on:
  schedule:
    - cron: "0 9 * * 1"
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
  actions: read
  copilot-requests: write
tools:
  github:
    mode: gh-proxy
    toolsets: [default, actions]
safe-outputs:
  create-pull-request:
    title-prefix: "[agents-md] "
    draft: true
    close-older-pull-requests: true
    allowed-files:
      - "AGENTS.md"
---

# Weekly AGENTS.md Maintenance

## Task

Update the repository's `AGENTS.md` so it reflects current contributor guidance.

1. Determine the current workflow run timestamp and identify the previous successful run of this workflow.
2. Build the review window from the previous successful run to now.
3. Review merged pull requests in that window and capture guidance-impacting changes.
4. Review source file changes in that window and capture additional guidance-impacting changes.
5. Update `AGENTS.md` only when there are concrete, repository-relevant guidance changes supported by that evidence.
6. Keep updates concise, accurate, and aligned with existing repository conventions.

## Safe Outputs

- Use `create-pull-request` only when `AGENTS.md` needs updates.
- Use `noop` with a short reason when no AGENTS.md changes are required.
