import mysql.connector
db = mysql.connector.connect(user = 'root', password = '123456789', host = 'localhost')
#query
code = 'create database `test`'
#run
mycursor = db.cursor()
mycursor.execute(code)
