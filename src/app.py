from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

# Models
from models.UserModel import UserModel

# Entities
from models.entities.User import User


app = Flask(__name__)
csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return UserModel().getById(db, id) #Se debe instanciar un objeto del modelo 
                                       #Cuando no se instancia el modelo, se produce el error missing 1 required positional argument: 'id'


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form['txtLogin'])
        #print(request.form['txtPassword'])
        user = User(0, request.form['txtLogin'], request.form['txtPassword'])
        logged_user = UserModel.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user) #Almacenar el usuario loggeado en FlashSession
                return redirect(url_for("home"))
            else:
                flash("Invalid password...")    
                return render_template("login/login.html")    
        else:
            flash("User not found.")    
            return render_template("login/login.html")
    else:
        return render_template("login/login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/home")
@login_required
def home():
    return render_template("home/home.html")

@app.route("/protected")
@login_required
def protected():
    return render_template("home/protected.html")

def status_401(error):
    return redirect(url_for("login"))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True, port=5000)