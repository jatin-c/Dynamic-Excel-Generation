import smtplib
from Excel_writer import xlsx_write
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def vaishali():
    fromaddr = "from_mail"
    password = "Votxxxx"
    toaddr = "to_mail"
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Email job confirmation-Rajeev"

    # string to store the body of the mail
    body = "Email sent successfully"

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

def jatin():
    fromaddr = "from_mail"
    password = "Votxxxx"
    toaddr = "to_mail"


    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Email job confirmation-Rajeev"

    # string to store the body of the mail
    body = "Email sent successfully"

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


def jatin_err(filepath):
    fromaddr = "from_mail"
    password = "Votxxxx"
    toaddr = "to_mail"


    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Email Warning-Rajeev"

    # string to store the body of the mail
    body = "Email job encoutered an error,Hurry!, ERROR:"+filepath

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

def vaishali_err(filepath):
    fromaddr = "from_mail"
    password = "Votxxxx"
    toaddr = "to_mail"
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Email Warning-Rajeev"

    # string to store the body of the mail
    body = "Email job encoutered an error,Hurry!, ERROR:"+filepath

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

def rajeev(filepath):
    fromaddr = "from_mail"
    password = "Votxxxx"
    toaddr="to_mail"
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Daily Productivity Report"

    # string to store the body of the mail
    body = "Please, find attachment."

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    #filepath = "Daily Productivity Report(HO).xlsx"
    attachment = open(filepath['filepath'], "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())


    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filepath['filename'])

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    server = smtplib.SMTP('outlook.office365.com', 587)
    server.starttls()
    server.login(fromaddr,password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    server.send_message(msg)

    server.quit()


if __name__ == '__main__':
    flag='R'
    filepath=xlsx_write(flag)
    #filepath={}
    #filepath['filepath']="/home/centos/iassist/bot/dlpexcel/DailyProductivityReport(HO).xlsx"
    if type(filepath)==dict:
        rajeev(filepath)
        #prakash(filepath)
        jatin()
        vaishali()
    else:
        jatin_err(filepath)
        vaishali_err(filepath)