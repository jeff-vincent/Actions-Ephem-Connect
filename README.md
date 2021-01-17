# GitHub-Actions-Self-Hosted-Runner-Connect

A simple script for dynamically registering and starting GitHub Actions Self-Hosted Runners for a single repository. 

## Prereqs:
The self-hosted runner proper must be downloaded and extracted on the build machine.

## To use:
Update all fields in the config to align with your project.

In the build env, 
set environment variable `GITHUB_USERNAME`
set environment variable `GITHUB_PERSONAL_ACCESS_TOKEN`

run `python3 github_actions_ephem_connect.py`
