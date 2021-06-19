from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Email:
    def __init__(self, data):
        self.id=data['id']
        self.email=data['email']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def save(cls, data):
        query="INSERT INTO emails (email, created_at, updated_at)" \
            "VALUES (%(email)s, NOW(), NOW());"
        connectToMySQL('email_validation_schema').query_db(query, data)
        flash(f"{data['email']} was added successfully!")

    @classmethod
    def get_all(cls):
        query="SELECT * FROM emails;"
        results = connectToMySQL('email_validation_schema').query_db(query)
        all_emails=[]
        for email in results:
            all_emails.append(cls(email))
        return all_emails

    @classmethod
    def delete(cls, data):
        query="DELETE FROM emails WHERE id=%(id)s;"
        connectToMySQL('email_validation_schema').query_db(query, data)
        flash('User deleted')

    @staticmethod
    def validate_email(data):
        is_valid=True
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address!')
            is_valid=False
        elif Email.check_duplicate(data):
            flash(f"{data['email']} is already in use on this site")
            is_valid=False
        return is_valid

    @staticmethod
    def check_duplicate(data):
        query='SELECT * FROM emails WHERE email=%(email)s;'
        results=connectToMySQL('email_validation_schema').query_db(query, data)
        print(len(results))
        is_dup=False
        if len(results)>0:
            is_dup=True
        return is_dup