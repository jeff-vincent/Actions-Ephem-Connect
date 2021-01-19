import configparser
import json
import logging
import os
from pathlib import Path
import random
import requests
import string
import subprocess
import tarfile


logging.basicConfig(filename='runner-connect.log', level=logging.DEBUG)
CONFIG = configparser.ConfigParser()
CONFIG.read('runner_connect.cfg')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
GITHUB_PERSONAL_ACCESS_TOKEN = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKEN')
GITHUB_REPO_NAME = CONFIG['repo']['name']
PATH_TO_RUNNER = CONFIG['runner']['path']

class GitHubActionsRunnerConnect:
    def __init__(self):
        self.api_base_url = CONFIG['github']['api_base_url']
        self.gh_session = requests.Session()
        self.gh_session.auth = (GITHUB_USERNAME, GITHUB_PERSONAL_ACCESS_TOKEN)
        self.headers = {'Accept':'application/vnd.github.v3+json'}
        self.token = None

    def check_for_runner(self):
        Path(PATH_TO_RUNNER).mkdir(parents=True, exist_ok=True)
        runner_installed = False
        if 'bin' in os.listdir(PATH_TO_RUNNER):
            runner_installed = True
        return runner_installed

    def install_runner(self):
        download_url = CONFIG['github']['runner_download_url']
        filename = CONFIG['github']['download_name']
        filepath = os.path.join(PATH_TO_RUNNER, filename)
        r = requests.get(download_url, allow_redirects=True)
        with open(filepath, 'wb') as download:
            download.write(r.content)
        tar = tarfile.open(filepath)
        tar.extractall(PATH_TO_RUNNER)

    def _build_get_token_request_url(self):
        try:
            return f"{self.api_base_url}repos/{GITHUB_USERNAME}/{GITHUB_REPO_NAME}/actions/runners/registration-token"
        except Exception as e:
            logging.error(str(e))

    def generate_token(self):
        try:
            url = self._build_get_token_request_url()
            response = self.gh_session.post(url, headers=self.headers)
            response = json.loads(response._content)
            self.token = response['token']
            log = f"Token created: {self.token}"
            logging.info(log)
        except Exception as e:
            logging.error(str(e))

    def _create_runner_name(self):
        letters = string.ascii_lowercase
        prefix = CONFIG['runner']['name']
        suffix = ''.join(random.choice(letters) for i in range(10))
        return f"{prefix}-{suffix}"

    def register_runner(self):
        try:
            repo_path = CONFIG['repo']['path']
            labels = CONFIG['runner']['labels']
            name = self._create_runner_name()
            runner_path = PATH_TO_RUNNER
            config_path = os.path.join(runner_path, 'config.sh')
            cmd = [config_path, '--url', repo_path, '--token', self.token, '--name', name, '--work', '_work', '--labels', labels]
            response = subprocess.run(cmd, capture_output=True)
            logging.info(f"RUNNER-NAME: {name}")
            logging.info(str(response.stdout))
        except Exception as e:
            logging.error(str(e))

    def start_runner(self):
        try:
            runner_path = PATH_TO_RUNNER
            start_path = os.path.join(runner_path, 'run.sh')
            subprocess.run(start_path)
            logging.info('Successfully started runner')
        except Exception as e:
            logging.error(str(e))

if __name__ == '__main__':
    runner_connect = GitHubActionsRunnerConnect()
    if runner_connect.check_for_runner():
        runner_connect.generate_token()
        runner_connect.register_runner()
        runner_connect.start_runner()
    else:
        runner_connect.install_runner()
        runner_connect.generate_token()
        runner_connect.register_runner()
        runner_connect.start_runner()
