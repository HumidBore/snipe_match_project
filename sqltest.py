import pyodbc
server = 'betmatcher.database.windows.net'
database = 'betmatcher'
username = 'azureadmin'
password = 'xcazU7qpal3.'   
driver= '{ODBC Driver 17 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        # cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        cursor.execute("""
            INSERT INTO dbo.PurchaseOrderDetail  
            VALUES (20080414);
            """)
        # row = cursor.fetchone()
        # while row:
        #     print (str(row[0]) + " " + str(row[1]))
        #     row = cursor.fetchone()