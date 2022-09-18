from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Planet
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home_page():
    return render_template("home_page.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    print(request.form)
    if not User.validate_create(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash,
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/login', methods=["POST"])
def login():
    print(request.form)
    data = {
        "email" : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("dashboard.html", logged_in_user = User.get_by_id(data), all_the_recipes = Planet.all_recipes())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')