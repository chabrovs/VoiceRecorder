import unittest
import sys
import os
import tkinter as tk

# ADD TESTED MODULES TO THE PATH DYNAMICALLY.
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir, 'voice_recorder'))
sys.path.append(parent_dir)

# IMPORT TESTED MODULES BELLOW:
from GUI import VoiceRecorderApp


class TestRecordsList(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tk.Tk()
        self.voice_recorder_app = VoiceRecorderApp(self.root)
        return super().setUp()

    def helper(cls, record_name: str) -> int:
        """Checks if an element is greater or equal to the next element"""

        return all(record_name[i] <= record_name[i+1] for i in range(len(record_name) - 1))

    def test_sort_records(self) -> None:
        """
        Test 'sort_records' method
        TIME: O(N * M); SPACE: O(N)
        """
        records_list_before_sorting = list(
            self.voice_recorder_app.records_listbox.get(0, "end"))
        self.voice_recorder_app.sort_records()
        records_list_after_sorting = list(
            self.voice_recorder_app.records_listbox.get(0, "end"))

        self.assertEqual(self.helper(records_list_after_sorting), True)
        

if __name__ == '__main__':
    unittest.main()
