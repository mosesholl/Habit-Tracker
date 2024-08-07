from db import Main_Db
from GUI import GUI

Main_Db().create_table()
GUI().run()