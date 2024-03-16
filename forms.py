from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, DateField, SelectField
from wtforms.validators import DataRequired
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

# Add toDo item form
class addToDo(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subheading = StringField("Subheading", validators=[DataRequired()])
    content = CKEditorField("What are you trying to do", validators=[DataRequired()])
    dueDate = DateField(validators=[DataRequired()])
    priority = SelectField("Priority Level", choices=[("urgent", "Urgent"), ("high", "High"), ("medium", "Medium"), ("low", "Low")], validators=[DataRequired()])
    submit = SubmitField("Add Item")