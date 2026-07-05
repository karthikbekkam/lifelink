from flask import Blueprint
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_required, current_user
from flask import request

from extensions import db

from utils.email import send_email


from models.user import User
from models.contact import Contact
from models.blood_request import BloodRequest


from forms.contact_form import ContactForm
from forms.search_form import SearchForm
from forms.request_form import RequestForm

home_bp = Blueprint(
    "home",
    __name__
)

@home_bp.route("/")
def home():

    total_users = User.query.count()

    total_contacts = Contact.query.count()

    available_donors = User.query.filter_by(
        role="Donor",
        available=True
    ).count()

    return render_template(
        "public/home.html",
        total_users=total_users,
        total_contacts=total_contacts,
        available_donors=available_donors
    )


@home_bp.route("/about")
def about():

    return render_template(
        "public/about.html"
    )


@home_bp.route("/contact", methods=["GET", "POST"])
def contact():

    form = ContactForm()

    if form.validate_on_submit():

        new_message = Contact(
            full_name=form.full_name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )

        db.session.add(new_message)

        db.session.commit()

        flash(
            "Thank you! Your message has been sent successfully.",
            "success"
        )

        return redirect(
            url_for("home.contact")
        )

    return render_template(
        "public/contact.html",
        form=form
    )


@home_bp.route("/map")
def map_page():

    return render_template(
        "public/map.html"
    )


@home_bp.route("/search", methods=["GET", "POST"])
@login_required
def search():

    form = SearchForm()
    donors = None

    if request.method == "POST":

        blood_group = request.form.get("blood_group")
        city = request.form.get("city")

        donors = User.query.filter(
            User.role == "Donor",
            User.available == True,
            User.blood_group == blood_group,
            User.city.ilike(f"%{city}%")
        ).all()

        donors = [d for d in donors if d.id != current_user.id]

        print("Found:", len(donors))

    return render_template(
        "public/search.html",
        form=form,
        donors=donors
    )

@home_bp.route("/request/<int:donor_id>", methods=["GET", "POST"])
def request_blood(donor_id):

    donor = User.query.get_or_404(donor_id)

    form = RequestForm()

    if form.validate_on_submit():

        new_request = BloodRequest(

            requester_name=form.requester_name.data,

            requester_email=form.requester_email.data,

            requester_phone=form.requester_phone.data,

            blood_group=donor.blood_group,

            city=form.city.data,

            message=form.message.data,

            donor_id=donor.id

        )

        db.session.add(new_request)

        db.session.commit()


        try:

            send_email(

                receiver=donor.email,

                subject="🩸 New Blood Request - LifeLink",

                body=f"""
Hello {donor.full_name},

A new blood request has been submitted through LifeLink.

----------------------------------------

Patient Name : {form.requester_name.data}

Patient Email : {form.requester_email.data}

Phone Number : {form.requester_phone.data}

Blood Group : {donor.blood_group}

City : {form.city.data}

Message :

{form.message.data}

----------------------------------------

Please login to your LifeLink account to view the complete request.

Thank you,

LifeLink Team
"""

            )

        except Exception as e:

            print("Email Error :", e)

        flash(

            "Blood Request Sent Successfully!",

            "success"

        )

        return redirect(

            url_for("home.search")

        )

    return render_template(

        "public/request.html",

        form=form,

        donor=donor

    )

from flask_login import login_required, current_user

@home_bp.route("/hospitals")
@login_required
def hospitals():

    city = current_user.city

    hospitals = []

    if city.lower() == "vijayawada":

        hospitals = [

            {
                "name": "Apollo Hospital",
                "address": "MG Road, Vijayawada",
                "phone": "0866-1234567",
                "map": "https://www.google.com/maps/search/?api=1&query=Apollo+Hospital+Vijayawada"
            },

            {
                "name": "Government General Hospital",
                "address": "One Town, Vijayawada",
                "phone": "0866-7654321",
                "map": "https://www.google.com/maps/search/?api=1&query=Government+General+Hospital+Vijayawada"
            }

        ]

    elif city.lower() == "guntur":

        hospitals = [

            {
                "name": "KIMS Hospital",
                "address": "Kothapet, Guntur",
                "phone": "0863-4567890",
                "map": "https://www.google.com/maps/search/?api=1&query=KIMS+Hospital+Guntur"
            }

        ]

    elif city.lower() == "mangalagiri":

        hospitals = [

            {
                "name": "AIIMS Mangalagiri",
                "address": "Mangalagiri",
                "phone": "08645-231777",
                "map": "https://www.google.com/maps/search/?api=1&query=AIIMS+Mangalagiri"
            }

        ]

    return render_template(
        "public/hospitals.html",
        hospitals=hospitals,
        city=city
    )
      

@home_bp.route("/nearby-donors")
@login_required
def nearby_donors():

    donors = User.query.filter_by(
        role="Donor",
        available=True
    ).all()

    return render_template(
        "public/nearby_donors.html",
        donors=donors
    )
