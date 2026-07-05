from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_token(email):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    return serializer.dumps(
        email,
        salt="password-reset"
    )


def verify_token(token, expiration=1800):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:

        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=expiration
        )

        return email

    except Exception:

        return None