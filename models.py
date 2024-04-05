# Flask Modules
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, LoginManager
# DB management
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import relationship
from typing import List


# Init App
app = Flask(__name__)
app.config['SECRET_KEY'] = "os.environ.get('FLASK_KEY')"
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sqlite3.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

## User Table
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstName: Mapped[str] = mapped_column(String(250), nullable=False)
    lastName: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=True)

    # Foreign keys linking the other tables
    itemList: Mapped[List["Post"]] = relationship(back_populates="author")
    groupMember: Mapped[List["Membership"]] = relationship(back_populates="userMember")

## Group Table
class Group(db.Model): #Previously Named Grouplist
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Foreign Key forming relationship with Post
    group_item: Mapped[List["Post"]] = relationship(back_populates="group_list")
    # Foreign Key forming relationship with Membership
    groupIdentifier: Mapped[List["Membership"]] = relationship(back_populates="groupName")


## Membership Table
class Membership(db.Model): # Need to create a form for assigning users to the membership which includes roles and CRUD ops
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # FK User Table
    userId: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    userMember: Mapped["User"] = relationship(back_populates="groupMember")
    # FK Group Table
    groupId: Mapped[int] = mapped_column(db.ForeignKey("group.id"))
    groupName: Mapped["Group"] = relationship(back_populates="groupIdentifier")

    role: Mapped[str] = mapped_column(String, nullable=False)


## Post Table 
class Post(db.Model): #Previously Named ListedItem
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    subheading: Mapped[str] = mapped_column(String(250), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String)
    dueDate: Mapped[str] = mapped_column(String)

    # Foreign Key forming relationship with User
    author_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="itemList")
    # Foreign Key forming relationshop with GroupList
    group_id: Mapped[int] = mapped_column(db.ForeignKey("group.id"))
    group_list: Mapped["Group"] = relationship(back_populates="group_item")

with app.app_context():
    db.create_all()


# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)