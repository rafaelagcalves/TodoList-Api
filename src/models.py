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
            "name": self.name,
        }
    
    @classmethod
    def get_by_name(cls, name):
        user= cls.query.filter_by(name = name).first()
        return user

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update_name(self, name):
        self.name = name
        db.session.commit()
        return self

    def delete_user(self):
        db.session.delete(self)
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

    @classmethod
    def get_by_id(cls, task_id):
        task = cls.query.filter_by(id = task_id).first()
        return task

    @classmethod
    def get_task(cls, id_tasks):
        tasks= cls.query.get(id_tasks)
        return tasks

    def add(self, user):
        db.session.add(self)
        db.session.commit()

    def update_task(self, new_label, new_done):
        self.label = new_label
        self.is_done = new_done
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()