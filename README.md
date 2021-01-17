# Actions-Ephem-Connect

A simple script for dynamically registering and starting GitHub Actions Self-Hosted Runners. 

## Prereqs:
The self-hosted runner proper must be downloaded and extracted on the build machine.

## To use:
run `export GITHUB_USERNAME=<your username>`

run `export GITHUB_PERSONAL_ACCESS_TOKEN=<Your PAT>`

update all fields in the config to align with your project.

run `python3 github_actions_ephem_connect.py`
