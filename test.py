import pyodbc 
import re
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:betmatcher.database.windows.net' 
database = 'betmatcher' 
username = 'azureadmin' 
password = 'xcazU7qpal3.' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

a = ["a", 'b', 1]
string = "   prova <> 1"
print(re.sub(r'^.*? <> ', '', string))