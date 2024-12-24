import customtkinter as ctk
from PIL import Image
import mysql.connector
import tkinter.messagebox as MessageBox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App_main_window(ctk.CTk):  # parent window
    def __init__(self):  # auto run function
        super().__init__()  # auto run command
        self.title('Graphical Figure')  # Give title in top
        self.iconbitmap("image\\app.ico")  # Change ctk logo
        self.geometry('600x500')  # giving size
        self.resizable(False, False)  # not to full screen

        # Load images
        # created admin name
        self.logo_image = Image.open("image\\created_by.png")
        self.creater_photo = ctk.CTkImage(self.logo_image, size=(250, 250))

        # app image
        self.app_image = Image.open("image\\app_image.png")
        self.app_photo = ctk.CTkImage(self.app_image, size=(150, 150))

        # id icon
        self.logo_id = Image.open("image\\id.ico")
        self.id_photo = ctk.CTkImage(self.logo_id, size=(25, 25))

        # password icon
        self.logo_password = Image.open("image\\password.ico")
        self.password_photo = ctk.CTkImage(self.logo_password, size=(25, 25))

        # create frame inside widget
        self.main_frame1 = ctk.CTkFrame(self)
        self.main_frame1.place(x=330 / 2, y=100)

        # displaying creater photo
        self.al1 = ctk.CTkLabel(self.main_frame1, text=None, image=self.creater_photo)
        self.al1.pack(padx=20, pady=20)

        # transwer to frame2
        def show_frame1():
            self.after(300, self.show_frame2)

        # call another widget
        self.after(500, show_frame1)

    def show_frame2(self):
        # Destroying frame 1
        self.main_frame1.destroy()

        # Creating frame 2
        self.title('Login Page')
        self.resizable(0, 0)
        self.main_frame2 = ctk.CTkFrame(self)
        self.main_frame2.place(x=300 / 2, y=20)

        self.al1 = ctk.CTkLabel(self.main_frame2, text=None, image=self.app_photo)
        self.al1.grid(padx=20, pady=10, column=0, row=0, sticky='nsew')

        self.al2 = ctk.CTkLabel(self.main_frame2, image=self.id_photo, text='         id', font=('Forte', 25))
        self.al2.grid(sticky='w', column=0, row=1)

        self.ae1 = ctk.CTkEntry(self.main_frame2, width=250, font=('Amasis MT Pro Black', 20), height=35)
        self.ae1.grid(padx=40, pady=10, column=0, row=3)

        self.al2 = ctk.CTkLabel(self.main_frame2, text=None, image=self.password_photo, font=('Forte', 25))
        self.al3 = ctk.CTkLabel(self.main_frame2, text='password', font=('Forte', 25))
        self.al2.grid(sticky='w', pady=10, column=0, row=4, padx=30)
        self.al3.grid(sticky='w', pady=10, column=0, row=4, padx=60)

        self.ae2 = ctk.CTkEntry(self.main_frame2, width=250, font=('Amasis MT Pro Black', 20), show="*", height=35)
        self.ae2.grid(padx=20, column=0, row=5)

        self.ab1 = ctk.CTkButton(self.main_frame2, text="Enter", font=('Script MT Bold', 20), corner_radius=25,
                                 command=self.Transwer_data_databases)
        self.ab1.grid(pady=18, column=0, row=6)

        self.al4 = ctk.CTkLabel(self.main_frame2, text=None, font=('Script MT Bold', 20))
        self.al4.grid(pady=10, column=0, row=7)

    def Transwer_data_databases(self):
        # Receiving data
        self.app_id = self.ae1.get()  # Get id for login
        self.app_password = self.ae2.get()  # Get password for login

        # Load MySQL credentials from a text file
        def load_credentials(file_path):
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    username = None
                    password = None

                    for line in lines:
                        if line.startswith('Username:'):
                            username = line.split(':')[1].strip()
                        elif line.startswith('Password:'):
                            password = line.split(':')[1].strip()

                    if username and password:
                        return username, password
                    else:
                        raise ValueError("Invalid credentials file format.")
            except FileNotFoundError:
                raise FileNotFoundError(f"Credentials file '{file_path}' not found.")
            except Exception as e:
                raise Exception(f"An error occurred while reading credentials: {e}")

        # Path to the uploaded file
        file_path = 'mysql_details.txt'

        # Load and print the credentials
        username, password = load_credentials(file_path)
        print(f"Username: {username}")
        print(f"Password: {password}")

        # Connect with mysql details
        self.host = 'localhost'
        self.user = username
        self.userpassword = password

        # Connecting to mysql
        self.conection = mysql.connector.connect(host=self.host, user=self.user, password=self.userpassword,
                                                 database='graphical_figure')  # Connecting to database
        self.cur = self.conection.cursor()

        # Checking whether mysql is connected
        if self.conection.is_connected():  # Connected

            print('mysql is connected')
            # Executing command
            self.cur.execute('select * from users;')
            self.res = self.cur.fetchall()

            # Receiving data from mysql
            for i in self.res:
                self.database_id = i[0]
                self.database_password = i[1]
                print('id=', self.database_id, '\n', 'password=', self.database_password)  # Check purpose

            # Errors of unmatched received data from mysql
            def errors():
                self.wrong_image = Image.open("image\\wrong.ico")
                self.x_photo = ctk.CTkImage(self.wrong_image, size=(50, 50))
                al4 = ctk.CTkLabel(self.main_frame2, text=None, image=self.x_photo, font=('Script MT Bold', 20))
                al4.grid(padx=20, pady=0, column=0, row=7, sticky='w')

                al5 = ctk.CTkLabel(self.main_frame2, text=self.Error_command, font=('Script MT Bold', 20))
                al5.grid(padx=60, pady=0, column=0, row=7)

                # Deleting error
                def errors_delete():
                    al4.destroy()
                    al5.destroy()

                self.after(500, errors_delete)

            if self.app_id == self.database_id and self.app_password == self.database_password:
                print('transferring to another page')
                self.conection.close()
                self.main_frame2.destroy()
                self.call_inside_window = App_inside_window(self)
                self.call_inside_window.setup_page()  # Call the setup_page method

            elif self.app_id != self.database_id and self.app_password == self.database_password:
                print('id')
                self.Error_command = 'Wrong id'
                self.after(1, errors)

            elif self.app_id == self.database_id and self.app_password != self.database_password:
                print('password')
                self.Error_command = 'Wrong password'
                self.after(1, errors)

            elif self.app_id != self.database_id and self.app_password != self.database_password:
                print('two')
                self.Error_command = 'Wrong id and password'
                self.after(1, errors)
        else:  # Databases are not connected
            print('mysql database are not connected')
            self.main_frame2.destroy()
            self.mysq_not_connected_frame = ctk.CTkFrame(self)
            self.mysq_not_connected_frame.pack()

        # Add widgets or setup the new page layout here


class App_inside_window(ctk.CTk):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def setup_page(self):

        print('you are inside sub window')

        self.parent.title('Giving details')
        self.parent.geometry('1200x600')
        self.parent.resizable(True, True)

        self.parent.outer_frame = ctk.CTkScrollableFrame(self.parent, width=1000, height=900)
        self.parent.outer_frame.pack(padx=10, pady=20, fill="both", expand=True)

        self.parent.inside_framed = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.inside_framed.pack(pady=20)

        # Add the label for "Balance Sheet as on"
        self.topic_label = ctk.CTkLabel(self.parent.inside_framed, text="Balance Sheet as on ", font=('Algerian', 25))
        self.topic_label.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        self.parent.inside_framep = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.inside_framep.pack()

        self.Pframe = self.parent.inside_framep

        self.parent.ll1 = ctk.CTkLabel(self.Pframe, text="Particulars", font=('Algerian', 25))
        self.parent.ll1.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        self.parent.ll2 = ctk.CTkLabel(self.Pframe, text="            ", font=('Algerian', 25))
        self.parent.ll2.grid(padx=10, pady=10, column=1, row=0, sticky='nsew')

        # only get int or float command
        # Validation function to allow only float input
        def validate_float_input(value):
            if value == '':  # Allow empty value
                return True
            try:
                float(value)  # Attempt to convert input to float
                int(value)
                return True
            except ValueError:
                return False

        # Register the validation function
        self.validate_command = (self.parent.register(validate_float_input), "%P")

        # Create the first entry field
        self.entry_1 = ctk.CTkEntry(self.Pframe, font=('Algerian', 25))
        self.entry_1.grid(padx=50, pady=10, column=2, row=0, sticky='e')
        self.entry_1.bind("<KeyRelease>", self.update_topic)  # Binding key release to the update method

        # Create the second entry field
        self.entry_2 = ctk.CTkEntry(self.Pframe, font=('Algerian', 25))
        self.entry_2.grid(padx=10, pady=10, column=4, row=0, sticky='e')
        self.entry_2.bind("<KeyRelease>", self.update_topic)  # Binding key release to the update method

        # liabilities Frame
        self.parent.inside_frame1 = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.inside_frame1.pack(pady=20)

        self.Lframe = self.parent.inside_frame1

        self.parent.ll1 = ctk.CTkLabel(self.Lframe, text="I.EQUITY AND LIABILITIES", font=('Algerian', 25))
        self.parent.ll1.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        # Shareholder funds
        self.parent.ll2 = ctk.CTkLabel(self.Lframe, text="1)Shareholder's Funds", font=('Aharoni', 20))
        self.parent.ll2.grid(padx=10, pady=5, column=0, row=1, sticky='w')

        self.parent.ll3 = ctk.CTkLabel(self.Lframe, text="a)Share Capital", font=('Aptos Black', 18))
        self.parent.ll3.grid(padx=30, pady=5, column=0, row=2, sticky='w')

        self.parent.ll4 = ctk.CTkLabel(self.Lframe, text="b)Reserves and Surplus", font=('Aptos Black', 18))
        self.parent.ll4.grid(padx=30, pady=5, column=0, row=3, sticky='w')

        # Non-current liabilities labels
        self.parent.ll5 = ctk.CTkLabel(self.Lframe, text="2)Non-current Liabilities", font=('Aharoni', 20))
        self.parent.ll5.grid(padx=10, pady=5, column=0, row=4, sticky='w')

        self.parent.ll6 = ctk.CTkLabel(self.Lframe, text='a)Long term borrowing', font=('Aptos Black', 18))
        self.parent.ll6.grid(padx=30, pady=5, column=0, row=5, sticky='w')

        self.parent.ll7 = ctk.CTkLabel(self.Lframe, text="b)Deferred tax liabilities", font=('Aptos Black', 18))
        self.parent.ll7.grid(padx=30, pady=5, column=0, row=6, sticky='w')

        self.parent.ll8 = ctk.CTkLabel(self.Lframe, text="c)Other long term liabilities", font=('Aptos Black', 18))
        self.parent.ll8.grid(padx=30, pady=5, column=0, row=7, sticky='w')

        self.parent.ll9 = ctk.CTkLabel(self.Lframe, text="d)Long term provisions", font=('Aptos Black', 18))
        self.parent.ll9.grid(padx=30, pady=5, column=0, row=8, sticky='w')

        # Current Liabilities labels
        self.parent.ll10 = ctk.CTkLabel(self.Lframe, text="3)Current Liabilities", font=('Aharoni', 20))
        self.parent.ll10.grid(padx=10, pady=5, column=0, row=9, sticky='w')

        self.parent.ll11 = ctk.CTkLabel(self.Lframe, text='a)Short-term borrowing', font=('Aptos Black', 18))
        self.parent.ll11.grid(padx=30, pady=5, column=0, row=10, sticky='w')

        self.parent.ll12 = ctk.CTkLabel(self.Lframe, text="b)Trade payables", font=('Aptos Black', 18))
        self.parent.ll12.grid(padx=30, pady=5, column=0, row=11, sticky='w')

        self.parent.ll13 = ctk.CTkLabel(self.Lframe, text="c)Other current liabilities", font=('Aptos Black', 18))
        self.parent.ll13.grid(padx=30, pady=5, column=0, row=12, sticky='w')

        self.parent.ll14 = ctk.CTkLabel(self.Lframe, text="d)Short-term provisions", font=('Aptos Black', 18))
        self.parent.ll14.grid(padx=30, pady=5, column=0, row=13, sticky='w')

        self.parent.ll15 = ctk.CTkLabel(self.Lframe, text="Total", font=('Algerian', 25))
        self.parent.ll15.grid(padx=10, pady=10, column=0, row=14, sticky='nsew')

        # entry box column1 liabilities
        # shareholder funds
        self.parent.le1 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le1.grid(row=2, column=1, padx=30, pady=5, sticky='w')

        self.parent.le2 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le2.grid(row=3, column=1, padx=30, pady=5, sticky='w')

        # entry column1 Non-current liabilities
        self.parent.le3 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le3.grid(padx=30, pady=5, column=1, row=5, sticky='w')

        self.parent.le4 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le4.grid(padx=30, pady=5, column=1, row=6, sticky='w')

        self.parent.le5 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le5.grid(padx=30, pady=5, column=1, row=7, sticky='w')

        self.parent.le6 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le6.grid(padx=30, pady=5, column=1, row=8, sticky='w')

        # entry column1 Current Liabilities
        self.parent.le7 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le7.grid(padx=30, pady=5, column=1, row=10, sticky='w')

        self.parent.le8 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le8.grid(padx=30, pady=5, column=1, row=11, sticky='w')

        self.parent.le9 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le9.grid(padx=30, pady=5, column=1, row=12, sticky='w')

        self.parent.le10 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le10.grid(padx=30, pady=5, column=1, row=13, sticky='w')

        # total liabilities column1
        self.parent.lb11 = ctk.CTkButton(self.Lframe, font=('Algerian', 25), text='Year1', command=self.LY1)
        self.parent.lb11.grid(padx=30, pady=10, column=1, row=14, sticky='w')

        # entry box year 2
        # entry Shareholder funds column2
        self.parent.le21 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le21.grid(padx=30, pady=5, column=2, row=2, sticky='w')

        self.parent.le22 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le22.grid(padx=30, pady=5, column=2, row=3, sticky='w')

        # entry column2 Non-current liabilities
        self.parent.le23 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le23.grid(padx=30, pady=5, column=2, row=5, sticky='w')

        self.parent.le24 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le24.grid(padx=30, pady=5, column=2, row=6, sticky='w')

        self.parent.le25 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le25.grid(padx=30, pady=5, column=2, row=7, sticky='w')

        self.parent.le26 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le26.grid(padx=30, pady=5, column=2, row=8, sticky='w')

        # entry column2 Current Liabilities
        self.parent.le27 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le27.grid(padx=30, pady=5, column=2, row=10, sticky='w')

        self.parent.le28 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le28.grid(padx=30, pady=5, column=2, row=11, sticky='w')

        self.parent.le29 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le29.grid(padx=30, pady=5, column=2, row=12, sticky='w')

        self.parent.le210 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                         validatecommand=self.validate_command)
        self.parent.le210.grid(padx=30, pady=5, column=2, row=13, sticky='w')

        # total liabilities column2
        self.parent.lb211 = ctk.CTkButton(self.Lframe, font=('Algerian', 25), text='Year2', command=self.LY2)
        self.parent.lb211.grid(padx=30, pady=10, column=2, row=14, sticky='w')

        # assert frame
        self.parent.inside_frame2 = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        # self.parent.inside_frame2.grid(column=0,row=3,padx=20,pady=20)
        self.parent.inside_frame2.pack()

        self.Aframe = self.parent.inside_frame2

        # Assert side Label
        self.parent.al1 = ctk.CTkLabel(self.Aframe, text="II.ASSETS", font=('Algerian', 25))
        self.parent.al1.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        # Non-Current Assets
        self.parent.al2 = ctk.CTkLabel(self.Aframe, text="1)Non-Current Assets", font=('Aharoni', 20))
        self.parent.al2.grid(padx=10, pady=5, column=0, row=1, sticky='w')

        self.parent.al3 = ctk.CTkLabel(self.Aframe, text="a)Fixed assets", font=('Aptos Black', 18))
        self.parent.al3.grid(padx=30, pady=5, column=0, row=2, sticky='w')

        self.parent.al4 = ctk.CTkLabel(self.Aframe, text="b)Non-current investments", font=('Aptos Black', 18))
        self.parent.al4.grid(padx=30, pady=5, column=0, row=3, sticky='w')

        self.parent.al5 = ctk.CTkLabel(self.Aframe, text="c)Deferred tax assets(net)", font=('Aptos Black', 18))
        self.parent.al5.grid(padx=30, pady=5, column=0, row=4, sticky='w')

        self.parent.al6 = ctk.CTkLabel(self.Aframe, text="d)Long-term loan and advance", font=('Aptos Black', 18))
        self.parent.al6.grid(padx=30, pady=5, column=0, row=5, sticky='w')

        self.parent.al7 = ctk.CTkLabel(self.Aframe, text="e)Other non-current assets", font=('Aptos Black', 18))
        self.parent.al7.grid(padx=30, pady=5, column=0, row=6, sticky='w')

        # Current Assets
        self.parent.al8 = ctk.CTkLabel(self.Aframe, text="2)Current Assets", font=('Aharoni', 20))
        self.parent.al8.grid(padx=10, pady=5, column=0, row=7, sticky='w')

        self.parent.al9 = ctk.CTkLabel(self.Aframe, text='a)Current investments', font=('Aptos Black', 18))
        self.parent.al9.grid(padx=30, pady=5, column=0, row=8, sticky='w')

        self.parent.al10 = ctk.CTkLabel(self.Aframe, text="b)Inventories", font=('Aptos Black', 18))
        self.parent.al10.grid(padx=30, pady=5, column=0, row=9, sticky='w')

        self.parent.al11 = ctk.CTkLabel(self.Aframe, text="c)Trade receivables", font=('Aptos Black', 18))
        self.parent.al11.grid(padx=30, pady=5, column=0, row=10, sticky='w')

        self.parent.al12 = ctk.CTkLabel(self.Aframe, text="d)Cash and cash equivalents", font=('Aptos Black', 18))
        self.parent.al12.grid(padx=30, pady=5, column=0, row=11, sticky='w')

        self.parent.al13 = ctk.CTkLabel(self.Aframe, text="e)Short term loan and advance", font=('Aptos Black', 18))
        self.parent.al13.grid(padx=30, pady=5, column=0, row=12, sticky='w')

        self.parent.al14 = ctk.CTkLabel(self.Aframe, text="f)other current assets", font=('Aptos Black', 18))
        self.parent.al14.grid(padx=30, pady=5, column=0, row=13, sticky='w')

        # Total assert
        self.parent.al15 = ctk.CTkLabel(self.Aframe, text="Total", font=('Algerian', 25))
        self.parent.al15.grid(padx=10, pady=10, column=0, row=14, sticky='nsew')

        # assert
        # entry box year1
        # entry NON-current Assert column1
        self.parent.ae1 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae1.grid(padx=30, pady=5, column=1, row=2, sticky='w')

        self.parent.ae2 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae2.grid(padx=30, pady=5, column=1, row=3, sticky='w')

        self.parent.ae3 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae3.grid(padx=30, pady=5, column=1, row=4, sticky='w')

        self.parent.ae4 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae4.grid(padx=30, pady=5, column=1, row=5, sticky='w')

        self.parent.ae5 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae5.grid(padx=30, pady=5, column=1, row=6, sticky='w')

        # entry column1 Current Assert
        self.parent.ae6 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae6.grid(padx=30, pady=5, column=1, row=8, sticky='w')

        self.parent.ae7 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae7.grid(padx=30, pady=5, column=1, row=9, sticky='w')

        self.parent.ae8 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae8.grid(padx=30, pady=5, column=1, row=10, sticky='w')

        self.parent.ae9 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae9.grid(padx=30, pady=5, column=1, row=11, sticky='w')

        self.parent.ae10 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae10.grid(padx=30, pady=5, column=1, row=12, sticky='w')

        self.parent.ae11 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae11.grid(padx=30, pady=5, column=1, row=13, sticky='w')

        # total assert column1
        self.parent.ab12 = ctk.CTkButton(self.Aframe, font=('Algerian', 25), text='Year1', command=self.AY1)
        self.parent.ab12.grid(padx=30, pady=10, column=1, row=14, sticky='w')

        # entry box year 2
        # entry non-current assets column2
        self.parent.ae21 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae21.grid(padx=30, pady=5, column=2, row=2, sticky='w')

        self.parent.ae22 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae22.grid(padx=30, pady=5, column=2, row=3, sticky='w')

        self.parent.ae23 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae23.grid(padx=30, pady=5, column=2, row=4, sticky='w')

        self.parent.ae24 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae24.grid(padx=30, pady=5, column=2, row=5, sticky='w')

        self.parent.ae25 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae25.grid(padx=30, pady=5, column=2, row=6, sticky='w')

        # entry column2 Current Assets
        self.parent.ae26 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae26.grid(padx=30, pady=5, column=2, row=8, sticky='w')

        self.parent.ae27 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae27.grid(padx=30, pady=5, column=2, row=9, sticky='w')

        self.parent.ae28 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae28.grid(padx=30, pady=5, column=2, row=10, sticky='w')

        self.parent.ae29 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae29.grid(padx=30, pady=5, column=2, row=11, sticky='w')

        self.parent.ae210 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                         validatecommand=self.validate_command)
        self.parent.ae210.grid(padx=30, pady=5, column=2, row=12, sticky='w')

        self.parent.ae211 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                         validatecommand=self.validate_command)
        self.parent.ae211.grid(padx=30, pady=5, column=2, row=13, sticky='w')

        # total assert column2
        self.parent.ab212 = ctk.CTkButton(self.Aframe, font=('Algerian', 25), text='Year2', command=self.AY2)
        self.parent.ab212.grid(padx=30, pady=10, column=2, row=14, sticky='w')

        # next page process button
        # button
        self.parent.npb = ctk.CTkButton(self.parent.outer_frame, text='Process', font=('Algerian', 25),
                                        command=self.Process)
        self.parent.npb.pack(pady=20)

        self.parent.npb1 = ctk.CTkButton(self.parent.outer_frame, text='Open File', font=('Algerian', 25),
                                         command=self.new_pandas_frames)
        self.parent.npb1.pack(pady=20)

    def update_topic(self, event=None):
        """
        Dynamically update the 'Balance Sheet as on' label with the values from the entry fields.
        """
        # Get values from entry fields
        value_1 = self.entry_1.get().strip()
        value_2 = self.entry_2.get().strip()

        print(f"Entries: '{value_1}' and '{value_2}'")  # Debugging: Check entered values

        # Construct the topic text
        if value_1 and value_2:
            topic = f"Balance Sheet as on {value_1} and {value_2}"
        else:
            topic = "Balance Sheet as on"

        # Update the topic label dynamically
        self.topic_label.configure(text=topic)
        print(f"Label updated to: {topic}")  # Debugging: Check if the label is updated

    def LY1(self):
        print('total y1')
        # to convert string to 0
        """
        Validate all entry fields to ensure they contain only integers.
        """
        liabilitiesy1_entries = [self.parent.le1,
                                 self.parent.le2,
                                 self.parent.le3,
                                 self.parent.le4,
                                 self.parent.le5,
                                 self.parent.le6,
                                 self.parent.le7,
                                 self.parent.le8,
                                 self.parent.le9,
                                 self.parent.le10]
        for entry in liabilitiesy1_entries:
            if not entry.get():  # Check if entry is empty
                entry.insert(0, "0")  # Set default value to "0" if empty
        self.liabilities_total_1year = float(self.parent.le1.get()) + float(self.parent.le2.get()) + float(
            self.parent.le3.get()) + float(self.parent.le4.get()) + float(self.parent.le5.get()) + float(
            self.parent.le6.get()) + float(self.parent.le7.get()) + float(self.parent.le8.get()) + float(
            self.parent.le9.get()) + float(self.parent.le10.get())
        self.parent.lb11.configure(text=self.liabilities_total_1year)

    def LY2(self):
        print('total y2')
        # to convert string to 0
        """
        Validate all entry fields to ensure they contain only integers.
        """
        liabilitiesy2_entries = [self.parent.le21,
                                 self.parent.le22,
                                 self.parent.le23,
                                 self.parent.le24,
                                 self.parent.le25,
                                 self.parent.le26,
                                 self.parent.le27,
                                 self.parent.le28,
                                 self.parent.le29,
                                 self.parent.le210]
        for entry in liabilitiesy2_entries:
            if not entry.get():  # Check if entry is empty
                entry.insert(0, "0")  # Set default value to "0" if empty
        # add and store
        self.liabilities_total_2year = float(self.parent.le21.get()) + float(self.parent.le22.get()) + float(
            self.parent.le23.get()) + float(self.parent.le24.get()) + float(self.parent.le25.get()) + float(
            self.parent.le26.get()) + float(self.parent.le27.get()) + float(self.parent.le28.get()) + float(
            self.parent.le29.get()) + float(self.parent.le210.get())
        self.parent.lb211.configure(text=self.liabilities_total_2year)

    def AY1(self):
        print('total y1')
        # to convert string to 0
        """
        Validate all entry fields to ensure they contain only integers.
        """
        assetsy1_entries = [self.parent.ae1,
                            self.parent.ae2,
                            self.parent.ae3,
                            self.parent.ae4,
                            self.parent.ae5,
                            self.parent.ae6,
                            self.parent.ae7,
                            self.parent.ae8,
                            self.parent.ae9,
                            self.parent.ae10,
                            self.parent.ae11]
        for entry in assetsy1_entries:
            if not entry.get():  # Check if entry is empty
                entry.insert(0, "0")  # Set default value to "0" if empty
        self.assets_total_1year = float(self.parent.ae1.get()) + float(self.parent.ae2.get()) + float(
            self.parent.ae3.get()) + float(self.parent.ae4.get()) + float(self.parent.ae5.get()) + float(
            self.parent.ae6.get()) + float(self.parent.ae7.get()) + float(self.parent.ae8.get()) + float(
            self.parent.ae9.get()) + float(self.parent.ae10.get()) + float(self.parent.ae11.get())
        self.parent.ab12.configure(text=self.assets_total_1year)

    def AY2(self):
        print('total y2')
        # to convert string to 0
        """
        Validate all entry fields to ensure they contain only integers.
        """
        assetsy2_entries = [self.parent.ae21,
                            self.parent.ae22,
                            self.parent.ae23,
                            self.parent.ae24,
                            self.parent.ae25,
                            self.parent.ae26,
                            self.parent.ae27,
                            self.parent.ae28,
                            self.parent.ae29,
                            self.parent.ae210,
                            self.parent.ae211]
        for entry in assetsy2_entries:
            if not entry.get():  # Check if entry is empty
                entry.insert(0, "0")  # Set default value to "0" if empty
        # add and store
        self.assets_total_2year = float(self.parent.ae21.get()) + float(self.parent.ae22.get()) + float(
            self.parent.ae23.get()) + float(self.parent.ae24.get()) + float(self.parent.ae25.get()) + float(
            self.parent.ae26.get()) + float(self.parent.ae27.get()) + float(self.parent.ae28.get()) + float(
            self.parent.ae29.get()) + float(self.parent.ae210.get()) + float(self.parent.ae211.get())
        self.parent.ab212.configure(text=self.assets_total_2year)

    def Process(self):

        liabilities = {self.entry_1.get(): [self.parent.le1.get(),
                                            self.parent.le2.get(),
                                            self.parent.le3.get(),
                                            self.parent.le4.get(),
                                            self.parent.le5.get(),
                                            self.parent.le6.get(),
                                            self.parent.le7.get(),
                                            self.parent.le8.get(),
                                            self.parent.le9.get(),
                                            self.parent.le10.get(),
                                            self.liabilities_total_1year
                                            ],
                       self.entry_2.get(): [self.parent.le21.get(),
                                            self.parent.le22.get(),
                                            self.parent.le23.get(),
                                            self.parent.le24.get(),
                                            self.parent.le25.get(),
                                            self.parent.le26.get(),
                                            self.parent.le27.get(),
                                            self.parent.le28.get(),
                                            self.parent.le29.get(),
                                            self.parent.le210.get(),
                                            self.liabilities_total_2year
                                            ]}

        assets = {self.entry_1.get(): [self.parent.ae1.get(),
                                       self.parent.ae2.get(),
                                       self.parent.ae3.get(),
                                       self.parent.ae4.get(),
                                       self.parent.ae5.get(),
                                       self.parent.ae6.get(),
                                       self.parent.ae7.get(),
                                       self.parent.ae8.get(),
                                       self.parent.ae9.get(),
                                       self.parent.ae10.get(),
                                       self.parent.ae11.get(),
                                       self.assets_total_2year
                                       ],
                  self.entry_2.get(): [self.parent.ae21.get(),
                                       self.parent.ae22.get(),
                                       self.parent.ae23.get(),
                                       self.parent.ae24.get(),
                                       self.parent.ae25.get(),
                                       self.parent.ae26.get(),
                                       self.parent.ae27.get(),
                                       self.parent.ae28.get(),
                                       self.parent.ae29.get(),
                                       self.parent.ae210.get(),
                                       self.parent.ae211.get(),
                                       self.assets_total_2year
                                       ]}

        liabilities_table = pd.DataFrame(liabilities)
        # change datatype
        liabilities_table = liabilities_table.astype({self.entry_1.get(): 'float', self.entry_1.get(): 'float'})
        print(liabilities_table)

        assets_table = pd.DataFrame(assets)
        # change datatype
        assets_table = assets_table.astype({self.entry_1.get(): 'float', self.entry_1.get(): 'float'})
        print(assets_table)

        # Create a pop-up window
        popup = ctk.CTkToplevel(self)
        popup.title("Save File")
        popup.geometry("300x200")
        popup.iconbitmap("E:\\enviroments\\Graphical_Figure\\Graphical Figure app\\image\\app.ico")  # Change ctk logo

        # Label for file name entry
        label = ctk.CTkLabel(popup, text="Enter the file name:")
        label.pack(pady=10)

        # Entry box to enter file name
        file_entry = ctk.CTkEntry(popup, width=200)
        file_entry.pack(pady=5)

        # Function to get the entered file name
        def save_file():
            file_name = file_entry.get().strip()
            if file_name:
                MessageBox.showinfo("File Name", f"File name '{file_name}' saved!")
                popup.destroy()  # Close the pop-up
                name_of_file_a = f'{file_name}a.csv'
                name_of_file_l = f'{file_name}l.csv'
                assets_table.to_csv(name_of_file_a, index=False)
                liabilities_table.to_csv(name_of_file_l, index=False)
                popup.after(100, self.new_pandas_frames)

            else:
                MessageBox.showerror("Error", "Please enter a file name.")

        # Save button
        save_button = ctk.CTkButton(popup, text="Save", command=save_file)
        save_button.pack(pady=10)

        # Cancel button to close without saving
        cancel_button = ctk.CTkButton(popup, text="Cancel", command=popup.destroy)
        cancel_button.pack(pady=5)

    def new_pandas_frames(self):

        # Create a pop-up window open file
        popup_pandas = ctk.CTkToplevel(self)
        popup_pandas.title("open File")
        popup_pandas.geometry("300x200")
        popup_pandas.iconbitmap(
            "E:\\enviroments\\Graphical_Figure\\Graphical Figure app\\image\\app.ico")  # Change ctk logo

        # Label for file name entry
        label_pandas = ctk.CTkLabel(popup_pandas, text="Enter the file name:")
        label_pandas.pack(pady=10)

        # Entry box to enter file name
        file_entry_pandas = ctk.CTkEntry(popup_pandas, width=200)
        file_entry_pandas.pack(pady=5)

        # Function to get the entered file name
        def save_file():
            file_name_pandas = file_entry_pandas.get().strip()
            if file_name_pandas:
                try:
                    MessageBox.showinfo("File Name", f"File name '{file_name_pandas}' open")
                    popup_pandas.destroy()  # Close the pop-up
                    find_of_file_a = f'{file_name_pandas}a.csv'
                    find_of_file_l = f'{file_name_pandas}l.csv'
                    self.assets_table_pandas = pd.read_csv(find_of_file_a)
                    self.liabilities_table_pandas = pd.read_csv(find_of_file_l)
                    print('assets')
                    print(self.assets_table_pandas)
                    print('liabilities')
                    print(self.liabilities_table_pandas)
                    # destroy balance sheet frame
                    self.parent.inside_framed.destroy()
                    self.parent.inside_framep.destroy()
                    self.parent.inside_frame1.destroy()
                    self.parent.inside_frame2.destroy()
                    self.parent.npb.destroy()
                    self.parent.npb1.destroy()
                    popup_pandas.after(100, self.open_pandas_file)
                except Exception as e:
                    MessageBox.showerror("Error", f"Failed to find file:\n{e}")
            else:
                MessageBox.showerror("Error", "Please enter a file name.")

        # Save button
        save_button_pandas = ctk.CTkButton(popup_pandas, text="open", command=save_file)
        save_button_pandas.pack(pady=10)

        # Cancel button to close without saving
        cancel_button_pandas = ctk.CTkButton(popup_pandas, text="Cancel", command=popup_pandas.destroy)
        cancel_button_pandas.pack(pady=5)

    def open_pandas_file(self):
        self.parent.title('Result')
        self.column_titles_list = self.assets_table_pandas.columns.tolist()
        print(self.column_titles_list)

        self.parent.pandas_framed = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.pandas_framed.pack(pady=20)

        # Add the label for "Balance Sheet as on"
        text = f"Comparative Balance Sheet as at March 31,{self.column_titles_list[0]} and {self.column_titles_list[1]}"
        self.topic_label_pandas = ctk.CTkLabel(self.parent.pandas_framed, text=text, font=('Algerian', 25))
        self.topic_label_pandas.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        self.parent.pandas_frameP = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.pandas_frameP.pack()

        self.Pandas_Pframe = self.parent.pandas_frameP

        self.parent.ll1_pandas = ctk.CTkLabel(self.Pandas_Pframe, text="Particulars", font=('Algerian', 25))
        self.parent.ll1_pandas.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        self.parent.ll2_pandas = ctk.CTkLabel(self.Pandas_Pframe, text="            ", font=('Algerian', 25))
        self.parent.ll2_pandas.grid(padx=10, pady=10, column=1, row=0, sticky='nsew')

        self.parent.ll3_pandas = ctk.CTkLabel(self.Pandas_Pframe, text="            ", font=('Algerian', 25))
        self.parent.ll3_pandas.grid(padx=5, pady=10, column=2, row=0, sticky='nsew')

        self.parent.ll4_pandas = ctk.CTkLabel(self.Pandas_Pframe, text="    ", font=('Algerian', 25))
        self.parent.ll4_pandas.grid(padx=5, pady=10, column=3, row=0, sticky='nsew')

        self.parent.ll5_pandas = ctk.CTkLabel(self.Pandas_Pframe, text=self.column_titles_list[0],
                                              font=('Algerian', 25))
        self.parent.ll5_pandas.grid(padx=40, pady=10, column=4, row=0, sticky='nsew')

        # self.parent.ll5_pandas = ctk.CTkLabel(self.Pandas_Pframe, text="            ", font=('Algerian', 25))
        # self.parent.ll5_pandas.grid(padx=10, pady=10, column=4, row=0, sticky='nsew')

        self.parent.ll6_pandas = ctk.CTkLabel(self.Pandas_Pframe, text=self.column_titles_list[1],
                                              font=('Algerian', 25))
        self.parent.ll6_pandas.grid(padx=30, pady=10, column=5, row=0, sticky='nsew')

        # self.parent.ll7_pandas = ctk.CTkLabel(self.Pandas_Pframe, text="            ", font=('Algerian', 25))
        # self.parent.ll7_pandas.grid(padx=10, pady=10, column=6, row=0, sticky='nsew')

        self.parent.ll8_pandas = ctk.CTkLabel(self.Pandas_Pframe, text='Absolute(+)or(-)', font=('Algerian', 25))
        self.parent.ll8_pandas.grid(padx=30, pady=10, column=6, row=0, sticky='nsew')

        # self.parent.ll9_pandas = ctk.CTkLabel(self.Pandas_Pframe, text="            ", font=('Algerian', 25))
        # self.parent.ll9_pandas.grid(padx=10, pady=10, column=8, row=0, sticky='nsew')

        self.parent.ll10_pandas = ctk.CTkLabel(self.Pandas_Pframe, text='Percentage', font=('Algerian', 25))
        self.parent.ll10_pandas.grid(padx=30, pady=10, column=7, row=0, sticky='nsew')

        # liabilities Frame pandas
        self.parent.pandas_frame1 = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.pandas_frame1.pack(pady=20)

        self.pandas_Lframe = self.parent.pandas_frame1

        self.parent.ll1 = ctk.CTkLabel(self.pandas_Lframe, text="I.EQUITY AND LIABILITIES", font=('Algerian', 25))
        self.parent.ll1.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        # Shareholder funds
        self.parent.ll2 = ctk.CTkLabel(self.pandas_Lframe, text="1)Shareholder's Funds", font=('Aharoni', 20))
        self.parent.ll2.grid(padx=10, pady=5, column=0, row=1, sticky='w')

        self.parent.ll3 = ctk.CTkLabel(self.pandas_Lframe, text="a)Share Capital", font=('Aptos Black', 18))
        self.parent.ll3.grid(padx=30, pady=5, column=0, row=2, sticky='w')

        self.parent.ll4 = ctk.CTkLabel(self.pandas_Lframe, text="b)Reserves and Surplus", font=('Aptos Black', 18))
        self.parent.ll4.grid(padx=30, pady=5, column=0, row=3, sticky='w')

        # Non-current liabilities labels
        self.parent.ll5 = ctk.CTkLabel(self.pandas_Lframe, text="2)Non-current Liabilities", font=('Aharoni', 20))
        self.parent.ll5.grid(padx=10, pady=5, column=0, row=4, sticky='w')

        self.parent.ll6 = ctk.CTkLabel(self.pandas_Lframe, text='a)Long term borrowing', font=('Aptos Black', 18))
        self.parent.ll6.grid(padx=30, pady=5, column=0, row=5, sticky='w')

        self.parent.ll7 = ctk.CTkLabel(self.pandas_Lframe, text="b)Deferred tax liabilities", font=('Aptos Black', 18))
        self.parent.ll7.grid(padx=30, pady=5, column=0, row=6, sticky='w')

        self.parent.ll8 = ctk.CTkLabel(self.pandas_Lframe, text="c)Other long term liabilities",
                                       font=('Aptos Black', 18))
        self.parent.ll8.grid(padx=30, pady=5, column=0, row=7, sticky='w')

        self.parent.ll9 = ctk.CTkLabel(self.pandas_Lframe, text="d)Long term provisions", font=('Aptos Black', 18))
        self.parent.ll9.grid(padx=30, pady=5, column=0, row=8, sticky='w')

        # Current Liabilities labels
        self.parent.ll10 = ctk.CTkLabel(self.pandas_Lframe, text="3)Current Liabilities", font=('Aharoni', 20))
        self.parent.ll10.grid(padx=10, pady=5, column=0, row=9, sticky='w')

        self.parent.ll11 = ctk.CTkLabel(self.pandas_Lframe, text='a)Short-term borrowing', font=('Aptos Black', 18))
        self.parent.ll11.grid(padx=30, pady=5, column=0, row=10, sticky='w')

        self.parent.ll12 = ctk.CTkLabel(self.pandas_Lframe, text="b)Trade payables", font=('Aptos Black', 18))
        self.parent.ll12.grid(padx=30, pady=5, column=0, row=11, sticky='w')

        self.parent.ll13 = ctk.CTkLabel(self.pandas_Lframe, text="c)Other current liabilities",
                                        font=('Aptos Black', 18))
        self.parent.ll13.grid(padx=30, pady=5, column=0, row=12, sticky='w')

        self.parent.ll14 = ctk.CTkLabel(self.pandas_Lframe, text="d)Short-term provisions", font=('Aptos Black', 18))
        self.parent.ll14.grid(padx=30, pady=5, column=0, row=13, sticky='w')

        self.parent.ll15 = ctk.CTkLabel(self.pandas_Lframe, text="Total", font=('Algerian', 25))
        self.parent.ll15.grid(padx=10, pady=10, column=0, row=14, sticky='nsew')

        # amounts year1
        # df
        lt = self.liabilities_table_pandas
        l1 = lt.iloc[0, 0]
        l2 = lt.iloc[1, 0]
        l3 = lt.iloc[2, 0]
        l4 = lt.iloc[3, 0]
        l5 = lt.iloc[4, 0]
        l6 = lt.iloc[5, 0]
        l7 = lt.iloc[6, 0]
        l8 = lt.iloc[7, 0]
        l9 = lt.iloc[8, 0]
        l10 = lt.iloc[9, 0]
        l11 = lt.iloc[10, 0]

        self.parent.lp1b = ctk.CTkLabel(self.pandas_Lframe, text=" ", font=('Aptos Black', 18))
        self.parent.lp1b.grid(padx=30, pady=5, column=1, row=2, sticky='w')

        self.parent.lp1 = ctk.CTkLabel(self.pandas_Lframe, text=l1, font=('Aptos Black', 18))
        self.parent.lp1.grid(padx=30, pady=5, column=2, row=2, sticky='w')

        self.parent.lp2 = ctk.CTkLabel(self.pandas_Lframe, text=l2, font=('Aptos Black', 18))
        self.parent.lp2.grid(padx=30, pady=5, column=2, row=3, sticky='w')

        self.parent.lp3 = ctk.CTkLabel(self.pandas_Lframe, text=l3, font=('Aptos Black', 18))
        self.parent.lp3.grid(padx=30, pady=5, column=2, row=5, sticky='w')

        self.parent.lp4 = ctk.CTkLabel(self.pandas_Lframe, text=l4, font=('Aptos Black', 18))
        self.parent.lp4.grid(padx=30, pady=5, column=2, row=6, sticky='w')

        self.parent.lp5 = ctk.CTkLabel(self.pandas_Lframe, text=l5, font=('Aptos Black', 18))
        self.parent.lp5.grid(padx=30, pady=5, column=2, row=7, sticky='w')

        self.parent.lp6 = ctk.CTkLabel(self.pandas_Lframe, text=l6, font=('Aptos Black', 18))
        self.parent.lp6.grid(padx=30, pady=5, column=2, row=8, sticky='w')

        self.parent.lp7 = ctk.CTkLabel(self.pandas_Lframe, text=l7, font=('Aptos Black', 18))
        self.parent.lp7.grid(padx=30, pady=5, column=2, row=10, sticky='w')

        self.parent.lp8 = ctk.CTkLabel(self.pandas_Lframe, text=l8, font=('Aptos Black', 18))
        self.parent.lp8.grid(padx=30, pady=5, column=2, row=11, sticky='w')

        self.parent.lp9 = ctk.CTkLabel(self.pandas_Lframe, text=l9, font=('Aptos Black', 18))
        self.parent.lp9.grid(padx=30, pady=5, column=2, row=12, sticky='w')

        self.parent.lp10 = ctk.CTkLabel(self.pandas_Lframe, text=l10, font=('Aptos Black', 18))
        self.parent.lp10.grid(padx=30, pady=5, column=2, row=13, sticky='w')

        self.parent.lp11 = ctk.CTkLabel(self.pandas_Lframe, text=l11, font=('Algerian', 25))
        self.parent.lp11.grid(padx=10, pady=10, column=2, row=14, sticky='nsew')

        # amounts year2
        # df
        lt = self.liabilities_table_pandas
        l11 = lt.iloc[0, 1]
        l12 = lt.iloc[1, 1]
        l13 = lt.iloc[2, 1]
        l14 = lt.iloc[3, 1]
        l15 = lt.iloc[4, 1]
        l16 = lt.iloc[5, 1]
        l17 = lt.iloc[6, 1]
        l18 = lt.iloc[7, 1]
        l19 = lt.iloc[8, 1]
        l110 = lt.iloc[9, 1]
        l111 = lt.iloc[10, 1]

        self.parent.lp11 = ctk.CTkLabel(self.pandas_Lframe, text=' ', font=('Aptos Black', 18))
        self.parent.lp11.grid(padx=30, pady=5, column=3, row=2, sticky='w')

        self.parent.lp11 = ctk.CTkLabel(self.pandas_Lframe, text=l11, font=('Aptos Black', 18))
        self.parent.lp11.grid(padx=30, pady=5, column=4, row=2, sticky='w')

        self.parent.lp12 = ctk.CTkLabel(self.pandas_Lframe, text=l12, font=('Aptos Black', 18))
        self.parent.lp12.grid(padx=30, pady=5, column=4, row=3, sticky='w')

        self.parent.lp13 = ctk.CTkLabel(self.pandas_Lframe, text=l13, font=('Aptos Black', 18))
        self.parent.lp13.grid(padx=30, pady=5, column=4, row=5, sticky='w')

        self.parent.lp14 = ctk.CTkLabel(self.pandas_Lframe, text=l14, font=('Aptos Black', 18))
        self.parent.lp14.grid(padx=30, pady=5, column=4, row=6, sticky='w')

        self.parent.lp15 = ctk.CTkLabel(self.pandas_Lframe, text=l15, font=('Aptos Black', 18))
        self.parent.lp15.grid(padx=30, pady=5, column=4, row=7, sticky='w')

        self.parent.lp16 = ctk.CTkLabel(self.pandas_Lframe, text=l16, font=('Aptos Black', 18))
        self.parent.lp16.grid(padx=30, pady=5, column=4, row=8, sticky='w')

        self.parent.lp17 = ctk.CTkLabel(self.pandas_Lframe, text=l17, font=('Aptos Black', 18))
        self.parent.lp17.grid(padx=30, pady=5, column=4, row=10, sticky='w')

        self.parent.lp18 = ctk.CTkLabel(self.pandas_Lframe, text=l18, font=('Aptos Black', 18))
        self.parent.lp18.grid(padx=30, pady=5, column=4, row=11, sticky='w')

        self.parent.lp19 = ctk.CTkLabel(self.pandas_Lframe, text=l19, font=('Aptos Black', 18))
        self.parent.lp19.grid(padx=30, pady=5, column=4, row=12, sticky='w')

        self.parent.lp110 = ctk.CTkLabel(self.pandas_Lframe, text=l110, font=('Aptos Black', 18))
        self.parent.lp110.grid(padx=30, pady=5, column=4, row=13, sticky='w')

        self.parent.lp111 = ctk.CTkLabel(self.pandas_Lframe, text=l111, font=('Algerian', 25))
        self.parent.lp111.grid(padx=10, pady=10, column=4, row=14, sticky='nsew')

        # amount +-
        lt['absolute + or -'] = lt.iloc[:, 1] - lt.iloc[:, 0]
        print(lt)
        lt = self.liabilities_table_pandas
        l21 = lt.iloc[0, 2]
        l22 = lt.iloc[1, 2]
        l23 = lt.iloc[2, 2]
        l24 = lt.iloc[3, 2]
        l25 = lt.iloc[4, 2]
        l26 = lt.iloc[5, 2]
        l27 = lt.iloc[6, 2]
        l28 = lt.iloc[7, 2]
        l29 = lt.iloc[8, 2]
        l210 = lt.iloc[9, 2]
        l211 = lt.iloc[10, 2]

        self.parent.lp211b = ctk.CTkLabel(self.pandas_Lframe, text='', font=('Aptos Black', 18))
        self.parent.lp211b.grid(padx=30, pady=5, column=5, row=2, sticky='w')

        self.parent.lp21b = ctk.CTkLabel(self.pandas_Lframe, text='', font=('Aptos Black', 18))
        self.parent.lp21b.grid(padx=30, pady=5, column=6, row=2, sticky='w')

        self.parent.lp21 = ctk.CTkLabel(self.pandas_Lframe, text=l21, font=('Aptos Black', 18))
        self.parent.lp21.grid(padx=30, pady=5, column=7, row=2, sticky='w')

        self.parent.lp22 = ctk.CTkLabel(self.pandas_Lframe, text=l22, font=('Aptos Black', 18))
        self.parent.lp22.grid(padx=30, pady=5, column=7, row=3, sticky='w')

        self.parent.lp23 = ctk.CTkLabel(self.pandas_Lframe, text=l23, font=('Aptos Black', 18))
        self.parent.lp23.grid(padx=30, pady=5, column=7, row=5, sticky='w')

        self.parent.lp24 = ctk.CTkLabel(self.pandas_Lframe, text=l24, font=('Aptos Black', 18))
        self.parent.lp24.grid(padx=30, pady=5, column=7, row=6, sticky='w')

        self.parent.lp25 = ctk.CTkLabel(self.pandas_Lframe, text=l25, font=('Aptos Black', 18))
        self.parent.lp25.grid(padx=30, pady=5, column=7, row=7, sticky='w')

        self.parent.lp26 = ctk.CTkLabel(self.pandas_Lframe, text=l26, font=('Aptos Black', 18))
        self.parent.lp26.grid(padx=30, pady=5, column=7, row=8, sticky='w')

        self.parent.lp27 = ctk.CTkLabel(self.pandas_Lframe, text=l27, font=('Aptos Black', 18))
        self.parent.lp27.grid(padx=30, pady=5, column=7, row=10, sticky='w')

        self.parent.lp28 = ctk.CTkLabel(self.pandas_Lframe, text=l28, font=('Aptos Black', 18))
        self.parent.lp28.grid(padx=30, pady=5, column=7, row=11, sticky='w')

        self.parent.lp29 = ctk.CTkLabel(self.pandas_Lframe, text=l29, font=('Aptos Black', 18))
        self.parent.lp29.grid(padx=30, pady=5, column=7, row=12, sticky='w')

        self.parent.lp210 = ctk.CTkLabel(self.pandas_Lframe, text=l210, font=('Aptos Black', 18))
        self.parent.lp210.grid(padx=30, pady=5, column=7, row=13, sticky='w')

        self.parent.lp211 = ctk.CTkLabel(self.pandas_Lframe, text=l211, font=('Algerian', 25))
        self.parent.lp211.grid(padx=10, pady=10, column=7, row=14, sticky='nsew')

        # percentage
        lt['percentage + or -'] = lt.iloc[:, 2] / lt.iloc[:, 0] * 100
        lt['percentage + or -'] = lt['percentage + or -'].round(1)
        print(lt)
        lt = self.liabilities_table_pandas
        l31 = lt.iloc[0, 3]
        l32 = lt.iloc[1, 3]
        l33 = lt.iloc[2, 3]
        l34 = lt.iloc[3, 3]
        l35 = lt.iloc[4, 3]
        l36 = lt.iloc[5, 3]
        l37 = lt.iloc[6, 3]
        l38 = lt.iloc[7, 3]
        l39 = lt.iloc[8, 3]
        l310 = lt.iloc[9, 3]
        l311 = lt.iloc[10, 3]

        self.parent.lp31b = ctk.CTkLabel(self.pandas_Lframe, text='', font=('Aptos Black', 18))
        self.parent.lp31b.grid(padx=30, pady=5, column=8, row=2, sticky='w')

        # self.parent.lp31b= ctk.CTkLabel(self.pandas_Lframe, text='', font=('Aptos Black', 18))
        # self.parent.lp31b.grid(padx=30, pady=5, column=9, row=2, sticky='w')

        self.parent.lp31 = ctk.CTkLabel(self.pandas_Lframe, text=l31, font=('Aptos Black', 18))
        self.parent.lp31.grid(padx=30, pady=5, column=10, row=2, sticky='w')

        self.parent.lp32 = ctk.CTkLabel(self.pandas_Lframe, text=l32, font=('Aptos Black', 18))
        self.parent.lp32.grid(padx=30, pady=5, column=10, row=3, sticky='w')

        self.parent.lp33 = ctk.CTkLabel(self.pandas_Lframe, text=l33, font=('Aptos Black', 18))
        self.parent.lp33.grid(padx=30, pady=5, column=10, row=5, sticky='w')

        self.parent.lp34 = ctk.CTkLabel(self.pandas_Lframe, text=l34, font=('Aptos Black', 18))
        self.parent.lp34.grid(padx=30, pady=5, column=10, row=6, sticky='w')

        self.parent.lp35 = ctk.CTkLabel(self.pandas_Lframe, text=l35, font=('Aptos Black', 18))
        self.parent.lp35.grid(padx=30, pady=5, column=10, row=7, sticky='w')

        self.parent.lp36 = ctk.CTkLabel(self.pandas_Lframe, text=l36, font=('Aptos Black', 18))
        self.parent.lp36.grid(padx=30, pady=5, column=10, row=8, sticky='w')

        self.parent.lp37 = ctk.CTkLabel(self.pandas_Lframe, text=l37, font=('Aptos Black', 18))
        self.parent.lp37.grid(padx=30, pady=5, column=10, row=10, sticky='w')

        self.parent.lp38 = ctk.CTkLabel(self.pandas_Lframe, text=l38, font=('Aptos Black', 18))
        self.parent.lp38.grid(padx=30, pady=5, column=10, row=11, sticky='w')

        self.parent.lp39 = ctk.CTkLabel(self.pandas_Lframe, text=l39, font=('Aptos Black', 18))
        self.parent.lp39.grid(padx=30, pady=5, column=10, row=12, sticky='w')

        self.parent.lp310 = ctk.CTkLabel(self.pandas_Lframe, text=l310, font=('Aptos Black', 18))
        self.parent.lp310.grid(padx=30, pady=5, column=10, row=13, sticky='w')

        self.parent.lp311 = ctk.CTkLabel(self.pandas_Lframe, text=l311, font=('Algerian', 25))
        self.parent.lp311.grid(padx=10, pady=10, column=10, row=14, sticky='nsew')

        # assert frame
        self.parent.pandas_frame2 = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.pandas_frame2.pack()

        self.pandas_Aframe = self.parent.pandas_frame2

        # Assert side Label
        self.parent.al1 = ctk.CTkLabel(self.pandas_Aframe, text="II.ASSETS", font=('Algerian', 25))
        self.parent.al1.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        # Non-Current Assets
        self.parent.al2 = ctk.CTkLabel(self.pandas_Aframe, text="1)Non-Current Assets", font=('Aharoni', 20))
        self.parent.al2.grid(padx=10, pady=5, column=0, row=1, sticky='w')

        self.parent.al3 = ctk.CTkLabel(self.pandas_Aframe, text="a)Fixed assets", font=('Aptos Black', 18))
        self.parent.al3.grid(padx=30, pady=5, column=0, row=2, sticky='w')

        self.parent.al4 = ctk.CTkLabel(self.pandas_Aframe, text="b)Non-current investments", font=('Aptos Black', 18))
        self.parent.al4.grid(padx=30, pady=5, column=0, row=3, sticky='w')

        self.parent.al5 = ctk.CTkLabel(self.pandas_Aframe, text="c)Deferred tax assets(net)", font=('Aptos Black', 18))
        self.parent.al5.grid(padx=30, pady=5, column=0, row=4, sticky='w')

        self.parent.al6 = ctk.CTkLabel(self.pandas_Aframe, text="d)Long-term loan and advance",
                                       font=('Aptos Black', 18))
        self.parent.al6.grid(padx=30, pady=5, column=0, row=5, sticky='w')

        self.parent.al7 = ctk.CTkLabel(self.pandas_Aframe, text="e)Other non-current assets", font=('Aptos Black', 18))
        self.parent.al7.grid(padx=30, pady=5, column=0, row=6, sticky='w')

        # Current Assets
        self.parent.al8 = ctk.CTkLabel(self.pandas_Aframe, text="2)Current Assets", font=('Aharoni', 20))
        self.parent.al8.grid(padx=10, pady=5, column=0, row=7, sticky='w')

        self.parent.al9 = ctk.CTkLabel(self.pandas_Aframe, text='a)Current investments', font=('Aptos Black', 18))
        self.parent.al9.grid(padx=30, pady=5, column=0, row=8, sticky='w')

        self.parent.al10 = ctk.CTkLabel(self.pandas_Aframe, text="b)Inventories", font=('Aptos Black', 18))
        self.parent.al10.grid(padx=30, pady=5, column=0, row=9, sticky='w')

        self.parent.al11 = ctk.CTkLabel(self.pandas_Aframe, text="c)Trade receivables", font=('Aptos Black', 18))
        self.parent.al11.grid(padx=30, pady=5, column=0, row=10, sticky='w')

        self.parent.al12 = ctk.CTkLabel(self.pandas_Aframe, text="d)Cash and cash equivalents",
                                        font=('Aptos Black', 18))
        self.parent.al12.grid(padx=30, pady=5, column=0, row=11, sticky='w')

        self.parent.al13 = ctk.CTkLabel(self.pandas_Aframe, text="e)Short term loan and advance",
                                        font=('Aptos Black', 18))
        self.parent.al13.grid(padx=30, pady=5, column=0, row=12, sticky='w')

        self.parent.al14 = ctk.CTkLabel(self.pandas_Aframe, text="f)other current assets", font=('Aptos Black', 18))
        self.parent.al14.grid(padx=30, pady=5, column=0, row=13, sticky='w')

        # Total assert
        self.parent.al15 = ctk.CTkLabel(self.pandas_Aframe, text="Total", font=('Algerian', 25))
        self.parent.al15.grid(padx=10, pady=10, column=0, row=14, sticky='nsew')

        # amounts year1 assets
        # df
        at = self.assets_table_pandas
        a1 = at.iloc[0, 0]
        a2 = at.iloc[1, 0]
        a3 = at.iloc[2, 0]
        a4 = at.iloc[3, 0]
        a5 = at.iloc[4, 0]
        a6 = at.iloc[5, 0]
        a7 = at.iloc[6, 0]
        a8 = at.iloc[7, 0]
        a9 = at.iloc[8, 0]
        a10 = at.iloc[9, 0]
        a11 = at.iloc[10, 0]
        a12 = at.iloc[11, 0]

        self.parent.ap1b = ctk.CTkLabel(self.pandas_Aframe, text=" ", font=('Aptos Black', 18))
        self.parent.ap1b.grid(padx=30, pady=5, column=1, row=2, sticky='w')

        self.parent.ap1 = ctk.CTkLabel(self.pandas_Aframe, text=a1, font=('Aptos Black', 18))
        self.parent.ap1.grid(padx=30, pady=5, column=2, row=2, sticky='w')

        self.parent.ap2 = ctk.CTkLabel(self.pandas_Aframe, text=a2, font=('Aptos Black', 18))
        self.parent.ap2.grid(padx=30, pady=5, column=2, row=3, sticky='w')

        self.parent.ap3 = ctk.CTkLabel(self.pandas_Aframe, text=a3, font=('Aptos Black', 18))
        self.parent.ap3.grid(padx=30, pady=5, column=2, row=5, sticky='w')

        self.parent.ap4 = ctk.CTkLabel(self.pandas_Aframe, text=a4, font=('Aptos Black', 18))
        self.parent.ap4.grid(padx=30, pady=5, column=2, row=6, sticky='w')

        self.parent.ap5 = ctk.CTkLabel(self.pandas_Aframe, text=a5, font=('Aptos Black', 18))
        self.parent.ap5.grid(padx=30, pady=5, column=2, row=7, sticky='w')

        self.parent.ap6 = ctk.CTkLabel(self.pandas_Aframe, text=a6, font=('Aptos Black', 18))
        self.parent.ap6.grid(padx=30, pady=5, column=2, row=8, sticky='w')

        self.parent.ap7 = ctk.CTkLabel(self.pandas_Aframe, text=a7, font=('Aptos Black', 18))
        self.parent.ap7.grid(padx=30, pady=5, column=2, row=10, sticky='w')

        self.parent.ap8 = ctk.CTkLabel(self.pandas_Aframe, text=a8, font=('Aptos Black', 18))
        self.parent.ap8.grid(padx=30, pady=5, column=2, row=11, sticky='w')

        self.parent.ap9 = ctk.CTkLabel(self.pandas_Aframe, text=a9, font=('Aptos Black', 18))
        self.parent.ap9.grid(padx=30, pady=5, column=2, row=12, sticky='w')

        self.parent.ap10 = ctk.CTkLabel(self.pandas_Aframe, text=a10, font=('Aptos Black', 18))
        self.parent.ap10.grid(padx=30, pady=5, column=2, row=13, sticky='w')

        self.parent.ap11 = ctk.CTkLabel(self.pandas_Aframe, text=a11, font=('Algerian', 25))
        self.parent.ap11.grid(padx=10, pady=10, column=2, row=14, sticky='nsew')

        self.parent.ap12 = ctk.CTkLabel(self.pandas_Aframe, text=a12, font=('Algerian', 25))
        self.parent.ap12.grid(padx=10, pady=10, column=2, row=14, sticky='nsew')

        # amounts year2 assets
        # df
        at = self.assets_table_pandas
        a11 = at.iloc[0, 1]
        a12 = at.iloc[1, 1]
        a13 = at.iloc[2, 1]
        a14 = at.iloc[3, 1]
        a15 = at.iloc[4, 1]
        a16 = at.iloc[5, 1]
        a17 = at.iloc[6, 1]
        a18 = at.iloc[7, 1]
        a19 = at.iloc[8, 1]
        a110 = at.iloc[9, 1]
        a111 = at.iloc[10, 1]
        a112 = at.iloc[11, 1]

        self.parent.ap11b = ctk.CTkLabel(self.pandas_Aframe, text=" ", font=('Aptos Black', 18))
        self.parent.ap11b.grid(padx=30, pady=5, column=3, row=2, sticky='w')

        self.parent.ap11 = ctk.CTkLabel(self.pandas_Aframe, text=a11, font=('Aptos Black', 18))
        self.parent.ap11.grid(padx=30, pady=5, column=4, row=2, sticky='w')

        self.parent.ap12 = ctk.CTkLabel(self.pandas_Aframe, text=a12, font=('Aptos Black', 18))
        self.parent.ap12.grid(padx=30, pady=5, column=4, row=3, sticky='w')

        self.parent.ap13 = ctk.CTkLabel(self.pandas_Aframe, text=a13, font=('Aptos Black', 18))
        self.parent.ap13.grid(padx=30, pady=5, column=4, row=5, sticky='w')

        self.parent.ap14 = ctk.CTkLabel(self.pandas_Aframe, text=a14, font=('Aptos Black', 18))
        self.parent.ap14.grid(padx=30, pady=5, column=4, row=6, sticky='w')

        self.parent.ap15 = ctk.CTkLabel(self.pandas_Aframe, text=a15, font=('Aptos Black', 18))
        self.parent.ap15.grid(padx=30, pady=5, column=4, row=7, sticky='w')

        self.parent.ap16 = ctk.CTkLabel(self.pandas_Aframe, text=a16, font=('Aptos Black', 18))
        self.parent.ap16.grid(padx=30, pady=5, column=4, row=8, sticky='w')

        self.parent.ap17 = ctk.CTkLabel(self.pandas_Aframe, text=a17, font=('Aptos Black', 18))
        self.parent.ap17.grid(padx=30, pady=5, column=4, row=10, sticky='w')

        self.parent.ap18 = ctk.CTkLabel(self.pandas_Aframe, text=a18, font=('Aptos Black', 18))
        self.parent.ap18.grid(padx=30, pady=5, column=4, row=11, sticky='w')

        self.parent.ap19 = ctk.CTkLabel(self.pandas_Aframe, text=a19, font=('Aptos Black', 18))
        self.parent.ap19.grid(padx=30, pady=5, column=4, row=12, sticky='w')

        self.parent.ap110 = ctk.CTkLabel(self.pandas_Aframe, text=a110, font=('Aptos Black', 18))
        self.parent.ap110.grid(padx=30, pady=5, column=4, row=13, sticky='w')

        self.parent.ap111 = ctk.CTkLabel(self.pandas_Aframe, text=a111, font=('Algerian', 25))
        self.parent.ap111.grid(padx=10, pady=10, column=4, row=14, sticky='nsew')

        self.parent.ap112 = ctk.CTkLabel(self.pandas_Aframe, text=a112, font=('Algerian', 25))
        self.parent.ap112.grid(padx=10, pady=10, column=4, row=14, sticky='nsew')

        # amount +- assets
        at['absolute + or -'] = at.iloc[:, 1] - at.iloc[:, 0]
        print(at)
        at = self.assets_table_pandas
        a21 = at.iloc[0, 2]
        a22 = at.iloc[1, 2]
        a23 = at.iloc[2, 2]
        a24 = at.iloc[3, 2]
        a25 = at.iloc[4, 2]
        a26 = at.iloc[5, 2]
        a27 = at.iloc[6, 2]
        a28 = at.iloc[7, 2]
        a29 = at.iloc[8, 2]
        a210 = at.iloc[9, 2]
        a211 = at.iloc[10, 2]
        a212 = at.iloc[11, 2]

        self.parent.ap211b = ctk.CTkLabel(self.pandas_Aframe, text=" ", font=('Aptos Black', 18))
        self.parent.ap211b.grid(padx=30, pady=5, column=5, row=2, sticky='w')

        self.parent.ap212b = ctk.CTkLabel(self.pandas_Aframe, text=" ", font=('Aptos Black', 18))
        self.parent.ap212b.grid(padx=30, pady=5, column=6, row=2, sticky='w')

        self.parent.ap21 = ctk.CTkLabel(self.pandas_Aframe, text=a21, font=('Aptos Black', 18))
        self.parent.ap21.grid(padx=30, pady=5, column=7, row=2, sticky='w')

        self.parent.ap22 = ctk.CTkLabel(self.pandas_Aframe, text=a22, font=('Aptos Black', 18))
        self.parent.ap22.grid(padx=30, pady=5, column=7, row=3, sticky='w')

        self.parent.ap23 = ctk.CTkLabel(self.pandas_Aframe, text=a23, font=('Aptos Black', 18))
        self.parent.ap23.grid(padx=30, pady=5, column=7, row=5, sticky='w')

        self.parent.ap24 = ctk.CTkLabel(self.pandas_Aframe, text=a24, font=('Aptos Black', 18))
        self.parent.ap24.grid(padx=30, pady=5, column=7, row=6, sticky='w')

        self.parent.ap25 = ctk.CTkLabel(self.pandas_Aframe, text=a25, font=('Aptos Black', 18))
        self.parent.ap25.grid(padx=30, pady=5, column=7, row=7, sticky='w')

        self.parent.ap26 = ctk.CTkLabel(self.pandas_Aframe, text=a26, font=('Aptos Black', 18))
        self.parent.ap26.grid(padx=30, pady=5, column=7, row=8, sticky='w')

        self.parent.ap27 = ctk.CTkLabel(self.pandas_Aframe, text=a27, font=('Aptos Black', 18))
        self.parent.ap27.grid(padx=30, pady=5, column=7, row=10, sticky='w')

        self.parent.ap28 = ctk.CTkLabel(self.pandas_Aframe, text=a28, font=('Aptos Black', 18))
        self.parent.ap28.grid(padx=30, pady=5, column=7, row=11, sticky='w')

        self.parent.ap29 = ctk.CTkLabel(self.pandas_Aframe, text=a29, font=('Aptos Black', 18))
        self.parent.ap29.grid(padx=30, pady=5, column=7, row=12, sticky='w')

        self.parent.ap210 = ctk.CTkLabel(self.pandas_Aframe, text=a210, font=('Aptos Black', 18))
        self.parent.ap210.grid(padx=30, pady=5, column=7, row=13, sticky='w')

        self.parent.ap211 = ctk.CTkLabel(self.pandas_Aframe, text=a211, font=('Algerian', 25))
        self.parent.ap211.grid(padx=10, pady=10, column=7, row=14, sticky='nsew')

        self.parent.ap212 = ctk.CTkLabel(self.pandas_Aframe, text=a212, font=('Algerian', 25))
        self.parent.ap212.grid(padx=10, pady=10, column=7, row=14, sticky='nsew')

        # percentage assets
        at['percentage + or -'] = at.iloc[:, 2] / at.iloc[:, 0] * 100
        at['percentage + or -'] = at['percentage + or -'].round(1)
        print(at)
        at = self.assets_table_pandas
        a31 = at.iloc[0, 3]
        a32 = at.iloc[1, 3]
        a33 = at.iloc[2, 3]
        a34 = at.iloc[3, 3]
        a35 = at.iloc[4, 3]
        a36 = at.iloc[5, 3]
        a37 = at.iloc[6, 3]
        a38 = at.iloc[7, 3]
        a39 = at.iloc[8, 3]
        a310 = at.iloc[9, 3]
        a311 = at.iloc[10, 3]
        a312 = at.iloc[11, 3]

        self.parent.ap311b = ctk.CTkLabel(self.pandas_Aframe, text=" ", font=('Aptos Black', 18))
        self.parent.ap311b.grid(padx=30, pady=5, column=8, row=2, sticky='w')

        # self.parent.ap312b= ctk.CTkLabel(self.pandas_Aframe, text=" ", font=('Aptos Black', 18))
        # self.parent.ap312b.grid(padx=30, pady=5, column=9, row=2, sticky='w')

        self.parent.ap31 = ctk.CTkLabel(self.pandas_Aframe, text=a31, font=('Aptos Black', 18))
        self.parent.ap31.grid(padx=30, pady=5, column=10, row=2, sticky='w')

        self.parent.ap32 = ctk.CTkLabel(self.pandas_Aframe, text=a32, font=('Aptos Black', 18))
        self.parent.ap32.grid(padx=30, pady=5, column=10, row=3, sticky='w')

        self.parent.ap33 = ctk.CTkLabel(self.pandas_Aframe, text=a33, font=('Aptos Black', 18))
        self.parent.ap33.grid(padx=30, pady=5, column=10, row=5, sticky='w')

        self.parent.ap34 = ctk.CTkLabel(self.pandas_Aframe, text=a34, font=('Aptos Black', 18))
        self.parent.ap34.grid(padx=30, pady=5, column=10, row=6, sticky='w')

        self.parent.ap35 = ctk.CTkLabel(self.pandas_Aframe, text=a35, font=('Aptos Black', 18))
        self.parent.ap35.grid(padx=30, pady=5, column=10, row=7, sticky='w')

        self.parent.ap36 = ctk.CTkLabel(self.pandas_Aframe, text=a36, font=('Aptos Black', 18))
        self.parent.ap36.grid(padx=30, pady=5, column=10, row=8, sticky='w')

        self.parent.ap37 = ctk.CTkLabel(self.pandas_Aframe, text=a37, font=('Aptos Black', 18))
        self.parent.ap37.grid(padx=30, pady=5, column=10, row=10, sticky='w')

        self.parent.ap38 = ctk.CTkLabel(self.pandas_Aframe, text=a38, font=('Aptos Black', 18))
        self.parent.ap38.grid(padx=30, pady=5, column=10, row=11, sticky='w')

        self.parent.ap39 = ctk.CTkLabel(self.pandas_Aframe, text=a39, font=('Aptos Black', 18))
        self.parent.ap39.grid(padx=30, pady=5, column=10, row=12, sticky='w')

        self.parent.ap310 = ctk.CTkLabel(self.pandas_Aframe, text=a310, font=('Aptos Black', 18))
        self.parent.ap310.grid(padx=30, pady=5, column=10, row=13, sticky='w')

        self.parent.ap311 = ctk.CTkLabel(self.pandas_Aframe, text=a311, font=('Algerian', 25))
        self.parent.ap311.grid(padx=10, pady=10, column=10, row=14, sticky='nsew')

        self.parent.ap312 = ctk.CTkLabel(self.pandas_Aframe, text=a312, font=('Algerian', 25))
        self.parent.ap312.grid(padx=10, pady=10, column=10, row=14, sticky='nsew')

        # matplotlib plot
        self.parent.pandas_frame3 = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.pandas_frame3.pack(pady=20)

        self.parent.p_d = ctk.CTkLabel(self.parent.pandas_frame3, text='Pie Diagram', font=('Algerian', 25))
        self.parent.p_d.pack()

        self.parent.pandas_frame4 = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3, width=600,
                                                 height=500)
        self.parent.pandas_frame4.pack(pady=20)

        self.pandas_frame_liabilities = self.parent.pandas_frame4

        # pandas data import liabilities
        self.m_t_l = self.liabilities_table_pandas

        self.lcalY1 = (self.m_t_l.iloc[10, 0] / (self.m_t_l.iloc[10, 0] + self.m_t_l.iloc[10, 1])) * 360
        self.lcalY2 = (self.m_t_l.iloc[10, 1] / (self.m_t_l.iloc[10, 0] + self.m_t_l.iloc[10, 1])) * 360

        print(self.lcalY1)
        print(self.lcalY2)

        labels = [self.column_titles_list[0], self.column_titles_list[1]]
        sizes = [self.lcalY1, self.lcalY2]
        colors = ['blue', 'green']

        # Create the pie chart using matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(sizes, labels=labels, colors=colors, autopct='%6.2F', startangle=90)
        ax.set_title('comparative statement\nTotal liabilities', fontsize=16)
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

        # Embed the matplotlib figure in the customtkinter app
        canvas = FigureCanvasTkAgg(fig, master=self.pandas_frame_liabilities)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.parent.pandas_frame5 = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3, width=600,
                                                 height=500)
        self.parent.pandas_frame5.pack(pady=20)

        self.pandas_frame_assets = self.parent.pandas_frame5

        # pandas data import assets
        self.m_t_a = self.assets_table_pandas

        self.acalY1 = (self.m_t_a.iloc[11, 0] / (self.m_t_a.iloc[11, 0] + self.m_t_a.iloc[11, 1])) * 360
        self.acalY2 = (self.m_t_a.iloc[11, 1] / (self.m_t_a.iloc[11, 0] + self.m_t_a.iloc[11, 1])) * 360

        print(self.acalY1)
        print(self.acalY2)

        labels = [self.column_titles_list[0], self.column_titles_list[1]]
        sizes = [self.acalY1, self.acalY2]
        colors = ['blue', 'green']

        # Create the pie chart using matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(sizes, labels=labels, colors=colors, autopct='%6.2F', startangle=90)
        ax.set_title('comparative statement\nTotal assets', fontsize=16)
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

        # Embed the matplotlib figure in the customtkinter app
        canvas = FigureCanvasTkAgg(fig, master=self.pandas_frame_assets)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.parent.bb = ctk.CTkButton(self.parent.outer_frame, text='Open', font=('Algerian', 25),
                                       command=self.open_again_table)
        self.parent.bb.pack(pady=20)

        self.parent.bb2 = ctk.CTkButton(self.parent.outer_frame, text='back', font=('Algerian', 25),
                                        command=self.back_page)
        self.parent.bb2.pack(pady=20)

    def open_again_table(self):
        print('Again')
        popup_pandas2 = ctk.CTkToplevel(self)
        popup_pandas2.title("open File")
        popup_pandas2.geometry("300x200")
        popup_pandas2.iconbitmap(
            "E:\\enviroments\\Graphical_Figure\\Graphical Figure app\\image\\app.ico")  # Change ctk logo

        # Label for file name entry
        label_pandas2 = ctk.CTkLabel(popup_pandas2, text="Enter the file name:")
        label_pandas2.pack(pady=10)

        # Entry box to enter file name
        file_entry_pandas2 = ctk.CTkEntry(popup_pandas2, width=200)
        file_entry_pandas2.pack(pady=5)

        # Function to get the entered file name
        def open_file2():
            file_name_pandas = file_entry_pandas2.get().strip()
            if file_name_pandas:
                try:
                    MessageBox.showinfo("File Name", f"File name '{file_name_pandas}' open")
                    popup_pandas2.destroy()  # Close the pop-up
                    find_of_file_a = f'{file_name_pandas}a.csv'
                    find_of_file_l = f'{file_name_pandas}l.csv'
                    self.assets_table_pandas = pd.read_csv(find_of_file_a)
                    self.liabilities_table_pandas = pd.read_csv(find_of_file_l)
                    print('assets')
                    print(self.assets_table_pandas)
                    print('liabilities')
                    print(self.liabilities_table_pandas)
                    # destroy balance sheet frame
                    self.parent.bb.destroy()
                    self.parent.pandas_framed.destroy()
                    self.parent.pandas_frameP.destroy()
                    self.parent.pandas_frame1.destroy()
                    self.parent.pandas_frame2.destroy()
                    self.parent.pandas_frame3.destroy()
                    self.parent.pandas_frame4.destroy()
                    self.parent.pandas_frame5.destroy()
                    self.parent.bb2.destroy()

                    popup_pandas2.after(100, self.open_pandas_file)
                except Exception as e:
                    MessageBox.showerror("Error", f"Failed to find file:\n{e}")
            else:
                MessageBox.showerror("Error", "Please enter a file name.")

        # Save button
        save_button_pandas2 = ctk.CTkButton(popup_pandas2, text="open", command=open_file2)
        save_button_pandas2.pack(pady=10)

        # Cancel button to close without saving
        cancel_button_pandas2 = ctk.CTkButton(popup_pandas2, text="Cancel", command=popup_pandas2.destroy)
        cancel_button_pandas2.pack(pady=5)

    def back_page(self):
        print('back')
        popup_again = ctk.CTkToplevel(self)
        popup_again.title("back")
        popup_again.geometry("200x150")
        popup_again.iconbitmap(
            "E:\\enviroments\\Graphical_Figure\\Graphical Figure app\\image\\app.ico")  # Change ctk logo

        # Function to get the entered file name
        def open_again():
            try:
                popup_again.destroy()  # Close the pop-up

                # destroy balance sheet frame
                self.parent.bb.destroy()
                self.parent.pandas_framed.destroy()
                self.parent.pandas_frameP.destroy()
                self.parent.pandas_frame1.destroy()
                self.parent.pandas_frame2.destroy()
                self.parent.pandas_frame3.destroy()
                self.parent.pandas_frame4.destroy()
                self.parent.pandas_frame5.destroy()
                self.parent.bb2.destroy()

                popup_again.after(100, self.again_balance_sheet)
            except Exception as e:
                MessageBox.showerror("Error", f"Failed to open again close and reopen:\n{e}")

        # Save button
        save_button_again = ctk.CTkButton(popup_again, text="yes", command=open_again)
        save_button_again.pack(pady=10)

        # Cancel button to close without saving
        cancel_button_again = ctk.CTkButton(popup_again, text="Cancel", command=popup_again.destroy)
        cancel_button_again.pack(pady=5)

    def again_balance_sheet(self):
        print('balance_sheet_again')
        self.parent.title('Giving details')
        self.parent.geometry('1200x600')
        self.parent.resizable(True, True)

        self.parent.inside_framed = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.inside_framed.pack(pady=20)

        # Add the label for "Balance Sheet as on"
        self.topic_label = ctk.CTkLabel(self.parent.inside_framed, text="Balance Sheet as on ", font=('Algerian', 25))
        self.topic_label.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        self.parent.inside_framep = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.inside_framep.pack()

        self.Pframe = self.parent.inside_framep

        self.parent.ll1 = ctk.CTkLabel(self.Pframe, text="Particulars", font=('Algerian', 25))
        self.parent.ll1.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        self.parent.ll2 = ctk.CTkLabel(self.Pframe, text="            ", font=('Algerian', 25))
        self.parent.ll2.grid(padx=10, pady=10, column=1, row=0, sticky='nsew')

        # only get int or float command
        # Validation function to allow only float input
        def validate_float_input(value):
            if value == '':  # Allow empty value
                return True
            try:
                float(value)  # Attempt to convert input to float
                int(value)
                return True
            except ValueError:
                return False

        # Register the validation function
        self.validate_command = (self.parent.register(validate_float_input), "%P")

        # Create the first entry field
        self.entry_1 = ctk.CTkEntry(self.Pframe, font=('Algerian', 25))
        self.entry_1.grid(padx=50, pady=10, column=2, row=0, sticky='e')
        self.entry_1.bind("<KeyRelease>", self.update_topic)  # Binding key release to the update method

        # Create the second entry field
        self.entry_2 = ctk.CTkEntry(self.Pframe, font=('Algerian', 25))
        self.entry_2.grid(padx=10, pady=10, column=4, row=0, sticky='e')
        self.entry_2.bind("<KeyRelease>", self.update_topic)  # Binding key release to the update method

        # liabilities Frame
        self.parent.inside_frame1 = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        self.parent.inside_frame1.pack(pady=20)

        self.Lframe = self.parent.inside_frame1

        self.parent.ll1 = ctk.CTkLabel(self.Lframe, text="I.EQUITY AND LIABILITIES", font=('Algerian', 25))
        self.parent.ll1.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        # Shareholder funds
        self.parent.ll2 = ctk.CTkLabel(self.Lframe, text="1)Shareholder's Funds", font=('Aharoni', 20))
        self.parent.ll2.grid(padx=10, pady=5, column=0, row=1, sticky='w')

        self.parent.ll3 = ctk.CTkLabel(self.Lframe, text="a)Share Capital", font=('Aptos Black', 18))
        self.parent.ll3.grid(padx=30, pady=5, column=0, row=2, sticky='w')

        self.parent.ll4 = ctk.CTkLabel(self.Lframe, text="b)Reserves and Surplus", font=('Aptos Black', 18))
        self.parent.ll4.grid(padx=30, pady=5, column=0, row=3, sticky='w')

        # Non-current liabilities labels
        self.parent.ll5 = ctk.CTkLabel(self.Lframe, text="2)Non-current Liabilities", font=('Aharoni', 20))
        self.parent.ll5.grid(padx=10, pady=5, column=0, row=4, sticky='w')

        self.parent.ll6 = ctk.CTkLabel(self.Lframe, text='a)Long term borrowing', font=('Aptos Black', 18))
        self.parent.ll6.grid(padx=30, pady=5, column=0, row=5, sticky='w')

        self.parent.ll7 = ctk.CTkLabel(self.Lframe, text="b)Deferred tax liabilities", font=('Aptos Black', 18))
        self.parent.ll7.grid(padx=30, pady=5, column=0, row=6, sticky='w')

        self.parent.ll8 = ctk.CTkLabel(self.Lframe, text="c)Other long term liabilities", font=('Aptos Black', 18))
        self.parent.ll8.grid(padx=30, pady=5, column=0, row=7, sticky='w')

        self.parent.ll9 = ctk.CTkLabel(self.Lframe, text="d)Long term provisions", font=('Aptos Black', 18))
        self.parent.ll9.grid(padx=30, pady=5, column=0, row=8, sticky='w')

        # Current Liabilities labels
        self.parent.ll10 = ctk.CTkLabel(self.Lframe, text="3)Current Liabilities", font=('Aharoni', 20))
        self.parent.ll10.grid(padx=10, pady=5, column=0, row=9, sticky='w')

        self.parent.ll11 = ctk.CTkLabel(self.Lframe, text='a)Short-term borrowing', font=('Aptos Black', 18))
        self.parent.ll11.grid(padx=30, pady=5, column=0, row=10, sticky='w')

        self.parent.ll12 = ctk.CTkLabel(self.Lframe, text="b)Trade payables", font=('Aptos Black', 18))
        self.parent.ll12.grid(padx=30, pady=5, column=0, row=11, sticky='w')

        self.parent.ll13 = ctk.CTkLabel(self.Lframe, text="c)Other current liabilities", font=('Aptos Black', 18))
        self.parent.ll13.grid(padx=30, pady=5, column=0, row=12, sticky='w')

        self.parent.ll14 = ctk.CTkLabel(self.Lframe, text="d)Short-term provisions", font=('Aptos Black', 18))
        self.parent.ll14.grid(padx=30, pady=5, column=0, row=13, sticky='w')

        self.parent.ll15 = ctk.CTkLabel(self.Lframe, text="Total", font=('Algerian', 25))
        self.parent.ll15.grid(padx=10, pady=10, column=0, row=14, sticky='nsew')

        # entry box column1 liabilities
        # shareholder funds
        self.parent.le1 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le1.grid(row=2, column=1, padx=30, pady=5, sticky='w')

        self.parent.le2 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le2.grid(row=3, column=1, padx=30, pady=5, sticky='w')

        # entry column1 Non-current liabilities
        self.parent.le3 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le3.grid(padx=30, pady=5, column=1, row=5, sticky='w')

        self.parent.le4 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le4.grid(padx=30, pady=5, column=1, row=6, sticky='w')

        self.parent.le5 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le5.grid(padx=30, pady=5, column=1, row=7, sticky='w')

        self.parent.le6 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le6.grid(padx=30, pady=5, column=1, row=8, sticky='w')

        # entry column1 Current Liabilities
        self.parent.le7 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le7.grid(padx=30, pady=5, column=1, row=10, sticky='w')

        self.parent.le8 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le8.grid(padx=30, pady=5, column=1, row=11, sticky='w')

        self.parent.le9 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.le9.grid(padx=30, pady=5, column=1, row=12, sticky='w')

        self.parent.le10 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le10.grid(padx=30, pady=5, column=1, row=13, sticky='w')

        # total liabilities column1
        self.parent.lb11 = ctk.CTkButton(self.Lframe, font=('Algerian', 25), text='Year1', command=self.LY1)
        self.parent.lb11.grid(padx=30, pady=10, column=1, row=14, sticky='w')

        # entry box year 2
        # entry Shareholder funds column2
        self.parent.le21 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le21.grid(padx=30, pady=5, column=2, row=2, sticky='w')

        self.parent.le22 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le22.grid(padx=30, pady=5, column=2, row=3, sticky='w')

        # entry column2 Non-current liabilities
        self.parent.le23 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le23.grid(padx=30, pady=5, column=2, row=5, sticky='w')

        self.parent.le24 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le24.grid(padx=30, pady=5, column=2, row=6, sticky='w')

        self.parent.le25 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le25.grid(padx=30, pady=5, column=2, row=7, sticky='w')

        self.parent.le26 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le26.grid(padx=30, pady=5, column=2, row=8, sticky='w')

        # entry column2 Current Liabilities
        self.parent.le27 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le27.grid(padx=30, pady=5, column=2, row=10, sticky='w')

        self.parent.le28 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le28.grid(padx=30, pady=5, column=2, row=11, sticky='w')

        self.parent.le29 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.le29.grid(padx=30, pady=5, column=2, row=12, sticky='w')

        self.parent.le210 = ctk.CTkEntry(self.Lframe, font=('Aptos Black', 18), validate="key",
                                         validatecommand=self.validate_command)
        self.parent.le210.grid(padx=30, pady=5, column=2, row=13, sticky='w')

        # total liabilities column2
        self.parent.lb211 = ctk.CTkButton(self.Lframe, font=('Algerian', 25), text='Year2', command=self.LY2)
        self.parent.lb211.grid(padx=30, pady=10, column=2, row=14, sticky='w')

        # assert frame
        self.parent.inside_frame2 = ctk.CTkFrame(self.parent.outer_frame, corner_radius=10, border_width=3)
        # self.parent.inside_frame2.grid(column=0,row=3,padx=20,pady=20)
        self.parent.inside_frame2.pack()

        self.Aframe = self.parent.inside_frame2

        # Assert side Label
        self.parent.al1 = ctk.CTkLabel(self.Aframe, text="II.ASSETS", font=('Algerian', 25))
        self.parent.al1.grid(padx=10, pady=10, column=0, row=0, sticky='nsew')

        # Non-Current Assets
        self.parent.al2 = ctk.CTkLabel(self.Aframe, text="1)Non-Current Assets", font=('Aharoni', 20))
        self.parent.al2.grid(padx=10, pady=5, column=0, row=1, sticky='w')

        self.parent.al3 = ctk.CTkLabel(self.Aframe, text="a)Fixed assets", font=('Aptos Black', 18))
        self.parent.al3.grid(padx=30, pady=5, column=0, row=2, sticky='w')

        self.parent.al4 = ctk.CTkLabel(self.Aframe, text="b)Non-current investments", font=('Aptos Black', 18))
        self.parent.al4.grid(padx=30, pady=5, column=0, row=3, sticky='w')

        self.parent.al5 = ctk.CTkLabel(self.Aframe, text="c)Deferred tax assets(net)", font=('Aptos Black', 18))
        self.parent.al5.grid(padx=30, pady=5, column=0, row=4, sticky='w')

        self.parent.al6 = ctk.CTkLabel(self.Aframe, text="d)Long-term loan and advance", font=('Aptos Black', 18))
        self.parent.al6.grid(padx=30, pady=5, column=0, row=5, sticky='w')

        self.parent.al7 = ctk.CTkLabel(self.Aframe, text="e)Other non-current assets", font=('Aptos Black', 18))
        self.parent.al7.grid(padx=30, pady=5, column=0, row=6, sticky='w')

        # Current Assets
        self.parent.al8 = ctk.CTkLabel(self.Aframe, text="2)Current Assets", font=('Aharoni', 20))
        self.parent.al8.grid(padx=10, pady=5, column=0, row=7, sticky='w')

        self.parent.al9 = ctk.CTkLabel(self.Aframe, text='a)Current investments', font=('Aptos Black', 18))
        self.parent.al9.grid(padx=30, pady=5, column=0, row=8, sticky='w')

        self.parent.al10 = ctk.CTkLabel(self.Aframe, text="b)Inventories", font=('Aptos Black', 18))
        self.parent.al10.grid(padx=30, pady=5, column=0, row=9, sticky='w')

        self.parent.al11 = ctk.CTkLabel(self.Aframe, text="c)Trade receivables", font=('Aptos Black', 18))
        self.parent.al11.grid(padx=30, pady=5, column=0, row=10, sticky='w')

        self.parent.al12 = ctk.CTkLabel(self.Aframe, text="d)Cash and cash equivalents", font=('Aptos Black', 18))
        self.parent.al12.grid(padx=30, pady=5, column=0, row=11, sticky='w')

        self.parent.al13 = ctk.CTkLabel(self.Aframe, text="e)Short term loan and advance", font=('Aptos Black', 18))
        self.parent.al13.grid(padx=30, pady=5, column=0, row=12, sticky='w')

        self.parent.al14 = ctk.CTkLabel(self.Aframe, text="f)other current assets", font=('Aptos Black', 18))
        self.parent.al14.grid(padx=30, pady=5, column=0, row=13, sticky='w')

        # Total assert
        self.parent.al15 = ctk.CTkLabel(self.Aframe, text="Total", font=('Algerian', 25))
        self.parent.al15.grid(padx=10, pady=10, column=0, row=14, sticky='nsew')

        # assert
        # entry box year1
        # entry NON-current Assert column1
        self.parent.ae1 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae1.grid(padx=30, pady=5, column=1, row=2, sticky='w')

        self.parent.ae2 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae2.grid(padx=30, pady=5, column=1, row=3, sticky='w')

        self.parent.ae3 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae3.grid(padx=30, pady=5, column=1, row=4, sticky='w')

        self.parent.ae4 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae4.grid(padx=30, pady=5, column=1, row=5, sticky='w')

        self.parent.ae5 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae5.grid(padx=30, pady=5, column=1, row=6, sticky='w')

        # entry column1 Current Assert
        self.parent.ae6 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae6.grid(padx=30, pady=5, column=1, row=8, sticky='w')

        self.parent.ae7 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae7.grid(padx=30, pady=5, column=1, row=9, sticky='w')

        self.parent.ae8 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae8.grid(padx=30, pady=5, column=1, row=10, sticky='w')

        self.parent.ae9 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                       validatecommand=self.validate_command)
        self.parent.ae9.grid(padx=30, pady=5, column=1, row=11, sticky='w')

        self.parent.ae10 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae10.grid(padx=30, pady=5, column=1, row=12, sticky='w')

        self.parent.ae11 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae11.grid(padx=30, pady=5, column=1, row=13, sticky='w')

        # total assert column1
        self.parent.ab12 = ctk.CTkButton(self.Aframe, font=('Algerian', 25), text='Year1', command=self.AY1)
        self.parent.ab12.grid(padx=30, pady=10, column=1, row=14, sticky='w')

        # entry box year 2
        # entry non-current assets column2
        self.parent.ae21 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae21.grid(padx=30, pady=5, column=2, row=2, sticky='w')

        self.parent.ae22 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae22.grid(padx=30, pady=5, column=2, row=3, sticky='w')

        self.parent.ae23 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae23.grid(padx=30, pady=5, column=2, row=4, sticky='w')

        self.parent.ae24 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae24.grid(padx=30, pady=5, column=2, row=5, sticky='w')

        self.parent.ae25 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae25.grid(padx=30, pady=5, column=2, row=6, sticky='w')

        # entry column2 Current Assets
        self.parent.ae26 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae26.grid(padx=30, pady=5, column=2, row=8, sticky='w')

        self.parent.ae27 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae27.grid(padx=30, pady=5, column=2, row=9, sticky='w')

        self.parent.ae28 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae28.grid(padx=30, pady=5, column=2, row=10, sticky='w')

        self.parent.ae29 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                        validatecommand=self.validate_command)
        self.parent.ae29.grid(padx=30, pady=5, column=2, row=11, sticky='w')

        self.parent.ae210 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                         validatecommand=self.validate_command)
        self.parent.ae210.grid(padx=30, pady=5, column=2, row=12, sticky='w')

        self.parent.ae211 = ctk.CTkEntry(self.Aframe, font=('Aptos Black', 18), validate="key",
                                         validatecommand=self.validate_command)
        self.parent.ae211.grid(padx=30, pady=5, column=2, row=13, sticky='w')

        # total assert column2
        self.parent.ab212 = ctk.CTkButton(self.Aframe, font=('Algerian', 25), text='Year2', command=self.AY2)
        self.parent.ab212.grid(padx=30, pady=10, column=2, row=14, sticky='w')

        # next page process button
        # button
        self.parent.npb = ctk.CTkButton(self.parent.outer_frame, text='Process', font=('Algerian', 25),
                                        command=self.Process)
        self.parent.npb.pack(pady=20)

        self.parent.npb1 = ctk.CTkButton(self.parent.outer_frame, text='Open File', font=('Algerian', 25),
                                         command=self.new_pandas_frames)
        self.parent.npb1.pack(pady=20)


app_start = App_main_window()
app_start.mainloop()
