import functools
from jinja2 import Template
from flask import Blueprint, flash, g, render_template,request, session, url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from .auth import Alogin_required,Ulogin_required
import datetime


def defaultOption(query,QM=()):
    global error,bl,db
    error = None
    db = get_db()
    
    g.list = []
    bl = db.execute(query,QM).fetchall()
    for item in bl:
        g.list.append(f"{item["id"]},{item["bookName"]}, {item["author"]}")

bp = Blueprint("user",__name__,url_prefix="")
@bp.route("/<int:id>",methods=("GET","POST"))
@Ulogin_required    
def user(id):
    return render_template("func/user/user.html")

@bp.route("/<int:id>/borrow",methods=("GET","POST"))
@Ulogin_required
def borrowB(id):
    db = get_db()
    defaultOption("select id,bookName,author from books")
    if request.method == "POST":
        amountS = request.form.values()
        amountList = list(amountS)[0]
        amountID = amountList.split(",")[0]
        try:
            borrow_date = datetime.date.today()
            db.execute("insert into borrowings(username_id,book_id,borrow_date)values(?,?,?)"
                        ,(id,amountID,borrow_date))
            db.execute("update books set amount = amount - 1 where id = ?",(amountID,))
            db.commit()
            flash("Borrowing was successful")
        except:
            error = "Book is not available"
            flash(error)
    return render_template("func/user/borrow.html")

@bp.route("/<int:id>/return",methods=("GET","POST"))
@Ulogin_required
def returnB(id):
    db = get_db()
    
    if request.method == "POST":
        amountS = request.form.values()
        amountList = list(amountS)[0]
        amountID = amountList.split(",")[0]
        amountName = amountList.split(",")[1]
        return_date = datetime.date.today()
        print(return_date,amountID)
        try:
            db.execute("update borrowings set return_date = ? where id = ?",(return_date,amountID))
            db.execute("update books set amount = amount + 1 where bookName = ?",(amountName,))
            db.commit()
            error = "Book successfuly returned"
            flash(error)
        except:
            error = "Chyba"
            flash(error)

    defaultOption(query="select borrowings.id,books.bookName,books.author from books join borrowings ON books.id = borrowings.book_id  where username_id = ? and return_date is NULL",QM=(g.user["id"],))
    if bl == []:
        g.list.append("No books borrowed")
    return render_template("func/user/return.html")
    

@bp.route("/<int:id>/account",methods=("GET","POST"))
@Ulogin_required
def account(id):
    db = get_db()
    if request.method == "POST":
        amountS = request.form.values()
        amountList = list(amountS)
        print(amountList)
    defaultOption(query="select borrowings.id,books.bookName,books.author from books join borrowings ON books.id = borrowings.book_id  where username_id = ? and return_date is NULL",QM=(g.user["id"],))
    if bl == []:
        g.list.append("No books borrowed")
    g.list2 = []
    bl2 = db.execute("select borrowings.id,books.bookName,books.author,borrowings.borrow_date, borrowings.return_date from books join borrowings ON books.id = borrowings.book_id  where username_id = ? and return_date is not NULL",(g.user["id"],)).fetchall()
    for item in bl2:
        g.list2.append(f"{item["bookName"]}, {item["author"]}, borrowed: {item["borrow_date"]}, returned: {item["return_date"]}")

    return render_template("func/user/account.html")