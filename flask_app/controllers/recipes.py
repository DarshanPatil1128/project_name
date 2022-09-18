from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Planet
from flask_bcrypt import Bcrypt

@app.route('/new')
def create_planet_form():
    if "user_id" not in session:
        return redirect('/')
    return render_template('new.html')

@app.route('/back')
def back():
    return redirect('/dashboard')


@app.route('/submit_recipe', methods=["POST"])
def submit_recipe():
    if "user_id" not in session:
        return redirect('/')
    #validations
    # if not Planet.validate_create(request.form):
        # return redirect('/new')
    data = {
        "recipe_name" : request.form["recipe_name"],
        "instructions" : request.form["instructions"],
        "date" : request.form["date"],
        "under" : request.form["under"],
        "description" : request.form["description"],
        "user_id" : session["user_id"]
    }
    Planet.create(data)
    return redirect('/dashboard')

@app.route("/recipes/edit/<int:id>")
def recipe_edit_page(id):
    data ={ 
        "id":id
    }
    return render_template("edit_recipe.html",recipe=Planet.get_one(data))

@app.route('/recipe/update/<int:id>', methods = ["POST"])
def update(id):
    data = {
        "id" : id,
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "date" : request.form['date'],
        "under" : request.form['under'],
    }
    Planet.update(data)
    return redirect('/dashboard')

@app.route('/recipe/delete/<int:id>')
def delete(id):
    data = {
        "id" : id
    }
    Planet.delete(data)
    return redirect('/dashboard')


@app.route('/recipe/view/<int:recipe_id>')
def recipe_detail(recipe_id):
    user = User.get_id(session["user_id"])
    recipe = Planet.get_by_id(recipe_id)
    return render_template("view.html", user=user, recipe=recipe)