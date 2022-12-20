from tkinter import *
from tkinter import messagebox
from functools import partial

CREDS =  [["admin","password1"],["nene","password2"]]

#Define a new function to open the window
def open_mainWindow():
	mainWindow = Tk()
	mainWindow.geometry("750x250")
	mainWindow.title("New Window")

	#Create a Label in New window
	Label(mainWindow, text="Hey, Howdy?", font=('Helvetica 17 bold')).pack(pady=30)

	mainWindow.mainloop()

def validateLogin(loginWindow, username, password):
	print("username entered :", username.get())
	print("password entered :", password.get())
	for i in CREDS:
		if username.get() == i[0] :
			if password.get() == i[1] :
				messagebox.showinfo(title='Correct', message='Username and Password correct')
				loginWindow.destroy()
				open_mainWindow()
				break
			else:
				messagebox.showerror(tittle=None, message='Username and Password incorrect')
				break
		if i[0] == CREDS [-1][0] :
			messagebox.showerror(tittle=None, message='Username and Password incorrect')
	return

def loginWin():
	#window
	loginWindow = Tk()  
	loginWindow.geometry('400x150')  
	loginWindow.title('Login Form')

	#username label and text entry box
	usernameLabel = Label(loginWindow, text="User Name").grid(row=0, column=0)
	username = StringVar()
	usernameEntry = Entry(loginWindow, textvariable=username).grid(row=0, column=1)  

	#password label and password entry box
	passwordLabel = Label(loginWindow,text="Password").grid(row=1, column=0)  
	password = StringVar()
	passwordEntry = Entry(loginWindow, textvariable=password, show='*').grid(row=1, column=1)  

	x = partial(validateLogin,loginWindow, username, password)

	#login button
	loginButton = Button(loginWindow, text="Login", command=x).grid(row=4, column=0)

	loginWindow.mainloop()



loginWin()