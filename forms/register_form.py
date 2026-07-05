from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    IntegerField,
    FloatField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    NumberRange
)


class RegisterForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=10, max=10)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    role = SelectField(

        "Register As",

        choices=[
            ("Donor", "Blood Donor"),
            ("Needer", "Blood Needer")
        ],

        validators=[
            DataRequired()
        ]

    )

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

        validators=[
            DataRequired()
        ]

    )

    age = IntegerField(

        "Age",

        validators=[
            DataRequired(),
            NumberRange(min=18, max=65)
        ]

    )

    gender = SelectField(

        "Gender",

        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]

    )

    weight = FloatField(

        "Weight (kg)",

        validators=[
            DataRequired(),
            NumberRange(min=45)
        ]

    )

    city = StringField(

        "City",

        validators=[
            DataRequired()
        ]

    )

    state = StringField(

        "State",

        validators=[
            DataRequired()
        ]

    )

    address = StringField(

        "Address",

        validators=[
            DataRequired()
        ]

    )

    pincode = StringField(

        "Pincode",

        validators=[
            DataRequired(),
            Length(min=6, max=6)
        ]

    )

    submit = SubmitField(
        "Register"
    )