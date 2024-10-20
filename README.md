# DB_Metabolitics_GUI

A Graphical User Interface designed to store metabolitic data from a SQLite database, tailored for the needs of the "Laboratorio de Analisis Bioquimico e Instrumental".

## Getting Started

### Using the "main" Executable (Ubuntu Linux 24.04+)

1. **Permissions:**
   - Give execution permissions to the app.
   
2. **Database Setup:**
   - Create the Database using the `Database_patched.txt` instructions.
   - Load the database inside the app.
   - Do not delete the `LABi_sqliteDB.ini` file as it saves the database location.

### Libraries Required for Python (if not using the "main" executable)

- `sqlite3`
- `tkinter`
- `ttkbootstrap`
- `configparser`

### Creating the Executable

The executable file is created using `pyinstaller`. Use the following command:

```bash
pyinstaller main.py --hidden-import='PIL._tkinter_finder' --onefile -w
```

## Important Notes

- If you already have a database in use, do not download the new database as it contains only test data.

- If your database has columns from before the patch, follow the `Patch_database.txt` instructions to retrofit the database with the new app.
