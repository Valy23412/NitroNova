import tkinter as tk
import sqlite3

Window = tk.Tk()
Window.geometry("700x700")
Window.title("NitroNova")

LoginFrame = tk.Frame(Window, bg="#0A0A2A")
LoginFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

ForgotPasswordFrame1 = tk.Frame(Window, bg="#0A0A2A")
ForgotPasswordFrame2 = tk.Frame(Window, bg="#0A0A2A")
CreateAccountFrame = tk.Frame(Window, bg="#0A0A2A")
HomePageFrame = tk.Frame(Window, bg="#0A0A2A")

### Creating Frames and the main Window ###

def construct(typeOfFrame ,typeOfWidget, textOfLabel, Xaxis, Yaxis, sizeOfWidget, clickable = False):
    if typeOfWidget == "Label":
        widget = tk.Label(typeOfFrame,
                          text=textOfLabel,
                          font=("Agency FB", sizeOfWidget, "bold"),
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
        widget.bind("<Button-1>")

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
LogInButton.configure(width = 14, command = lambda: change_frame(LoginFrame, HomePageFrame))

ForgotPasswordLabel = construct(LoginFrame,"Label",  "Forgot Password?",  270, 550, 20, clickable = True)
ForgotPasswordLabel.bind("<Button-1>", lambda frame: change_frame(LoginFrame, ForgotPasswordFrame1))
CreateAccountLabel = construct(LoginFrame, "Label", "Create account", 270, 585, 20, clickable = True)
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
            ### Create a table with all the features I want to implement on the 'Create Account'
            ### Page, so I can loop and place them on the Frame

EntryTable = {}

for labelText, Xaxis, Yaxis in LabelTable:
    construct(CreateAccountFrame, "Label", labelText, Xaxis, Yaxis, 20)
    EntryTable[labelText] = construct(CreateAccountFrame, "Entry", labelText, Xaxis, Yaxis+ 40, 20)

            ### entries stores all the Entry widgets after the for loop iterates through my LabelTable
            ### table and places them on the frame

CreateAccountLabelPage = construct(CreateAccountFrame, "Label", "Create Account", 50, 20, 50)
NextButton = construct(CreateAccountFrame, "Button", ">>", 500, 600, 25)
NextButton.configure(width = 14, command = lambda: change_frame(CreateAccountFrame, LoginFrame))

### Created the "Create Account" Frame" ###

ForgotPasswordTitle = construct(ForgotPasswordFrame1, "Label", "Forgot Password", 50, 20, 50)
EmailAddressLabel = construct(ForgotPasswordFrame1, "Label", "Email Address", 50, 150, 30)
EmailAddressEntry = construct(ForgotPasswordFrame1, "Entry", "Email Address", 50, 210, 30)
ConfirmEmailAddressLabel = construct(ForgotPasswordFrame1, "Label", "Confirm Email Address", 50, 270, 30)
ConfirmEmailAddressEntry = construct(ForgotPasswordFrame1, "Entry", "Confirm Email Address", 50, 330, 30)

EmailAddressButton = construct(ForgotPasswordFrame1, "Button", ">>", 500, 600, 25)
EmailAddressButton.configure(width = 14, command = lambda: change_frame(ForgotPasswordFrame1, ForgotPasswordFrame2))

### Created the 1st "Forgot Password" Frame that will use the email address to search the security questions in the database ###

SecurityQuestionsButton = construct(ForgotPasswordFrame2, "Button", ">>", 500, 600, 25)
SecurityQuestionsButton.configure(width = 14, command = lambda: change_frame(ForgotPasswordFrame2, LoginFrame))

### Created the 2nd "Forgot Password" Frame that will ask the user the 2 security questions.
### It will be created after my database is created, so I can extract the information
### The user is then redirected to the Log-In page so they can use their credentials to enter NitroNova

HomePageLabel = construct(HomePageFrame, "Label", "Home Page", 50, 20, 50)

### Created "Home Page" Frame ###
connection = sqlite3.connect(r"C:\Users\valen\Desktop\NitroNova.db")
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

### Created database ###Users/valen/Pychram
Window.mainloop()