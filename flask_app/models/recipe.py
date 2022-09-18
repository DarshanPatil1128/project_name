from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Planet:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #self.user_id = data['user_id']
        self.maker = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, instructions, date, under, description, user_id) VALUES (%(recipe_name)s, %(instructions)s, %(date)s, %(under)s, %(description)s, %(user_id)s);"
        results = connectToMySQL('recipes').query_db(query, data)
        print(results)
        return results

    @classmethod
    def all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id "
        results = connectToMySQL('recipes').query_db(query)
        print(results)
        all_recipes = []
        for one in results: 
            one_recipe = cls(one)
            user_data = {
                "id" : one['users.id'],
                "first_name" : one['first_name'],
                "last_name" : one['last_name'],
                "email" : one['email'],
                "name" : one['name'],
                "under" : one['under'],
                "password" : one['password'],
                "created_at" : one['users.created_at'],
                "updated_at" : one['users.updated_at']
            }
            user_obj = user.User(user_data)
            one_recipe.creater = user_obj
            all_recipes.append(one_recipe)
        return all_recipes


    @classmethod
    def get_by_id(cls, recipe):
        query = "SELECT * FROM recipes WHERE id = %(recipe_id)s;"
        results = connectToMySQL("recipes").query_db(query,recipe)
        print(results)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL("recipes").query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes set name = %(name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s, under = %(under)s  WHERE id = %(id)s;"
        result = connectToMySQL('recipes').query_db(query,data)
        print(result)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_by_id(cls, recipe_id):
        print(f"get recipe by id {recipe_id}")
        data = {
            "id" : recipe_id
        }
        query = "SELECT recipes.id, recipes.name, recipes.instructions, recipes.date, recipes.under, recipes.description, recipes.created_at, recipes.updated_at, users.id as user_id, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu FROM recipes JOIN users on users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        print(results)
        results = results[0]
        recipe = cls(results)

        recipe.user = user.User(
                {
                    "id" : results['user_id'],
                    "first_name" : results['first_name'],
                    "last_name" : results['last_name'],
                    "email" : results['email'],
                    "password" : results['password'],
                    "created_at" : results['uc'],
                    "updated_at" : results['uu'],
                }
        )
        return recipe