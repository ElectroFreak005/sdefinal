import bcrypt 
from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import Announcement, User
from werkzeug.security import generate_password_hash,check_password_hash
from .import db
from flask_login import login_user,login_required,logout_user,current_user
from flask_login import LoginManager
from .import db
from .models import User,Note,Service,Announcement
from datetime import datetime




auth=Blueprint('auth',__name__)

@auth.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('pass')
        user=User.query.filter_by(email=email).first()
        if email == "admin@gmail.com":
            if check_password_hash(user.password,password):
                return redirect("/admin")
        if user:
            if check_password_hash(user.password,password):
                login_user(user,remember=True)
                return redirect(url_for("auth.tenent"))
                # return render_template("tenent.html",user=user)

            else:
                flash("incorrect password, try again",category='error')
        else:
            flash("email does not exist ",category='error')
    return render_template("login.html",user=current_user)


# @auth.route("/tenent",methods=["POST","GET"])
# def tenent(email):
#     user=User.query.filter_by(email=email).first()
#     return render_template("tenent.html",user=user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("logged out successfully")
    return redirect(url_for("auth.login"))



@auth.route("/tenent",methods=['POST','GET'])
@login_required
def tenent():
    # print("hweri")
    users=User.query.filter().all()
    # print(users[0].email)
    
    if request.method=='POST':
        # print("prasanna")
        note=request.form.get("notes")

        #destination email
        dest = request.form.get("dest")
        print(dest)

        #post message
        current_dateTime = datetime.now()
        newnote=Note(user_id=current_user.id,source=current_user.email,dest = dest,data=note,date=current_dateTime)
        print(current_user.name)
        db.session.add(newnote)
        db.session.commit()
        return render_template("tenent.html",user=current_user, email=users)
        
    #recieved messages by current user
    curr_msg = Note.query.filter().all()
    return render_template("tenent.html",user=current_user, email=users, curr_msg=curr_msg)


@auth.route("/service")
@login_required
def service():
    services = Service.query.filter().all()
    return render_template("service.html",list=services)


@auth.route("/announcements",methods=['POST', 'GET'])
def ann():
    services = Announcement.query.filter().all()
    if request.method == 'POST':
        
        note=request.form.get("notes")

        #destination email
        dest = request.form.get("dest")
        print(dest)
        if dest == "Announcements":
            current_dateTime = datetime.now()
            newnote=Announcement(data=note,date=current_dateTime)
            # print(current_user.name)
            db.session.add(newnote)
            db.session.commit()
        else:
            newnote=Note(user_id=1,source="admin@gmail.com",dest = dest,data=note,date=current_dateTime)
            # print(current_user.name)
            db.session.add(newnote)
            db.session.commit()
        return redirect("admin/announce")
    return render_template("announcements.html",list=services)


@auth.route("/signup",methods=['POST','GET'])
def signup():
    if request.method=='POST':
       username=request.form.get("username")
       name=request.form.get("name")
       apno=request.form.get("apno")
       email=request.form.get("email")
       password=request.form.get("password")
       password1=request.form.get("password1")
       user=User.query.filter_by(email=email).first()
       
       if user:
            flash("email already exists",category='error')
       elif len(email) <4:
            flash("email should be greater than 3 characters",category="error")
       elif len(name) and len(username) <2:
            flash("name and username should be greater than 3 characters",category="error")
        
       elif password1!=password:
            flash("password do not match",category="error")
        
       elif len(password1) <7:
            flash("password should be greater than 6 characters",category="error")
        
       else:
            new_user=User(email=email,password=generate_password_hash(password,method='sha256'),name=name,apno=apno,username=username)
            db.session.add(new_user)
            db.session.commit()
            # login_user(user,remember=True)
            flash("Account Created!!",category="success")
            return redirect("/login")
        #return redirect(url_for('views.home'))
            # return redirect(url_for('auth.login'))

       
    return render_template("signup.html",user=current_user)