import tkinter as tk

Window = tk.Tk()
Window.geometry("700x700")

LoginFrame = tk.Frame(Window, bg="#0A0A2A")
LoginFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

ForgotPasswordFrame = tk.Frame(Window, bg="#0A0A2A")
CreateAccountFrame = tk.Frame(Window, bg="#0A0A2A")
def construct(typeOfFrame ,typeOfWidget, textOfLabel, Xaxis, Yaxis, sizeOfLabel):
    if typeOfWidget == "Label":

        widget = tk.Label(typeOfFrame,
                               text = textOfLabel,
                               font=("Agency FB", sizeOfLabel, "bold"),
                               bg = "#0A0A2A")

        widget.place(x = Xaxis, y = Yaxis)
        return widget

    elif typeOfWidget == "Entry":
        widget = tk.Entry(typeOfFrame,
                               text= textOfLabel,
                               font=("Agency FB", sizeOfLabel, "bold"),
                               bg="#A9A9A9")

        widget.place(x=Xaxis, y=Yaxis)
        return widget

def clickable_label(typeOfFrame, textOfLabel, Xaxis, Yaxis, sizeOfLabel):
    LabelClick = construct(typeOfFrame, "Label", textOfLabel, Xaxis, Yaxis, sizeOfLabel)
    LabelClick.configure(cursor = "hand2")
    LabelClick.bind("<Button-1>")
    return LabelClick

LogInLabel = construct(LoginFrame, "Label", "Log In", 275, 50, 50)
UsernameLabel = construct(LoginFrame, "Label", "Username", 120, 225, 25)
UsernameEntry = construct(LoginFrame, "Entry", "Username", 125, 275, 25)
PasswordLabel = construct(LoginFrame, "Label", "Password", 120, 325, 25)
PasswordEntry = construct(LoginFrame, "Entry", "Password", 125, 375, 25)

ForgotPasswordLabel = clickable_label(LoginFrame, "Forgot Password?",  235, 500, 25)
CreateAccountLabel = clickable_label(LoginFrame, "Create account", 235, 550, 25)

Window.mainloop()