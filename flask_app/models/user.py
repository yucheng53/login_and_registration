from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re	# the regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')   # create a regular expression object that we'll use later   


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() )"
        return connectToMySQL('login_and_registration_schema').query_db( query, data )

    @classmethod
    def one_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("login_and_registration_schema").query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users-schema').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_and_registration_schema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Last name must be at least 8 characters.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

