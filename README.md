# DB_Metabolitics_GUI
A Graphical User Interface made to store Metabolitic data from a sqlite database designed to care for the needs of the "Laboratorio de Analisis Bioquimico e Instrumental"</br>

If you're using the "main" executable (that only works in Ubuntu Linux 24.04+), give permisions of execution to the app and make sure to download the database or create it with the Database_patch.txt instructions. Once you have loaded the database inside the app, don't delete the "LABi_sqliteDB.ini" file as it saves where your database is located

Libraries required for python if you dont want to use the "main" executable:</br>
sqlite3</br>
tkinter</br>
ttkbootstrap</br>
configparser</br>

the creation of the executable file has been made with pyinstaller, and the next command is required to succesfully create it:</br>
'''
pyinstaller main.py --hidden-import='PIL._tkinter_finder' --onefile -w
'''
</br>
If you already have a database in use and it has the columns before the patch, follow the Patch_database.txt file instructions copying them in the in the linux terminal
