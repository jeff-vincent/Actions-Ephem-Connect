import configparser
import json
import os
import requests
import subprocess

CONFIG = configparser.ConfigParser()
CONFIG.read('github_actions_ephem_connect.cfg')

GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
GITHUB_PERSONAL_ACCESS_TOKEN = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')

GITHUB_REPO_NAME = CONFIG['repo']['name']
PATH_TO_RUNNER = CONFIG['runner']['path']


class GitHubActionsEphemConnect:
    def __init__(self):
        self.api_base_url = CONFIG['github']['api_base_url']
        self.gh_session = requests.Session()
        self.gh_session.auth = (GITHUB_USERNAME, GITHUB_PERSONAL_ACCESS_TOKEN)
        self.headers = {'Accept':'application/vnd.github.v3+json'}
        self.token = None


    def _build_get_token_request_url(self):
        return f"{self.api_base_url}repos/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}/actions/runners/registration-token"


    def generate_token(self):
        url = self._build_get_token_request_url()
        response = self.gh_session.post(url, headers=self.headers)
        response = json.loads(response._content)
        print(response['token'])
        self.token = response['token']


    def register_runner(self):
        repo_path = CONFIG['repo']['path']
        labels = CONFIG['runner']['labels']
        name = CONFIG['runner']['name']
        runner_path = PATH_TO_RUNNER
        config_path = os.path.join(runner_path, 'config.sh')
        cmd = [config_path, '--url', repo_path, '--token', self.token, '--name', name, '--work', '_work', '--labels', labels]
        response = subprocess.run(cmd, capture_output=True)
        print(response)


    def start_runner(self):
        runner_path = PATH_TO_RUNNER
        start_path = os.path.join(runner_path, 'run.sh')
        response = subprocess.run(start_path, capture_output=True)
        print(response)


if __name__ == '__main__':
    ephem_connect = GitHubActionsEphemConnect()
    ephem_connect.generate_token()
    ephem_connect.register_runner()
    ephem_connect.start_runner()
