from datetime import datetime

from flask_login import UserMixin

from extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"


    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="Donor"
    )

    blood_group = db.Column(
        db.String(5),
        nullable=False
    )

    age = db.Column(
        db.Integer
    )

    gender = db.Column(
        db.String(10)
    )

    weight = db.Column(
        db.Float
    )

    city = db.Column(
        db.String(100)
    )

    state = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.Text
    )

    pincode = db.Column(
        db.String(10)
    )

    latitude = db.Column(
        db.Float,
        default=0.0
    )

    longitude = db.Column(
        db.Float,
        default=0.0
    )

    available = db.Column(
        db.Boolean,
        default=True
    )

    last_donation = db.Column(
        db.Date
    )
    profile_image = db.Column(
        db.String(200),
        default="default.png"
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):

        return f"<User {self.full_name}>"