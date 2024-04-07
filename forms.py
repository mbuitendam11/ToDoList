from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, DateField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Optional
from wtforms.fields import DateTimeLocalField
from flask_ckeditor import CKEditorField


# Register User Form
class RegisterUser(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    role = SelectField("What is your role?", choices=[("admin", "Admin"), ("manager", "Manager"), ("employee", "Employee")], validators=[DataRequired()])
    submit = SubmitField("Register")


# Login User Form
class loginUser(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# CREATE/UPDATE Post form
class addToDo(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subheading = StringField("Subheading", validators=[DataRequired()])
    content = CKEditorField("What are you trying to do", validators=[DataRequired()])
    dueDate = DateTimeLocalField("Due Date", validators=[Optional()])
    priority = SelectField("Priority Level", choices=[("1", "Urgent"), ("2", "High"), ("3", "Medium"), ("4", "Low")], validators=[DataRequired()])
    submit = SubmitField("Add Item")

# CREATE/UPDATE Group form
class createGroup(FlaskForm):
    name = StringField("Name of Group", validators=[DataRequired()])
    submit = SubmitField("Add Item")

# CREATE/UPDATE Membership form
class createMember(FlaskForm):
    groupId = StringField("Group Name", validators=[DataRequired()])
    userMember = StringField("What is there email?", validators=[DataRequired()])
    role = SelectField("What is their role", choices=[("admin", "Admin"), ("manager", "Manager"), ("employee", "Employee")], validators=[DataRequired()])
    submit = SubmitField("Add User")