import threading
from client import League
from time import sleep
from tray import Tray

class Accept:
    def __init__(self):
        self.client = League()
        self.tray = Tray()
        self.auto_accept_thread = None
        self.running = True

    def run(self):
        self.auto_accept_thread = threading.Thread(target=self._auto_accept_queue)
        self.auto_accept_thread.start()
        self.tray.run()

    def _auto_accept_queue(self):
        while self.running:
            response = self.client.run("get", "/lol-gameflow/v1/gameflow-phase")
            sleep(1)

            if response == "ReadyCheck":
                if self.tray.get_toggle_state():
                    self.client.run("post", "/lol-matchmaking/v1/ready-check/accept")

            if response == "ChampSelect":
                self.tray.set_toggle_state(False)

    def stop(self):
        self.running = False
        if self.auto_accept_thread:
            self.auto_accept_thread.join()