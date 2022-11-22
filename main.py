from flask import Flask,redirect,url_for,render_template,request
from website import create_app
app=create_app()
# app=Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/signup",methods=["POST","GET"])
# def signup():
#     # if request.method=="POST":
#         return render_template("signup.html")

# @app.route("/login",methods=["POST","GET"])
# def login():
#     return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True)