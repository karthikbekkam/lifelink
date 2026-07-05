from flask_wtf import FlaskForm

from wtforms import PasswordField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Length


class ResetPasswordForm(FlaskForm):

    password = PasswordField(

        "New Password",

        validators=[
            DataRequired(),
            Length(min=6)
        ]

    )

    confirm_password = PasswordField(

        "Confirm Password",

        validators=[
            DataRequired(),
            EqualTo("password")
        ]

    )

    submit = SubmitField(

        "Reset Password"

    )