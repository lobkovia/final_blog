import sqlite3

conn = sqlite3.connect('database.db')

try:
    conn.execute('CREATE TABLE users (name varchar(20),password varchar(255))')
    conn.execute('CREATE TABLE posts (author varchar(20),message varchar(255),date varchar(30) )')
    print("Tables created successfully")
    conn.close()
except:
    print("Problem with tables creation :( ")