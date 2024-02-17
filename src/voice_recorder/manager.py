# Annotation
from abc import ABC, abstractmethod
from typing import Any

# OS
from os import path, makedirs
from pathlib import Path
import json

# GLOBAL VARIABLES
BASEDIR = Path(__file__).resolve().parent
SETTINGS = path.join(BASEDIR, "settings.json", )


class Manager(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.__settings: dict

    @abstractmethod
    def get_setting(self, setting: str) -> Any:
        """
        Return a specific setting from a dictionary
        constructed from settings.json
        """
        ...

    @abstractmethod
    def _load_settings(self) -> None:
        """
        Load settings from settings.json
        """
        ...


class Settings(Manager):
    """
    "Settings" class is responsible for general settings across the application.
    General settings are set in the "Settings.json" file.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__settings = self._load_settings()
        self._build_icon_path()

    @staticmethod
    def _add_base_dir(settings_data: dict) -> None:
        """Adding base directory to the settings"""
        settings_data['base_dir'] = BASEDIR.__str__()

    @staticmethod
    def _build_save_records_path(settings_data: dict) -> int:
        """Return a path to a directory where records will be saved"""

        def is_valid_dir(records_directory: str) -> None:
            if not path.exists(records_directory):
                makedirs(records_directory)

        directory = settings_data.get('save_records_path')

        if directory != "":
            is_valid_dir(directory)
            settings_data['save_records_path'] = directory

        directory = path.join(BASEDIR, 'records',)
        is_valid_dir(directory)

        settings_data['save_records_path'] = directory

        return 0

    def _build_icon_path(self) -> int:
        """Builds full icon path"""

        def does_file_exist(directory: str) -> bool:
            return Path(directory).exists()

        icon_path = path.join(BASEDIR, self.get_setting('GUI.icon_path'))

        if not does_file_exist(icon_path):
            raise LookupError(
                f"ERROR: 'manager, settings manager, build icon path' \nICON file does not exist in the directory '{icon_path}'")

        self.__settings['GUI']['icon_path'] = icon_path

        return 0

    def _load_settings(self) -> dict:
        settings = SETTINGS
        with open(settings, 'r') as file:
            settings_data = json.load(file)

        self._add_base_dir(settings_data)
        self._build_save_records_path(settings_data)

        return settings_data

    def get_setting(self, setting: str) -> Any:
        keys = setting.split('.')
        current_data = self.__settings

        try:
            for key in keys:
                current_data = current_data[key]
            return current_data
        except (KeyError, TypeError):
            raise ValueError(
                f'The setting was not found by this address "{setting}"')


# Interface

class SettingsManager:
    """
    "SettingsManager" interface. Provides access for the "Settings" class.
    """
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            # Class initialization here
            cls.settings = Settings()

        return cls._instance

    def get_setting(self, setting: str = 'GUI.icon_path') -> Any:
        """Returns a value from the settings dictionary loaded from Settings.json"""

        return self.settings.get_setting(setting=setting)


