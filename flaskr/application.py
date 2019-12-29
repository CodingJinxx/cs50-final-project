from flask import (Flask, render_template, redirect,  request)
from flask_login import (LoginManager, login_required, login_user, logout_user)
from user import (User)
from database import (InitDatabase)
import os

#----App Configurations----
app=   Flask(__name__)
app.secret_key = "t1KhONWYGNEtZ0sh"

app.config["TEMPLATES_AUTO_RELOAD"] = True

if(os.getenv("INIT_DATABASE") == "True"):
    InitDatabase()
    os.putenv("INIT_DATABASE", "False")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view
#--------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/', methods=["GET"])
def hello_world():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        return 0
    else:
        return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route('/profile', methods=["GET"])
@login_required
def profile():
    return render_template("profile.html", Username="Jinxx", Stars_collected="6")

@app.route('/level', methods=["GET"])
@login_required
def level():
    return render_template("level.html")

if __name__ == "__main__":
    app.run()