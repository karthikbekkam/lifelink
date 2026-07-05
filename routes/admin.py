from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from extensions import db
from flask_login import login_required
from flask_login import current_user

from forms.change_password_form import ChangePasswordForm
from extensions import bcrypt


from utils.email import send_email


from models.user import User
from models.contact import Contact
from models.blood_request import BloodRequest

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin_bp.route("/")
@login_required
def dashboard():

    total_users = User.query.count()

    total_donors = User.query.filter_by(
        role="Donor"
    ).count()

    total_needers = User.query.filter_by(
        role="Needer"
    ).count()

    total_contacts = Contact.query.count()

    total_requests = BloodRequest.query.count()


    available_donors = User.query.filter_by(
        role="Donor",
        available=True
    ).count()

    unavailable_donors = User.query.filter_by(
        role="Donor",
        available=False
    ).count()

    pending_requests = BloodRequest.query.filter_by(
        status="Pending"
    ).count()

    approved_requests = BloodRequest.query.filter_by(
        status="Approved"
    ).count()

    rejected_requests = BloodRequest.query.filter_by(
        status="Rejected"
    ).count()

    return render_template(

        "admin/dashboard.html",

        total_users=total_users,

        total_donors=total_donors,

        total_needers=total_needers,

        total_contacts=total_contacts,

        total_requests=total_requests,

        available_donors=available_donors,

        unavailable_donors=unavailable_donors,

        pending_requests=pending_requests,

        approved_requests=approved_requests,

        rejected_requests=rejected_requests

    )

@admin_bp.route("/users")
def users():

    users = User.query.order_by(
        User.id.desc()
    ).all()

    return render_template(
        "admin/users.html",
        users=users
    )

@admin_bp.route("/donors")
def donors():

    donors = User.query.filter_by(
        role="Donor"
    ).order_by(
        User.id.desc()
    ).all()

    return render_template(
        "admin/donors.html",
        donors=donors
    )


@admin_bp.route("/needers")
def needers():

    needers = User.query.filter_by(
        role="Needer"
    ).order_by(
        User.id.desc()
    ).all()

    return render_template(
        "admin/needers.html",
        needers=needers
    )


@admin_bp.route("/requests")
def blood_requests():

    requests = BloodRequest.query.order_by(
        BloodRequest.created_at.desc()
    ).all()

    return render_template(
        "admin/requests.html",
        requests=requests
    )


@admin_bp.route("/contacts")
def contacts():

    contacts = Contact.query.order_by(
        Contact.created_at.desc()
    ).all()

    return render_template(
        "admin/contacts.html",
        contacts=contacts
    )


@admin_bp.route("/delete-user/<int:user_id>")
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    db.session.commit()

    flash(
        "User deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.users")
    )

@admin_bp.route("/approve-request/<int:request_id>")
def approve_request(request_id):

    request = BloodRequest.query.get_or_404(request_id)

    request.status = "Approved"

    db.session.commit()


    try:

        send_email(

            receiver=request.requester_email,

            subject="🩸 Blood Request Approved | LifeLink",

            body=f"""
Hello {request.requester_name},

Congratulations!

Your blood request has been APPROVED.

----------------------------------------

Blood Group : {request.blood_group}

City : {request.city}

Status : Approved

----------------------------------------

Please login to your LifeLink account for more information.

Thank you,

LifeLink Team
"""

        )

    except Exception as e:

        print("Approval Email Error :", e)

    flash(

        "Blood request approved successfully.",

        "success"

    )

    return redirect(

        url_for("admin.blood_requests")

    )


@admin_bp.route("/reject-request/<int:request_id>")
def reject_request(request_id):

    request = BloodRequest.query.get_or_404(request_id)

    request.status = "Rejected"

    db.session.commit()


    try:

        send_email(

            receiver=request.requester_email,

            subject="❌ Blood Request Rejected | LifeLink",

            body=f"""
Hello {request.requester_name},

Unfortunately,

Your blood request has been rejected.

----------------------------------------

Blood Group : {request.blood_group}

City : {request.city}

Status : Rejected

----------------------------------------

Please search for another donor using the LifeLink application.

Thank you,

LifeLink Team
"""

        )

    except Exception as e:

        print("Rejection Email Error :", e)

    flash(

        "Blood request rejected successfully.",

        "warning"

    )

    return redirect(

        url_for("admin.blood_requests")

    )


@admin_bp.route("/user/<int:user_id>")
def view_user(user_id):

    user = User.query.get_or_404(user_id)

    return render_template(

        "admin/view_user.html",

        user=user

    )

@admin_bp.route("/change-password", methods=["GET", "POST"])
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
                url_for("admin.change_password")
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
            url_for("admin.dashboard")
        )

    return render_template(
        "admin/change_password.html",
        form=form
    )

@admin_bp.route("/activate-user/<int:user_id>")
@login_required
def activate_user(user_id):

    user = User.query.get_or_404(user_id)

    user.active = True

    db.session.commit()

    flash(
        "User Activated Successfully.",
        "success"
    )

    return redirect(
        url_for("admin.users")
    )

@admin_bp.route("/deactivate-user/<int:user_id>")
@login_required
def deactivate_user(user_id):

    user = User.query.get_or_404(user_id)

    user.active = False

    db.session.commit()

    flash(
        "User Deactivated Successfully.",
        "warning"
    )

    return redirect(
        url_for("admin.blood_requests")
    )