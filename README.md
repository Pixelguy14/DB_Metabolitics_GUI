# DB_Metabolitics_GUI
A Graphical User Interface made to store Metabolitic data from a sqlite database created for a LABI member

Libraries required for python if you dont want to use the "main" executable:
sqlite3
tkinter
ttkbootstrap
configparser

the creation of the executable file has been made with pyinstaller, and the next command is required to succesfully create it:
pyinstaller main.py --hidden-import='PIL._tkinter_finder' --onefile -w


