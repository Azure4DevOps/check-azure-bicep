[![Build Status](https://dev.azure.com/Azure4DevOps/Azure4DevOps/_apis/build/status/Azure4DevOps.check-azure-bicep-ci?branchName=master)](https://dev.azure.com/Azure4DevOps/Azure4DevOps/_build/latest?definitionId=2&branchName=master)
[![CI](https://github.com/Azure4DevOps/check-azure-bicep/actions/workflows/github-action-ci.yml/badge.svg)](https://github.com/Azure4DevOps/check-azure-bicep/actions/workflows/github-action-ci.yml)

# check-azure-bicep
[Pre-commit](https://pre-commit.com/) hooks for [Azure Bicep](https://github.com/Azure/bicep) validation,
with built-in support for GitHub Workflows, Azure Pipelines, and more! Enbaling [shift left](https://devopedia.org/shift-left) aproach for [Azure Bicep](https://github.com/Azure/bicep) infrastructure as code. 

## About

This repository provide one hook to use with [pre-commit](https://pre-commit.com/) that validate bicep files: it will call `az bicep build`.

It requires the `az bicep` toolchain installed, and uses [`az bicep`](https://github.com/Azure/bicep) under the hood.

### Azure Bicep Install
To install `az bicep` use [install](https://docs.microsoft.com/pl-pl/azure/azure-resource-manager/bicep/install) or [install](https://github.com/Azure/bicep) or `az bicep install` for Azure cli.

### Pre-commit Install
Before you can run hooks, you need to have the pre-commit package manager installed. Using pip:
```
pip install pre-commit
```
## Example usage

Add a snippet to your `.pre-commit-config.yaml` file in root of repository.

```yaml
- repo: https://github.com/Azure4DevOps/check-azure-bicep
  rev: 0.2.0 # ${LATEST_SHA_OR_VERSION}
  hooks:
    - id: check-azure-bicep
```
## 
run `pre-commit install` to set up the git hook scripts in your git repository # scan all modyfied miles before making commint (git hooks)
or
run `pre-commit run --all-files` # scaning all fiels

at result all bicep files will or modyfied will be validated doing `az bicep build`





