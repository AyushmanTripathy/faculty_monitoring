import smtplib
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = getenv("SENDER_APP_PASSWORD")

email_mapping = {}
email_mapping['ayush@giet.edu'] = 'ayushmantripathy2004@gmail.com'
email_mapping['tripathy@giet.edu'] = '23cse417.ayushmantripathy@giet.edu'

if SENDER_EMAIL == None or SENDER_APP_PASSWORD == None:
    print("missing credentials")
    exit(1)

def send_otp(mail, otp):
    if mail in email_mapping:
        mail = email_mapping[mail]
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
    message = f"Subject: Requested Otp\nRequested otp is {otp}\n"
    s.sendmail(SENDER_EMAIL, mail, message)
    s.quit()
