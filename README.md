# check-azure-bicep

[![Build Status](https://dev.azure.com/Azure4DevOps/Azure4DevOps/_apis/build/status/Azure4DevOps.check-azure-bicep-ci?branchName=master)](https://dev.azure.com/Azure4DevOps/Azure4DevOps/_build/latest?definitionId=2&branchName=master)

[![CI](https://github.com/Azure4DevOps/check-azure-bicep/actions/workflows/github-action-ci.yml/badge.svg)](https://github.com/Azure4DevOps/check-azure-bicep/actions/workflows/github-action-ci.yml)

pre-commit hooks for azure bicep validation,
with built-in support for GitHub Workflows, Renovate, Azure Pipelines, and more!

## About

asd
This repo provide one hook to use with [pre-commit](https://pre-commit.com/) that validate bicep files: it will call az bicep build.

⚠️ It requires the `az bicep` toolchain installed, and uses [`az bicep`](https://github.com/Azure/bicep) under the hood.

To install `az bicep`, head to <https://docs.microsoft.com/pl-pl/azure/azure-resource-manager/bicep/install> or <https://github.com/Azure/bicep> and do it.

## Example usage

Then: add a similar snippet to your `.pre-commit-config.yaml` file

```yaml
- repo: https://github.com/JanuszNowak/check-azure-bicep
  rev: ${LATEST_SHA_OR_VERSION}
  hooks:
    - id: check-azure-bicep
```

Optionally, you can

```yaml
- repo: https://github.com/JanuszNowak/check-azure-bicep
  rev: ${LATEST_SHA_OR_VERSION}
  hooks:
    - id: check-azure-bicep
      args: [--arg]
```
