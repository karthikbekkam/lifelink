from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import TextAreaField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Email


class RequestForm(FlaskForm):

    requester_name = StringField(

        "Patient Name",

        validators=[DataRequired()]

    )

    requester_email = StringField(

        "Email Address",

        validators=[
            DataRequired(),
            Email()
        ]

    )

    requester_phone = StringField(

        "Phone Number",

        validators=[DataRequired()]

    )

    city = StringField(

        "City",

        validators=[DataRequired()]

    )

    message = TextAreaField(

        "Message"

    )

    submit = SubmitField(

        "Send Blood Request"

    )