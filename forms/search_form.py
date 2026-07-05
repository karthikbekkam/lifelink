from flask_wtf import FlaskForm

from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField

from wtforms.validators import DataRequired


class SearchForm(FlaskForm):

    blood_group = SelectField(

        "Blood Group",

        choices=[

            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
            ("O+", "O+"),
            ("O-", "O-")

        ],

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

    submit = SubmitField(

        "Search Donors"

    )