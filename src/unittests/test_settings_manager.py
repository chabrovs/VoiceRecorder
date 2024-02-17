import unittest
import sys
import os

# ADD TESTED MODULES TO THE PATH DYNAMICALLY.
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

# IMPORT TESTED MODULES BELLOW:
from voice_recorder.manager import SettingsManager


class TestSettingsManager(unittest.TestCase):
    """In this class test the 'SettingsManager' as an interface for the 'Settings' class"""

    def setUp(self) -> None:
        self.settings_manager = SettingsManager()
        self.settings_manager_1 = SettingsManager()
        self.settings_manager_2 = SettingsManager()
        self.random = ''
        return super().setUp()

    def test_singleton_pattern(self) -> None:
        """Checks if the Singleton pattern works properly in the interface"""

        self.assertEqual(self.settings_manager_1, self.settings_manager_2)


if __name__ == '__main__':
    unittest.main()
