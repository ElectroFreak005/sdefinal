import bcrypt 
from io import BytesIO
from flask import Blueprint,render_template,request,flash,redirect,url_for,send_file
from .models import Announcement, User
from werkzeug.security import generate_password_hash,check_password_hash
from .import db
from flask_login import login_user,login_required,logout_user,current_user
from flask_login import LoginManager
from .import db
from .models import User,Note,Service,Announcement,To_do
from datetime import datetime
import smtplib
import ssl
from email.message import EmailMessage

email_sender = 'swathika.appartments@gmail.com'
email_password = 'oppboasaputtehar'
email_receiver = ''


auth=Blueprint('auth',__name__)

@auth.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('pass')
        user=User.query.filter_by(email=email).first()
        if email == "admin@gmail.com":
            if password == "123456789":
                # login_user(user,remember=True)
                return redirect("admin")
        if user:
            if check_password_hash(user.password,password):
                login_user(user,remember=True)
                return redirect(url_for("auth.tenent"))
                # return render_template("tenent.html",user=user)

            else:
                flash("incorrect password, try again",category='error')
        else:
            flash("email does not exist ",category='error')
    # n = To_do.query.filter_by(user_id=3).first()
    # print(n.rent)
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
        file=request.files['img']
        fn=file.filename
        print(file)
        #destination email
        dest = request.form.get("dest")
        img_file = request.form.get("img")
        print(img_file)
        print(dest)

        #post message
        current_dateTime = datetime.now()

        #email-sending-section
        subject = 'New message recieved!'
        body = f""" From : {current_user.email}
        Name: {current_user.name}
        Message : {note}"""
        email_receiver = str(dest)
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        newnote=Note(user_id=current_user.id,source=current_user.email,dest = dest,data=note,filename=fn,raw_data=file.read(),date=current_dateTime)
        print(current_user.name)
        db.session.add(newnote)
        db.session.commit()
        return render_template("tenent.html",user=current_user, email=users)
        
    #recieved messages by current user
    curr_msg = Note.query.filter().all()
    # print(session["username"])
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
            rent = False
            new_list = To_do(email=email, rent = rent,main = rent,dr = rent, eb = rent)
            db.session.add(new_list)
            db.session.commit()
            # login_user(user,remember=True)
            flash("Account Created!!",category="success")
            return redirect("/login")
        #return redirect(url_for('views.home'))
            # return redirect(url_for('auth.login'))

       
    return render_template("signup.html",user=current_user)

# @auth.route("/admin-login")
# def admin():
#     # services = Service.query.filter().all()
#     return render_template("login.html")

@auth.route("/todo")
def to_do():
    curr_user = current_user.id
    curr_email = current_user.email
    new = To_do.query.filter_by(email = curr_email).first()
    print(curr_user)
    print(new.user_id)
    return render_template("to_do.html",val=new)

@auth.route("/to-do",methods=["POST","GET"])
def to():
    if request.method == "POST":
        email = request.form.get("email")
        rent = request.form.get("rent")
        if rent == 'True':
            rent = True
        else:
            rent = False
        main = request.form.get("main")
        if main == 'True':
            main = True
        else:
            main = False
        dr = request.form.get("dr")
        if dr == 'True':
            dr = True
        else:
            dr = False
        eb = request.form.get("eb")
        if eb == 'True':
            eb = True
        else:
            eb = False
        print("email",email)
        print("email",rent)
        print("email",main)
        print("email",dr)
        print("email",eb)
        # new_list = To_do(email=email, rent = rent,main = main,dr = dr, eb = eb)
        
        # db.session.add(new_list)
        entry = To_do.query.filter_by(email=email).first()
        entry.rent = rent
        entry.main = main
        entry.dr = dr
        entry.eb = eb
        db.session.commit()
        return "Post request"

@auth.route("/download/<upload_id>")
def download(upload_id):
    fc = Note.query.filter_by(id=upload_id).first()
    print(fc.filename)
    return send_file(BytesIO(fc.raw_data),download_name = fc.filename, as_attachment=True)
    # print(upload_id)