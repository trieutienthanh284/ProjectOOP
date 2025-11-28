import mysql.connector
db = mysql.connector.connect(user = 'root', password = '123456789', host = 'localhost', database = 'database')
cursor = db.cursor()
