import functools

from flask import Blueprint, flash, g, render_template,request, session, url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint("auth",__name__,url_prefix="/auth")

@bp.route("/signin",methods=("GET","POST"))
def signin():
    if request.method == "POST":
        # db = get_db()  
        # db.execute("update user set password = ? where username = admin",(generate_password_hash("admin"),))
        # db.commit()
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()      
        error = None
        if not username:
            error = "Username is required."
        elif not password and username:
            error =  "Username and password is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                # db.execute("insert into user(username,password,admin)values('admin',?,1)",(generate_password_hash("admin"),))
                db.execute("insert into user(username,password,admin) VALUES(?,?,?)",(username,generate_password_hash(password),0))
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already in use."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/signin.html")

@bp.route("/login",methods=("POST","GET"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username,password)
        db = get_db()
        error = None
        user = db.execute("select * from user where username = ?",(username,)).fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"],password):
            error = "Incorrect password"
        if error is None and user["admin"] == 1:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("func.admin"))
        elif error is None and user["admin"] == 0:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("user.user",id = user["id"]))
        flash(error)
    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("select * from user where id = ?",(user_id,)).fetchone()

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

def Ulogin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user["admin"] == 1:
            return redirect(url_for('func.admin'))
        else:
            return view(**kwargs)
    return wrapped_view

def Alogin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        
        if g.user is None:
            return redirect(url_for('auth.login'))
        elif g.user["admin"] == 1:
            
            return view(**kwargs)
        else: 
            return redirect(url_for('user.user',id = g.user["id"]))
    return wrapped_view
# @bp.route("/list",methods=("POST","GET"))
# def listUsers():
#     db = get_db()
#     usersL = db.execute("select * from user").fetchall()
#     for i in usersL:
#         print(i["username"],i["password"],i["admin"],"\n")

