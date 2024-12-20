import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.orm import Session

from src.repositories.alternatives import submit_alternatives, get_all_requests, toJsonSerializable, get_request_by_id, \
    add_response, get_all_requests_by_filter
from src.repositories.clients import get_client_by_id
from src.repositories.managers import get_manager_by_id
from src.schemas.alternative_schemas import AlternativeRequestBase, AlternativeResponseBase, AlternativeFilterRequest


def submit_alternatives_service(request: AlternativeRequestBase, db: Session):
    return submit_alternatives(request, db)

def get_all_alternatives_service(db: Session):
    return toJsonSerializable(get_all_requests(db), db)

def get_all_alternatives_by_filter(request: AlternativeFilterRequest, db: Session):
    return toJsonSerializable(get_all_requests_by_filter(request, db), db)

def send_response_service(response: AlternativeResponseBase, db: Session):
    response = add_response(db, response)
    request = get_request_by_id(db, response.request_id)
    client = get_client_by_id(db, request.client_id)
    manager = get_manager_by_id(db, response.manager_id)
    send_email(
        to_address=client.email,
        subject="Baraiyq: Response for your request",
        content=f"""
                    <p>Manager <b>{manager.name}</b> reviewed your request and considered some 
                    solution!</p>
                    <p><b>{response.response_details}</b></p>
                    <p>In the hope that we've found the best solution for you.
                """
    )

    db.delete(request)
    db.commit()

    return response

def send_email(to_address: str, subject: str, content: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "nuspekovalihan@gmail.com"
    sender_password = "sbwlgtbryqkgynvv"
    sender_name = "baraiyq.kz"

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = to_address

    message.attach(MIMEText(content, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_address, message.as_string())
    except Exception as e:
        print("Failed to send email:", e)
        raise
