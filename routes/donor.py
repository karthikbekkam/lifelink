import os

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app

from flask_login import login_required
from flask_login import current_user

from werkzeug.utils import secure_filename

from extensions import db
from extensions import bcrypt

from models.blood_request import BloodRequest

from forms.profile_form import ProfileForm
from forms.change_password_form import ChangePasswordForm


donor_bp = Blueprint(
    "donor",
    __name__,
    url_prefix="/donor"
)


@donor_bp.route("/")
@login_required
def dashboard():

    total_requests = BloodRequest.query.filter_by(
        donor_id=current_user.id
    ).count()

    pending_requests = BloodRequest.query.filter_by(
        donor_id=current_user.id,
        status="Pending"
    ).count()

    approved_requests = BloodRequest.query.filter_by(
        donor_id=current_user.id,
        status="Approved"
    ).count()

    rejected_requests = BloodRequest.query.filter_by(
        donor_id=current_user.id,
        status="Rejected"
    ).count()

    return render_template(
        "donor/dashboard.html",
        total_requests=total_requests,
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        rejected_requests=rejected_requests
    )



@donor_bp.route("/profile", methods=["GET", "POST"])
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
            url_for("donor.profile")
        )

    form.full_name.data = current_user.full_name
    form.phone.data = current_user.phone
    form.city.data = current_user.city
    form.state.data = current_user.state
    form.address.data = current_user.address
    form.pincode.data = current_user.pincode

    return render_template(
        "donor/profile.html",
        form=form
    )


@donor_bp.route("/requests")
@login_required
def requests():

    requests = BloodRequest.query.filter_by(
        donor_id=current_user.id
    ).order_by(
        BloodRequest.created_at.desc()
    ).all()

    return render_template(
        "donor/requests.html",
        requests=requests
    )

@donor_bp.route("/history")
@login_required
def history():

    history = BloodRequest.query.filter_by(
        donor_id=current_user.id,
        status="Approved"
    ).order_by(
        BloodRequest.created_at.desc()
    ).all()

    return render_template(
        "donor/history.html",
        history=history
    )


@donor_bp.route("/toggle-availability")
@login_required
def toggle_availability():

    current_user.available = not current_user.available

    db.session.commit()

    if current_user.available:

        flash(
            "You are now Available for Donation.",
            "success"
        )

    else:

        flash(
            "You are now Unavailable for Donation.",
            "warning"
        )

    return redirect(
        url_for("donor.dashboard")
    )


@donor_bp.route("/change-password", methods=["GET", "POST"])
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
                url_for("donor.change_password")
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
            url_for("donor.dashboard")
        )

    return render_template(
        "donor/change_password.html",
        form=form
    )


@donor_bp.route("/accept/<int:request_id>")
@login_required
def accept_request(request_id):

    blood_request = BloodRequest.query.get_or_404(request_id)

    if blood_request.donor_id != current_user.id:

        flash(
            "Unauthorized request.",
            "danger"
        )

        return redirect(
            url_for("donor.requests")
        )

    blood_request.status = "Approved"

    db.session.commit()

    flash(
        "Blood Request Accepted Successfully.",
        "success"
    )

    return redirect(
        url_for("donor.requests")
    )


@donor_bp.route("/reject/<int:request_id>")
@login_required
def reject_request(request_id):

    blood_request = BloodRequest.query.get_or_404(request_id)

    if blood_request.donor_id != current_user.id:

        flash(
            "Unauthorized request.",
            "danger"
        )

        return redirect(
            url_for("donor.requests")
        )

    blood_request.status = "Rejected"

    db.session.commit()

    flash(
        "Blood Request Rejected.",
        "warning"
    )

    return redirect(
        url_for("donor.requests")
    )