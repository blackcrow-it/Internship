import sqlite3

conn = sqlite3.connect('database.db')
print "Opened database successfully";

conn.execute('CREATE TABLE user (email varchar(50), name varchar(50), date varchar(10))')
print "Table created successfully";
conn.close()