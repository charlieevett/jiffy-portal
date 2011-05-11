from wtforms import Form, TextField, PasswordField, HiddenField, validators


class UserForm(Form):
    email = TextField('Email Address', [validators.Required(), validators.Length(min=3, max=100), validators.Email()])
    first_name = TextField('First Name', [validators.Required(), validators.Length(max=100)])
    last_name = TextField('Last Name', [validators.Required(), validators.Length(max=100)])
    id = HiddenField()

class NewUserForm(UserForm):
    password = PasswordField("Password", [validators.Required(), validators.Length(min=3, max=100), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Confirm Password", [validators.Required(), validators.Length(min=3, max=100)])

class LoginForm(Form):
    email = TextField('Email Address', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

class PasswordForm(Form):
    password = PasswordField("Password", [validators.Length(min=3, max=100), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField("Confirm Password", [validators.Length(min=3, max=100)])
