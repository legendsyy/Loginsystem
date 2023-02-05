import customtkinter as ct
import mysql.connector
import re
import bcrypt
import codecs


root = ct.CTk()
height = 500
width = 800 
#setting windows start position to center of screen
x = (root.winfo_screenwidth()//2)-(width//2)
y = (root.winfo_screenheight()//2)-(height//2)
root.geometry('{}x{}+{}+{}'.format(width,height,x,y))
root.resizable(False, False)
root.title("")

#database connections 
cn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234", 
    database="database"
)

db  = cn.cursor()


validsymbols = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

#you need to create a database and do a query "CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, username char(50), passwd char(255))"
#setting querys to variables 
usernamequery = """SELECT * FROM Users WHERE username = %s"""
loginquery = """SELECT * FROM Users WHERE username = %s""" 
registerquery = """INSERT INTO Users (username, passwd) VALUES (%s, %s)"""
everythingquery = """SELECT * FROM Users"""
passwdquery = """SELECT passwd FROM Users"""
updatequery = """UPDATE Users SET passwd =%s WHERE username = %s"""
deletequery = """DELETE FROM Users WHERE username = %s"""


class LoginSystem(): 
    def __init__(self):
        self.loginGui()
        
    def on_login(self): # runs when login button is clicked 
        username = self.login.get().strip() # taking all spaces out of username
        password = self.passw.get() 
        db.execute(loginquery, (username,)) # executing login query with username variable
        if db.fetchall(): # checking username exists in database
            db.execute(passwdquery) # executing passwd query
            for xi in db.fetchall():
                passwords = xi[0]
                if bcrypt.checkpw(password.encode('utf-8'), passwords.encode('utf-8')): # checking hashed password against inputted password
                    self.loginframe.forget()
                    Main(username, password) # calling to main class and passing username and password
                    break
                else: 
                    self.failemail.place(relx = 0.5, rely = 0.645, anchor = ct.CENTER)
        else: 
            self.failemail.place(relx = 0.5, rely = 0.645, anchor = ct.CENTER)
    
    def on_register_click(self): # runs when register button is clicked
        self.loginframe.forget()
        RegisterSystem() # calling register system
    
    
    def logincheckbox_event(self): # runs when show password checkbox is clicked
        if self.passwordcheck_status.get() == 1: # if pressed it shows password else not
            self.passw.configure(show = '')
        else:
            self.passw.configure(show = '*')
        
        
    def loginGui(self): # declaration of GUI
        # giving all colors which needed
        self.DARKPURPLE = "#404258"
        self.PURPLE = "#474E68"
        self.LIGHTPURPLE = "#6B728E"
        self.WHITEPURPLE = "#50577A"
        self.ICECOLOR= "#E3F6FF"
        self.LIGHTRED = "#ffc6c4"
        root.config(bg = self.PURPLE)
        
        self.loginframe = ct.CTkFrame(master=root, fg_color=self.LIGHTPURPLE, bg_color=self.PURPLE)
        self.loginframe.pack(padx = 40, pady = 40, fill="both", expand = True,)
        
        self.passwordcheck_status = ct.IntVar()
        
        logintext = ct.CTkLabel(master = self.loginframe, 
                                text = "Login", 
                                font =("Arial",30), 
                                text_color=self.ICECOLOR)
        logintext.place(relx = 0.5, rely = 0.22, anchor = ct.CENTER)
        
        self.login = ct.CTkEntry(master = self.loginframe, 
                                 placeholder_text = "example@gmail.com", 
                                 width = 200, height=35, fg_color=self.WHITEPURPLE, 
                                 border_color=self.DARKPURPLE, 
                                 placeholder_text_color=self.ICECOLOR,
                                 text_color=self.ICECOLOR,)
        self.login.place(relx = 0.5, rely = 0.4, anchor = ct.CENTER)
        
        self.passw = ct.CTkEntry(master = self.loginframe, 
                                 placeholder_text = "Example1234", 
                                 show="*", 
                                 width=200, 
                                 height=35, 
                                 fg_color=self.WHITEPURPLE, 
                                 border_color=self.DARKPURPLE, 
                                 placeholder_text_color=self.ICECOLOR, 
                                 text_color=self.ICECOLOR)
        self.passw.place(relx = 0.5, rely = 0.58, anchor = ct.CENTER)

        self.failemail = ct.CTkLabel(master = self.loginframe, 
                                     text = "Email or password is invalid", 
                                     font=("Arial", 11), 
                                     text_color=self.LIGHTRED, 
                                     height=2) 
        
        showpassbox = ct.CTkCheckBox(master = self.loginframe, 
                                     text = "Show password", 
                                     command = self.logincheckbox_event, 
                                     variable = self.passwordcheck_status, 
                                     checkbox_height=15, 
                                     checkbox_width=15, 
                                     hover_color=self.WHITEPURPLE, 
                                     text_color=self.ICECOLOR, 
                                     border_color=self.ICECOLOR, 
                                     fg_color=self.DARKPURPLE)
        showpassbox.place(relx = 0.5, rely = 0.8, anchor = ct.CENTER)
        
        loginlabel = ct.CTkLabel(master = self.loginframe, 
                                 text = "Email*", 
                                 font=("Arial", 14, "bold"), 
                                 text_color=self.ICECOLOR, 
                                 height=2,)      
        loginlabel.place(relx = 0.39, rely = 0.32, anchor = ct.CENTER)

        passwordlabel = ct.CTkLabel(master = self.loginframe, 
                                    text = "Password*", 
                                    font=("Arial", 14, "bold"),
                                    text_color=self.ICECOLOR, 
                                    height=2, )      
        passwordlabel.place(relx = 0.41, rely = 0.5, anchor = ct.CENTER)
        
        loginbutton = ct.CTkButton(master = self.loginframe, 
                                   text = "Login", 
                                   command = self.on_login, 
                                   text_color=self.ICECOLOR, 
                                   fg_color=self.DARKPURPLE, 
                                   width= 95, 
                                   hover_color=self.WHITEPURPLE) 
        loginbutton.place(relx = 0.575, rely = 0.7, anchor = ct.CENTER)
        
        registerbutton = ct.CTkButton(master = self.loginframe, 
                                      text = "Register", 
                                      command =self.on_register_click, 
                                      text_color=self.ICECOLOR, 
                                      fg_color=self.DARKPURPLE, 
                                      width= 95, 
                                      hover_color=self.WHITEPURPLE) 
        registerbutton.place(relx = 0.425, rely = 0.7, anchor = ct.CENTER)
        
        root.mainloop()



class RegisterSystem():
    def __init__(self, ): 
        self.RegisterGui()
    
    
    def on_return(self): # runs when return button is clicked
        self.registerframe.forget()
        LoginSystem()
        
    def on_confirm_click(self): # runs when  confirm button is clicked
        self.faillabel.configure(text = "") # setting fail label to empty string every time confirm button is clicked
        username = self.username.get() # setting entered username to a variable 
        hashedpass = bcrypt.hashpw(self.passwdre.get().encode(), bcrypt.gensalt()) # hashing the entered password
        encoded = codecs.decode(hashedpass) # decoding the hashed password

        usrpass = [username, encoded] # creating a list to store the username and encoded password
        username1 = [self.username.get()] 

        db.execute(usernamequery, username1)

        
        if db.fetchall() == []: # checking if the username already exists in the database
            if re.fullmatch(validsymbols, self.username.get()): # checking if the entered username is valid
                if self.passwdre.get() == self.passwdreconf.get():  # checking if the entered passwords match
                    if len(self.passwdre.get()) >= 8: # checking if the entered password is longer than 8 characters
                        db.execute(registerquery, usrpass) # executing the register query
                        cn.commit()
                        self.ConfirmGui() # calling the ConfirmGui function
                    else: 
                        self.faillabel.configure(text = "Password too short") # runs if the entered password is shorter than 8 characters
                else: 
                    self.faillabel.configure(text = "Passwords do not match") # runs if the entered passwords do not match
            else: 
                self.faillabel.configure(text = "Invalid email address") # runs if the entered email address is invalid
        else:  
            self.faillabel.configure(text = "Email has already been used") # runs if the entered email address has already been used
        
        
        
    
    def registercheckbox_event(self): # runs when showpassword checkbox is clicked
        if self.passwordcheck_status.get() == 1: # if showpassword checkbox is checked shows password else not 
            self.passwdre.configure(show = '')
            self.passwdreconf.configure(show = '')
        else:
            self.passwdre.configure(show = '*')
            self.passwdreconf.configure(show = '*')


            
    def on_loginclick(self): # runs when login button is clicked and returns to login frame
        self.registerframe.forget()
        self.app.destroy() 
        LoginSystem() 
    
    def on_exitclick(self): # runs when exitbutton is clicked in confirmframe and destroys every window
        self.app.destroy()
        root.destroy()

    
    def ConfirmGui(self): # confirmgui, which runs after a successful registration
        self.app = ct.CTk()
        self.app.geometry("250x200")
        self.app.resizable(False, False)
        self.app.title("")
        self.app.config(bg = self.PURPLE)
        
        confirmframe = ct.CTkFrame(master = self.app, fg_color=self.LIGHTPURPLE, bg_color=self.PURPLE)
        confirmframe.pack(padx = 10, pady = 10, fill = "both", expand = True)
        
        self.confirmloginbutton  = ct.CTkButton(master = confirmframe, 
                                                text = "Login", 
                                                command=self.on_loginclick, 
                                                text_color=self.ICECOLOR, 
                                                fg_color=self.DARKPURPLE, 
                                                width= 95, 
                                                hover_color=self.WHITEPURPLE)
        self.confirmexitbutton  = ct.CTkButton(master = confirmframe, text = "Exit", command=self.on_exitclick, text_color=self.ICECOLOR, fg_color=self.DARKPURPLE, width= 95, hover_color=self.WHITEPURPLE)
        
        self.confirmloginbutton.place(relx = 0.52, rely = 0.6, anchor = ct.W)
        self.confirmexitbutton.place(relx = 0.48, rely = 0.6, anchor = ct.E)
        
        self.questionlabel = ct.CTkLabel(master = confirmframe, text = "Do you want to login or exit?", font=("Arial", 14, "bold"), text_color=self.ICECOLOR) 
        self.questionlabel.place(relx = 0.5, rely = 0.3, anchor = ct.CENTER)
        
        
        self.app.mainloop()
        
    
    
    def RegisterGui(self): # Registergui 
        self.DARKPURPLE = "#404258"
        self.PURPLE = "#474E68"
        self.LIGHTPURPLE= "#6B728E"
        self.WHITEPURPLE = "#50577A"
        self.ICECOLOR= "#E3F6FF"
        self.LIGHTRED = "#ffc6c4"
        
        
        self.registerframe = ct.CTkFrame(master=root, fg_color=self.LIGHTPURPLE, bg_color=self.PURPLE)
        self.registerframe.pack(padx = 40, pady = 40, fill="both", expand = True, )
        
        self.passwordcheck_status = ct.IntVar()
        
        logintext = ct.CTkLabel(master = self.registerframe, text = "Register", font =("Arial",30), text_color=self.ICECOLOR)
        logintext.place(relx = 0.5, rely = 0.1, anchor = ct.CENTER)

        self.username = ct.CTkEntry(master = self.registerframe, 
                                    placeholder_text = "Username", 
                                    width = 200, height=35, 
                                    fg_color=self.WHITEPURPLE, 
                                    border_color=self.DARKPURPLE, 
                                    placeholder_text_color=self.ICECOLOR, 
                                    text_color= self.ICECOLOR)
        self.username.place(relx = 0.5, rely = 0.29, anchor = ct.CENTER)
        self.passwdre = ct.CTkEntry(master = self.registerframe, 
                                    placeholder_text = "Min 8. characters", 
                                    show="*", 
                                    width=200, 
                                    height=35, 
                                    fg_color=self.WHITEPURPLE, 
                                    border_color=self.DARKPURPLE, 
                                    placeholder_text_color=self.ICECOLOR, 
                                    text_color= self.ICECOLOR)
        self.passwdre.place(relx = 0.5, rely = 0.46, anchor = ct.CENTER)
        self.passwdreconf = ct.CTkEntry(master = self.registerframe, 
                                        placeholder_text = "Min 8. characters", 
                                        show="*", 
                                        width=200, 
                                        height=35, 
                                        fg_color=self.WHITEPURPLE, 
                                        border_color=self.DARKPURPLE, 
                                        placeholder_text_color=self.ICECOLOR, 
                                        text_color= self.ICECOLOR)
                                 
        self.passwdreconf.place(relx = 0.5, rely = 0.63, anchor = ct.CENTER)
        
        confirmlabel = ct.CTkLabel(master = self.registerframe, text = "Confirm password*", font=("Arial", 14, "bold"),text_color=self.ICECOLOR, height=2)
        confirmlabel.place(relx = 0.45, rely = 0.55, anchor=ct.CENTER)
        passwdconfirmlabel = ct.CTkLabel(master = self.registerframe, text = "Password*", font=("Arial", 14, "bold"),text_color=self.ICECOLOR, height=2)
        passwdconfirmlabel.place(relx = 0.41, rely = 0.38, anchor = ct.CENTER)
        usernamelabel = ct.CTkLabel(master = self.registerframe, text = "Username*", font=("Arial", 14, "bold"),text_color=self.ICECOLOR, height=2)
        usernamelabel.place(relx = 0.36, rely = 0.19)
        
        
        showpassbox = ct.CTkCheckBox(master = self.registerframe, text = "Show password", command = self.registercheckbox_event, variable = self.passwordcheck_status, 
                                     checkbox_height=15, checkbox_width=15, hover_color=self.WHITEPURPLE, text_color=self.ICECOLOR, border_color=self.ICECOLOR, fg_color=self.DARKPURPLE)

        showpassbox.place(relx = 0.5, rely = 0.85, anchor = ct.CENTER)
        
        self.faillabel = ct.CTkLabel(master = self.registerframe, text="", font=("Arial", 11), text_color=self.LIGHTRED, height=2) 
        self.faillabel.place(relx = 0.36, rely = 0.695, anchor = ct.W)
        


        
        self.confirm = ct.CTkButton(master = self.registerframe, text = "Confirm", command = self.on_confirm_click, text_color=self.ICECOLOR, fg_color=self.DARKPURPLE, width= 95, hover_color=self.WHITEPURPLE) 
        self.confirm.place(relx = 0.575, rely = 0.75, anchor = ct.CENTER)
        self.returnbutton = ct.CTkButton(master = self.registerframe, text = "Return", command = self.on_return,text_color=self.ICECOLOR, fg_color=self.DARKPURPLE, width= 95, hover_color=self.WHITEPURPLE) 
        self.returnbutton.place(relx = 0.425, rely = 0.75, anchor = ct.CENTER)

    
        root.mainloop()
        

class Main(): 
    def __init__(self, username, password):  #setting passed variables to a self variable  and calling to main function 
        self.username = username
        self.password = password
        self.main()
        
    def logout(self): # runs when logout button is clicked 
        self.mainframe.forget()
        LoginSystem() 
    
    def delete_account(self): # runs when delete account button is clicked 
        if self.deleteacc.get() == self.password: # checks if password is correct 
            db.execute(deletequery, (self.username,)) # deletes the account
            cn.commit()
            self.confirmGui("Account has been deleted") # calling confirmGui and passing a label text 
        else:
            self.deleterror.configure(text = "Incorrect password") # runs if password is incorrect 
  
    def change_password(self): 
        hashedpass = bcrypt.hashpw(self.newpassword.get().encode(), bcrypt.gensalt()) # hashing the newpassword 
        if self.changepassword.get() == self.password: # checks if password is correct 
            if len(self.newpassword.get()) >= 8: #checking if the entered password is longer than 8 characters
                db.execute(updatequery, (hashedpass, self.username,)) # inserting new password into the database 
                self.password = self.newpassword.get() # setting the new password into a variable because if user tries to change password again it updates the needed password to the new on
                cn.commit()
                self.confirmGui("Password changed") # cllaing confirmGui and passing a label text 
            else: 
                self.changerror.configure(text = "Password must be at least 8 characters") # runs if password is shorter than 8 characters 
        else: 
            self.changerror.configure(text = "Incorrect password") # runs if password is incorrect 


    def confirmreturn(self):
        self.confirm.destroy()
        self.mainframe.forget()
        LoginSystem()


    def confirmGui(self, e): 
        self.confirm = ct.CTk()
        self.confirm.geometry("250x200")
        self.confirm.resizable(False, False)
        self.confirm.title("")
        self.confirm.config(bg = self.PURPLE)
        self.confirmframe = ct.CTkFrame(master = self.confirm, fg_color=self.LIGHTPURPLE, bg_color=self.PURPLE)
        self.confirmframe.pack(padx = 10, pady = 10, fill = "both", expand = True)
        self.button = ct.CTkButton(master = self.confirmframe, text = "OK",text_color=self.ICECOLOR, fg_color=self.DARKPURPLE, width= 95, hover_color=self.WHITEPURPLE, command=self.confirmreturn) 
        self.button.place(relx = 0.5, rely = 0.6, anchor = ct.CENTER)
        self.label = ct.CTkLabel(master = self.confirmframe, text=e, font=("Arial", 18, "bold"), text_color=self.ICECOLOR) 
        self.label.place(relx = 0.5, rely = 0.4, anchor = ct.CENTER)
        
        self.confirm.mainloop()

    
        

        
    def main(self): #Main Gui

        self.DARKPURPLE = "#404258"
        self.PURPLE = "#474E68"
        self.LIGHTPURPLE= "#6B728E"
        self.WHITEPURPLE = "#50577A"
        self.ICECOLOR= "#E3F6FF"
        self.LIGHTRED = "#ffc6c4"
        root.config(bg = self.PURPLE)

        
        
        self.mainframe = ct.CTkFrame(master=root, fg_color=self.LIGHTPURPLE, bg_color=self.PURPLE)
        self.mainframe.pack(padx = 40, pady = 40, fill="both", expand = True,)
        
        self.welcomelabel = ct.CTkLabel(master = self.mainframe, text = "Welcome ", font=("Arial", 40, "bold"),text_color=self.ICECOLOR) 
        self.welcomelabel.place(relx = 0.5, rely = 0.05, anchor = ct.N) 
        self.changerror = ct.CTkLabel(master = self.mainframe, text = "", font=("Arial", 11) ,text_color=self.LIGHTRED, height=2, width=95) 
        self.changerror.place(relx = 0.235, rely = 0.77, anchor = ct.CENTER) 
        self.deleterror = ct.CTkLabel(master = self.mainframe, text = "", font=("Arial", 11) ,text_color=self.LIGHTRED, height=2, width=95) 
        self.deleterror.place(relx = 0.765, rely = 0.67, anchor = ct.CENTER) 
        self.loggedinlable = ct.CTkLabel(master = self.mainframe, text = f"Logged in as: {self.username}", font=("Arial", 20,),text_color=self.ICECOLOR) 
        self.loggedinlable.place(relx = 0.5, rely = 0.2, anchor = ct.N) 
        self.changelabel = ct.CTkLabel(master = self.mainframe, text = "Change password ", font=("Arial", 15, "bold"),text_color=self.ICECOLOR)
        self.changelabel.place(relx = 0.15, rely = 0.4, anchor =  ct.W) 
        self.changepassword = ct.CTkEntry(master = self.mainframe, 
                                    placeholder_text = "Current password", 
                                    width=200, 
                                    show="*", 
                                    height=35, 
                                    fg_color=self.WHITEPURPLE, 
                                    border_color=self.DARKPURPLE, 
                                    placeholder_text_color=self.ICECOLOR, 
                                    text_color= self.ICECOLOR)
        self.changepassword.place(relx = 0.1, rely = 0.5, anchor = ct.W)
        self.newpassword = ct.CTkEntry(master = self.mainframe, 
                            placeholder_text = "New password", 
                            show="*", 
                            width=200, 
                            height=35, 
                            fg_color=self.WHITEPURPLE, 
                            border_color=self.DARKPURPLE, 
                            placeholder_text_color=self.ICECOLOR, 
                            text_color= self.ICECOLOR)
        self.newpassword.place(relx = 0.1, rely = 0.6, anchor = ct.W)
        self.changebutton = ct.CTkButton(master = self.mainframe, text = "Change",text_color=self.ICECOLOR, 
                                         fg_color=self.DARKPURPLE, width= 95, hover_color=self.WHITEPURPLE, command = self.change_password) 
        self.changebutton.place(relx = 0.17, rely = 0.7, anchor = ct.W)
        self.deleteacc = ct.CTkEntry(master = self.mainframe, 
                            placeholder_text = "Password", 
                            width=200, 
                            height=35, 
                            show="*", 
                            fg_color=self.WHITEPURPLE, 
                            border_color=self.DARKPURPLE, 
                            placeholder_text_color=self.ICECOLOR, 
                            text_color= self.ICECOLOR)
        self.deleteacc.place(relx = 0.9, rely = 0.5, anchor = ct.E)
        self.changelabel = ct.CTkLabel(master = self.mainframe,  text = "Delete account ", font=("Arial", 15, "bold"),text_color=self.ICECOLOR)
        self.changelabel.place(relx = 0.85, rely = 0.4, anchor =  ct.E) 
        self.deletebutton = ct.CTkButton(master = self.mainframe, text = "Delete",text_color=self.ICECOLOR, fg_color=self.DARKPURPLE, width= 95, hover_color=self.WHITEPURPLE, command = self.delete_account)
        self.deletebutton.place(relx = 0.83, rely = 0.6, anchor = ct.E)
        self.logoutbutton = ct.CTkButton(master = self.mainframe, text = "Logout",text_color=self.ICECOLOR, fg_color=self.DARKPURPLE, width= 95, hover_color=self.WHITEPURPLE, command = self.logout) 
        self.logoutbutton.place(relx = 0.99, rely = 0.02, anchor = ct.NE)
        root.mainloop()
        


if __name__ == "__main__":
    login = LoginSystem()
    