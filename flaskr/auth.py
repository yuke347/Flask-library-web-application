import functools

from flask import Blueprint, flash, g, render_template,request, session, url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint("auth",__name__,url_prefix="/auth")
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
        if g.user is None and view.__name__ == "login":
            print(view.__name__)
            return view(**kwargs)
        elif g.user is None and view.__name__ == "signin":
            print(view.__name__)
            return view(**kwargs)
        elif g.user is None:
            return redirect(url_for("auth.login"))
        elif g.user["admin"] == 1 and (view.__name__ == "login" or view.__name__ == "signin" or view.__name__ == "NoEndpoint"):
            print(view.__name__)
            return redirect(url_for("func.admin"))
        elif g.user["admin"] == 1:
            return view(**kwargs)
        else: 
            return redirect(url_for('user.user',id = g.user["id"]))

    return wrapped_view

@bp.route("/signin",methods=("GET","POST"))
@Alogin_required
def signin():
    if request.method == "POST":
        # db = get_db()  
        # db.execute("update user set password = ? where username = admin",(generate_password_hash("admin"),))
        # db.commit()
        username = request.form["username"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        password = request.form["password"]
        dob = request.form["dob"]
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
                # db.execute("INSERT into user (username,FirstName,LastName,Password,DOB,admin)values('admin','admin','admin',?,'11.03.1997',1)",(generate_password_hash("admin"),))
                db.execute("insert into user(username,FirstName,LastName,password,DOB,admin) VALUES(?,?,?,?,?,?)",(username,firstname,lastname,generate_password_hash(password),dob,0))
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already in use."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/signin.html")

@bp.route("/login",methods=("POST","GET"))
@Alogin_required
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
        g.user = get_db().execute("select id,username,FirstName,LastName,Password,admin from user where id = ?",(user_id,)).fetchone()
        
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))



# @bp.route("/",methods=("GET","POST"))
# @Alogin_required
# def NoEndpoint():
#     return render_template("auth/login.html")
# @bp.route("/list",methods=("POST","GET"))
# def listUsers():
#     db = get_db()
#     usersL = db.execute("select * from user").fetchall()
#     for i in usersL:
#         print(i["username"],i["password"],i["admin"],"\n")

