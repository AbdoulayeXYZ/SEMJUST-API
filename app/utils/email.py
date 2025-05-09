import logging
from pathlib import Path
from typing import Any, Dict

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

from app.core.config import settings

logger = logging.getLogger(__name__)

def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    if not settings.EMAILS_ENABLED:
        logger.warning("No provided configuration for email variables. Skipping email sending.")
        return

    message = MessageSchema(
        subject=subject_template,
        recipients=[email_to],
        body=html_template,
        subtype="html",
    )

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.SMTP_USER,
        MAIL_PASSWORD=settings.SMTP_PASSWORD,
        MAIL_FROM=settings.EMAILS_FROM_EMAIL,
        MAIL_PORT=settings.SMTP_PORT,
        MAIL_SERVER=settings.SMTP_HOST,
        MAIL_FROM_NAME=settings.EMAILS_FROM_NAME,
        MAIL_TLS=settings.SMTP_TLS,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
        TEMPLATE_FOLDER=Path(__file__).parent / 'email-templates/build',
    )

    fm = FastMail(conf)
    fm.send_message(message)
    logger.info(f"send email to {email_to}")

def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(__file__).parent / "email-templates/build/new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )

def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(__file__).parent / "email-templates/build/reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    ) 