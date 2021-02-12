from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Date, Time
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

class User(db.Model):
    __tablename__="user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    task = db.relationship('Task', lazy=True)

    def __repr__(self):
        return f'User {self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
    @classmethod
    def get_by_name(cls, name):
        user= cls.query.filter_by(name= name).first()
        return user

    def add(self):
        db.session.add(self)
        db.session.commit()


class Task(db.Model):
    __tablename__="tasks"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(250), nullable=False)
    is_done = db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f'The task {self.label} has the status {self.is_done}'
        
    def serialize(self):
        return {
            "id": self.user_id,
            "label": self.label,
            "is_done": self.is_done,
        }

    @classmethod
    def get_by_user(cls, user):
        tasks= cls.query.filter_by(user_id=user)
        return tasks

    def add(self, user):
        db.session.add(self)
        db.session.commit()