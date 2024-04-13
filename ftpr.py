import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter
import os
import json
import subprocess

# SETTINGS
SETTINGS_FILE = "settings.json"
# Get current working directory
LOCAL = os.getcwd()

class StartPage(tk.Frame):
    def __init__(self, parent, show_settings_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.show_settings_callback = show_settings_callback

        title = customtkinter.CTkLabel(self, text="FTP File Replacer - By Daale")
        title.pack(padx=10, pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack()

        self.load_button = customtkinter.CTkButton(button_frame, text='Choose File', command=self.load_file)
        self.load_button.pack(side="left", padx=10, pady=10)

        self.clear_button = customtkinter.CTkButton(button_frame, text='Clear', command=self.clear_file, state="disabled")
        self.clear_button.pack(side="left", padx=5, pady=10)

        self.upload_button = customtkinter.CTkButton(self, text="Upload", command=self.start_upload,
                                                      state="disabled")
        self.upload_button.pack(padx=10, pady=10)

        self.settings_button = customtkinter.CTkButton(self, text="Settings", command=self.show_settings)
        self.settings_button.pack(padx=10, pady=10)

        # Bind the delete_temp_file method to the app's destroy event
        parent.protocol("WM_DELETE_WINDOW", self.delete_temp_file)

        # Pack clear button initially
        self.clear_button.pack(side="left", padx=5, pady=10)

    def load_file(self):
        try:
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                target_file = settings.get("target_file", "")  # Get target_file from settings
                # Get file path from user
                file_path = filedialog.askopenfilename()
                if file_path:
                    self.load_button.configure(text=os.path.basename(file_path))
                    self.clear_button.configure(state="normal")
                    self.upload_button.configure(state="normal")
                # Create a path for a temporary copy of the uploaded file
                self.temp_path = os.path.join(LOCAL, target_file)  # Store temp path as an attribute
                print(self.temp_path)
                # Copy the file and make a temporary file in the current directory
                os.popen(f'cp "{file_path}" "{self.temp_path}"')
        except FileNotFoundError:
            print("Settings file not found.")

    def clear_file(self):
        self.load_button.configure(text='Choose File')
        self.clear_button.configure(state="disabled")
        self.upload_button.configure(state="disabled")

    def start_upload(self):
        try:
            print("--------------Starting upload-------------")
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                target_file = settings.get("target_file", "")  # Use "target_file" key instead of "targetname"
                DESTINATION = settings.get("destination_path", "")  # Use "destination_path" key instead of "DESTINATION"
                HOST = settings.get("host", "")  # Use "host" key instead of "HOST"
                USER = settings.get("username", "")  # Use "username" key instead of "USER"
                PASSWORD = settings.get("password", "")  # Use "password" key instead of "PASSWORD"

                print("Filename:", target_file)
                print("Destination:", DESTINATION)
                print("Local:", LOCAL)
                print("Host:", HOST)
                print("User:", USER)
                print("Password:", PASSWORD)

                # Use subprocess.Popen to get output
                output = subprocess.Popen(['sh', "./script.sh", target_file, DESTINATION, LOCAL, HOST, USER, PASSWORD], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = output.communicate()
                print(out.decode())  # Print stdout
                print(err.decode())  # Print stderr

                # Change the text of the upload button
                self.upload_button.configure(text="* Upload Finished! *")
                
        except FileNotFoundError:
            print("Settings file not found.")
        except Exception as e:
            print("Error occurred during upload:", e)
        print("-------------------Upload end!----------------")

    def show_settings(self):
        self.settings_button.pack_forget()  # Hide the settings button
        self.load_button.pack_forget()  # Hide the load button
        self.clear_button.pack_forget()  # Hide the clear button
        self.upload_button.pack_forget()  # Hide the upload button
        self.show_settings_callback()

    def delete_temp_file(self):
        # Delete the temporary file if it exists
        if hasattr(self, 'temp_path') and os.path.exists(self.temp_path):
            os.remove(self.temp_path)
        self.parent.destroy()


class SettingsPage(tk.Frame):
    def __init__(self, parent, start_page, show_start_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.start_page = start_page
        self.show_start_callback = show_start_callback

        guide_text = "Setup Guide"
        guide_button = customtkinter.CTkButton(self, text=guide_text, command=self.open_guide)
        guide_button.pack(padx=5, pady=5)

        file_settings_label = customtkinter.CTkLabel(self, text="File Settings", font=("Arial", 12, "bold"),
                                                     underline=True)
        file_settings_label.pack(padx=10, pady=5, anchor="w")

        # File settings widgets...
        target_file_label = customtkinter.CTkLabel(self, text="Target File Name:")
        target_file_label.pack(padx=10, pady=5, anchor="w")
        self.target_file_entry = ttk.Entry(self)
        self.target_file_entry.pack(padx=10, pady=5, fill="x")

        destination_path_label = customtkinter.CTkLabel(self, text="Destination Path:")
        destination_path_label.pack(padx=10, pady=5, anchor="w")
        self.destination_path_entry = ttk.Entry(self)
        self.destination_path_entry.pack(padx=10, pady=5, fill="x")

        ftp_settings_label = customtkinter.CTkLabel(self, text="FTP Settings", font=("Arial", 12, "bold"),
                                                     underline=True)
        ftp_settings_label.pack(padx=10, pady=5, anchor="w")

        # FTP settings widgets...
        host_label = customtkinter.CTkLabel(self, text="Host:")
        host_label.pack(padx=10, pady=5, anchor="w")
        self.host_entry = ttk.Entry(self)
        self.host_entry.pack(padx=10, pady=5, fill="x")

        username_label = customtkinter.CTkLabel(self, text="Username:")
        username_label.pack(padx=10, pady=5, anchor="w")
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(padx=10, pady=5, fill="x")

        password_label = customtkinter.CTkLabel(self, text="Password:")
        password_label.pack(padx=10, pady=5, anchor="w")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(padx=10, pady=5, fill="x")

        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.save_settings,
                                                   state="disabled")
        self.save_button.pack(side="left", padx=10, pady=10)

        back_button = customtkinter.CTkButton(self, text="Back", command=self.show_start)
        back_button.pack(side="right", padx=10, pady=10)

        # Validate settings fields
        self.validate_settings()

    def validate_settings(self):
        # Add validation to enable/disable save button
        self.target_file_entry.bind("<KeyRelease>", self.check_settings)
        self.destination_path_entry.bind("<KeyRelease>", self.check_settings)
        self.host_entry.bind("<KeyRelease>", self.check_settings)
        self.username_entry.bind("<KeyRelease>", self.check_settings)
        self.password_entry.bind("<KeyRelease>", self.check_settings)

    def check_settings(self, event):
        # Enable save button if all settings are filled out
        if (self.target_file_entry.get() and self.destination_path_entry.get() and
                self.host_entry.get() and self.username_entry.get() and self.password_entry.get()):
            self.save_button.configure(state="normal")
        else:
            self.save_button.configure(state="disabled")

    def save_settings(self):
        settings = {
            "target_file": self.target_file_entry.get(),
            "destination_path": self.destination_path_entry.get(),
            "host": self.host_entry.get(),
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }
        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file)
        # Enable upload button after saving settings
        self.show_start_callback()

    def show_start(self):
        self.pack_forget()  # Hide the current frame
        self.show_start_callback()

    def open_guide(self):
        # Open the GitHub page in the default web browser
        import webbrowser
        webbrowser.open("https://github.com/yourusername/yourproject")

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x750")
        self.title("FTP Replace")
        self.create_widgets()

        # Load settings from file
        self.load_settings()

    def create_widgets(self):
        self.start_page = StartPage(self, self.show_settings_page)
        self.settings_page = SettingsPage(self, self.start_page, self.show_start_page)

        self.start_page.pack()

    def show_settings_page(self):
        self.settings_page.pack()
        self.settings_page.lift()  # Bring the settings page to the top of the stack

    def show_start_page(self):
        self.settings_page.pack_forget()  # Hide the settings page
        self.start_page.load_button.pack(side="left", padx=10, pady=10)  # Show the load button
        self.start_page.clear_button.pack(side="left", padx=5, pady=10)  # Show the clear button
        self.start_page.upload_button.pack(padx=10, pady=10)  # Show the upload button
        self.start_page.settings_button.pack(padx=10, pady=10)  # Show the settings button at the bottom

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                # Update entries with loaded settings
                self.settings_page.target_file_entry.insert(0, settings.get("target_file", ""))
                self.settings_page.destination_path_entry.insert(0, settings.get("destination_path", ""))
                self.settings_page.host_entry.insert(0, settings.get("host", ""))
                self.settings_page.username_entry.insert(0, settings.get("username", ""))
                self.settings_page.password_entry.insert(0, settings.get("password", ""))
                # Enable upload button if settings exist
                self.start_page.upload_button.configure(state="normal")
        except FileNotFoundError:
            # If settings file does not exist, do nothing
            pass


# System settings
customtkinter.set_default_color_theme("blue")

# Run app
if __name__ == "__main__":
    app = App()
    app.mainloop()
