import functools
from jinja2 import Template
from flask import Blueprint, flash, g, render_template,request, session, url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from .auth import Alogin_required,check_password_hash
import time
bp = Blueprint("func",__name__,url_prefix="/admin")



@bp.route("/",methods=("GET","POST"))
@Alogin_required
def admin():
    # print(g.user["admin"] )
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
   
    # session.pop('_flashes', None)
    db = get_db()
    error = None
    g.list = []
    bl = db.execute("select bookName,author from books").fetchall()
    if request.method == "POST":
        amountS = request.form.values()
        
        try:
            amount = int(request.form["setAmount"])
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
    bl = db.execute("select id,bookName,author from books").fetchall()
    if request.method == "POST":
        amountS = request.form.values()
        try:
            amountSID = list(amountS)[0].split(",")[0]
            a = db.execute("""delete from books 
where books.ID not in (select book_id from borrowings where borrowings.return_date is NULL) and books.ID = ? returning ID""",(amountSID,))
            db.commit()
            flash("Remove successful")
        except:
            error = "Book is still borrowed"
            flash(error)

    for item in bl:
        g.list.append(f"{item["id"]}, {item["bookName"]}, {item["author"]}")
    return render_template("func/admin/removeBook.html")

@bp.route("/manageUsers",methods=("GET","POST"))
@Alogin_required
def manageUsers():
    db = get_db()
    error = None
    g.list = []
    g.listB = []
    g.listR = []
    print(request.method)
    if request.method == "POST":
        passws = list(request.form.values())
        print(passws)
        user = passws[0].strip()
        old = passws[1]
        new = passws[2]
        print(user,old,new)
        userP = db.execute("select password from user where username = ?",(user,)).fetchone()
        # userP = list(userP)[0]
        
        if  userP is not None and check_password_hash(list(userP)[0],old) == True:
            
            db.execute("update user set password = ? where username = ?",(generate_password_hash(new),user))
            db.commit()
            flash("Password changed")
        else:
            flash("Incorrect password")
    ul = db.execute("select * from user").fetchall()
    bl = db.execute("select * from books").fetchall()
    rl = db.execute("""select borrowings.id,user.username,bookArchive.bookName,borrow_date,return_date  from borrowings
                        join bookArchive on borrowings.book_id = bookArchive.id
                        join user on borrowings.username_id = user.id""").fetchall()
    for item in ul:
        g.list.append(f"{item["Username"]}")
    for item in bl:
        g.listB.append(f"{item["bookName"]}, Amount: {item["amount"]}")
    for item in rl:
        g.listR.append(list(item))

    
    return render_template("func/admin/manageUsers.html")   

