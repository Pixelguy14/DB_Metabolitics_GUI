#  Copyright 2024 Jose Julian Sierra Alvarez <julian@julian-Lenovo-G50-30> coded on Linux
# main.py
import sqlite3
import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from os import path
import icon #import of the icon.py file
import configparser
from tkinter import filedialog

# Function that recieves db location and loads the database into the interface
def load_db():
	mb = Messagebox.show_warning("Enter a valid database for the system","Warning")
	filename = filedialog.askopenfilename()
	#Has to be .db or it fails
	while(filename.lower().endswith('.db') ==  False):
		mb = Messagebox.show_error("Enter a valid database for the system","Error!")
		filename = filedialog.askopenfilename()
	config_writer = configparser.ConfigParser()
	config_writer['default'] = {
		'db_location' : filename
	}
	with open('LABI_SqliteDB.ini','w') as configfile:
		config_writer.write(configfile)
	mb = Messagebox.show_info("Database added correctly","LABI 2024")

# Function that searches for the db file and saves its location		
def verify_init():
	global config_reader
	config_reader = configparser.ConfigParser()
	config_reader.read('LABI_SqliteDB.ini')
	if(config_reader.sections() == []):
		load_db()
	else:
		#double check que el archivo cargado sea .db
		if config_reader['default']['db_location'].lower().endswith('.db') ==  False:
			mb = Messagebox.show_error("Enter a valid database for the system","Error!")
			load_db()

# Function that detects when an element is clicked and allows or disables the edition buttons.
def element_selection(event):
	global SelectStr, tabPosition
	SelectStr = dt.get_rows(selected=True)
	if dt.view.selection():
		tabPosition = dt.view.index(dt.view.selection()[0])
	#print (tabPosition)
	if Add_btn["text"] == "Add":
		if Edit_btn["text"] == "Edit":
			Delete_btn.config(state="normal")
		Edit_btn.config(state="normal")

# Function that recalls the headers of the sqlite table and loads it into the tk table
def headers_db():
	# query used to get headers from table
	query = 'SELECT name FROM pragma_table_info ('+tablename+') ORDER BY cid;'
	cursor = sqliteConnection.execute(query)
	ncol = len(cursor.fetchall())
	cursor = sqliteConnection.execute(query) # query execution has to be repeated
	for j in range(0,ncol):
		for i in cursor:
			dt.insert_column('end',text=str(i[j]), stretch=False) # Insert columns after the table has been created
			dt.load_table_data()

# Function that fills the tk table with data retrieved from the database
def filling():
	dt.delete_rows()
	query = 'SELECT * FROM '+tablename+';'
	cursor = sqliteConnection.execute(query)
	for i in cursor:
		strRow = [str(j) for j in i]
		dt.insert_row('end', strRow)
	dt.pack(fill=BOTH, expand=NO, padx=10, pady=10)
	dt.load_table_data() # dt.unload_table_data()

# Function that creates an alert to make sure the user wants to delete a row from the table
def delete_warning():
	mb = Messagebox.yesno("Do you want to delete the selected record? ("+SelectStr[0].values[1]+")","Record has been deleted")
	if mb == "Sí" or mb == "Yes":
		#print("entre!")
		query = 'SELECT name FROM pragma_table_info ('+tablename+') ORDER BY cid LIMIT 1;'
		cursor = sqliteConnection.execute(query)
		table_id=cursor.fetchall()
		query = 'DELETE FROM '+tablename+' WHERE "'+table_id[0][0]+'" = '+SelectStr[0].values[0]+';'
		print(query)
		sqliteConnection.execute(query)
		sqliteConnection.commit() # Commit is necesary for the changes inside the database to be made
	filling()
	
	dt.view.selection_set(dt.view.get_children()[0])
	dt.view.focus(dt.view.get_children()[0])
	'''
	if tabPosition != 0:
		dt.view.selection_set(tabPosition-1)
		dt.view.focus(tabPosition-1)
	else:
		dt.view.selection_set(tabPosition)
		dt.view.focus(tabPosition)
	'''

# Function that creates the tk frame that allows to add or edit rows in the database
def data_fill_func():
	global Data_fill_frame
	global db_name_data, db_RT_data, db_mz_data, db_Ion_type_data, db_Ion_Formula_data, db_ppm_data
	global db_Fragments_Ions_data, db_Ionization_mode_data, db_Structure_data, db_Extra_Information_data, db_Reference_data
	# Creation of tk variables
	db_name_data = tk.StringVar()
	db_RT_data = tk.DoubleVar()
	db_mz_data = tk.DoubleVar()
	db_Ion_type_data = tk.StringVar()
	db_Ion_Formula_data = tk.StringVar()
	db_ppm_data = tk.DoubleVar()
	
	db_Fragments_Ions_data = tk.DoubleVar()
	db_Ionization_mode_data = tk.StringVar()
	''' por ahora dejamos que sea string pero se tiene que modificar '''
	db_Structure_data = tk.StringVar() 
	db_Extra_Information_data = tk.StringVar()
	db_Reference_data = tk.StringVar()
	# Data info frame interface
	Data_fill_frame = ttk.Labelframe(Main_frame, text = "Insert Data")
	# First row labels
	#Name (Text), RT (Real), mz (Real), Ion_type (Text), Ion_Formula (Text)
	db_name_label = ttk.Label(Data_fill_frame, text="Name")
	db_name_label.grid(row=0, column=0)
	
	db_RT_label = ttk.Label(Data_fill_frame, text="RT")
	db_RT_label.grid(row=0, column=1)
	
	db_mz_label = ttk.Label(Data_fill_frame, text="mz")
	db_mz_label.grid(row=0, column=2)
	
	db_Ion_type_label = ttk.Label(Data_fill_frame, text="Ion_type")
	db_Ion_type_label.grid(row=0, column=3)
	
	db_Ion_Formula_label = ttk.Label(Data_fill_frame, text="Ion_Formula")
	db_Ion_Formula_label.grid(row=0, column=4)
	
	# First row entries
	#Name (Text), RT (Real), mz (Real), Ion_type (Text), Ion_Formula (Text)
	db_name_entry = ttk.Entry(Data_fill_frame, textvariable = db_name_data)
	db_name_entry.grid(row=1, column=0)
	
	db_RT_entry = ttk.Entry(Data_fill_frame, validate="key", validatecommand=(Data_fill_frame.register(validate_float), "%P"),
	textvariable = db_RT_data)
	db_RT_entry.grid(row=1, column=1)
	
	db_mz_entry = ttk.Entry(Data_fill_frame, validate="key", validatecommand=(Data_fill_frame.register(validate_float), "%P"),
	textvariable = db_mz_data)
	db_mz_entry.grid(row=1, column=2)
	
	db_Ion_type_entry = ttk.Entry(Data_fill_frame, textvariable = db_Ion_type_data)
	db_Ion_type_entry.grid(row=1, column=3)
	
	db_Ion_Formula_entry = ttk.Entry(Data_fill_frame, textvariable = db_Ion_Formula_data)
	db_Ion_Formula_entry.grid(row=1, column=4)
	
	# Second row labels
	#ppm (Real), Fragments_Ions (Real), Ionization_Mode (String), Structure (BLOB), Extra_Information (String), Reference (String)
	db_ppm_label = ttk.Label(Data_fill_frame, text="ppm")
	db_ppm_label.grid(row=2, column=0)
	
	db_Fragments_Ions_label = ttk.Label(Data_fill_frame, text="Fragments_Ions")
	db_Fragments_Ions_label.grid(row=2, column=1)
	
	db_Ionization_Mode_label = ttk.Label(Data_fill_frame, text="Ionization_Mode")
	db_Ionization_Mode_label.grid(row=2, column=2)
	
	db_Structure_label = ttk.Label(Data_fill_frame, text="Structure")
	db_Structure_label.grid(row=2, column=3)
	
	db_Extra_Information_label = ttk.Label(Data_fill_frame, text="Extra_Information")
	db_Extra_Information_label.grid(row=2, column=4)
	
	db_Reference_label = ttk.Label(Data_fill_frame, text="Reference")
	db_Reference_label.grid(row=2, column=5)
	
	# Second row entries
	#ppm (Real), Fragments_Ions (Real), Ionization_Mode (String), Structure (BLOB), Extra_Information (String), Reference (String)
	db_ppm_entry = ttk.Entry(Data_fill_frame, validate="key", validatecommand=(Data_fill_frame.register(validate_float), "%P"),
	textvariable = db_ppm_data)
	db_ppm_entry.grid(row = 3, column = 0)
	
	db_Fragments_Ions_entry = ttk.Entry(Data_fill_frame, validate="key", validatecommand=(Data_fill_frame.register(validate_float), "%P"),
	textvariable = db_Fragments_Ions_data)
	db_Fragments_Ions_entry.grid(row = 3, column = 1)
	
	db_Ionization_Mode_entry = ttk.Entry(Data_fill_frame, textvariable = db_Ionization_mode_data)
	db_Ionization_Mode_entry.grid(row = 3, column = 2)
	
	db_Structure_btn = ttk.Button(Data_fill_frame, text = "Add Image", command = Structure_image, style = 'Secondary.Outline.TButton')
	db_Structure_btn.grid(row = 3, column = 3)
	
	db_Extra_Information_entry = ttk.Entry(Data_fill_frame, textvariable = db_Extra_Information_data)
	db_Extra_Information_entry.grid(row = 3, column = 4)
	
	db_Reference_entry = ttk.Entry(Data_fill_frame, textvariable = db_Reference_data)
	db_Reference_entry.grid(row = 3, column = 5)
	
# Function that recieves the input from the buttons and alters the interface 
def add_dialog():
	Delete_btn.config(state = "disabled")
	Edit_btn.config(state = "disabled")
	global Set_Add_btn
	if Add_btn["text"] == "Add":
		Add_btn.config(text = "Cancel")
		Add_btn.config(style = "warning.Outline.TButton")
		data_fill_func()
		#Final Add
		Set_Add_btn = ttk.Button(Function_frame, text = "Add record", style = "success.TButton", command = add_db)
		Set_Add_btn.pack(side = tk.RIGHT, padx = 10, pady = 5)
		Data_fill_frame.pack(padx = 20, pady = (10,20))
		Data_fill_frame.update_idletasks()
		Main_frame.yview_moveto(1)
	else:
		Add_btn.config(text = "Add")
		Add_btn.config(style = "success.Outline.TButton")
		Data_fill_frame.destroy() #Delete everything inside frame
		Set_Add_btn.destroy()
		Main_frame.yview_moveto(0)
	window.geometry("")
	Delete_btn.config(state = "disabled")
	Edit_btn.config(state = "disabled")
	filling()

# function that inserts values from the interface to the database
def add_db ():
	D1 = str(db_name_data.get())
	D2 = str(db_RT_data.get())
	D3 = str(db_mz_data.get())
	D4 = str(db_Ion_type_data.get())
	D5 = str(db_Ion_Formula_data.get())
	D6 = str(db_ppm_data.get())
	# db_Fragments_Ions_data, db_Ionization_mode_data, db_Structure_data, db_Extra_Information_data, db_Reference_data
	D7 = str(db_Fragments_Ions_data.get())
	D8 = str(db_Ionization_mode_data.get())
	D9 = str(db_Structure_data.get())
	D10 = str(db_Extra_Information_data.get())
	D11 = str(db_Reference_data.get())
	#query= 'INSERT INTO '+tablename+' (name, RT, mz, Ion_type, Ion_formula, ppm) VALUES ("'+D1+'","'+D2+'","'+D3+'","'+D4+'","'+D5+'","'+D6+'");'
	query= 'INSERT INTO '+tablename+' (name, RT, mz, Ion_type, Ion_formula, ppm, Fragments_ions, Ionization_mode, Structure, Extra_information, Reference) VALUES ("'+D1+'","'+D2+'","'+D3+'","'+D4+'","'+D5+'","'+D6+'","'+D7+'","'+D8+'","'+D9+'","'+D10+'","'+D11+'");'
	print(query)
	cursor = sqliteConnection.execute(query)
	sqliteConnection.commit() # Commit is necessary for doing the changes inside the database
	Add_btn.config(text = "Add")
	Add_btn.config(style = "success.Outline.TButton")
	Data_fill_frame.destroy() #Delete everything inside frame
	Set_Add_btn.destroy()
	Main_frame.yview_moveto(0)
	window.geometry("")
	filling()
	# Going to the last element created in the view
	dt.goto_last_page()
	dt.view.selection_set(dt.view.get_children()[-1])
	dt.view.focus(dt.view.get_children()[-1])

# Function that recieves the input from the buttons and alters the interface 	
def edit_dialog():
	Delete_btn.config(state="disabled")
	Add_btn.config(state="disabled")
	global Set_Edit_btn
	if Edit_btn["text"] == "Edit":
		global id_selected
		id_selected=SelectStr[0].values[0]
		Edit_btn.config(text = "Cancel")
		Edit_btn.config(style = "warning.Outline.TButton")
		data_fill_func()
		db_name_data.set(SelectStr[0].values[1])
		db_RT_data.set(SelectStr[0].values[2])
		db_mz_data.set(SelectStr[0].values[3])
		db_Ion_type_data.set(SelectStr[0].values[4])
		db_Ion_Formula_data.set(SelectStr[0].values[5])
		db_ppm_data.set(SelectStr[0].values[6])
		# db_Fragments_Ions_data, db_Ionization_mode_data, db_Structure_data, db_Extra_Information_data, db_Reference_data
		db_Fragments_Ions_data.set(SelectStr[0].values[7])
		db_Ionization_mode_data.set(SelectStr[0].values[8])
		db_Structure_data.set(SelectStr[0].values[9])
		db_Extra_Information_data.set(SelectStr[0].values[10])
		db_Reference_data.set(SelectStr[0].values[11])
		
		Set_Edit_btn = ttk.Button(Function_frame, text = "Edit record", style = "success.TButton", command = edit_db)
		Set_Edit_btn.pack(side = tk.RIGHT, padx = 10, pady = 5)
		Data_fill_frame.pack(padx = 20, pady = (10,20))
		Data_fill_frame.update_idletasks()
		Main_frame.yview_moveto(1)
	else:
		Edit_btn.config(text = "Edit")
		Edit_btn.config(style = "info.Outline.TButton")
		Delete_btn.config(state = "disabled")
		Edit_btn.config(state = "disabled")
		Add_btn.config(state = "enabled")
		Data_fill_frame.destroy()
		Set_Edit_btn.destroy()
		Main_frame.yview_moveto(0)
	window.geometry("")
	filling()

# function that inserts values from the interface to alter the database	
def edit_db():
	D1 = str(db_name_data.get())
	D2 = str(db_RT_data.get())
	D3 = str(db_mz_data.get())
	D4 = str(db_Ion_type_data.get())
	D5 = str(db_Ion_Formula_data.get())
	D6 = str(db_ppm_data.get())
	# db_Fragments_Ions_data, db_Ionization_mode_data, db_Structure_data, db_Extra_Information_data, db_Reference_data
	D7 = str(db_Fragments_Ions_data.get())
	D8 = str(db_Ionization_mode_data.get())
	D9 = str(db_Structure_data.get())
	D10 = str(db_Extra_Information_data.get())
	D11 = str(db_Reference_data.get())
	query = 'SELECT name FROM pragma_table_info ('+tablename+') ORDER BY cid LIMIT 1;'
	cursor = sqliteConnection.execute(query)
	table_id =cursor.fetchall()
	#query= 'UPDATE '+tablename+' SET name="'+D1+'", RT='+D2+', mz='+D3+', Ion_type="'+D4+'", Ion_formula="'+D5+'", ppm='+D6+' WHERE "'+table_id[0][0]+'" = '+id_selected+';'
	query = (
		'UPDATE ' + tablename + 
		' SET name="' + D1 + '", RT=' + D2 + ', mz=' + D3 + 
		', Ion_type="' + D4 + '", Ion_formula="' + D5 + '", ppm=' + D6 + 
		', Fragments_ions="' + D7 + '", Ionization_mode="' + D8 + 
		'", Structure="' + D9 + '", Extra_information="' + D10 + 
		'", Reference="' + D11 + 
		'" WHERE "' + table_id[0][0] + '" = ' + id_selected + ';'
	)
	print(query)
	cursor = sqliteConnection.execute(query)
	sqliteConnection.commit() 
	Edit_btn.config(text = "Edit")
	Edit_btn.config(style = "info.Outline.TButton")
	Delete_btn.config(state = "disabled")
	Edit_btn.config(state = "disabled")
	Add_btn.config(state = "enabled")
	Data_fill_frame.destroy()
	Set_Edit_btn.destroy()
	Main_frame.yview_moveto(0)
	window.geometry("")
	filling()
	
# Function that allows only float values into certain entries
def validate_float(value):
    try:
        if value in ("", "-", "+"):  # Allow empty input and sign characters
            return True
        float(value)  # Validate other float values
        return True
    except ValueError:
        return False
   
# Function that handles the selection of an image     
def Structure_image ():
	db_Structure_data.set("test000")

# Creation of the main window frame
window = ttk.Window(
	themename = 'minty', 
	title = 'DB Metabolites GUI',
	)
window.resizable(True, True)
icon.apply_icon(window) # The icon.y is aplied as a window icon
# Calls the function that verifies creation of the ini file
verify_init()
config_reader.read('LABI_SqliteDB.ini')
try:
	## Db conection
	sqliteConnection = sqlite3.connect(config_reader['default']['db_location'])
	cursor = sqliteConnection.cursor()
	tablename = '"Data_espectrometry"'
	## Title creation
	title_label = ttk.Label(master = window, text = "Metabolites Database GUI for LABI", font = 'Calibri 21')
	title_label.pack(pady = (10, 0))
	Main_frame = ScrolledFrame(window,autohide = True,height = 600, width = 1090)
	Main_frame.pack(fill = tk.BOTH, expand = tk.YES, padx = 1, pady = 2)
	## Table creation
	dt = Tableview(
		master = Main_frame,
		coldata = [],#col and row data initialization
		rowdata = [],
		paginated = True,
		searchable = True,
		bootstyle = PRIMARY,
		autofit = True,
		autoalign = True,
		pagesize = 15,
		height = 15
	)
	## Data inserts on the table
	# Creation of columns for the table
	headers_db()
	dt.hide_selected_column(cid = 0)
	# Initial filling for the table
	filling()
	## Formating
	dt.autofit_columns() 
	dt.view.bind('<<TreeviewSelect>>', element_selection) # Adds functionality for table selection
	dt.view.unbind("<Button-3>") # Deletes right click functionalization
	## Buttons for editing table records
	Function_frame = ttk.Labelframe(Main_frame, text = "Function buttons")
	Add_btn = ttk.Button(Function_frame, text = "Add", style = "success.Outline.TButton", command = add_dialog)
	Add_btn.pack(side = tk.LEFT, padx = 10, pady = 5)
	Delete_btn = ttk.Button(Function_frame, text = "Delete", style = "danger.Outline.TButton", command = delete_warning)
	Delete_btn.pack(side = tk.LEFT, padx = 10, pady = 5)
	Delete_btn.config(state = "disabled")
	Edit_btn = ttk.Button(Function_frame, text = "Edit",style = "info.Outline.TButton", command = edit_dialog)
	Edit_btn.pack(side = tk.LEFT, padx = 10, pady = 5)
	Edit_btn.config(state = "disabled")
	Function_frame.pack(pady = 0, padx = 10, fill = "x")
	window.mainloop() # Hold here! active window
	cursor.close() # We release the SQLite cursor
except sqlite3.Error as error:
	print("Sudden error: - ",error)
finally:
	if sqliteConnection:
		sqliteConnection.close()
		print('Sqlite conection has ended')
