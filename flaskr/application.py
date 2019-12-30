from flask import (Flask, render_template, redirect,  request, url_for)
from flask_sqlalchemy import (SQLAlchemy)
from flask_login import (LoginManager, login_required, login_user, current_user, logout_user, UserMixin)
from werkzeug.security import (generate_password_hash, check_password_hash)
import io

#----App Configurations----
app =   Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db';
app.config['SECRET_KEY'] = "t1KhONWYGNEtZ0sh"

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
#--------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passwordhash = db.Column(db.String(64), nullable=False)
    stars = db.Column(db.Integer, default=0, nullable=False)
    
    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#---------- ROUTES ----------
@app.route('/', methods=["GET"])
def index():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = str(request.)
        print(username)
        password = str(request.args.get("password"))
        print(password)
        confirm = str(request.args.get("confirm"))
        print(confirm)

        if(len(username) == 0 or len(password) == 0 or len(confirm) == 0):
            return "Invalid Length"

        if(password != confirm):
            return "Passwords dont match"

        passwordhashed = generate_password_hash(password)
        return render_template("profile.html")
    else:
        return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        redirect(url_for(index))
    
    return render_template("login.html")

@app.route('/profile', methods=["GET"])
@login_required
def profile():
    return render_template("profile.html", Username="Jinxx", Stars_collected="6")

@app.route('/level', methods=["GET"])
@login_required
def level():
    return render_template("level.html")


