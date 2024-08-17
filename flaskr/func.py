import functools
from jinja2 import Template
from flask import Blueprint, flash, g, render_template,request, session, url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from .auth import Alogin_required

bp = Blueprint("func",__name__,url_prefix="/admin")

@bp.route("/",methods=("GET","POST"))
@Alogin_required
def admin():
    return render_template("func/admin/admin.html")

@bp.route("/addBook",methods=("GET","POST"))
@Alogin_required
def addBook():
    if request.method == "POST":
        bookName = request.form["bookName"]
        author = request.form["Author"]
        published = request.form["Published"]
        genre = request.form["Genre"]
        db = get_db()
        error = None
        try:
            db.execute("insert into bookArchive(bookName,author,published,genre)values(?,?,?,?)",(bookName,author,published,genre))
        except:
            pass
        try:
            db.execute("insert into books(bookName,author,published,genre)values(?,?,?,?)",(bookName,author,published,genre))
            
            db.commit()
            error = f"{bookName} was successfuly registered"
        except db.IntegrityError:
            error = f"{bookName} is already registered"
        flash(error)

    return render_template("func/admin/addBook.html")

@bp.route("/setAmount",methods=("GET","POST"))
@Alogin_required
def setAmount():
    db = get_db()
    error = None
    g.list = []
    bl = db.execute("select bookName,author from books").fetchall()
    if request.method == "POST":
        amountS = request.form.values()
        amount = int(request.form["setAmount"])
        try:
            amountSname = list(amountS)[0].split(",")[0]
            print(amountSname)
            db.execute("update books set amount = ? where bookName=?",(amount,amountSname))
            db.commit()
            flash("Set successful")
        except:
            error = "Chyba"
            flash(error)
            
    for item in bl:
        
        g.list.append(f"{item["bookName"]}, {item["author"]}")
        

    return render_template("func/admin/setAmount.html")

@bp.route("/removeBook",methods=("GET","POST"))
@Alogin_required
def removeBook():
    db = get_db()
    error = None
    g.list = []
    bl = db.execute("select bookName,author from books").fetchall()
    if request.method == "POST":
        amountS = request.form.values()
        try:
            amountSname = list(amountS)[0].split(",")[0]
            db.execute("delete from books where bookName = ?",(amountSname,))
            db.commit()
            flash("Remove successful")
        except:
            error = "Chyba"
            flash(error)

    for item in bl:
        g.list.append(f"{item["bookName"]}, {item["author"]}")
    return render_template("func/admin/removeBook.html")

