from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

db = 'login'

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw_hash = data['pw_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#C
    @classmethod
    def save(cls, info):
        query = 'INSERT INTO users(first_name, last_name, email, pw_hash) VALUE(%(first_name)s,%(last_name)s,%(email)s,%(pw_hash)s)'
        data = {
            "first_name": info['first_name'],
            "last_name": info['last_name'],
            "email": info['email'],
            "pw_hash": info['pw_hash'],
        }
        new_user_id = connectToMySQL(db).query_db(query, data)
        return new_user_id



#R
    @classmethod
    def get_all(cls):
        pass

    @classmethod
    def get_one_by_email(cls, email):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        data = {
            "email": email
        }
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_by_id(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        data = {
            "id": id
        }
        return connectToMySQL(db).query_db(query, data)

#U
    @classmethod
    def update_one(cls):
        pass

#D
    @classmethod
    def delete_one(cls):
        pass


    @staticmethod
    def validate_user(form_data):
        is_valid = True

        if len(form_data['first_name']) < 3 or type(form_data['first_name']) != str:
            is_valid = False
            flash("first name must be a letter and must be 3 or more characters long.")

        if len(form_data['last_name']) < 3 or type(form_data['last_name']) != str:
            is_valid = False
            flash("last name must be a letter and must be 3 or more characters long.")

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form_data['email']): 
            is_valid = False
            flash("Invalid email address!")

        if form_data['pw_hash'] != form_data['confirm_pw_hash']:
            is_valid = False
            flash("Passwords do not match")

        if len(form_data['pw_hash']) < 8 :
            is_valid = False
            flash("Passwords must be 8 characters or longer")

        return is_valid