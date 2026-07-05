import os

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app
from forms.change_password_form import ChangePasswordForm

from extensions import bcrypt

from werkzeug.utils import secure_filename

from flask_login import login_required
from flask_login import current_user

from extensions import db

from models.blood_request import BloodRequest

from forms.profile_form import ProfileForm

needer_bp = Blueprint(
    "needer",
    __name__,
    url_prefix="/needer"
)

@needer_bp.route("/")
@login_required
def dashboard():

    total = BloodRequest.query.count()

    pending = BloodRequest.query.filter_by(
        status="Pending"
    ).count()

    approved = BloodRequest.query.filter_by(
        status="Approved"
    ).count()

    rejected = BloodRequest.query.filter_by(
        status="Rejected"
    ).count()

    return render_template(
        "needer/dashboard.html",
        total=total,
        pending=pending,
        approved=approved,
        rejected=rejected
    )

@needer_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = ProfileForm()

    if form.validate_on_submit():

        current_user.full_name = form.full_name.data
        current_user.phone = form.phone.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.address = form.address.data
        current_user.pincode = form.pincode.data

        # Upload Profile Image
        if form.profile_image.data:

            filename = secure_filename(
                form.profile_image.data.filename
            )

            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )

            form.profile_image.data.save(filepath)

            current_user.profile_image = filename

        db.session.commit()

        flash(
            "Profile Updated Successfully!",
            "success"
        )

        return redirect(
            url_for("needer.profile")
        )

    form.full_name.data = current_user.full_name
    form.phone.data = current_user.phone
    form.city.data = current_user.city
    form.state.data = current_user.state
    form.address.data = current_user.address
    form.pincode.data = current_user.pincode

    return render_template(
        "needer/profile.html",
        form=form
    )

@needer_bp.route("/requests")
@login_required
def my_requests():

    requests = BloodRequest.query.order_by(
        BloodRequest.created_at.desc()
    ).all()

    return render_template(
        "needer/requests.html",
        requests=requests
    )

@needer_bp.route("/search")
@login_required
def search_donors():

    return render_template(
        "needer/search.html"
    )


@needer_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not bcrypt.check_password_hash(

            current_user.password,

            form.current_password.data

        ):

            flash(

                "Current Password is incorrect.",

                "danger"

            )

            return redirect(

                url_for("needer.change_password")

            )

        current_user.password = bcrypt.generate_password_hash(

            form.new_password.data

        ).decode("utf-8")

        db.session.commit()

        flash(

            "Password changed successfully.",

            "success"

        )

        return redirect(

            url_for("needer.dashboard")

        )

    return render_template(

        "needer/change_password.html",

        form=form

    )