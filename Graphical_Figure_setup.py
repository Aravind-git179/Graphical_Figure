import customtkinter as ctk
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image
import mysql.connector
import os
import sys
import win32com.client
import shutil
import threading
import subprocess
from pathlib import Path
import ctypes
import logging


#image location
icon="app_image\\Graphical_Figure_app.ico"
app_name="app_image\\App_name.png"
creater_logo="app_image\\creater_logo.png"
create_id="app_image\\create_id.png"
agree="app_image\\relationship.png"
app_logo="app_image\\app_logo.png"

#location of py file
python_file_location='Graphical_Figure\\Graphical_Figure.py'

#mysql database
mysql_text="mysql_details.txt"
location="mysql_details"



class SetupWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.title("Condition Page")
        self.geometry('800x550')
        self.resizable(False, False)
        ctk.set_appearance_mode("system")

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(anchor="center", pady=30)
        self.iconbitmap(icon)

        # Display primary logo
        self.display_image(
            app_name,
            self.main_frame,
            size=(484, 170),
            position={"column": 1, "row": 1, "padx": 20, "pady": 5, "columnspan": 2}
        )

        # Display secondary logo
        self.display_image(
            creater_logo,
            self.main_frame,
            size=(170, 220),
            position={"column": 1, "row": 2, "padx": 30}
        )

        # Add description
        self.render_description()

        # Add agree button
        self.add_agree_button()

    def display_image(self, image_path, parent, size, position):
        """
        Display an image if the file exists.
        """
        if os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                photo = ctk.CTkImage(image, size=size)
                ctk.CTkLabel(parent, text=None, image=photo).grid(**position)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
        else:
            print(f"File not found: {image_path}")

    def render_description(self):
        """
        Render a scrollable frame with app description text.
        """
        sub_frame = ctk.CTkScrollableFrame(self.main_frame, width=350, height=50)
        sub_frame.grid(column=2, row=2, pady=5, padx=40)
        ctk.CTkLabel(
            sub_frame,
            text="Reason of Creation",
            font=('Amasis MT Pro Black', 20)
        ).pack()

        text_reason_of_creation = (
            "Graphical Figure app was created by Aravidhan.\n"
            "It was testing a desktop application. The main \n"
            "reason for creating this app is education.\n"
            "To learn Python pip module. Guidelines for\n"
            "creating this app were gained from books, \n"
            "websites, and YouTube. The app is authorized \n"
            "by AI and data science developer.\n"
            "Copyrights gained by Aravindhan as the creator.\n\n"
            "Thank you for choosing this app."
        )
        ctk.CTkLabel(
            sub_frame,
            text=text_reason_of_creation,
            font=('Amasis MT Pro Black', 15)
        ).pack(padx=1)

        ctk.CTkLabel(
            sub_frame,
            text="\n                                                        Aravindhan,",
            font=('Amasis MT Pro Black', 15)
        ).pack()

        ctk.CTkLabel(
            sub_frame,
            text="                                    Signature",
            font=('Amasis MT Pro Black', 20)
        ).pack()

    def add_agree_button(self):
        """
        Add the 'Agree' button with image and install functionality.
        """
        icon_path = agree
        if os.path.exists(icon_path):
            try:
                agree_image = Image.open(icon_path)
                agree_icon = ctk.CTkImage(agree_image, size=(45, 45))

                ctk.CTkButton(
                    self.main_frame,
                    image=agree_icon,
                    text="Agree",
                    font=('Cooper Black', 25),
                    fg_color="#FF5733",
                    hover_color="#4682B4",
                    corner_radius=65,
                    command=self.mysql_warning
                ).grid(column=1, row=3, pady=20, columnspan=2)
            except Exception as e:
                print(f"Error loading button image {icon_path}: {e}")
        else:
            print(f"File not found: {icon_path}")

    def mysql_warning(self):
        def check_mysql_installed():
            """Check if MySQL is installed."""
            try:
                # Try running the `mysql --version` command to check if it's in PATH
                result = subprocess.run(["mysql", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True)
                if result.returncode == 0:
                    return True
            except FileNotFoundError:
                pass

            # Alternative: Check default installation paths (Windows)
            common_paths = [
                r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
                r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return True

            return False

        def save_credentials():
            """Save MySQL credentials to a text file."""
            file_path = os.path.join(location, mysql_text)
            if Widget.winfo_exists(self):  # Check if the widget still exists
                Widget.focus_set(self)
                with open(file_path, "w") as file:
                    file.write(f"Username: {self.username}\n")
                    file.write(f"Password: {self.password}\n")

                self.after(100,self.select_output_dir)
            #messagebox.showinfo("Success", "MySQL credentials saved successfully.")

        def show_mysql_form():
            """Show a CTk form to collect MySQL credentials."""

            def on_submit():
                self.username = username_entry.get()
                self.password = password_entry.get()
                if self.username and self.password:
                    save_credentials()
                else:
                    messagebox.showwarning("Input Error", "Please fill out both fields.")

            self.title("Database...")
            self.geometry('700x400')
            self.resizable(False, False)

            # Clear the main frame for new content
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            sub_frame = ctk.CTkFrame(self.main_frame, width=350, height=50)
            sub_frame.pack( pady=20, padx=40)
            ctk.CTkLabel(
                sub_frame,
                text="***Warning***",
                font=('Amasis MT Pro Black', 25),
                text_color='red'
            ).pack()
            text_reason_of_creation = (
                "We do not have a centralised databases. \n"
                "So user only need to install mysql server \n"
                " and setup. The app creater suggested to\n"
                "install mysql and give the bellow details.\n"
                "Thank you for choosing this app."
            )
            ctk.CTkLabel(
                sub_frame,
                text=text_reason_of_creation,
                font=('Amasis MT Pro Black', 18)
            ).pack(padx=10,pady=10)

            # MySQL Username
            username_entry = ctk.CTkEntry(self.main_frame, width=250,placeholder_text="MySQL Username")
            username_entry.pack(pady=5)

            # MySQL Password
            password_entry = ctk.CTkEntry(self.main_frame, width=250, show="*",placeholder_text="MySQL Password")
            password_entry.pack(pady=5)

            # Submit Button
            submit_button = ctk.CTkButton(self.main_frame, text="Submit", command=on_submit)
            submit_button.pack(pady=20)

        if check_mysql_installed():
            show_mysql_form()
        else:
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            ctk.CTkLabel(
                self.main_frame,
                text="***Warning***",
                font=('Amasis MT Pro Black', 25),
                text_color='red'
            ).pack()
            text_reason_of_creation = (
                "We do not have a centralised databases. \n"
                "So user only need to install mysql server. \n"
                "Install mysql and try again."
            )
            ctk.CTkLabel(
                self.main_frame,
                text=text_reason_of_creation,
                font=('Amasis MT Pro Black', 18)
            ).pack(padx=10, pady=10)

    def select_output_dir(self):
        self.title("Locating app...")
        self.geometry('700x400')
        self.resizable(False, False)

        # Clear the main frame for new content
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        def open_file_explorer():
            directory = filedialog.askdirectory()
            if directory:
                self.entry_output.delete(0, ctk.END)
                self.entry_output.insert(0, directory)
                check_input()  # Check input after selecting a directory

        def check_input():
            if self.entry_output.get().strip():  # Check if the field is filled
                location_save_button.configure(state="normal")
                if not os.path.exists(self.entry_output.get()):
                    messagebox.showerror("Invalid Path",
                                         "The specified output directory does not exist. Please select a valid location.")
                    return
                print(self.entry_output.get())
            else:
                location_save_button.configure(state="disabled")

        def save_directory_and_proceed():
            # Save the output directory value to the class variable
            self.output_directory = self.entry_output.get().strip()
            # Proceed to the next step
            self.start_installation_process()

        # App logo
        image = Image.open(app_logo)
        photo = ctk.CTkImage(image, size=(200, 200))
        ctk.CTkLabel(self.main_frame, text=None, image=photo).pack(pady=20)

        # Output directory
        frame_output = ctk.CTkFrame(self.main_frame)
        frame_output.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(frame_output, text="Location:").pack(side="left", padx=5)
        self.entry_output = ctk.CTkEntry(frame_output, width=400)
        self.entry_output.pack(side="left", padx=5, fill="x", expand=True)
        self.entry_output.bind("<KeyRelease>", lambda event: check_input())  # Trigger check_input on key release
        ctk.CTkButton(frame_output, text="File", command=open_file_explorer).pack(side="left", padx=5)

        # Save location button (Initially Disabled)
        location_save_button = ctk.CTkButton(
            self.main_frame,
            text="Save",
            command=save_directory_and_proceed,  # Save directory and proceed
            state="disabled"  # Disabled by default
        )
        location_save_button.pack(pady=15)

    def start_installation_process(self):
        """
        Start the installation process and show the relevant label and buttons.
        """
        # Clear the main frame for new content
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.title("Create ID")
        self.geometry('500x500')
        self.resizable(False, False)

        #app logo
        image = Image.open(app_logo)
        photo = ctk.CTkImage(image, size=(200,200))
        ctk.CTkLabel(self.main_frame, text=None, image=photo).pack(pady=20)


        # Add a label to indicate readiness for installation
        ctk.CTkLabel(
            self.main_frame,
            text="The program is ready to install.",
            font=('Bodoni MT Black', 25),
            text_color="green3"
        ).pack(pady=20,padx=10)

        # 'Yes' button to proceed
        ctk.CTkButton(
            self.main_frame,
            text="Yes",
            font=('Cooper Black', 20),
            fg_color="green3",
            command=self.create_id_page
        ).pack(pady=10)

        # 'No' button to exit
        ctk.CTkButton(
            self.main_frame,
            text="No",
            font=('Cooper Black', 20),
            fg_color="#FF5733",
            command=self.destroy
        ).pack(pady=10)

    def create_id_page(self):

        print(self.output_directory)  # Use the saved output directory value

        # Define the base location where the folder will be created
        base_location = self.output_directory

        folder_name = "Graphical_Figure"
        self.folder_path = os.path.join(base_location, folder_name)

        # Create the folder
        try:
            os.makedirs(self.folder_path)  # Use makedirs to create intermediate directories if needed
            print(f"Folder '{folder_name}' created at: {self.folder_path}")
        except FileExistsError:
            print(f"Folder '{folder_name}' already exists at: {self.folder_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while creating the folder:\n{e}")
            return

        # Create the folder
        try:
            source_dir = "Graphical_Figure\\image"  # Source folder path
            destination_dir = os.path.join(self.folder_path, 'image')  # Destination folder path

            # Copy the folder
            if os.path.exists(destination_dir):
                shutil.rmtree(destination_dir)  # Remove the folder if it already exists
            shutil.copytree(source_dir, destination_dir)

            print("Shortcut Created", f"Image folder copied to {destination_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy image folder:\n{e}")
            print(e)

        """transfer mysql details."""
        try:
            destination_dir = self.folder_path
            shutil.copy(f'{location}\\{mysql_text}', destination_dir)
        except Exception as e:
            messagebox.showerror("Error", f"transfer mysql details:\n{e}")

        # Proceed to render the Create ID page if successful
        self.clear_frame()

        # Title logo
        image = Image.open(create_id)
        photo = ctk.CTkImage(image, size=(150, 150))
        ctk.CTkLabel(self.main_frame, text=None, image=photo).pack(pady=20)

        # Entry fields for ID and Password
        self.user_id_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            font=('Amasis MT Pro Black', 20),
            placeholder_text="Enter your ID",
            height=35
        )
        self.user_id_entry.pack(padx=100, pady=5)

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            font=('Amasis MT Pro Black', 20),
            placeholder_text="Enter your Password",
            show="*",
            height=35
        )
        self.password_entry.pack(pady=5)

        # Save and Cancel buttons
        ctk.CTkButton(
            self.main_frame,
            text="Create",
            fg_color="green3",
            font=('Amasis MT Pro Black', 20),
            command=self.save_user_data  # Save user ID and password
        ).pack(pady=10)

        ctk.CTkButton(
            self.main_frame,
            text="Cancel",
            fg_color="#FF5733",
            font=('Amasis MT Pro Black', 20),
            command=self.exit_application
        ).pack(pady=10)

        # Label for status messages
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=('Arial', 15),
        )
        self.status_label.pack(pady=10)

    def save_user_data(self):
        """
        Collect the user's ID and password from input fields and save them into a database.
        """
        user_id = self.user_id_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validate inputs
        if not user_id or not password:
            self.status_label.configure(
                text="Error: Both ID and Password are required.",
                text_color="red"
            )
            return

        try:

            # Read the content from the mysql_details.txt file
            with open(f"{location}\\mysql_details.txt", "r") as file:
                content = file.read()
                print("Current content in mysql_details.txt:")
                print(content)

            # Update the file with the new username and password
            with open(f"{location}\\mysql_details.txt", "w") as file:
                file.write(f"Username: {user_id}\n")
                file.write(f"Password: {password}\n")

            # Extract MySQL user from the file (assuming the format is "user: <username>")
            mysql_user = None
            for line in content.splitlines():
                 if line.startswith("Username:"):
                    mysql_user = line.split(":")[1].strip()

            if not mysql_user:
                self.status_label.configure(
                    text="Error: Could not find MySQL user in the file.",
                    text_color="red"
                )
                return

            # Extract MySQL password from the file (assuming the format is "Password: <password>")
            mysql_password = None
            for line in content.splitlines():
                if line.startswith("Password:"):
                    mysql_password = line.split(":")[1].strip()

            if not mysql_password:
                self.status_label.configure(
                    text="Error: Could not find MySQL password in the file.",
                    text_color="red"
                )
                return

            # Connect to database
            connection = mysql.connector.connect(
                host="localhost",
                user=mysql_user,
                password=mysql_password  # Change to your MySQL password
            )
            cursor = connection.cursor()

            # Ensure database and table existence
            cursor.execute("CREATE DATABASE IF NOT EXISTS graphical_figure;")
            cursor.execute("USE graphical_figure;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(12) NOT NULL
                );
            """)

            # Save user data
            cursor.execute("INSERT INTO users (id, password) VALUES (%s, %s)", (user_id, password))
            connection.commit()

            # Feedback to the user
            self.status_label.configure(
                text="User ID is created successfully!",
                text_color="green3"
            )



            #call process function
            self.setup_to_install_gui()

        except mysql.connector.Error as db_error:
            self.status_label.configure(
                text=f"Database Error: {db_error}",
                text_color="red"
            )

        except Exception as e:
            self.status_label.configure(
                text=f"Error: {e}",
                text_color="red"
            )

        finally:
            # Ensure connection is closed
            if 'connection' in locals() and connection.is_connected():
                connection.close()

    def clear_frame(self):
        """
        Utility function to clear all widgets from the main frame.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def exit_application(self):
        """
        Exit the application.
        """
        self.destroy()

    def setup_to_install_gui(self):
        def build_executable():
            #droping button
            build_button.destroy()
            """Build the executable using PyInstaller."""
            try:
                script_path = python_file_location
                output_dir = self.folder_path
                use_one_file = True
                use_console = True
                icon_path = icon

                if not os.path.isfile(script_path):
                    messagebox.showerror("Error", "Script file not found.")
                    return

                command = ["pyinstaller", script_path]

                if use_one_file:
                    command.append("--onefile")
                if not use_console:
                    command.append("--noconsole")
                if output_dir:
                    command.extend(["--distpath", output_dir])
                if icon_path and os.path.isfile(icon_path):
                    command.extend(["--icon", icon_path])

                # Start subprocess in a separate thread
                threading.Thread(target=run_process, args=(command, output_dir)).start()

            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

        def run_process(command, output_dir):
            """Run the PyInstaller command and update the GUI after completion."""
            try:
                process = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
                )

                log_text.delete(1.0, "end")  # Clear previous logs
                log_text.insert("end", "Building executable...\n")
                log_text.see("end")

                progress_bar.set(0)  # Reset progress bar

                for line in process.stdout:
                    log_text.insert("end", line)
                    log_text.see("end")
                    self.update_idletasks()

                    # Update progress based on specific messages
                    if "building EXE from EXE" in line:
                        progress_bar.set(50)
                    elif "cleaning up" in line:
                        progress_bar.set(80)
                    elif "completed successfully" in line:
                        progress_bar.set(100)

                process.wait()

                if process.returncode == 0:
                    log_text.insert("end", "Build completed successfully!\n")
                    create_open_button(output_dir)
                else:
                    messagebox.showerror("Error", "Build failed. Check the logs for details.")
                    progress_bar.set(0)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during the process:\n{e}")

        def create_open_button(output_dir):
            """Replace the build button with an open button after successful build."""
            build_button.pack_forget()

            dist_dir = Path(output_dir)
            self.exe_path = next(dist_dir.glob("*.exe"), None)
            if not self.exe_path:
                messagebox.showerror("Error", "Executable not found in the output directory.")
                return

            def open_exe():
                """Open the built executable."""
                try:
                    os.startfile(str(self.exe_path))
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open executable:\n{e}")

            def create_shortcut():
                """Create a desktop shortcut for the built executable."""
                try:
                    destination_dir = os.path.join(os.environ["USERPROFILE"], "OneDrive\\Desktop")
                    shutil.copy(str(self.exe_path), destination_dir)
                    messagebox.showinfo("Shortcut Created", f"Shortcut created at {destination_dir}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create shortcut:\n{e}")

                try:
                    source_dir = "Graphical_Figure\\image"  # Source folder path
                    destination_dir = os.path.join(os.environ["USERPROFILE"], "OneDrive\\Desktop","image")  # Destination folder path

                    # Copy the folder
                    if os.path.exists(destination_dir):
                        shutil.rmtree(destination_dir)  # Remove the folder if it already exists
                    shutil.copytree(source_dir, destination_dir)

                    print("Shortcut Created", f"Image folder copied to {destination_dir}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy image folder:\n{e}")
                    print(e)

                """transfer mysql details."""
                try:
                    destination_dir =os.path.join(os.environ["USERPROFILE"], "OneDrive\\Desktop")
                    shutil.copy(f'{location}\\{mysql_text}', destination_dir)
                except Exception as e:
                    messagebox.showerror("Error", f"transfer mysql details:\n{e}")

                # Proceed to render the Create ID page if successful
                self.clear_frame()

            def add_shortcut_in_app_list():

                def add_to_start_menu(exe_path, app_name="Graphical Figure", icon_path=None):
                    """
                    Add an executable to the Start Menu by creating a shortcut in the Start Menu Programs directory.

                    :param exe_path: Full path to the executable file.
                    :param app_name: Name of the application (used for the shortcut name).
                    :param icon_path: Optional path to an icon file.
                    """
                    try:
                        # Validate the executable path
                        if not os.path.isfile(exe_path):
                            raise FileNotFoundError(f"Executable file not found: {exe_path}")

                        # Get the Start Menu Programs directory
                        start_menu_dir = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs")

                        # Ensure the Start Menu directory exists
                        os.makedirs(start_menu_dir, exist_ok=True)

                        # Define the shortcut file path in the Start Menu
                        shortcut_path = os.path.join(start_menu_dir, f"{app_name}.lnk")

                        # Create the shortcut
                        shell = win32com.client.Dispatch("WScript.Shell")
                        shortcut = shell.CreateShortcut(shortcut_path)
                        shortcut.TargetPath = exe_path
                        shortcut.WorkingDirectory = os.path.dirname(exe_path)

                        # Set the icon if provided
                        if icon_path and os.path.isfile(icon_path):
                            shortcut.IconLocation = icon_path
                        else:
                            shortcut.IconLocation = exe_path  # Use the .exe as the icon if no icon file is provided

                        shortcut.save()

                        # Notify the user
                        print(f"Application added to Start Menu: {shortcut_path}")
                        print("Start Menu", f"Application added to Start Menu: {shortcut_path}")

                    except Exception as e:
                        # Show error message
                        messagebox.showerror("Error", f"Failed to add application to Start Menu:\n{e}")
                        print(f"Error: {e}")

                    try:
                        # Define source and destination directories
                        source_dir = "Graphical_Figure\\image"  # Source folder path
                        destination_dir = os.path.join(
                            os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\image"
                        )  # Destination folder path

                        # Validate source folder
                        if not os.path.exists(source_dir):
                            raise FileNotFoundError(f"Source folder not found: {source_dir}")

                        # Remove the destination folder if it already exists
                        if os.path.exists(destination_dir):
                            shutil.rmtree(destination_dir)

                        # Copy the folder
                        shutil.copytree(source_dir, destination_dir)

                        # Notify the user
                        messagebox.showinfo("Shortcut Created", f"Image folder copied to {destination_dir}")
                    except Exception as e:
                        # Handle and notify errors
                        messagebox.showerror("Error", f"Failed to copy image folder:\n{e}")
                        print(e)

                    """transfer mysql details."""
                    try:
                        destination_dir = os.path.join(
                            os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs"
                        )  # Destination folder path
                        shutil.copy(f'{location}\\{mysql_text}', destination_dir)
                    except Exception as e:
                        messagebox.showerror("Error", f"transfer mysql details:\n{e}")

                """Create a app list shortcut for the built executable."""
                try:
                    destination_dir = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs")
                    shutil.copy(str(self.exe_path), destination_dir)
                    messagebox.showinfo("Shortcut Created", f"Shortcut created at {destination_dir}")
                    exe_path = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Graphical Figure.exe")  # Update with the full path to your .exe
                    icon_path = icon  # Optional, update with the path to your .ico file
                    self.after(10,add_to_start_menu(exe_path))
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create shortcut:\n{e}")

            open_button = ctk.CTkButton(self, text="Open Executable", command=open_exe)
            open_button.pack(pady=10, padx=10, anchor="e")

            shortcut_button = ctk.CTkButton(self, text="Create Shortcut", command=create_shortcut)
            shortcut_button.pack(pady=10, padx=10, anchor="e")

            #call app_list_shortcut
            self.after(10,add_shortcut_in_app_list)

        def toggle_logs():
            """Toggle the visibility of the logs section."""
            if self.log_frame.winfo_ismapped():
                self.log_frame.pack_forget()
                toggle_button.configure(text="Show Details >")
            else:
                self.log_frame.pack(pady=5, padx=5, fill="both", expand=True)
                toggle_button.configure(text="Hide Details ^")

        try:
            # Clear main frame for new content
            for widget in self.main_frame.winfo_children():
                widget.destroy()
                self.main_frame.destroy()

            self.title("Installing...")
            self.geometry("650x500")

            # app_name logo
            image = Image.open(app_name)
            photo = ctk.CTkImage(image, size=(484, 170))
            ctk.CTkLabel(self, text=None, image=photo).pack(pady=20)

            # Progress Bar
            self.frame_progress = ctk.CTkFrame(self)
            self.frame_progress.pack(pady=5, padx=5, fill="x")
            ctk.CTkLabel(self.frame_progress, text="Progress:").pack(side="left", padx=5)
            progress_bar = ctk.CTkProgressBar(self.frame_progress, width=300, height=20)
            progress_bar.pack(side="left", padx=5, fill="x", expand=True)

            # Toggle Logs button
            toggle_button = ctk.CTkButton(self, text="Show Details >", command=toggle_logs)
            toggle_button.pack(pady=5, anchor="w", padx=10)

            # Log Viewer
            self.log_frame = ctk.CTkFrame(self)
            self.log_frame.pack_forget()
            ctk.CTkLabel(self.log_frame, text="Build Logs:").pack(anchor="w", padx=5)
            log_text = ctk.CTkTextbox(self.log_frame, height=10)
            log_text.pack(fill="both", expand=True, padx=5, pady=5)

            # Build button
            build_button = ctk.CTkButton(self, text="Install", command=build_executable)
            build_button.pack(pady=10, padx=10, anchor="e")

        except ImportError:
            print("Error: Required module is not installed. Exiting.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)


if __name__ == "__main__":
    app = SetupWindow()
    app.mainloop()
