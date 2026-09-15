import tkinter as tk
import sqlite3
import hashlib
import tkinter.messagebox



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

    def get_security_questions(self, email):
        connection = self.connectDatabase()
        Query = connection.execute("""SELECT security_question_1, security_answer_1, 
                                    security_question_2, security_answer_2
                                    FROM users
                                    WHERE email = ?""", [email])
        Row = Query.fetchone()
        connection.close()
        return Row
        ### Retrieves the security questions needed for the 'Forgot Password' process ###

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

    def update_password(self, email, newHash):
        ### Updates the password hash for a user identified by email ###
        connection = self.connectDatabase()
        connection.execute("""UPDATE users SET password_hash = ?
                              WHERE email = ?""", (newHash, email))
        connection.commit()
        connection.close()

### Database class which contains different methods ###



def email_checker(Email, errorpage):
    if Email == "":
        errorpage.configure(text="Email cannot be blank")
        return False

    if Email.count("@") != 1:
        errorpage.configure(text="Email must contain exactly one @")
        return False

    AtPosition = Email.find("@")
    if Email.startswith("@"):
        errorpage.configure(text="Email must start with a name")
        return False

    DotPosition = Email.find(".", AtPosition + 1)
    if DotPosition == -1:
        errorpage.configure(text="Email must contain a dot after the @")
        return False

    DomainPart = Email[AtPosition + 1:].lower()
    if DomainPart.startswith("gmail") == False and DomainPart.startswith("yahoo") == False:
        errorpage.configure(text="Email must use gmail or yahoo")
        return False

    if DomainPart.endswith(".com") == False and DomainPart.endswith(".uk") == False:
        errorpage.configure(text="Email must end with .com or .uk")
        return False

    return True




def forgot_password_step1():
    ForgotErrorLabel.configure(text="")

    Email = EmailAddressEntry.get().strip()
    ConfirmEmail = ConfirmEmailAddressEntry.get().strip()

    if Email == "" or ConfirmEmail == "":
        ForgotErrorLabel.configure(text="Please fill in both email fields")
        return

    if Email != ConfirmEmail:
        ForgotErrorLabel.configure(text="Email addresses do not match")
        return

    ### REUSING your email_checker here ###
    if email_checker(Email, ForgotErrorLabel) == False:
        return

    global CurrentUserQuestions
    global CurrentUserEmail
    CurrentUserQuestions = DB.get_security_questions(Email)
    CurrentUserEmail = Email

    if CurrentUserQuestions is None:
        ForgotErrorLabel.configure(text="No account found with that email")
        return

    ### Loads the questions onto Frame 2 before switching ###
    ForgotPasswordQuestion1.configure(text=CurrentUserQuestions[0])
    ForgotPasswordQuestion2.configure(text=CurrentUserQuestions[2])

    change_frame(ForgotPasswordFrame1, ForgotPasswordFrame2)




def forgot_password_step2():
    ForgotErrorLabel2.configure(text="") ### Clears any previous error ###

    Answer1 = ForgotPasswordAnswer1.get().strip()
    Answer2 = ForgotPasswordAnswer2.get().strip()

    if Answer1 == "" or Answer2 == "":
        ForgotErrorLabel2.configure(text="Please answer both questions")
        return

    CorrectAnswer1 = CurrentUserQuestions[1].lower()
    CorrectAnswer2 = CurrentUserQuestions[3].lower()

    if Answer1.lower() != CorrectAnswer1 or Answer2.lower() != CorrectAnswer2:
        ForgotErrorLabel2.configure(text="Incorrect answers")
        return

    ### Answers match — go to step 3 to set new password ###
    change_frame(ForgotPasswordFrame2, ForgotPasswordFrame3)



def forgot_password_step3():
    ForgotErrorLabel3.configure(text="") ### Clears any previous error ###

    NewPassword = NewPasswordEntry.get()
    ConfirmNewPassword = ConfirmNewPasswordEntry.get()

    if NewPassword == "" or ConfirmNewPassword == "":
        ForgotErrorLabel3.configure(text="Please fill in both password fields")
        return

    ### Reuses the SAME password rules and validation as create_account ###
    PasswordHash = validate_and_hash_password(NewPassword, ConfirmNewPassword, ForgotErrorLabel3)
    if PasswordHash is None:
        return

    ### Update the database and redirect to Login ###
    DB.update_password(CurrentUserEmail, PasswordHash)

    ### Clear the entries so they don't stay visible ###
    NewPasswordEntry.delete(0, tk.END)
    ConfirmNewPasswordEntry.delete(0, tk.END)

    ### Redirect to Login ###
    change_frame(ForgotPasswordFrame3, LoginFrame)



def validate_and_hash_password(Password, ConfirmPassword, errorpage):
    ### Shared password rules used by create_account AND forgot_password_step3 ###
    if Password != ConfirmPassword:
        errorpage.configure(text="Passwords do not match")
        return None

    if len(Password) < 8:
        errorpage.configure(text="Password must be at least 8 characters")
        return None

    UppercaseFound = False
    LowercaseFound = False
    NumberFound = False

    ### Look through every character in the password ###
    for Character in Password:
        if Character.isupper():
            UppercaseFound = True
        if Character.islower():
            LowercaseFound = True
        if Character.isdigit():
            NumberFound = True

    if UppercaseFound == False:
        errorpage.configure(text="Password needs at least one capital letter")
        return None

    if LowercaseFound == False:
        errorpage.configure(text="Password needs at least one lowercase letter")
        return None

    if NumberFound == False:
        errorpage.configure(text="Password needs at least one number")
        return None

    ### Hash the password and returns it ###
    PasswordBytes = Password.encode()
    Scrambled = hashlib.sha256(PasswordBytes)
    return Scrambled.hexdigest()

def create_account():
    CreateAccountErrorLabel.configure(text="") ### Ensures no previous error message is being shown ###

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

    ### Storing all the information we get it from the user ###

    if (FirstName == "" or LastName == "" or Email == "" or Password == "" or ConfirmPassword == "" or Username == "" or SecurityQuestion1 == "" or SecurityAnswer1 == "" or SecurityQuestion2 == "" or SecurityAnswer2 == ""):
        CreateAccountErrorLabel.configure(text="Ensure no fields are left blank")
        return
    ### Making sure no fields are blank ###

    if email_checker(Email, CreateAccountErrorLabel) == False:
        return
    ### It checks the email address ###

    ### Validate the password and get the hash ###
    PasswordHash = validate_and_hash_password(Password, ConfirmPassword, CreateAccountErrorLabel)
    if PasswordHash is None:
        return

    ### Save to the database using the Database class ###
    Saved = DB.insert_user(FirstName, LastName, Username, Email, PasswordHash,
                           SecurityQuestion1, SecurityAnswer1, SecurityQuestion2, SecurityAnswer2)

    if Saved == False:
        CreateAccountErrorLabel.configure(text="Username or email already taken")
        return


    ### Only navigate on success ###
    change_frame(CreateAccountFrame, LoginFrame)

### function which validates the information given, then stores it in the database ###



def login():
    LoginErrorLabel.configure(text="") ### Ensures no previous error message is being shown ###

    Username = UsernameEntry.get().strip()
    Password = PasswordEntry.get()

    ### Check if the fields are empty ###
    if Username == "" or Password == "":
        LoginErrorLabel.configure(text="Please fill in all fields")
        return

    ### Hash the typed password (same blender as registration) ###
    PasswordBytes = Password.encode()
    Scrambled = hashlib.sha256(PasswordBytes)
    PasswordHash = Scrambled.hexdigest()

    ### Does the username exist? ###
    Row = DB.get_password_hash(Username)
    if Row is None:
        LoginErrorLabel.configure(text="Username not found")
        return

    ### Does the hash match? ###
    if Row[0] != PasswordHash:
        LoginErrorLabel.configure(text="Incorrect password")
        return

    ### Access granted that allows the user to reach Home ###
    Window.geometry("1200x700")
    change_frame(LoginFrame, HomePageFrame)

### Function that deals with the Log In authentication ###

def logout():
    Result = tk.messagebox.askyesno("Log Out", "Are you sure you want to log out?")
    if Result == True:
        Window.geometry("700x700")
        change_frame(HomePageFrame, LoginFrame)

### Functions that makes sure the user wants to log out ###

def search_focus_in(Event):
    if SearchBar.get() == "Search songs, artists...":
        SearchBar.delete(0, tk.END)
        SearchBar.configure(fg="#E8FFF0")

def search_focus_out(Event):
    if SearchBar.get() == "":
        SearchBar.insert(0, "Search songs, artists...")
        SearchBar.configure(fg="#808080")

### Functions that allows me to put text in the search bar, that dissapears when the user clicks onn it ###


DB = Database(r"C:\Users\valen\Desktop\NitroNova.db")
DB.create_table() ### One Database object shared by the whole app ###

CurrentUserQuestions = None ### Stores the security questions & answers fetched in step 1 ###
CurrentUserEmail = None ### Stores the email so step 3 can update the right account ###

Window = tk.Tk()
Window.geometry("700x700")
Window.title("NitroNova")

LoginFrame = tk.Frame(Window, bg="#0A0A2A")
LoginFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

ForgotPasswordFrame1 = tk.Frame(Window, bg="#0A0A2A")
ForgotPasswordFrame2 = tk.Frame(Window, bg="#0A0A2A")
ForgotPasswordFrame3 = tk.Frame(Window, bg="#0A0A2A")
CreateAccountFrame = tk.Frame(Window, bg="#0A0A2A")
HomePageFrame = tk.Frame(Window, bg="#2C3863")
ProfileFrame = tk.Frame(Window, bg="#0A0A2A")
SettingsFrame = tk.Frame(Window, bg="#0A0A2A")

### Windows and frames are created ###


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
                           bg="#40E0D0",
                           cursor="hand2")

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
PasswordEntry.configure(show = "•")
LogInButton = construct(LoginFrame, "Button", "Log In", 245, 475, 25)
LogInButton.configure(width = 14, command = login)

ForgotPasswordLabel = construct(LoginFrame, "Label", "Forgot Password?", 270, 550, 20, clickable=True)
ForgotPasswordLabel.bind("<Button-1>", lambda frame: change_frame(LoginFrame, ForgotPasswordFrame1))
CreateAccountLabel = construct(LoginFrame, "Label", "Create account", 270, 585, 20, clickable=True)
CreateAccountLabel.bind("<Button-1>", lambda frame: change_frame(LoginFrame, CreateAccountFrame))

LoginErrorLabel = construct(LoginFrame, "Label", "", 120, 370, 18)
LoginErrorLabel.configure(fg = "#FF5555")

### All Log In page features and widgets being created ###



LabelTable = [
    ("First Name", 50, 150), ("Last Name", 50, 230), ("Email Address", 50, 310),
    ("Password", 50, 390), ("Confirm Password", 50, 470), ("Username", 400, 150),
    ("Security Question 1", 400, 230), ("Correct Answer 1", 400, 310),
    ("Security Question 2", 400, 390), ("Correct Answer 2", 400, 470)]

     ### Create a table with all the features I want to implement on ###
     ### the 'Create Account' page, so I can loop and place them on the Frame ###

EntryTable = {}

for labelText, Xaxis, Yaxis in LabelTable:
    construct(CreateAccountFrame, "Label", labelText, Xaxis, Yaxis, 20)
    EntryTable[labelText] = construct(CreateAccountFrame, "Entry", labelText, Xaxis, Yaxis+ 40, 20)

### Entries stores all the Entry widgets after the for loop iterates through my LabelTable table and places them on the frame

CreateAccountLabelPage = construct(CreateAccountFrame, "Label", "Create Account", 50, 20, 50)
NextButton = construct(CreateAccountFrame, "Button", ">>", 400, 600, 25)
NextButton.configure(width = 14, command = create_account)

EntryTable["Password"].configure(show = "•")
EntryTable["Confirm Password"].configure(show = "•")

CreateAccountErrorLabel = construct(CreateAccountFrame, "Label", "", 50, 550, 18)
CreateAccountErrorLabel.configure(fg ="#FF5555")

### Created the "Create Account" Frame" ###



ForgotPasswordTitle = construct(ForgotPasswordFrame1, "Label", "Forgot Password", 50, 20, 50)
EmailAddressLabel = construct(ForgotPasswordFrame1, "Label", "Email Address", 50, 150, 30)
EmailAddressEntry = construct(ForgotPasswordFrame1, "Entry", "Email Address", 50, 210, 30)
ConfirmEmailAddressLabel = construct(ForgotPasswordFrame1, "Label", "Confirm Email Address", 50, 270, 30)
ConfirmEmailAddressEntry = construct(ForgotPasswordFrame1, "Entry", "Confirm Email Address", 50, 330, 30)

EmailAddressPageButton = construct(ForgotPasswordFrame1, "Button", ">>", 500, 600, 25)
EmailAddressPageButton.configure(width = 14, command = forgot_password_step1)

BackToLogInButton = construct(ForgotPasswordFrame1, "Button", "<<", 300, 600, 25)
BackToLogInButton.configure(width = 14, command = lambda: change_frame(ForgotPasswordFrame1, LoginFrame))

ForgotErrorLabel = construct(ForgotPasswordFrame1, "Label", "", 50, 390, 18)
ForgotErrorLabel.configure(fg = "#FF5555")

### Created the 1st "Forgot Password" Frame that will use the email address to search the security questions in the database ###

ForgotPasswordTitle2 = construct(ForgotPasswordFrame2, "Label", "Answer Security Questions", 50, 20, 40)

ForgotPasswordQuestion1 = construct(ForgotPasswordFrame2, "Label", "", 50, 150, 25)
ForgotPasswordAnswer1 = construct(ForgotPasswordFrame2, "Entry", "", 50, 210, 25)

ForgotPasswordQuestion2 = construct(ForgotPasswordFrame2, "Label", "", 50, 300, 25)
ForgotPasswordAnswer2 = construct(ForgotPasswordFrame2, "Entry", "", 50, 360, 25)

ForgotErrorLabel2 = construct(ForgotPasswordFrame2, "Label", "", 50, 420, 18)
ForgotErrorLabel2.configure(fg = "#FF5555")


SecurityQuestionsButton = construct(ForgotPasswordFrame2, "Button", ">>", 500, 600, 25)
SecurityQuestionsButton.configure(width = 14, command = forgot_password_step2)

BackToForgotPasswordButton = construct(ForgotPasswordFrame2, "Button", "<<", 300, 600, 25)
BackToForgotPasswordButton.configure(width = 14, command = lambda: change_frame(ForgotPasswordFrame2, ForgotPasswordFrame1))

### Created the 2nd "Forgot Password" Frame that will ask the user the 2 security questions.
### It will be created after my database is created, so I can extract the information
### The user is then redirected to Frame 3 to set a new password ###

ForgotPasswordTitle3 = construct(ForgotPasswordFrame3, "Label", "Set New Password", 50, 20, 40)

NewPasswordLabel = construct(ForgotPasswordFrame3, "Label", "New Password", 50, 150, 25)
NewPasswordEntry = construct(ForgotPasswordFrame3, "Entry", "New Password", 50, 210, 25)
NewPasswordEntry.configure(show = "•")

ConfirmNewPasswordLabel = construct(ForgotPasswordFrame3, "Label", "Confirm New Password", 50, 300, 25)
ConfirmNewPasswordEntry = construct(ForgotPasswordFrame3, "Entry", "Confirm New Password", 50, 360, 25)
ConfirmNewPasswordEntry.configure(show = "•")

ForgotErrorLabel3 = construct(ForgotPasswordFrame3, "Label", "", 50, 420, 18)
ForgotErrorLabel3.configure(fg = "#FF5555")

ResetPasswordButton = construct(ForgotPasswordFrame3, "Button", ">>", 500, 600, 25)
ResetPasswordButton.configure(width = 14, command = forgot_password_step3)

BackToSecurityQuestionsButton = construct(ForgotPasswordFrame3, "Button", "<<", 300, 600, 25)
BackToSecurityQuestionsButton.configure(width = 14, command = lambda: change_frame(ForgotPasswordFrame3, ForgotPasswordFrame2))

### Created the 3rd "Forgot Password" Frame where the user sets their new password.
### On success, the database is updated and the user returns to Login ###

HeaderFrame = tk.Frame(HomePageFrame, bg="#0A0A2A", height=60)
HeaderFrame.place(x=175, y=0, relwidth=1)
HeaderFrame.pack_propagate(False)

SuggestedFrame = tk.Frame(HomePageFrame, bg="#0A0A2A")
SuggestedFrame.place(x=175, y=62, relwidth=1, height=180)

PlaylistsFrame = tk.Frame(HomePageFrame, bg="#0A0A2A")
PlaylistsFrame.place(x=175, y=242, relwidth=1, height=396)

PlayerBar = tk.Frame(HomePageFrame, bg="#0A0A2A", height=60)
PlayerBar.place(x=175, y=640, relwidth=1)
PlayerBar.pack_propagate(False)



Divider1 = tk.Frame(HomePageFrame, bg="#1A1A4A", height=4)
Divider1.place(x=175, y=60, relwidth=1)

Divider2 = tk.Frame(HomePageFrame, bg="#1A1A4A", height=4)
Divider2.place(x=175, y=242, relwidth=1)

Divider3 = tk.Frame(HomePageFrame, bg="#1A1A4A", height=4)
Divider3.place(x=175, y=636, relwidth=1)

### Splits the main home page into different subsections that organises the app ###


SearchBar = tk.Entry(HomePageFrame, font=("Agency FB", 25), bg="#2c3863", fg="#000000", insertbackground="#E8FFF0", bd=0,highlightthickness=0)
SearchBar.place(x=200, y=10, width=300, height=40)
SearchBar.insert(0, "Search songs, artists...")
SearchBar.bind("<FocusIn>", search_focus_in)
SearchBar.bind("<FocusOut>", search_focus_out)

### Setting up the search bar ###

SidebarTitleLabel = tk.Label(HomePageFrame, text="NitroNova", font=("Agency FB", 35, "bold"), bg = "#2C3863")
SidebarTitleLabel.place(x=10, y=15)
SidebarDivider = tk.Frame(HomePageFrame, bg="#000000", width=4)
SidebarDivider.place(x=175, y=0, height=700)

ProfileLabel = tk.Label(HomePageFrame, text="Profile", font=("Agency FB", 20, "bold"), bg="#2c3863", cursor="hand2")
ProfileLabel.place(x=10, y=120)
ProfileLabel.bind("<Button-1>", lambda e: change_frame(HomePageFrame, ProfileFrame))

SettingsLabel = tk.Label(HomePageFrame, text="Settings", font=("Agency FB", 20, "bold"), bg="#2c3863", cursor="hand2")
SettingsLabel.place(x=10, y=150)
SettingsLabel.bind("<Button-1>", lambda e: change_frame(HomePageFrame, SettingsFrame))

SearchButton = tk.Button(HomePageFrame, text="🔎", font=("Segoe UI Emoji", 16), bg="#2c3863", fg="#E8FFF0", bd=0, cursor="hand2")
SearchButton.place(x=520, y=12, width=40, height=36)

LogoutLabel = tk.Label(HomePageFrame, text="Log Out", font=("Agency FB", 20, "bold"), bg="#2c3863", cursor="hand2")
LogoutLabel.place(x=10, y=660)
LogoutLabel.bind("<Button-1>", lambda e: logout())

PreviousButton = tk.Button(PlayerBar, text="⏮", font=("Segoe UI Emoji", 22), bg="#0A0A2A", fg="#E8FFF0", bd=0, cursor="hand2")
PreviousButton.place(x=10, y=10, width=40, height=40)

PlayButton = tk.Button(PlayerBar, text="▶", font=("Segoe UI Emoji", 22), bg="#0A0A2A", fg="#E8FFF0", bd=0, cursor="hand2")
PlayButton.place(x=55, y=10, width=40, height=40)

NextButton = tk.Button(PlayerBar, text="⏭", font=("Segoe UI Emoji", 22), bg="#0A0A2A", fg="#E8FFF0", bd=0, cursor="hand2")
NextButton.place(x=100, y=10, width=40, height=40)

MoreButton = tk.Button(PlayerBar, text="⋯", font=("Segoe UI Emoji", 22), bg="#2c3863", fg="#E8FFF0", bd=0, cursor="hand2")
MoreButton.place(x=900, y=10, width=40, height=40)

ExpandButton = tk.Button(PlayerBar, text="▲", font=("Segoe UI Emoji", 22), bg="#2c3863", fg="#E8FFF0", bd=0, cursor="hand2")
ExpandButton.place(x=950, y=10, width=40, height=40)

ProfileBackButton = construct(ProfileFrame, "Button", "<< Back", 20, 20, 20)
ProfileBackButton.configure(width=10, command=lambda: change_frame(ProfileFrame, HomePageFrame))

SettingsBackButton = construct(SettingsFrame, "Button", "<< Back", 20, 20, 20)
SettingsBackButton.configure(width=10, command=lambda: change_frame(SettingsFrame, HomePageFrame))
### Developed "Home Page" Frame ###

Window.mainloop()