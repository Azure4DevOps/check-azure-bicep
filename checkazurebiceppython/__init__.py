#!/usr/bin/env python
import argparse
import glob
import subprocess
import sys


def az_bicep_build():
    parser = argparse.ArgumentParser()
    parser.add_argument('-noupgrade', action='store_true')
    args = parser.parse_args(['-noupgrade'])

    biceps_version = subprocess.run(
        ["az", "bicep", "version"], stdout=subprocess.PIPE, text=True, shell=True)
    if not args.noupgrade:
        biceps_version = subprocess.run(
            ["az", "bicep", "upgrade"], stdout=subprocess.PIPE, text=True, shell=True)
    # print(biceps_version.stdout)

    # print(glob.glob("./**/*.bicep", recursive=True))
    any_error = None
    for bicep_file in glob.glob("./**/*.bicep", recursive=True):
        result = subprocess.run(["az", "bicep", "build", "--stdout",
                                "--file", bicep_file], shell=True, capture_output=True)

        if result.stderr:
            print(result.stderr)
            any_error = True

    if any_error:
        sys.exit(25)


def az_bicep_format():
    parser = argparse.ArgumentParser()
    parser.add_argument('--noupgrade', action='store_true')
    args = parser.parse_args(['--noupgrade'])

    biceps_version = subprocess.run(
        ["az", "bicep", "version"], stdout=subprocess.PIPE, text=True, shell=True)
    if not args.noupgrade:
        biceps_version = subprocess.run(
            ["az", "bicep", "upgrade"], stdout=subprocess.PIPE, text=True, shell=True)
    # print(biceps_version.stdout)

    # print(glob.glob("./**/*.bicep", recursive=True))
    any_error = None
    for bicep_file in glob.glob("./**/*.bicep", recursive=True):
        result = subprocess.run(
            ["az", "bicep", "format", "--file", bicep_file], shell=False, capture_output=True)

        if result.stderr:
            print(result.stderr)
            any_error = True

    if any_error:
        sys.exit(25)
