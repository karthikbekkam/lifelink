from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import TextAreaField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Length


class ContactForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    subject = StringField(
        "Subject",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Send Message"
    )