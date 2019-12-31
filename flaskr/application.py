import flask
import flask_login
import flask_sqlalchemy
import jsonify
from werkzeug.security import (generate_password_hash, check_password_hash)

# ---- Configs ----
app = flask.Flask(__name__)
app.config.from_pyfile('config.cfg')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

db = flask_sqlalchemy.SQLAlchemy(app)
# -----------------

# ---- Routes ----
@app.route('/', methods=['GET'])
def index():
    if flask_login.current_user.is_authenticated:
        return flask.redirect('/profile')
    else:
        return flask.redirect('/register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        if len(username) == 0 or len(password) == 0:
            return "Invalid Input"
        
        user = User.authenticateUser(username, password)
        if not user:
            return "Invalid Password or Username"
        flask_login(user)
        return flask.redirect("/profile")
    elif flask.request.method == 'GET':
        return flask.render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")
        confirm = flask.request.form.get("confirm")

        if User.findUser("username", username) != None:
            return "Username taken"

        if len(username) == 0 or len(password) == 0 or len(confirm) == 0:
            return "Invalid Input"

        if password != confirm:
            return "Passwords dont match"
  
        user = User(username, password)
        flask_login.login_user(user)
        return flask.redirect('/profile')
    elif flask.request.method == 'GET':
        return flask.render_template("register.html")

@app.route('/logout', methods=['GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect('/login')

@app.route('/profile', methods=['GET'])
@flask_login.login_required
def profile():
    return flask.render_template("profile.html", Username=flask_login.current_user.username, Games_Played=flask_login.current_user.games_played, Games_Won=flask_login.current_user.games_won)

@app.route('/level', methods=['GET'])
def level():
    return flask.render_template("level.html")

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    headers = ["Username", "Games Played", "Games Won"]
    data = []
    for user in User.dbAsArray():
        row = []
        row.append(user.username)
        row.append(user.games_played)
        row.append(user.games_won)
        data.append(row)
    return flask.render_template("leaderboard.html", headers=headers, data=data)

@app.route('/available', methods=['GET'])
def isUsernameAvailable():
    username = flask.request.args("username")
    if User.findUser("username", username) == None:
        return jsonify("True")
    return jsonify("False")

@app.route('/stats/', methods=['POST'])
def addStats():
    if flask_login.current_user.is_authenticated:
        stats = flask.request.json
        flask_login.current_user.playedGame(stats['won'])
        return flask.Response(status=200)
    return flask.Response(status=403)
# ----------------

# ---- Login Manager ----
@login_manager.user_loader
def load_user(user_id):
    return User.findUser("id", user_id)
# -----------------------

# ---- User Class ----
class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passwordhashed = db.Column(db.String(64), nullable=False)
    games_played = db.Column(db.Integer, nullable=False, default=0)
    games_won = db.Column(db.Integer, nullable=False, default=0)
    
    def __init__(self, username, password, addToDatabase=True):
        self.username = username
        self.passwordhashed = generate_password_hash(password)
        if(addToDatabase):
            User.addUser(self)
    
    def addUser(self):
        db.session.add(self)
        db.session.commit()

    def removeUser(self):
        db.session.remove(self)
        db.session.commit()

    def findUser(Key, Value):
        Key = str.lower(Key)
        if(Key == "username"):
            return User.query.filter_by(username=Value).first()
        if(Key == "id"):
            return User.query.filter_by(id=Value).first()

    def authenticateUser(username, password):
        user = User.findUser("username", username)
        if user == None:
            return False
        if check_password_hash(user.passwordhashed, password):
            return user
        else:
            return False
    
    def playedGame(self, Won=False):
        self.games_played += 1
        if Won:
            self.games_won += 1
        db.session.commit()
    
    def asArray(self):
        return [self.username, self.games_played, self.games_won]
    
    def dbAsArray():
        return User.query.order_by(User.games_won).all()
# --------------------
