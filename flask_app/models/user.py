from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def __repr__(self) -> str:
        return f"first_name:{self.first_name} last_name:{self.last_name} email:{self.email}"

    @staticmethod
    def validate_new_user(data):
        is_valid=True
        #test first name is at least 2 char and exists and  letters only
        if len(data['first_name']) <2:
            is_valid =False
            flash("First name should be at least 2 char long.","reg_error")
        #test last name is at least 2 char and exits and  letters only
        if len(data['last_name']) <2:
            is_valid =False
            flash("Last name should be at least 2 char long.","reg_error")
        #test email is in proper formation and exits, AND is not Already in db
        if len(data['email'])==0:
            is_valid= False
            flash("You need to provid an email address","reg_error")
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Please provide a valid email address","reg_error")
        elif User.get_user_by_email(data) !=None:
            is_valid=False
            flash("This email is already registered in our database","reg_error")
        #test password is 8 char long and exists
        if len(data['password']) <8 :
            is_valid=False
            flash("you must have a password that is at least 8 char long","reg_error")

        #test that password matches confimration password provided
        if data['password'] != data['password_confirm']:
            is_valid= False
            flash("Password confirmation did not match* please try again","reg_error")
        return is_valid
    
    @classmethod
    def createUser(self,data):
        query = "INSERT INTO users (first_name, last_name,email,password) Values(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL("login_reg_schema").query_db(query,data)
        return results #returns id of new insert

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL("login_reg_schema").query_db(query,data)

        if len(results)==0:
            return None
        else:
            return cls(results[0])
        