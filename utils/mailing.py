import smtplib
from email.mime.text import MIMEText
import yaml

with open("./utils/secrets.yaml", "r") as file:
    config = yaml.safe_load(file)

def send_email(to: str, subject: str, body: str):
    sender_email = config["gmail_account"]["EMAIL"]
    sender_password = config["gmail_account"]["PASSWORD"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, msg.as_string())
