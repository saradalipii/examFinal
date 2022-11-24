from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import flash


@app.route('/createRecipe')
def createForm():
    if 'user_id' not in session:
        return redirect('/logout')
        
    return render_template('createRecipe.html', loggedUser= User.get_user_by_id(data),)


@app.route('/create/recipe', methods = ['POST'])
def createRecipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
    
    Recipe.create_recipe(data)
    return redirect('/')
