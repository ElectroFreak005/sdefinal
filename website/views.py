from flask import Blueprint,render_template,request,redirect
from flask_login import login_user,login_required,logout_user,current_user
from .import db
from .models import User,Note
from datetime import datetime

views=Blueprint('views',__name__)

@views.route("/")
def home():
    return render_template("index.html")


# @views.route("/admina")
# def admin():
#     return redirect("/admin")


# @views.route("/tenent",methods=["POST","GET"])
# @login_required
# def tenent():
#     print("hweri")
#     if request.method=="POST":
#         print("prasanna")
#         note=request.form.get("notes")
#         current_dateTime = datetime.now()
#         newnote=Note(user_id=current_user.id,data=note,date=current_dateTime)
#         db.session.add(newnote)
#         db.session.commit()
#         return render_template("tenent.html",user=current_user)
#     return render_template("tenent.html",user=current_user)
