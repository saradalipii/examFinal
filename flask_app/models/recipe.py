from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# create a regular expression object that we'll use later   
class Recipe:
    db_name='recipes'
    def __init__(self,data):
        self.id = data['id'],
        self.name = data['name'],
        self.description = data['description'],
        self.dateMade = data['dateMade'],
        self.under30 = data['under30'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']
    
    @classmethod
    def getAllRecipes(cls):
        query= 'SELECT recipes.id,recipes.dateMade as dateMade,recipes.under30 as network, name, COUNT(sceptics.id) as likesNr, users.id as creator_id, users.email as email FROM recipes LEFT JOIN users on recipes.user_id = users.id LEFT JOIN sceptics on sceptics.recipe_id = recipes.id GROUP BY recipes.id;'

        results =  connectToMySQL(cls.db_name).query_db(query)
        recipes= []
        if results:
            for row in results:
                recipes.append(row)
            return recipes
        return recipes
    @classmethod
    def get_recipe_by_id(cls, data):
        query= 'SELECT * FROM recipes LEFT JOIN users on recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]
        
    @classmethod
    def get_user_by_email(cls, data):
        query= 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]
        

    @classmethod
    def get_all_user_info(cls, data):
        query= 'SELECT * FROM users LEFT JOIN posts on posts.user_id = users.id WHERE users.id = %(user_id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
        if results:
            for row in results:
                posts.append(row)
            return posts
        return posts
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM recipes WHERE id=%(recipe_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_recipe(cls,data):
        query = 'UPDATE recipes SET name=%(name)s,description=%(description)s, dateMade=%(dateMade)s, under30=%(under30)s, user_id = %(user_id)s WHERE recipes.id = %(recipe_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    #Class Method to create a user
    @classmethod
    def create_recipe(cls,data):
        query = 'INSERT INTO recipes (name, description, dateMade, under30, user_id) VALUES (%(name)s,%(description)s,%(dateMade)s,%(under30)s,%(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_logged_user_liked_posts(cls, data):
        query = 'SELECT post_id as id FROM likes LEFT JOIN users on likes.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        postsLiked = []
        for row in results:
            postsLiked.append(row['id'])
        return postsLiked

    @classmethod
    def addSceptic(cls, data):
        query= 'INSERT INTO sceptics (recipe_id, user_id) VALUES ( %(recipe_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeSceptic(cls, data):
        query= 'DELETE FROM sceptics WHERE recipe_id= %(recipe_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def removeScepticsPost(cls, data):
        query= 'DELETE FROM sceptics WHERE recipe_id= %(recipe_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 2:
            flash("Title must be at least 3 characters.", 'name')
            is_valid = False
        if len(recipe['under30']) < 2:
            flash("Network must be at least 3 characters.", 'under30')
            is_valid = False    
        if len(recipe['description']) < 3:
            flash("Show description be at least 3 characters.", 'description')
            is_valid = False
        if recipe['dateMade'] == '':
            flash("Date made is required", 'dateMade')
            is_valid = False
        if 'under30' not in recipe:
            flash("Date made is required", 'under30')
            is_valid = False
        return is_valid
    
