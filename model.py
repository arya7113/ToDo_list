from flask_sqlalchemy import SQLAlchemy
from enum import Enum
db = SQLAlchemy()

class Login(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    login_id = db.Column(db.Integer(),db.ForeignKey('login.id'), nullable=False)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(30),unique=True,nullable=False)

class category(Enum):
    Work = 'Work'
    Personal = 'Personal'
    Home = 'Home'
    Social = 'Social'
class TaskCategory(db.Model):
    __tablename__= 'task_category'
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(25),nullable=False,unique=True)
    

class priority(Enum):
    High = 'High'
    Medium = 'Medium'
    Low = 'Low'
class task_status(Enum):
    Pending = 'Pending'
    Completed = 'Completed'
    Canceled = 'Canceled'
class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    category_id = db.Column(db.Integer(),db.ForeignKey('task_category.id'), nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'), nullable=False)
    task = db.Column(db.String(), nullable=False)
    priority = db.Column(db.Enum(priority),nullable=False)
    status = db.Column(db.Enum(task_status),nullable=False)
    date = db.Column(db.DateTime(),nullable=False)
    category = db.relationship('TaskCategory', backref='tasks')

    @property
    def display_priority(self):
        """Return the human-readable priority."""
        return self.priority.name  

    @property
    def display_status(self):
        """Return the human-readable priority."""
        return self.status.name  

