from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Email


class ForgotPasswordForm(FlaskForm):

    email = StringField(

        "Email Address",

        validators=[
            DataRequired(),
            Email()
        ]

    )

    submit = SubmitField(

        "Send Reset Link"

    )