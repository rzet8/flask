import random
import secret
import pymysql as sql
import threading

from flask import Flask, \
    render_template, request, redirect, url_for, make_response, session

app = Flask(__name__)
db = sql.connect("eu-cdbr-west-03.cleardb.net","b6c312c632ac2c", "ac11d03d", "heroku_21197fac3394bf1")
cursor = db.cursor()
lock = threading.Lock()

@app.route("/")
def chat():
    try:
        token = session['token']

        with lock:
            cursor.execute(f"SELECT * FROM `users` WHERE `token` = '{token}'")
            data = cursor.fetchone()
        
        return f"Hello, {data[0]}"
    except:
        return redirect("/auth")
    return token

@app.route("/auth")
def auth():
    if request.args.get('err'):
        return render_template("auth.html", err=request.args.get('err'))

    else:
        return render_template("auth.html")

@app.route("/api/auth")
def api_auth():
    print(request.args.get('m'))
    if request.args.get('m') == 'reg':
        try:

            login = request.args.get('login')

            password = request.args.get('password')
            token = secret.generate()

            if len(login) > 12:
                return redirect("/auth")
            if len(password) > 24:
                return redirect("/auth")

            with lock:
                cursor.execute(f"INSERT INTO `users`(`login`, `password`, `dialogs`, `token`) VALUES ('{login}', '{password}', 'none', '{token}')")
                db.commit()

            session['token'] = token

            return redirect("/")
            
        except Exception as e:
            print(e)
            return redirect("/auth?err=This login already used")
    elif request.args.get('m') == 'log':
        try:
        
            login = request.args.get('login')
            password = request.args.get('password')
            token = secret.generate()
            with lock:
                cursor.execute(f"SELECT * FROM `users` WHERE `login` = '{login}'")
                data = cursor.fetchone()

            if data[1] == password:


                with lock:
                    cursor.execute(f"UPDATE `users` SET `token`= '{token}' WHERE `login` = '{login}'")
                    db.commit()
            
                session['token'] = token

                return redirect("/")
            else:
                return redirect("/auth?err=Invalid login or password")

        except Exception as e:
            return redirect("/auth?err=Invalid login or password")

    else:
        return "Error method"
        

@app.route("/profile/<string:id>")
def profile(id):
    return id

@app.route("/logout")
def logout():
    try:
        session['token'] = "logout"
    except:
        pass
    return redirect("/auth")

@app.errorhandler(404)
def go(e):
    return redirect("/")


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5555)
