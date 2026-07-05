from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.forgot_password_form import ForgotPasswordForm
from forms.reset_password_form import ResetPasswordForm

from models.user import User

from extensions import db
from extensions import bcrypt

from utils.email import send_email
from utils.token import generate_token
from utils.token import verify_token

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:

        if current_user.role == "Admin":
            return redirect(url_for("admin.dashboard"))

        elif current_user.role == "Donor":
            return redirect(url_for("donor.dashboard"))

        else:
            return redirect(url_for("needer.dashboard"))

    form = RegisterForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user:

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        new_user = User(

            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password,
            role=form.role.data,
            blood_group=form.blood_group.data,
            age=form.age.data,
            gender=form.gender.data,
            weight=form.weight.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            pincode=form.pincode.data

        )

        db.session.add(new_user)
        db.session.commit()

        flash(
            "Registration Successful! Please Login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html",
        form=form
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "Admin":
            return redirect(url_for("admin.dashboard"))

        elif current_user.role == "Donor":
            return redirect(url_for("donor.dashboard"))

        else:
            return redirect(url_for("needer.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(
                user,
                remember=form.remember.data
            )

            flash(
                "Login Successful.",
                "success"
            )

            if user.role == "Admin":

                return redirect(
                    url_for("admin.dashboard")
                )

            elif user.role == "Donor":

                return redirect(
                    url_for("donor.dashboard")
                )

            else:

                return redirect(
                    url_for("needer.dashboard")
                )

        flash(
            "Invalid Email or Password.",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("home.home")
    )


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    form = ForgotPasswordForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user is None:

            flash(
                "No account found with this email.",
                "warning"
            )

            return render_template(
                "auth/forgot_password.html",
                form=form
            )

        token = generate_token(
            user.email
        )

        reset_link = url_for(
            "auth.reset_password",
            token=token,
            _external=True
        )

        body = f"""
Hello {user.full_name},

A password reset request has been received for your LifeLink account.

Click the link below to reset your password:

{reset_link}

This link is valid for 30 minutes.

If you did not request this password reset, please ignore this email.

Regards,

LifeLink Team
"""

        try:

            send_email(
                receiver=user.email,
                subject="LifeLink Password Reset",
                body=body
            )

            flash(
                "Password reset link has been sent to your email.",
                "success"
            )

            return redirect(
                url_for("auth.login")
            )

        except Exception as e:

            print("Email Error:", e)

            flash(
                "Unable to send email.",
                "danger"
            )

    return render_template(
        "auth/forgot_password.html",
        form=form
    )


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    email = verify_token(token)

    if email is None:

        flash(
            "Invalid or Expired Reset Link.",
            "danger"
        )

        return redirect(
            url_for("auth.forgot_password")
        )

    user = User.query.filter_by(
        email=email
    ).first()

    if user is None:

        flash(
            "User not found.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    form = ResetPasswordForm()

    if form.validate_on_submit():

        user.password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        db.session.commit()

        flash(
            "Password changed successfully.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/reset_password.html",
        form=form
    )