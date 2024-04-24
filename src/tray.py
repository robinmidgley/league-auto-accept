import pystray
import os
from PIL import Image

BASE_PATH = os.path.abspath(".")

class Tray:
    def __init__(self):
        icon_path = os.path.join(BASE_PATH, "assets", "icon.png")
        self.image = Image.open(icon_path)
        self.icon = pystray.Icon("Menu", self.image)
        self.toggled = False
        self.icon.menu = self._menu_setup()

    def run(self):
        self.icon.run()

    def get_toggle_state(self):
        return self.toggled

    def set_toggle_state(self, state):
        self.toggled = state
        self.icon.menu = self._menu_setup()

    def _menu_setup(self):
        return pystray.Menu(
            pystray.MenuItem(self._get_toggle_text(), self._toggle),
            pystray.MenuItem("Exit", self._exit),
        )

    def _get_toggle_text(self):
        return "On" if self.toggled else "Off"

    def _toggle(self):
        self.toggled = not self.toggled
        self.icon.menu = self._menu_setup()

    def _exit(self):
        self.icon.stop()
        os._exit(0)