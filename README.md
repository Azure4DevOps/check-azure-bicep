[![Build Status](https://dev.azure.com/Azure4DevOps/Azure4DevOps/_apis/build/status/Azure4DevOps.check-azure-bicep-ci?branchName=master)](https://dev.azure.com/Azure4DevOps/Azure4DevOps/_build/latest?definitionId=2&branchName=master)
[![CI](https://github.com/Azure4DevOps/check-azure-bicep/actions/workflows/github-action-ci.yml/badge.svg)](https://github.com/Azure4DevOps/check-azure-bicep/actions/workflows/github-action-ci.yml)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/Azure4DevOps/check-azure-bicep)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Azure4DevOps/check-azure-bicep?include_prereleases)

# check-azure-bicep

[Pre-commit](https://pre-commit.com/) hooks for [Azure Bicep](https://github.com/Azure/bicep) validation,
with built-in support for GitHub Workflows, Azure Pipelines, and more! Enabling [shift left](https://devopedia.org/shift-left) approach for [Azure Bicep](https://github.com/Azure/bicep) infrastructure as code.

## About

This repository provide one hook to use with [pre-commit](https://pre-commit.com/) that validate bicep files: it will call `az bicep build`.

It requires the `az bicep` toolchain installed, and uses [`az bicep`](https://github.com/Azure/bicep) under the hood.

## Demo

Example usage of `pre-commit run --all-files` and
`git commit` after hook innstall in git repository `pre-commit install`

![alt text](https://raw.githubusercontent.com/Azure4DevOps/check-azure-bicep.example/master/example.gif)

### Azure Bicep Install

To install `az bicep` use [install](https://docs.microsoft.com/pl-pl/azure/azure-resource-manager/bicep/install) or [install](https://github.com/Azure/bicep) or `az bicep install` for Azure cli.

### Pre-commit Install

Before you can run hooks, you need to have the pre-commit package manager installed. Using pip:

```pip
pip install pre-commit
```

## Example usage

Add a snippet to your `.pre-commit-config.yaml` file in root of repository.

```yaml
- repo: https://github.com/Azure4DevOps/check-azure-bicep
  rev: v0.1.4 # ${LATEST_SHA_OR_VERSION}
  hooks:
    - id: check-azure-bicep
```

## Example local run

run `pre-commit install` to set up the git hook scripts in your git repository # scan all modyfied miles before making commint (git hooks)
or
run `pre-commit run --all-files` # scanning all files

at result all bicep files will or modified will be validated doing `az bicep build`

## Example Azure Pipelines usage `azure-pipelines-ci.yml`

```yaml
pool:
  vmImage: "ubuntu-latest"
steps:
  - script: |
      pip install pre-commit
      pre-commit --version
      pre-commit run --all-files
    displayName: Execute pre-commit
```

## Example Github Workflow usage `github-action-ci.yml`

```yaml
build:
  runs-on: ubuntu-latest
  steps:
    - name: Execute pre-commit
      run: |
        pip install pre-commit
        pre-commit --version
        pre-commit run --all-files
```
