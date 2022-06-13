import sqlite3

conn = sqlite3.connect('database.db')

try:
    conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name varchar(20) UNIQUE ,password varchar(255))')
    conn.execute('CREATE TABLE posts (message varchar(255), date varchar(30),user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id) )')
    print("Tables created successfully")
    conn.close()
except:
    print("Problem with tables creation :( ")