---
on:
  schedule: daily
  workflow_dispatch:

permissions:
  contents: read
  issues: read
  pull-requests: read

tools:
  github:
    mode: gh-proxy
    toolsets: [default]

safe-outputs:
  mentions: false
  allowed-github-references: []
  create-issue:
    title-prefix: "Daily Repository Activity Report:"
    labels: [report]
    close-older-issues: true
    expires: 14

---

# Daily repository activity report

Create a daily issue summarizing recent repository activity for the repository where this workflow runs.

## Reporting window

Use the last 24 full hours ending at workflow start time (UTC).

## Required content

Produce a concise report with these sections:

### Overview
- Total new issues opened in the window.
- Total pull requests merged in the window.
- Total open blockers currently present.

### New issues
- List each issue opened in the window with title, author, creation timestamp (UTC), and URL.
- If none, state that no new issues were opened.

### Merged pull requests
- List each pull request merged in the window with title, author, merger, merged timestamp (UTC), and URL.
- If none, state that no pull requests were merged.

### Open blockers
- Identify open blocker items by searching open issues and open pull requests for blocker indicators.
- Treat any item as a blocker if it has a label matching one of: `blocker`, `blocked`, `critical`, `sev1`, `priority:high`, or if the title starts with `BLOCKER:`.
- For each blocker, include type (issue or pull request), title, owner/assignee if available, age in days, and URL.
- If no blockers are found, state that none are currently open.

### References
- Include up to 3 relevant workflow or query URLs used for traceability.

## Guardrails

- Use only repository data available through GitHub tools.
- Do not create duplicate daily report issues; rely on the configured `close-older-issues` behavior.
- If there are no new issues, no merged pull requests, and no open blockers, call `noop` with: `No updates in last 24 full hours (<window_start_utc> to <window_end_utc>)`.
