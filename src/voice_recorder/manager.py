from abc import ABC, abstractmethod
from typing import Any


from os import path
from pathlib import Path
import json

# GLOBAL VARIABLES
BASEDIR = Path(__file__).resolve().parent
SETTINGS = path.join(BASEDIR, "settings.json", )


class Manager(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.__settings: dict = None

    @abstractmethod
    def get_setting(self, setting: str) -> Any:
        """
        Return a specific setting from a dictionary
        constructed from settings.json
        """
        ...

    @abstractmethod
    def load_settings(self) -> None:
        """
        Load settings from settings.json
        """
        ...


class SettingsManager(Manager):
    def __init__(self) -> None:
        super().__init__()
        self.__settings = self.load_settings()

    def add_base_dir(self, settings_data: dict) -> None:
        """Adding base directory to the settings"""
        settings_data['base_dir'] = BASEDIR.__str__()

    def load_settings(self) -> None:
        settings = SETTINGS
        with open(settings, 'r') as file:
            settings_data = json.load(file)

        self.add_base_dir(settings_data)

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


if __name__ == '__main__':
    pass
else:
    settings_manager = SettingsManager()
