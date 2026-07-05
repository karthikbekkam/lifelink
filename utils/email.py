from flask_mail import Message

from extensions import mail


def send_email(receiver, subject, body):

    msg = Message(

        subject=subject,

        recipients=[receiver],

        body=body

    )

    mail.send(msg)