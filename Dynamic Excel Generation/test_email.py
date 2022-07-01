import smtplib
from Excelwriter import xlsx_write
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def email():
    fromaddr = "from_mail"
    password = "Votxxx"
    toaddr = "to_mail"


    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Email Warning"

    # string to store the body of the mail
    body = "Email job encoutered an error,Hurry!"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    server = smtplib.SMTP('outlook.office365.com', 587)
    server.starttls()
    server.login(fromaddr,password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    server.send_message(msg)

    server.quit()

if __name__ =='__main__':
    email()