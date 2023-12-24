import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from threading import Thread
# Replace with your actual module and class
from recorder import Main as Recorder


class VoiceRecorderApp:
    root = tk.Tk()

    def __init__(self, master=root):
        self.master = master
        self.master.title("Voice Recorder App")
        self.master.geometry('1000x500')

        self.recorder = Recorder()  # Replace with your actual Recorder class
        self.is_recording = False

        # GUI Elements
        self.start_button = tk.Button(
            self.master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            self.master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

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

        # Listbox to display records
        self.records_listbox = tk.Listbox(self.records_frame, selectmode=tk.SINGLE, width=50)
        self.records_listbox.pack(side=tk.LEFT, padx=5)

        # List records button
        self.list_records_button = tk.Button(self.master, text="List Records", command=self.list_records)
        self.list_records_button.pack(pady=10)

    def confirm_delete(self, file):
        confirm_dialog = messagebox.askquestion(
            "Confirm Delete", f"Are you sure you want to delete {file}?", icon='warning')
        if confirm_dialog == 'yes':
            # Implement your logic to delete the file here
            # You can use os.remove() to delete the file
            print(f"Deleting {file}")
            # Update the listbox after deletion
            self.list_records()
    
    def rename_record(self, file):
        new_name = simpledialog.askstring("Rename Record", f"Enter new name for {file}:", parent=self.master)
        if new_name:
            # Implement your logic to rename the file here
            # You can use os.rename() to rename the file
            print(f"Renaming {file} to {new_name}")
            # Update the listbox after renaming
            self.list_records()

    def show_settings(self) -> None:
        raise NotImplementedError

    def list_records(self):
        # You can replace this with your own directory
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            self.records_listbox.delete(0, tk.END)
            # self.delete_buttons = []  # Clear the list of delete buttons
            records = [file for file in os.listdir(
                directory) if file.endswith(('.wav', '.mp3', '.ogg'))]
            if records:
                self.records_listbox.delete(
                    0, tk.END)  # Clear the current list
                for record in records:
                    # Create a frame for each row
                    record_frame = tk.Frame(self.records_listbox)
                    record_frame.pack(fill=tk.X)

                    # Label for the record name
                    record_label = tk.Label(record_frame, text=record, width=30, anchor='w')
                    record_label.pack(side=tk.LEFT)

                    # Rename button for each record
                    rename_button = tk.Button(record_frame, text="Rename", command=lambda file=record: self.rename_record(file))
                    rename_button.pack(side=tk.LEFT, padx=5)

                    # Delete button for each record
                    delete_button = tk.Button(record_frame, text="Delete", command=lambda file=record: self.confirm_delete(file))
                    delete_button.pack(side=tk.RIGHT)

                    # Insert the frame into the listbox
                    self.records_listbox.insert(tk.END, record_frame)
            else:
                self.records_listbox.delete(0, tk.END)
                self.records_listbox.insert(
                    tk.END, "No audio records found in the selected directory.")

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            # Start recording in a separate thread
            self.recording_thread = Thread(
                target=self.recorder.record)
            self.recording_thread.start()

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

            # Stop recording (you need to implement this method in your Recorder class)
            self.recorder.stop_recording()


if __name__ == "__main__":
    app = VoiceRecorderApp()
    app.root.mainloop()
