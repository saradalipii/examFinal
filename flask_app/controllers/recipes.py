from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import flash


@app.route('/createRecipe')
def createForm():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    return render_template('createRecipe.html', loggedUser= User.get_user_by_id(data),)


@app.route('/create/recipe', methods = ['POST'])
def createRecipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
    Recipe.create_recipe(request.form)
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'recipe_id': id,
        'user_id': session['user_id']
    }
    currentRecipe = Recipe.get_recipe_by_id(data)

    if not session['user_id'] == currentRecipe['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
    Recipe.removeScepticsPost(data)
    Recipe.delete(data)
    return redirect(request.referrer)


@app.route('/recipe/<int:id>')
def showOne(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'recipe_id': id,
        'user_id': session['user_id']
    }
    
    return render_template('recipe.html', loggedUser= User.get_user_by_id(data),recipe = Recipe.get_recipe_by_id(data),    userLikedRecipe2 = User.get_logged_user_liked_posts2(data), userLikedRecipe = User.get_logged_user_liked_posts(data)
)

@app.route('/edit/<int:id>')
def editForm(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
            'recipe_id': id,
            'user_id': session['user_id']
        }
    currentRecipe = Recipe.get_recipe_by_id(data)

    if not session['user_id'] == currentRecipe['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
    return render_template('updateRecipe.html', loggedUser= User.get_user_by_id(data), recipe = Recipe.get_recipe_by_id(data))

@app.route('/update/recipe/<int:id>', methods = ['POST'])
def updateRecipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
    data = {
        'recipe_id': id,
        'user_id': session['user_id'],
        'name' : request.form['name'],
        'description' : request.form['description'],
        'dateMade' : request.form['dateMade'],
        'under30' : request.form['under30'],
        }

    currentRecipe = Recipe.get_recipe_by_id(data)

    if not session['user_id'] == currentRecipe['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
    
    Recipe.update_recipe(data)

    return redirect('/')

@app.route('/sceptic/<int:id>')
def addSceptic(id):
    data = {
        'recipe_id' : id,
        'user_id' : session['user_id']
    }
    userLikedRecipe = User.get_logged_user_liked_posts(data)
    if 'recipe_id' in userLikedRecipe:
        return redirect(request.referrer)
    Recipe.addSceptic(data)
    return redirect(request.referrer)

@app.route('/unsceptic/<int:id>')
def removeSceptic(id):
    data = {
        'recipe_id' : id,
        'user_id' : session['user_id']
    }
    Recipe.addSceptic(data)
    Recipe.removeSceptic(data)
    return redirect(request.referrer)
