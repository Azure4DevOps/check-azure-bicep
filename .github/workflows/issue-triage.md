---
emoji: "🧭"
description: Triage newly opened issues by classifying, prioritizing, de-duplicating, and routing them.
intent: Classify each new issue, request clarification when needed, close true duplicates, and route actionable issues to the repository owner.
on:
  issues:
    types: [opened]
  roles: all
permissions:
  contents: read
  issues: read
  copilot-requests: write
strict: true
tools:
  bash: [cat, jq, grep, head, sed, wc]
steps:
  - name: Prefetch triage context
    run: |
      mkdir -p /tmp/gh-aw/data
      ISSUE_NUMBER="${{ github.event.issue.number }}"
      REPO="${{ github.repository }}"
      gh issue view "$ISSUE_NUMBER" --repo "$REPO" --json number,title,body,author,labels,assignees,url,createdAt,updatedAt > /tmp/gh-aw/data/trigger-issue.json
      gh issue list --repo "$REPO" --state open --limit 50 --json number,title,body,author,labels,assignees,url,createdAt,updatedAt \
        | jq --argjson issue_number "$ISSUE_NUMBER" '[.[] | select(.number != $issue_number) | {number,title,body,author:(.author.login // .author.name // ""),labels:[.labels[].name],assignees:[.assignees[].login],url,createdAt,updatedAt}]' \
        > /tmp/gh-aw/data/open-issues.json
      gh label list --repo "$REPO" --json name,description > /tmp/gh-aw/data/labels.json
      gh api "repos/$REPO/collaborators?per_page=100" | jq '[.[] | {login, permissions}]' > /tmp/gh-aw/data/collaborators.json
safe-outputs:
  allowed-github-references: [repo]
  noop:
    report-as-issue: false
  add-labels:
    allowed: [bug, enhancement, documentation, question, duplicate]
    pull-requests: false
    max: 2
  set-issue-type:
    allowed: [Bug, Feature, Task]
    max: 1
  set-issue-field:
    allowed-fields: [Priority]
    max: 1
  add-comment:
    hide-older-comments: true
    pull-requests: false
    max: 1
  assign-to-user:
    allowed: [JanuszNowak]
    max: 1
  close-issue:
    state-reason: [duplicate]
    max: 1
---

# Issue Triage

## Task

Objective: triage each newly opened issue in `${{ github.repository }}`.

Read these pre-fetched files before taking any action:

- `/tmp/gh-aw/data/trigger-issue.json`
- `/tmp/gh-aw/data/open-issues.json`
- `/tmp/gh-aw/data/labels.json`
- `/tmp/gh-aw/data/collaborators.json`

Use the safe outputs only. Do not use direct GitHub write permissions or shell commands to mutate GitHub state.

## Triage policy

For the triggering issue:

1. Set exactly one issue type:
   - `Bug` for broken behavior, regressions, errors, or failed validation
   - `Feature` for net-new capabilities or requested functionality
   - `Task` for maintenance, refactoring, housekeeping, or documentation work
2. Add the best matching label:
   - `bug` for `Bug`
   - `enhancement` for `Feature` or non-documentation `Task`
   - `documentation` for docs, README, examples, or usage guidance
   - `question` only when the issue is mainly a question or the report is too incomplete to classify confidently
3. Set the `Priority` field to one of `Urgent`, `High`, `Medium`, or `Low`.
   - `Urgent`: blocks releases, breaks the primary hook, or describes a security or data-loss risk
   - `High`: clear bug or high-value request with immediate user impact
   - `Medium`: actionable but not blocking
   - `Low`: minor improvement, polish, or low-confidence request
4. Detect duplicates by comparing the triggering issue with `/tmp/gh-aw/data/open-issues.json`. Only treat an issue as a duplicate when the underlying problem or requested outcome materially overlaps and another open issue is the better canonical tracker.

## Required actions

- If the issue is a true duplicate:
  - add the `duplicate` label
  - post a short comment that links to the canonical issue and explains the overlap
  - close the triggering issue as a duplicate of that canonical issue
- If the issue lacks the information needed to triage confidently:
  - add the `question` label
  - post a short comment asking only the minimum clarifying questions needed to continue
  - do not assign it
  - do not close it
- If the issue is actionable and not a duplicate:
  - assign it to `JanuszNowak`
  - post a short triage summary that includes the chosen issue type, label, priority, and why it was routed there

## Guardrails

- Keep comments concise, specific, and actionable.
- Prefer the existing issue templates: missing reproduction details strongly suggests a clarifying question for likely bugs; missing desired outcome strongly suggests a clarifying question for likely features.
- Do not call something a duplicate based on one shared keyword alone.
- Do not add more than one type label unless `duplicate` is also required.
- If the issue is already clearly triaged or there is not enough evidence to act safely, call `noop` with a short reason.
