from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Date, Time
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    children = db.relationship('Tasks', lazy=True)

    def __repr__(self):
        return f'User {self.username}'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    def new_User():
        new_user = User(username="rafaela", is_active=True)
        db.session.add(new_user)
        db.session.commit()

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_task = db.Column(db.String(250), nullable=False)
    is_done = db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f'Tasks {self.text_task}'
        
    def serialize(self):
        return {
            "id": self.id,
            "text_task": self.text_task
        }