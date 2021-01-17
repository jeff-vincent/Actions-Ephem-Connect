import configparser
import json
import os
import requests
from subprocess import Popen
from subprocess import PIPE

CONFIG = configparser.ConfigParser()
CONFIG.read('github_actions_ephem_connect.cfg')

GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
GITHUB_PERSONAL_ACCESS_TOKEN = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')

GITHUB_REPO_NAME = 'iOS-Example'
PATH_TO_RUNNER = '~/actions-runner/'


class GitHubActionsEphemConnect:
    def __init__(self):
        self.base_url = CONFIG['urls']['base_url']
        self.gh_session = requests.Session()
        self.gh_session.auth = (GITHUB_USERNAME, GITHUB_PERSONAL_ACCESS_TOKEN)
        self.headers = {'Accept':'application/vnd.github.v3+json'}
        self.token = None


    def _build_get_token_request_url(self):
        return f"{self.base_url}repos/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}/actions/runners/registration-token"


    def generate_token(self):
        url = self._build_get_token_request_url()
        response = self.gh_session.post(url, headers=self.headers)
        response = json.loads(response._content)
        print(response['token'])
        self.token = response['token']


    def register_runner(self):
        cmd = ['./config.sh', '--url', 'https://github.com/jeff-vincent/iOS-Example', '--token', self.token, '--name', 'test', '--work', '_work']
        p = Popen(cmd)
        response = p.communicate(input=b'\n')
        print(response)


ephem_connect = GitHubActionsEphemConnect()
ephem_connect.generate_token()
ephem_connect.register_runner()