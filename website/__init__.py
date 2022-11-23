import email
from flask import Flask,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager,current_user
from flask_admin import Admin,BaseView,expose
from flask_admin.contrib.sqla import ModelView

db=SQLAlchemy()
DB_NAME="database.db"

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']="Prasanna123"
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    
    admin = Admin(app,name='Admin',template_mode='bootstrap3')
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")

    from .models import User,Note,Service,Announcement

    with app.app_context():
        db.create_all()

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    class myModelView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('auth.login', next=request.url))
        
        def is_visible(self):
            return True  
    
    class Announcement(BaseView):
        @expose('/')
        def ann(self):
            users = User.query.filter().all()
            print(users[0].email)
            return self.render("admin/announce.html",email=users)

    admin.add_view(ModelView(User,db.session))
    admin.add_view(ModelView(Note,db.session))
    admin.add_view(ModelView(Service,db.session))
    admin.add_view(Announcement(name='Announcement',endpoint='announce'))

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("created database!!")
