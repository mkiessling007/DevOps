from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class RestApiForm(FlaskForm):
    hostname = StringField('Rest API Server', validators=[DataRequired()])
    restapicall = StringField('Rest API call', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    html = BooleanField('HTML Output')
    submit = SubmitField('Go!')
