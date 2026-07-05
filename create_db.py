from app import app
from extensions import db

from models.user import User
from models.contact import Contact
from models.blood_request import BloodRequest

with app.app_context():

    db.create_all()

    print("=" * 50)
    print("LifeLink Database Created Successfully!")
    print("=" * 50)