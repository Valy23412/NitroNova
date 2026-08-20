import tkinter as tk
import sqlite3
import hashlib

class Database:
    def __init__(self, path):
        self.Path = path

    def connectDatabase(self):
        return sqlite3.connect(self.Path)
        ### Open a connection ###

    def create_table(self):
        connection = self.connectDatabase()
        connection.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            security_question_1 TEXT,
            security_answer_1 TEXT,
            security_question_2 TEXT,
            security_answer_2 TEXT
        );""")
        connection.commit()
        connection.close()
        ### Create the users table if it doesn't exist ###

    def get_password_hash(self, username):
        connection = self.connectDatabase()
        Query = connection.execute("""SELECT password_hash
                                      FROM users 
                                      WHERE username = ?""",
                                   [username])
        Row = Query.fetchone()
        connection.close()
        return Row
        ### Finds the stored hashed password for a username. If none are found, None is returned ###

    def insert_user(self, firstName, lastName, username, email, passwordHash, securityQ1, securityA1, securityQ2, securityA2):
        connection = self.connectDatabase()
        try:
            connection.execute("""INSERT INTO users
                               (first_name, last_name, username, email, password_hash, security_question_1, security_answer_1, security_question_2, security_answer_2)
                                VALUES 
                               (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (firstName, lastName, username, email, passwordHash, securityQ1, securityA1, securityQ2, securityA2))
            connection.commit()
            Saved = True

        except sqlite3.IntegrityError:
            Saved = False

        connection.close()
        return Saved

def create_account():
    FirstName = EntryTable["First Name"].get().strip()
    LastName = EntryTable["Last Name"].get().strip()
    Email = EntryTable["Email Address"].get().strip()
    Password = EntryTable["Password"].get()
    ConfirmPassword = EntryTable["Confirm Password"].get()
    Username = EntryTable["Username"].get().strip()
    SecurityQuestion1 = EntryTable["Security Question 1"].get().strip()
    SecurityAnswer1 = EntryTable["Correct Answer 1"].get().strip()
    SecurityQuestion2 = EntryTable["Security Question 2"].get().strip()
    SecurityAnswer2 = EntryTable["Correct Answer 2"].get().strip()

    ### Storing all the information we get from the user ###

    if (FirstName == "" or LastName == "" or Email == "" or Password == "" or ConfirmPassword == "" or Username == "" or SecurityQuestion1 == ""
        or SecurityAnswer1 == "" or SecurityQuestion2 == "" or SecurityAnswer2 == ""):
        print("Please fill in all fields")
        return
        ### Making sure no fields are blank ###

    if Password != ConfirmPassword:
        print("Passwords do not match")
        return
        ### Checking if the passwords match ###

    PasswordBytes = Password.encode()  #Turn the password into bytes
    Scrambled = hashlib.sha256(PasswordBytes)  #Blend
    PasswordHash = Scrambled.hexdigest()  #Blend into text to store

    ### Save to the database using the Database class ###
    if not DB.insert_user(FirstName, LastName, Username, Email, PasswordHash,
                          SecurityQuestion1, SecurityAnswer1, SecurityQuestion2, SecurityAnswer2):
        print("Username or email already taken")
        return

    ### Only navigate on success ###
    change_frame(CreateAccountFrame, LoginFrame)

def login():
    Username = UsernameEntry.get().strip()
    Password = PasswordEntry.get()

    ### Check if the fields are empty ###
    if Username == "" or Password == "":
        print("Please fill in all fields")
        return

    ### Hash the typed password (same blender as registration) ###
    PasswordBytes = Password.encode()
    Scrambled = hashlib.sha256(PasswordBytes)
    PasswordHash = Scrambled.hexdigest()

    ### Does the username exist? ###
    Row = DB.get_password_hash(Username)
    if Row is None:
        print("Username not found")
        return

    ### Does the hash match? ###
    if Row[0] != PasswordHash:
        print("Incorrect password")
        return

    ### Access granted that allows the user to reach Home ###
    change_frame(LoginFrame, HomePageFrame)

### One Database object shared by the whole app ###
DB = Database(r"C:\Users\valen\Desktop\NitroNova.db")
DB.create_table()

Window = tk.Tk()
Window.geometry("700x700")
Window.title("NitroNova")

LoginFrame = tk.Frame(Window, bg="#0A0A2A")
LoginFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

ForgotPasswordFrame1 = tk.Frame(Window, bg="#0A0A2A")
ForgotPasswordFrame2 = tk.Frame(Window, bg="#0A0A2A")
CreateAccountFrame = tk.Frame(Window, bg="#0A0A2A")
HomePageFrame = tk.Frame(Window, bg="#0A0A2A")

def construct(typeOfFrame, typeOfWidget, textOfLabel, Xaxis, Yaxis, sizeOfWidget, clickable=False):
    if typeOfWidget == "Label":
        widget = tk.Label(typeOfFrame,
                          text=textOfLabel,
                          font=("Agency FB", sizeOfWidget, "bold"),
                          fg="#E8FFF0",
                          bg="#0A0A2A")

    elif typeOfWidget == "Entry":
        widget = tk.Entry(typeOfFrame,
                          font=("Agency FB", sizeOfWidget, "bold"),
                          bg="#A9A9A9")

    elif typeOfWidget == "Button":
        widget = tk.Button(typeOfFrame,
                           text=textOfLabel,
                           font=("Agency FB", sizeOfWidget, "bold"),
                           bg="#40E0D0")

    if clickable and typeOfWidget == "Label":
        widget.configure(cursor="hand2")

    widget.place(x=Xaxis, y=Yaxis)
    return widget

### Function that allow me to create different widgets + clickable labels ###

def change_frame(current, target):
    current.place_forget()
    target.place(x= 0, y= 0, relwidth= 1, relheight= 1)

### Function that enables frames to be swaped, needs 2 parameters: One for the current frame, and the other for the frame you want to switch to ###

LogInLabel = construct(LoginFrame, "Label", "Log In", 275, 50, 50)
UsernameLabel = construct(LoginFrame, "Label", "Username", 120, 175, 25)
UsernameEntry = construct(LoginFrame, "Entry", "Username", 125, 225, 25)
PasswordLabel = construct(LoginFrame, "Label", "Password", 120, 275, 25)
PasswordEntry = construct(LoginFrame, "Entry", "Password", 125, 325, 25)
LogInButton = construct(LoginFrame, "Button", "Log In", 245, 475, 25)
LogInButton.configure(width = 14, command = login)

ForgotPasswordLabel = construct(LoginFrame, "Label", "Forgot Password?", 270, 550, 20, clickable=True)
ForgotPasswordLabel.bind("<Button-1>", lambda frame: change_frame(LoginFrame, ForgotPasswordFrame1))
CreateAccountLabel = construct(LoginFrame, "Label", "Create account", 270, 585, 20, clickable=True)
CreateAccountLabel.bind("<Button-1>", lambda frame: change_frame(LoginFrame, CreateAccountFrame))

### All login features and widgets being created ###

LabelTable = [
    ("First Name", 50, 150),
    ("Last Name", 50, 230),
    ("Email Address", 50, 310),
    ("Password", 50, 390),
    ("Confirm Password", 50, 470),
    ("Username", 400, 150),
    ("Security Question 1", 400, 230),
    ("Correct Answer 1", 400, 310),
    ("Security Question 2", 400, 390),
    ("Correct Answer 2", 400, 470),
]

### Create a table with all the features I want to implement on the 'Create Account' page, so I can loop and place them on the Frame

EntryTable = {}

for labelText, Xaxis, Yaxis in LabelTable:
    construct(CreateAccountFrame, "Label", labelText, Xaxis, Yaxis, 20)
    EntryTable[labelText] = construct(CreateAccountFrame, "Entry", labelText, Xaxis, Yaxis+ 40, 20)

### Entries stores all the Entry widgets after the for loop iterates through my LabelTable table and places them on the frame

CreateAccountLabelPage = construct(CreateAccountFrame, "Label", "Create Account", 50, 20, 50)
NextButton = construct(CreateAccountFrame, "Button", ">>", 400, 600, 25)
NextButton.configure(width = 14, command = create_account)

### Created the "Create Account" Frame" ###

ForgotPasswordTitle = construct(ForgotPasswordFrame1, "Label", "Forgot Password", 50, 20, 50)
EmailAddressLabel = construct(ForgotPasswordFrame1, "Label", "Email Address", 50, 150, 30)
EmailAddressEntry = construct(ForgotPasswordFrame1, "Entry", "Email Address", 50, 210, 30)
ConfirmEmailAddressLabel = construct(ForgotPasswordFrame1, "Label", "Confirm Email Address", 50, 270, 30)
ConfirmEmailAddressEntry = construct(ForgotPasswordFrame1, "Entry", "Confirm Email Address", 50, 330, 30)

EmailAddressPageButton = construct(ForgotPasswordFrame1, "Button", ">>", 500, 600, 25)
EmailAddressPageButton.configure(width = 14, command = lambda: change_frame(ForgotPasswordFrame1, ForgotPasswordFrame2))

BackToLogInButton = construct(ForgotPasswordFrame1, "Button", "<<", 300, 600, 25)
BackToLogInButton.configure(width = 14, command = lambda: change_frame(ForgotPasswordFrame1, LoginFrame))

### Created the 1st "Forgot Password" Frame that will use the email address to search the security questions in the database ###

SecurityQuestionsButton = construct(ForgotPasswordFrame2, "Button", ">>", 500, 600, 25)
SecurityQuestionsButton.configure(width = 14, command = lambda: change_frame(ForgotPasswordFrame2, LoginFrame))

BackToForgotPasswordButton = construct(ForgotPasswordFrame2, "Button", "<<", 300, 600, 25)
BackToForgotPasswordButton.configure(width = 14, command = lambda: change_frame(ForgotPasswordFrame2, ForgotPasswordFrame1))

### Created the 2nd "Forgot Password" Frame that will ask the user the 2 security questions.
### It will be created after my database is created, so I can extract the information
### The user is then redirected to the Log-In page so they can use their credentials to enter NitroNova

HomePageLabel = construct(HomePageFrame, "Label", "Home Page", 50, 20, 50)
BackFromHomePageButton = construct(HomePageFrame, "Button", "<<", 500, 600, 25)
BackFromHomePageButton.configure(width = 14, command = lambda: change_frame(HomePageFrame, LoginFrame))

### Created "Home Page" Frame ###

Window.mainloop()