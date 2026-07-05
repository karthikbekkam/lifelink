from flask_wtf import FlaskForm

from wtforms import PasswordField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Length


class ChangePasswordForm(FlaskForm):

    current_password = PasswordField(

        "Current Password",

        validators=[
            DataRequired()
        ]

    )

    new_password = PasswordField(

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
            EqualTo("new_password")
        ]

    )

    submit = SubmitField(

        "Change Password"

    )