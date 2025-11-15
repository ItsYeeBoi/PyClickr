import json
import os
import sys
from pathlib import Path
from threading import Thread
from time import sleep

from dearpygui import dearpygui as dpg
from pynput import keyboard
from pynput.keyboard import Key
from pynput.mouse import Button, Controller

try:
    from pyclickr import __author__, __title__, __version__
except ImportError:
    from . import __author__, __title__, __version__


class App:

    def __init__(self):
        self.mouse = Controller()
        self.clicking = False
        self.click_thread = None

        # Default Settings
        self.settings_file = "settings.json"
        self.settings = self.load_settings()

        # User Settings
        self.cps = int(self.settings.get("cps", 10))
        self.click_interval = 1.0 / self.cps
        start_stop_name = self.settings.get("start_stop_key", "f6")
        try:
            self.start_stop_key = Key[start_stop_name]
        except KeyError:
            self.start_stop_key = Key.f6

        # Window Size
        self.window_width = 400
        self.window_height = 300

        # Setup
        self.setup_hotkey()
        self.setup_gui()

    @staticmethod
    def resource_path(relative_path):
        """
        Get the absolute path to a resource, works for development and for PyInstaller.

        :param relative_path: Relative path to the resource.
        :return: Absolute path to the resource.
        """
        meipass = getattr(sys, "_MEIPASS", None)

        if meipass is not None:
            base_path = Path(meipass)
        else:
            base_path = Path(__file__).resolve().parents[2]

        return str(base_path / relative_path)

    def get_user_settings_path(self):
        """
        Returns a path like:
        - Windows: %APPDATA%/PyClickr/settings.json
        - Linux:   ~/.config/PyClickr/settings.json
        - macOS:   ~/Library/Application Support/PyClickr/settings.json
        """
        """
        Only tested on Windows.
        Create PR/issue if you test on other OS and it doesn't work.
        """

        if os.name == "nt":
            base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))

        config_dir = base / __title__
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / self.settings_file

    def load_settings(self):
        """
        Load user settings from a JSON file or use default settings.

        :return: Dictionary containing the settings.
        """
        user_settings_path = self.get_user_settings_path()

        try:
            if user_settings_path.exists():
                with user_settings_path.open("r", encoding="utf-8") as f:
                    return json.load(f)

        except json.JSONDecodeError:
            defaults = {}

        try:
            default_path = Path(self.resource_path("assets/settings.json"))
            with default_path.open("r", encoding="utf-8") as f:
                defaults = json.load(f)

        except FileNotFoundError:
            defaults = {
                "cps": self.cps,
                "start_stop_key": self.start_stop_key.name,
            }

        with user_settings_path.open("w", encoding="utf-8") as f:
            json.dump(defaults, f, indent=4)

        return defaults

    def save_settings(self):
        """
        Save user settings to a JSON file.
        """
        user_settings_path = self.get_user_settings_path()
        settings = {"cps": int(self.cps), "start_stop_key": self.start_stop_key.name}
        with user_settings_path.open("w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

    def update_cps(self, sender, app_data):
        try:
            self.cps = int(app_data)
            self.click_interval = 1.0 / self.cps
        except Exception:
            pass

    def click_loop(self):
        while self.clicking:
            self.mouse.click(Button.left)
            sleep(self.click_interval)

    def toggle_clicking(self):
        """
        Toggle the clicking state on or off.
        """
        if self.clicking:
            self.clicking = False
            if self.click_thread:
                self.click_thread.join()
        else:
            self.clicking = True
            self.click_thread = Thread(target=self.click_loop)
            self.click_thread.start()

    def setup_hotkey(self):
        """
        Set up the hotkey listener for starting and stopping the clicking.
        """

        def on_key_press(key):
            """
            Handle the key press event for the hotkey.

            :param key: The key that was pressed.
            """
            if key == self.start_stop_key:
                self.toggle_clicking()

        listener = keyboard.Listener(on_press=on_key_press)
        listener.start()

    def change_hotkey(self):
        """
        Change the hotkey for starting and stopping the clicking.
        """

        def on_key_press(key):
            """
            Handle the key press event for changing the hotkey.

            :param key: The key that was pressed.
            """
            self.start_stop_key = key
            try:
                dpg.configure_item(
                    "hotkey_text", label=f"Hotkey: {self.start_stop_key.name}"
                )
            except Exception:
                dpg.configure_item(
                    "hotkey_text", label=f"Hotkey: {self.start_stop_key}"
                )
            listener.stop()

        listener = keyboard.Listener(on_press=on_key_press)
        listener.start()

    def setup_gui(self):
        """
        Set up the DearPyGui interface.
        """
        self.icon_path = self.resource_path(r"assets\PyClickr.ico")
        dpg.create_context()

        with dpg.theme(tag="fake_button_theme"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [51, 51, 55, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [51, 51, 55, 255])

        dpg.create_viewport(
            title="PyClickr",
            small_icon=self.icon_path,
            large_icon=self.icon_path,
            width=self.window_width,
            height=self.window_height,
            resizable=False,
        )

        with dpg.window(
            label="PyClickr",
            width=self.window_width,
            height=self.window_height,
            no_title_bar=True,
            no_resize=True,
            no_move=True,
        ):
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label=f"Hotkey: {self.start_stop_key.name}",
                    tag="hotkey_text",
                )
                dpg.bind_item_theme("hotkey_text", "fake_button_theme")
                dpg.add_button(label="Change Hotkey", callback=self.change_hotkey)
            dpg.add_slider_int(
                label="CPS",
                default_value=self.cps,
                min_value=1,
                max_value=1000,
                width=90,
                clamped=True,
                callback=self.update_cps,
            )
            with dpg.group(horizontal=True):
                dpg.add_text(f"version {__version__}")
                dpg.add_spacer(width=20)
                dpg.add_text(f"by {__author__}")

        dpg.setup_dearpygui()
        dpg.show_viewport()

        try:
            dpg.start_dearpygui()
        finally:
            self.save_settings()
            dpg.destroy_context()


if __name__ == "__main__":
    app = App()
