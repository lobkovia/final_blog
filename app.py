from types import NoneType
from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    try:
        with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(f"select name, date, message from posts JOIN users ON posts.user_id == users.id")
                all_posts = cur.fetchall()
    except Exception as e:
            con.rollback()
            all_posts = f"Произошла ошибка запроса сообщений, {e}"
    finally:
        return render_template('index.html',all_posts=all_posts)
        con.close()
    
@app.route('/register',methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            user = request.form['username']
            passw = generate_password_hash(request.form['password'])
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(f"select * from users WHERE name == '{user}'")
                check_username = cur.fetchone()
                if check_username:
                    msg =  "Пользователь с таким именем уже существует"
                    msg_type = 'danger'
                    msg_head = 'Ошибка'
                else:
                    cur.execute(f"INSERT INTO users(name, password) VALUES ('{user}','{passw}')")
                    con.commit()
                    msg = "Регистрация успешна"
                    msg_type = 'success'
                    msg_head = 'Успешно'
        except Exception as e:
            con.rollback()
            msg = f"Произошла ошибка регистрации, {e}"
            msg_type = 'danger'
            msg_head = 'Ошибка'
        finally:
            return render_template("result.html", msg=msg, msg_type=msg_type, msg_head=msg_head)
            con.close()
    else:
        return render_template("register.html")

@app.route('/message', methods = ['POST', 'GET'])
def message():    
    if request.method == 'POST':
        try:
            user = request.form['username']
            passw = request.form['password']
            message = request.form['message']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(f"SELECT id FROM users WHERE name == '{user}'")
                user_id = cur.fetchone()
                if user_id is None: 
                    msg = "Пользователь не зарегистрирован"
                    msg_type = 'danger'
                    msg_head = 'Ошибка'
                else:
                    user_id = user_id[0]
                    cur.execute(f"select password from users where name =='{user}'")
                    entered_passw = cur.fetchone()[0]
                    if check_password_hash(entered_passw,passw):
                        current_time = datetime.now().strftime("%H:%M %d.%m.%Y")
                        cur.execute(f"INSERT INTO posts(date,message,user_id) VALUES ('{current_time}','{message}',{user_id})")
                        msg = "Сообщение успешно опубликовано"
                        msg_type = 'success'
                        msg_head = 'Успешно'
                    else:
                        msg = "Неверный пароль"
                        msg_type = 'danger'
                        msg_head = 'Ошибка'
                con.commit()
        except Exception as e:
            con.rollback()
            msg = f"Произошла ошибка публикации сообщения, {e}"
            msg_type = 'danger'
            msg_head = 'Ошибка'
        finally:
            return render_template("result.html", msg=msg, msg_type=msg_type, msg_head=msg_head)
            con.close()
    
    return render_template('message.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
