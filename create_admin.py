from app import app
from extensions import db, bcrypt
from models.user import User

with app.app_context():

    admin = User.query.filter_by(
        email="admin@gmail.com"
    ).first()

    if admin:

        print("Admin already exists!")

    else:

        hashed_password = bcrypt.generate_password_hash(
            "admin123"
        ).decode("utf-8")

        admin = User(

            full_name="Administrator",

            email="admin@gmail.com",

            phone="9999999999",

            password=hashed_password,

            role="Admin",

            blood_group="O+",

            age=30,

            gender="Male",

            weight=70,

            city="Vijayawada",

            state="Andhra Pradesh",

            address="LifeLink Admin Office",

            pincode="520007",

            available=True,

            active=True

        )

        db.session.add(admin)

        db.session.commit()

        print("===================================")
        print("Admin Created Successfully!")
        print("===================================")
        print("Email    : admin@gmail.com")
        print("Password : admin123")