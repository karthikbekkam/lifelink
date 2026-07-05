from flask_wtf import FlaskForm

from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed

from wtforms import StringField
from wtforms import IntegerField
from wtforms import SubmitField

from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[DataRequired()]
    )

    phone = StringField(
        "Phone Number",
        validators=[DataRequired()]
    )

    city = StringField(
        "City",
        validators=[DataRequired()]
    )

    state = StringField(
        "State",
        validators=[DataRequired()]
    )

    address = StringField(
        "Address",
        validators=[DataRequired()]
    )

    pincode = IntegerField(
        "Pincode",
        validators=[DataRequired()]
    )

    profile_image = FileField(
        "Profile Photo",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Images only!"
            )
        ]
    )

    submit = SubmitField(
        "Update Profile"
    )