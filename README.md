# GitHub-Actions-Self-Hosted-Runner-Connect

Dynamically register and start GitHub Actions Self-Hosted Runners for a single repository. 

## Prereqs:
The self-hosted runner proper must be downloaded and extracted on the build machine.

## To use:
Update all fields in the config to align with your project.

In the build env, 
set environment variable `GITHUB_USERNAME`
set environment variable `GITHUB_PERSONAL_ACCESS_TOKEN`

run `python3 runner_connect.py`
