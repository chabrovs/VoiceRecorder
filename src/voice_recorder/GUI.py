# OS
import os
import subprocess
from threading import Thread
from platform import system

# TK
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Application
from recorder import Recorder
from manager import settings_manager


class VoiceRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Recorder App")
        self.master.geometry('450x500')

        self.recorder = Recorder()
        self.is_recording = False

        # GUI Elements
        self.start_button = tk.Button(
            self.master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            self.master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Canvas for recording indicator
        self.recording_indicator_canvas = tk.Canvas(
            self.master, width=20, height=20, bg="red", highlightthickness=0)

        self.recording_indicator_canvas.pack(
            side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        circle = self.recording_indicator_canvas.create_oval(
            50, 50, 150, 150, fill="red")

        # Menubar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(
            label="General Settings", command=self.show_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Frame to hold records list and buttons
        self.records_frame = tk.Frame(self.master)
        self.records_frame.pack(pady=10)

        # Listbox to display records with Scrollbar
        self.records_listbox = tk.Listbox(
            self.records_frame, selectmode=tk.SINGLE, width=50)
        self.records_listbox.pack(
            side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(
            self.records_frame, orient=tk.VERTICAL, command=self.records_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure Listbox to use the scrollbar
        self.records_listbox.config(yscrollcommand=scrollbar.set)

        # List records button
        self.list_records_button = tk.Button(
            self.master, text="List Records", command=self.list_records)
        self.list_records_button.pack(pady=10)

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.recording_indicator_canvas.config(
                bg="green")  # Change color to green when recording starts

            # Start recording in a separate thread
            self.recording_thread = Thread(
                target=self.recorder.record)
            self.recording_thread.start()

    def stop_recording(self):
        # TODO: Make it function
        if self.is_recording:
            self.is_recording = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.recording_indicator_canvas.config(
                bg="red")  # Change color back to red when recording stops

            # Stop recording (you need to implement this method in your Recorder class)
            self.recorder.stop_recording()

    def show_settings(self):
        operating_system = system().lower()
        settings_path = os.path.join(settings_manager.get_setting('base_dir'), 'settings.json', )

        match operating_system:
            case 'windows':
                subprocess.run(["notepad.exe", settings_path])
            case 'linux':
                subprocess.run(['xdg-open', settings_path])
            case 'darwin':
                subprocess.run(["open", "-t", settings_path])
            case _:
                raise Exception(f"Operating system '{operating_system}' is not supported")
    
    def list_records(self):
        # TODO: make rows deletion work correctly.
        # Can replace this with your own directory
        # directory = filedialog.askdirectory(title="Select Directory")
        directory = settings_manager.get_setting('save_records_path')
        if directory:
            # self.records_listbox.delete(0, tk.END)
            print(self.records_listbox.children)
            rows = self.records_listbox.children
            if rows != {}:
                for c in rows.values():
                    c.destroy()

            records = [file for file in os.listdir(
                directory) if file.endswith(('.wav', '.mp3', '.ogg'))]
            if records:
                if rows != {}:
                    for c in rows.values():
                        c.destroy()
                # self.records_listbox.delete(
                #     0, tk.END)  # Clear the current list
                for record in records:
                    # Create a frame for each row
                    record_frame = tk.Frame(self.records_listbox)
                    record_frame.pack(fill=tk.X)

                    # Label for the record name
                    record_label = tk.Label(
                        record_frame, text=record, width=30, anchor='w')
                    record_label.pack(side=tk.LEFT)

                    # Rename button for each record
                    rename_button = tk.Button(
                        record_frame, text="Rename", command=lambda file=record: self.rename_record(file))
                    rename_button.pack(side=tk.LEFT, padx=5)

                    # Delete button for each record
                    delete_button = tk.Button(
                        record_frame, text="Delete", command=lambda file=record: self.confirm_delete(file))
                    delete_button.pack(side=tk.RIGHT)

                    # Insert the frame into the listbox
                    self.records_listbox.insert(tk.END, record_frame)
            else:
                self.records_listbox.delete(0, tk.END)
                self.records_listbox.insert(
                    tk.END, "No audio records found in the selected directory.")

    def confirm_delete(self, file):
        confirm_dialog = messagebox.askquestion(
            "Confirm Delete", f"Are you sure you want to delete {file}?", icon='warning')
        if confirm_dialog == 'yes':
            os.remove(os.path.join(settings_manager.get_setting(
                'save_records_path'), file, ))
            # Update the listbox after deletion
            self.list_records()

    def rename_record(self, file):
        new_name = simpledialog.askstring(
            "Rename Record", f"Enter new name for {file}:", parent=self.master)
        if new_name:
            os.rename(
                os.path.join(settings_manager.get_setting(
                    'save_records_path'), file, ),
                os.path.join(settings_manager.get_setting(
                    'save_records_path'), new_name, )
            )
            # Update the listbox after renaming
            self.list_records()


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
else:
    def main():
        root = tk.Tk()
        app = VoiceRecorderApp(root)
        root.mainloop()