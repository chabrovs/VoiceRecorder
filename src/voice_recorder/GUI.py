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
        self.recording_thread = None
        self.selected_item = None
        self.master = master
        self.master.title("Voice Recorder App")
        self.master.geometry('250x500')
        self.icon_image = tk.PhotoImage(file=settings_manager.get_setting('GUI.icon_path'))
        self.master.wm_iconphoto(True, self.icon_image)

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

        # Listbox right mouse click menu config
        self.right_click_menu = tk.Menu(self.records_frame, tearoff=0)
        self.right_click_menu.add_command(
            label="Rename", command=self.rename_record)
        self.right_click_menu.add_command(
            label="Delete", command=self.confirm_delete)

        # Bin buttons
        self.records_listbox.bind("<Button-3>", self.show_context_menu)
        # Bind left mouse click on the root window to close the menu
        self.master.bind("<Button-1>", self.close_context_menu)

        # Bind menu to the FocusOut event to close when it loses focus
        self.right_click_menu.bind("<FocusOut>", self.close_context_menu)

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
            # self.recording_thread = Thread(
            #     target=self.recorder.record)
            # self.recording_thread.start()

            self.recorder.start_recording()

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.recording_indicator_canvas.config(
                bg="red")  # Change color back to red when recording stops

            # Stop recording (you need to implement this method in your Recorder class)
            self.recorder.stop_recording()

    @staticmethod
    def show_settings():
        operating_system = system().lower()
        settings_path = os.path.join(
            settings_manager.get_setting('base_dir'), 'settings.json', )

        match operating_system:
            case 'windows':
                subprocess.run(["notepad.exe", settings_path])
            case 'linux':
                subprocess.run(['xdg-open', settings_path])
            case 'darwin':
                subprocess.run(["open", "-t", settings_path])
            case _:
                raise Exception(
                    f"Operating system '{operating_system}' is not supported")

    def list_records(self):
        # TODO: sorting.
        # Can replace this with your own directory
        # directory = filedialog.askdirectory(title="Select Directory")
        directory = settings_manager.get_setting('save_records_path')
        if directory:
            self.records_listbox.delete(0, tk.END)
            records = [file for file in os.listdir(
                directory) if file.endswith(('.wav', '.mp3', '.ogg'))]
            if records:
                self.records_listbox.delete(
                    0, tk.END)  # Clear the current list
                for record in records:
                    # Insert the frame into the listbox
                    self.records_listbox.insert(tk.END, record)
            else:
                self.records_listbox.delete(0, tk.END)
                self.records_listbox.insert(
                    tk.END, "No audio records found in the selected directory.")

    def confirm_delete(self, file=None):
        if self.selected_item:
            file = self.selected_item

        confirm_dialog = messagebox.askquestion(
            "Confirm Delete", f"Are you sure you want to delete {file}?", icon='warning')
        if confirm_dialog == 'yes':
            os.remove(os.path.join(settings_manager.get_setting(
                'save_records_path'), file, ))
            # Update the listbox after deletion
            self.list_records()

    def rename_record(self, file=None):
        if self.selected_item:
            file = self.selected_item

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

    # Right mouse click menu
    # Create a context menu
    def show_context_menu(self, event):
        selected_item = self.records_listbox.get(
            self.records_listbox.nearest(event.y))
        self.selected_item = selected_item
        self.right_click_menu.post(event.x_root, event.y_root)

    def close_context_menu(self, event=None):
        self.right_click_menu.unpost()


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
else:
    def main():
        root = tk.Tk()
        # icon_image = tk.PhotoImage(file=settings_manager.get_setting('GUI.icon_path'))
        # root.wm_iconphoto(True, icon_image)
        app = VoiceRecorderApp(root)
        root.mainloop()
