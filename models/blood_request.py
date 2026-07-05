from datetime import datetime

from extensions import db


class BloodRequest(db.Model):

    __tablename__ = "blood_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    requester_name = db.Column(
        db.String(100),
        nullable=False
    )

    requester_email = db.Column(
        db.String(120),
        nullable=False
    )

    requester_phone = db.Column(
        db.String(15),
        nullable=False
    )

    blood_group = db.Column(
        db.String(5),
        nullable=False
    )

    city = db.Column(
        db.String(100),
        nullable=False
    )

    message = db.Column(
        db.Text
    )


    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    donor = db.relationship(
        "User",
        backref="blood_requests"
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )