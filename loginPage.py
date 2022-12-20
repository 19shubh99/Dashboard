from tkinter import *
from tkinter import messagebox
from functools import partial

CREDS =  [["administrator","password1"],["nene","password2"]]

def validateLogin(username, password):
	print("username entered :", username.get())
	print("password entered :", password.get())
	for i in CREDS:
		print(i[0] + " " + i[1] + " " + str(CREDS[-1][0]))
		if username.get() == i[0] :
			if password.get() == i[1] :
				messagebox.showinfo(title='Correct', message='Username and Password correct')
				loginPage.destroy()
				mainPage.open()
				break
			else:
				messagebox.showerror(tittle=None, message='Username and Password incorrect')
				break
		if i[0] == CREDS [-1][0] :
			messagebox.showerror(tittle=None, message='Username and Password incorrect')
	return

#window
tkWindow = Tk()  
tkWindow.geometry('400x150')  
tkWindow.title('Login Form')

#username label and text entry box
usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)  

#password label and password entry box
passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)  
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)  

validateLogin = partial(validateLogin, username, password)

#login button
loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

#message box


tkWindow.mainloop()