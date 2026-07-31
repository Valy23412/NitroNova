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
SubmitButton = construct(LoginFrame, "Button", "Log In", 245, 475, 25)
SubmitButton.configure(width = 15)

ForgotPasswordLabel = clickable_label(LoginFrame, "Forgot Password?",  270, 550, 20)
ForgotPasswordLabel.bind("<Button-1>", lambda frame: change_frame("Forgot Password?"))
CreateAccountLabel = clickable_label(LoginFrame, "Create account", 270, 585, 20)
CreateAccountLabel.bind("<Button-1>", lambda frame: change_frame("Create Account"))

### All login features and widgets being created ###

CreateAccountLabelPage = construct(CreateAccountFrame, "Label", "Create Account", 50, 20, 50)
FirstNameLabel = construct(CreateAccountFrame, "Label", "First Name", 50 , 150, 20)
FirstNameEntry = construct(CreateAccountFrame, "Entry", "First Name", 50, 190, 20)
LastNameLabel = construct(CreateAccountFrame, "Label", "Last Name", 50, 230, 20)
LastNameEntry = construct(CreateAccountFrame, "Entry", "Last Name", 50, 270, 20)
EmailAddressLabel = construct(CreateAccountFrame, "Label", "Email Address", 50, 310, 20)
EmailAddressEntry = construct(CreateAccountFrame, "Entry", "Email Address", 50, 350, 20)
PasswordLabel = construct(CreateAccountFrame, "Label", "Password", 50, 390, 20)
PasswordEntry = construct(CreateAccountFrame, "Entry", "Password", 50, 430, 20)
ConfirmPasswordLabel = construct(CreateAccountFrame, "Label", "Confirm Password", 50, 470, 20)
ConfirmPasswordEntry = construct(CreateAccountFrame, "Entry", "Confirm Password", 50, 510, 20)
NextButton = construct(CreateAccountFrame, "Button", ">>", 500, 600, 25)
NextButton.configure(width = 14, command = lambda: GoBackToLogInFrame("CreateAccountFrame"))

### Created the "Create Account" Frame" ###

Window.mainloop()