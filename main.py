#  Copyright 2024 Jose Julian Sierra Alvarez <julian@julian-Lenovo-G50-30> coded on Linux
# Pre_release01.py
import sqlite3
import tkinter as tk
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

def cargar_db():
	mb = Messagebox.show_warning("Enter a valid database for the system","Warning")
	filename = filedialog.askopenfilename()
	#Has to be .db or it crashes
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
		
def verificar_ini():
	global config_reader
	config_reader = configparser.ConfigParser()
	config_reader.read('LABI_SqliteDB.ini')
	if(config_reader.sections() == []):
		cargar_db()
	else:
		#double check que el archivo cargado sea .db
		if config_reader['default']['db_location'].lower().endswith('.db') ==  False:
			mb = Messagebox.show_error("Enter a valid database for the system","Error!")
			cargar_db()

def seleccion_de_elemento(event):
    global SelectStr
    SelectStr = dt.get_rows(selected=True)
    Delete_btn.config(state="normal")
    Edit_btn.config(state="normal")


def cabeceras():
	#query de los encabezados de la tabla
	query = 'SELECT name FROM pragma_table_info ('+tablename+') ORDER BY cid;'
	cursor = sqliteConnection.execute(query)
	ncol = len(cursor.fetchall())
	cursor = sqliteConnection.execute(query) #query execution has to be repeated
	for j in range(0,ncol):
		for i in cursor:
			dt.insert_column('end',text=str(i[j]), stretch=False) # Insert columns after the table has been created
			dt.load_table_data()

def llenado():
	dt.delete_rows()
	query = 'SELECT * FROM '+tablename+';'
	cursor = sqliteConnection.execute(query)
	for i in cursor:
		strRow = [str(j) for j in i]
		dt.insert_row('end', strRow)
	dt.pack(fill=BOTH, expand=NO, padx=10, pady=10)
	dt.load_table_data() #dt.unload_table_data()

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
		sqliteConnection.commit() #Commit is necesary for the changes inside the database to be made
	llenado() 
	Delete_btn.config(state="disabled")
	Edit_btn.config(state="disabled")
	
def data_fill_func():
	global Data_fill_frame
	global db_name_data, db_RT_data, db_mz_data, db_Ion_type_data, db_Ion_Formula_data, db_ppm_data
	db_name_data = tk.StringVar()
	db_RT_data = tk.DoubleVar()
	db_mz_data = tk.DoubleVar()
	db_Ion_type_data = tk.StringVar()
	db_Ion_Formula_data = tk.StringVar()
	db_ppm_data = tk.DoubleVar()
	#Data info frame
	Data_fill_frame = ttk.Labelframe(Main_frame, text = "Insert Data")
	#Name (Text), RT (Real), mz (Real)
	db_name_label = ttk.Label(Data_fill_frame, text="Name")
	db_name_label.grid(row=0, column=0)
	db_RT_label = ttk.Label(Data_fill_frame, text="RT")
	db_RT_label.grid(row=0, column=1)
	db_mz_label = ttk.Label(Data_fill_frame, text="mz")
	db_mz_label.grid(row=0, column=2)
	db_name_entry = ttk.Entry(Data_fill_frame, textvariable = db_name_data)
	db_name_entry.grid(row=1, column=0)
	db_RT_entry = ttk.Entry(Data_fill_frame, validate="key", validatecommand=(Data_fill_frame.register(valida_float), "%P"),
	textvariable = db_RT_data)
	db_RT_entry.grid(row=1, column=1)
	db_mz_entry = ttk.Entry(Data_fill_frame, validate="key", validatecommand=(Data_fill_frame.register(valida_float), "%P"),
	textvariable = db_mz_data)
	db_mz_entry.grid(row=1, column=2)
	#Ion_type (Text), Ion_Formula (Text), ppm (Real)
	db_Ion_type_label = ttk.Label(Data_fill_frame, text="Ion_type")
	db_Ion_type_label.grid(row=3, column=0)
	db_Ion_Formula_label = ttk.Label(Data_fill_frame, text="Ion_Formula")
	db_Ion_Formula_label.grid(row=3, column=1)
	db_ppm_label = ttk.Label(Data_fill_frame, text="ppm")
	db_ppm_label.grid(row=3, column=2)
	db_Ion_type_entry = ttk.Entry(Data_fill_frame, textvariable = db_Ion_type_data)
	db_Ion_type_entry.grid(row=4, column=0)
	db_Ion_Formula_entry = ttk.Entry(Data_fill_frame, textvariable = db_Ion_Formula_data)
	db_Ion_Formula_entry.grid(row=4, column=1)
	db_ppm_entry = ttk.Entry(Data_fill_frame, validate="key", validatecommand=(Data_fill_frame.register(valida_float), "%P"),
	textvariable = db_ppm_data)
	db_ppm_entry.grid(row=4, column=2)
	
def add_dialog():
	Delete_btn.config(state="disabled")
	Edit_btn.config(state="disabled")
	global Set_Add_btn
	if Add_btn["text"] == "Add":
		Add_btn.config(text = "Cancel")
		Add_btn.config(style = "warning.Outline.TButton")
		data_fill_func()
		#Final Add
		Set_Add_btn = ttk.Button(Function_frame, text = "Add record", style = "success.TButton", command = add_db)
		Set_Add_btn.pack(side = tk.RIGHT, padx=10, pady=5)
		Data_fill_frame.pack(padx=20, pady=10)
	else:
		Add_btn.config(text = "Add")
		Add_btn.config(style = "success.Outline.TButton")
		Data_fill_frame.destroy() #Delete everything inside frame
		Set_Add_btn.destroy()
	Main_frame.yview_moveto(0)
	window.geometry("")
	Delete_btn.config(state="disabled")
	Edit_btn.config(state="disabled")
	llenado()

def add_db ():
	D1 = str(db_name_data.get())
	D2 = str(db_RT_data.get())
	D3 = str(db_mz_data.get())
	D4 = str(db_Ion_type_data.get())
	D5 = str(db_Ion_Formula_data.get())
	D6 = str(db_ppm_data.get())
	query= 'INSERT INTO '+tablename+' (name, RT, mz, Ion_type, Ion_formula, ppm) VALUES ("'+D1+'","'+D2+'","'+D3+'","'+D4+'","'+D5+'","'+D6+'");'
	print(query)
	cursor = sqliteConnection.execute(query)
	sqliteConnection.commit() #Commit is necesary for the changes inside the database to be made
	Add_btn.config(text = "Añadir")
	Add_btn.config(style = "success.Outline.TButton")
	Data_fill_frame.destroy() #Delete everything inside frame
	Set_Add_btn.destroy()
	Main_frame.yview_moveto(0)
	window.geometry("")
	llenado()
	
def edit_db():
	D1 = str(db_name_data.get())
	D2 = str(db_RT_data.get())
	D3 = str(db_mz_data.get())
	D4 = str(db_Ion_type_data.get())
	D5 = str(db_Ion_Formula_data.get())
	D6 = str(db_ppm_data.get())
	query = 'SELECT name FROM pragma_table_info ('+tablename+') ORDER BY cid LIMIT 1;'
	cursor = sqliteConnection.execute(query)
	table_id=cursor.fetchall()
	query= 'UPDATE '+tablename+' SET name="'+D1+'", RT='+D2+', mz='+D3+', Ion_type="'+D4+'", Ion_formula="'+D5+'", ppm='+D6+' WHERE "'+table_id[0][0]+'" = '+id_selected+';'
	print(query)
	cursor = sqliteConnection.execute(query)
	sqliteConnection.commit() 
	Edit_btn.config(text = "Edit")
	Edit_btn.config(style = "info.Outline.TButton")
	Delete_btn.config(state="disabled")
	Edit_btn.config(state="disabled")
	Add_btn.config(state="enabled")
	Data_fill_frame.destroy()
	Set_Edit_btn.destroy()
	Main_frame.yview_moveto(0)
	window.geometry("")
	llenado()
	
def edit_dialog():
	Delete_btn.config(state="disabled")
	Add_btn.config(state="disabled")
	global id_selected
	id_selected=SelectStr[0].values[0]
	global Set_Edit_btn
	if Edit_btn["text"] == "Edit":
		Edit_btn.config(text = "Cancel")
		Edit_btn.config(style = "warning.Outline.TButton")
		data_fill_func()
		db_name_data.set(SelectStr[0].values[1])
		db_RT_data.set(SelectStr[0].values[2])
		db_mz_data.set(SelectStr[0].values[3])
		db_Ion_type_data.set(SelectStr[0].values[4])
		db_Ion_Formula_data.set(SelectStr[0].values[5])
		db_ppm_data.set(SelectStr[0].values[6])
		Set_Edit_btn = ttk.Button(Function_frame, text = "Edit record", style = "secondary.TButton", command = edit_db)
		Set_Edit_btn.pack(side = tk.RIGHT, padx=10, pady=5)
		Data_fill_frame.pack(padx=20, pady=10)
	else:
		Edit_btn.config(text = "Edit")
		Edit_btn.config(style = "info.Outline.TButton")
		Delete_btn.config(state="disabled")
		Edit_btn.config(state="disabled")
		Add_btn.config(state="enabled")
		Data_fill_frame.destroy()
		Set_Edit_btn.destroy()
	Main_frame.yview_moveto(0)
	window.geometry("")
	llenado()

def valida_float(value):
    try:
        if value in ("", "-", "+"):  #Allow empty input and sign characters
            return True
        float(value)  #Validate other float values
        return True
    except ValueError:
        return False

window = ttk.Window(
	themename = 'minty', 
	title = 'DB Metabolites GUI',
	resizable = [0,0]
	)
icon.apply_icon(window) #the icon.y is aplied as a window icon
# Function that verifies creation of the ini file
verificar_ini()
config_reader.read('LABI_SqliteDB.ini')
try:
	## Db conection
	sqliteConnection = sqlite3.connect(config_reader['default']['db_location'])
	cursor = sqliteConnection.cursor()
	tablename = '"Data_espectrometry"'
	## Title creation
	
	title_label = ttk.Label(master = window, text = "Metabolites Database GUI for LABI", font='Calibri 21')
	title_label.pack(pady=(10, 0))
	Main_frame = ScrolledFrame(window,autohide = True,height=500, width=590)
	Main_frame.pack(fill=tk.BOTH, expand=tk.YES, padx=1, pady=2)
	## Table creation
	dt = Tableview(
		master=Main_frame,
		coldata=[],#col and row data initialization
		rowdata=[],
		paginated=True,
		searchable=True,
		bootstyle=PRIMARY,
		autofit=True,
		autoalign=True,
		pagesize=15,
		height=15
	)
	## Data inserts on the table
	# creation of columns for the table
	cabeceras()
	dt.hide_selected_column(cid=0)
	# Initial filling for the table
	llenado()
	## Formating
	dt.autofit_columns() 
	dt.view.bind('<<TreeviewSelect>>', seleccion_de_elemento) #Adds functionality for table selection
	dt.view.unbind("<Button-3>") #Deletes right click functionalization
	## Buttons for editing table records
	Function_frame = ttk.Labelframe(Main_frame, text = "Function buttons")
	Add_btn = ttk.Button(Function_frame, text = "Add", style = "success.Outline.TButton", command = add_dialog)
	Add_btn.pack(side = tk.LEFT, padx=10, pady=5)
	Delete_btn = ttk.Button(Function_frame, text = "Delete", style = "danger.Outline.TButton", command = delete_warning)
	Delete_btn.pack(side = tk.LEFT, padx = 10, pady = 5)
	Delete_btn.config(state = "disabled")
	Edit_btn = ttk.Button(Function_frame, text = "Edit",style = "info.Outline.TButton", command = edit_dialog)
	Edit_btn.pack(side = tk.LEFT, padx = 10, pady = 5)
	Edit_btn.config(state = "disabled")
	Function_frame.pack(pady = 0, padx = 10, fill = "x")
	window.mainloop() #Hold here! active window
	cursor.close() #We release the SQLite cursor
except sqlite3.Error as error:
	print("Sudden error: - ",error)
finally:
	if sqliteConnection:
		sqliteConnection.close()
		print('Sqlite conection has ended')
