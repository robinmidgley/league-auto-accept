import requests
import urllib3
import base64
import psutil
import time
import os

class League:
    def __init__(self):
        self.host = "127.0.0.1"
        self.league_process = "LeagueClient.exe"
        self.username = "riot"
        self.password = ""
        self.port = 0
        self.headers = ""
        self.session = requests.session()

    def run(self, method: str, url: str):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._get_lock_file()
        if self.port == 0:
            time.sleep(5)
            return "Cannot locate lockfile. Is the game open?"
        response = self._request(method, url)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {}
        
    def _find_lock_file(self):
        for process in psutil.process_iter(['name', 'exe']):
            if process.info['name'] == self.league_process:
                path = process.info['exe']
                return os.path.join(os.path.dirname(path), "lockfile")
        return None

    def _get_lock_file(self):
        lock_file_path = self._find_lock_file()
        if lock_file_path and os.path.exists(lock_file_path):
            with open(lock_file_path, "r") as lockfile:
                data = lockfile.read().split(":")
                self.password = data[3]
                self.port = data[2]
            token = base64.b64encode(f"{self.username}:{self.password}".encode('utf-8')).decode("ascii")
            self.headers = {'Authorization': f'Basic {token}'}

    def _request(self, method: str, path: str):
        url = f"https://{self.host}:{self.port}{path}"
        fn = getattr(self.session, method)
        response = fn(url, verify=False, headers=self.headers)
        return response