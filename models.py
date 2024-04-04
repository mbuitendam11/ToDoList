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

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstName: Mapped[str] = mapped_column(String(250), nullable=False)
    lastName: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)

    # Foreign keys linking the other tables
    itemList: Mapped[List["ListedItem"]] = relationship(back_populates="author")
    UserGroup_id: Mapped[List["Grouplist"]] = relationship(back_populates="group")

class Grouplist(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Foregin Key forming relationshop with User
    author_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    group: Mapped["User"] = relationship(back_populates="UserGroup_id")
    # Foregin Key forming relationshop with ListedItem
    group_item: Mapped[List["ListedItem"]] = relationship(back_populates="group_list")
    
class ListedItem(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    subheading: Mapped[str] = mapped_column(String(250), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String)
    dueDate: Mapped[str] = mapped_column(String)

    # Foreign Key forming relationship with User
    author_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="itemList")
    # Foregin Key forming relationshop with GroupList
    group_id: Mapped[int] = mapped_column(db.ForeignKey("grouplist.id"))
    group_list: Mapped["Grouplist"] = relationship(back_populates="group_item")

with app.app_context():
    db.create_all()


# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)