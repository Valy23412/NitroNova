import tkinter as tk

Window = tk.Tk()
Window.geometry("700x700")
Window.title("NitroNova")

LoginFrame = tk.Frame(Window, bg="#0A0A2A")
LoginFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

ForgotPasswordFrame = tk.Frame(Window, bg="#0A0A2A")
CreateAccountFrame = tk.Frame(Window, bg="#0A0A2A")

### Creating Frames and the main Window ###

def construct(typeOfFrame ,typeOfWidget, textOfLabel, Xaxis, Yaxis, sizeOfWidget):
    if typeOfWidget == "Label":
        widget = tk.Label(typeOfFrame,
                          text=textOfLabel,
                          font=("Agency FB", sizeOfWidget, "bold"),
                          bg="#0A0A2A")

    elif typeOfWidget == "Entry":
        widget = tk.Entry(typeOfFrame,
                          text=textOfLabel,
                          font=("Agency FB", sizeOfWidget, "bold"),
                          bg="#A9A9A9")

    elif typeOfWidget == "Button":
        widget = tk.Button(typeOfFrame,
                           text=textOfLabel,
                           font=("Agency FB", sizeOfWidget, "bold"),
                           bg="#40E0D0")

    widget.place(x=Xaxis, y=Yaxis)
    return widget


def clickable_label(typeOfFrame, textOfLabel, Xaxis, Yaxis, sizeOfWidget):
    LabelClick = construct(typeOfFrame, "Label", textOfLabel, Xaxis, Yaxis, sizeOfWidget)
    LabelClick.configure(cursor = "hand2")
    LabelClick.bind("<Button-1>")
    return LabelClick

### Functions that allow me to create different widgets + clickable labels ###

def change_frame(target):
    LoginFrame.place_forget()
    if target == "Forgot Password?":
        ForgotPasswordFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)
    elif target == "Create Account":
        CreateAccountFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

### Function that enables frames to be swaped ###

def GoBackToLogInFrame(currentFrame):
    if currentFrame == "CreateAccountFrame":
        CreateAccountFrame.place_forget()
    LoginFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

LogInLabel = construct(LoginFrame, "Label", "Log In", 275, 50, 50)
UsernameLabel = construct(LoginFrame, "Label", "Username", 120, 175, 25)
UsernameEntry = construct(LoginFrame, "Entry", "Username", 125, 225, 25)
PasswordLabel = construct(LoginFrame, "Label", "Password", 120, 275, 25)
PasswordEntry = construct(LoginFrame, "Entry", "Password", 125, 325, 25)
LogInButton = construct(LoginFrame, "Button", "Log In", 245, 475, 25)
LogInButton.configure(width = 15)

ForgotPasswordLabel = clickable_label(LoginFrame, "Forgot Password?",  270, 550, 20)
ForgotPasswordLabel.bind("<Button-1>", lambda frame: change_frame("Forgot Password?"))
CreateAccountLabel = clickable_label(LoginFrame, "Create account", 270, 585, 20)
CreateAccountLabel.bind("<Button-1>", lambda frame: change_frame("Create Account"))

### All login features and widgets being created ###
table = [
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

entries = {}

for labelText, Xaxis, Yaxis in table:
    construct(CreateAccountFrame, "Label", labelText, Xaxis, Yaxis, 20)
    entries[labelText] = construct(CreateAccountFrame, "Entry", labelText, Xaxis, Yaxis+ 40, 20)

CreateAccountLabelPage = construct(CreateAccountFrame, "Label", "Create Account", 50, 20, 50)
NextButton = construct(CreateAccountFrame, "Button", ">>", 500, 600, 25)
NextButton.configure(width = 14, command = lambda: GoBackToLogInFrame("CreateAccountFrame"))

### Created the "Create Account" Frame" ###

Window.mainloop()