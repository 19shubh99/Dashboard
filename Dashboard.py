from tkinter import *
from tkinter import messagebox
from functools import partial
import datetime
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar
import sqlite3

#Creating the universal font variable
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)"
)

CREDS =  [["admin","password1"],["nene","password2"]]

def adminWindow(username, password):
	global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
	# Creating the functions
	def reset_fields():
		global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
		for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'stream_strvar']:
			exec(f"{i}.set('')")
		dob.set_date(datetime.datetime.now().date())
	def reset_form():
		global tree
		tree.delete(*tree.get_children())
		reset_fields()
	def display_records():
		tree.delete(*tree.get_children())
		curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
		data = curr.fetchall()
		for records in data:
			tree.insert('', END, values=records)
	def add_record():
		global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
		name = name_strvar.get()
		email = email_strvar.get()
		contact = contact_strvar.get()
		gender = gender_strvar.get()
		DOB = dob.get_date()
		stream = stream_strvar.get()
		if not name or not email or not contact or not gender or not DOB or not stream:
			mb.showerror('Error!', "Please fill all the missing fields!!")
		else:
			try:
				connector.execute('INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)', (name, email, contact, gender, DOB, stream))
				connector.commit()
				mb.showinfo('Record added', f"Record of {name} was successfully added")
				reset_fields()
				display_records()
			except:
				mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')
	def remove_record():
		if not tree.selection():
			mb.showerror('Error!', 'Please select an item from the database')
		else:
			current_item = tree.focus()
			values = tree.item(current_item)
			selection = values["values"]
			tree.delete(current_item)
			connector.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
			connector.commit()
			mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
			display_records()
	def view_record():
		global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
		if not tree.selection():
			mb.showerror('Error!', 'Please select a record to view')
		else:
			current_item = tree.focus()
			values = tree.item(current_item)
			selection = values["values"]

			name_strvar.set(selection[1]); email_strvar.set(selection[2])
			contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
			date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))
			dob.set_date(date);stream_strvar.set(selection[6])

	# Initializing the GUI window
	main = Tk()
	main.title('DataFlair School Management System')
	main.geometry('1000x600')
	main.resizable(0, 0)
	# Creating the background and foreground color variables
	lf_bg = 'MediumSpringGreen' # bg color for the left_frame
	cf_bg = 'PaleGreen' # bg color for the center_frame
	# Creating the StringVar or IntVar variables
	name_strvar = StringVar()
	email_strvar = StringVar()
	contact_strvar = StringVar()
	gender_strvar = StringVar()
	stream_strvar = StringVar()
	# Placing the components in the main window
	Label(main, text="MANAGEMENT SYSTEM", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)
	left_frame = Frame(main, bg=lf_bg)
	left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)
	center_frame = Frame(main, bg=cf_bg)
	center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)
	right_frame = Frame(main, bg="Gray35")
	right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)
	# Placing components in the left frame
	Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(relx=0.375, rely=0.05)
	Label(left_frame, text="Service Number", font=labelfont, bg=lf_bg).place(relx=0.175, rely=0.18)
	Label(left_frame, text="Call Sign", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.31)
	Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.44)
	Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg=lf_bg).place(relx=0.1, rely=0.57)
	Label(left_frame, text="Squadron", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.7)
	Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.1)
	Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.23)
	Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.36)
	Entry(left_frame, width=19, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.75)
	OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.49, relwidth=0.5)
	dob = DateEntry(left_frame, font=("Arial", 12), width=15)
	dob.place(x=20, rely=0.62)
	Button(left_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)
	# Placing components in the center frame
	Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
	Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
	Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
	Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)
	# Placing components in the right frame
	Label(right_frame, text='Cadets Records', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)
	tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE, columns=('Cadet ID', "Name", "Service Number", "Call Sign", "Gender", "Date of Birth", "Squadron"))
	X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
	Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
	X_scroller.pack(side=BOTTOM, fill=X)
	Y_scroller.pack(side=RIGHT, fill=Y)
	tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
	tree.heading('Cadet ID', text='Cadet ID', anchor=CENTER)
	tree.heading('Name', text='Name', anchor=CENTER)
	tree.heading('Service Number', text='Service Number', anchor=CENTER)
	tree.heading('Call Sign', text='Call Sign', anchor=CENTER)
	tree.heading('Gender', text='Gender', anchor=CENTER)
	tree.heading('Date of Birth', text='DOB', anchor=CENTER)
	tree.heading('Squadron', text='Squadron', anchor=CENTER)
	tree.column('#0', width=0, stretch=NO)
	tree.column('#1', width=40, stretch=NO)
	tree.column('#2', width=140, stretch=NO)
	tree.column('#3', width=200, stretch=NO)
	tree.column('#4', width=80, stretch=NO)
	tree.column('#5', width=80, stretch=NO)
	tree.column('#6', width=80, stretch=NO)
	tree.column('#7', width=150, stretch=NO)
	tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
	display_records()
	# Finalizing the GUI window
	main.update()
	main.mainloop()

def userWindow(username):
	
	userWindow = Tk()
	userWindow.geometry("750x250")
	userWindow.title("User Window")

	# Update the listbox
	def update(data):
	# Clear the listbox
		my_list.delete(0, END)

		# Add names to listbox
		for item in data:
			my_list.insert(END, item)

	# Update entry box with listbox clicked
	def fillout(e):
		# Delete whatever is in the entry box
		my_entry.delete(0, END)
	
		# Add clicked list item to entry box
		my_entry.insert(0, my_list.get(ANCHOR))
	
		t = Toplevel()
		message = Message(t, text='text')
		message.pack(side="top", fill="both", expand=True, padx=50, pady=50)

	# Create function to check entry vs listbox
	def check(e):
		# grab what was typed
		typed = my_entry.get()

		if typed == '':
			data = nameList
		else:
			data = []
			for item in nameList:
				if typed.lower() in item.lower():
					data.append(item)

		# update our listbox with selected items
		update(data)				


	# Create a label
	my_label = Label(userWindow, text="Name",font=("Helvetica", 14), fg="grey")

	my_label.pack(pady=20)

	# Create an entry box
	my_entry = Entry(userWindow, font=("Helvetica", 20))
	my_entry.pack()

	# Create a listbox
	my_list = Listbox(userWindow, width=50)
	my_list.pack(pady=40)

	# Create a list
	nameList=[]
	cursor.execute('SELECT * FROM SCHOOL_MANAGEMENT')
	result = cursor.fetchall()
	for data in result:
		print(data)
		nameList.append(data[1])  

	# Add the items to our list
	update(nameList)

	# Create a binding on the listbox onclick
	my_list.bind("<<ListboxSelect>>", fillout)

	# Create a binding on the entry box
	my_entry.bind("<KeyRelease>", check)

	userWindow.mainloop()
	
	
#Define a new function to open the window
def open_mainWindow(username, password):
	
	if username.get() == 'admin':
		print("open admin window")
		adminWindow(username, password)
	else:
		print(username.get() + " " + password.get())
		userWindow(username)
		#mainWindow = Tk()
		#mainWindow.geometry("750x250")
		#mainWindow.title("New Window")

		#Create a Label in New window
		#Label(mainWindow, text="Hey, Howdy?", font=('Helvetica 17 bold')).pack(pady=30)

		#mainWindow.mainloop()

def validateLogin(loginWindow, username, password):
	print("username entered :", username.get())
	print("password entered :", password.get())
	for i in CREDS:
		if username.get() == i[0] :
			if password.get() == i[1] :
				messagebox.showinfo(title='Correct', message='Username and Password correct')
				loginWindow.destroy()
				open_mainWindow(username, password)
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


