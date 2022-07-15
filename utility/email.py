import re
import os

from dotenv import load_dotenv
import smtplib

load_dotenv()
regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

server = smtplib.SMTP('smtp.gmail.com', 587)
server.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
server.starttls()

def validate_email(email):
    return bool(re.fullmatch(regex, email))
    
def send_verification(email):
    server.sendmail(os.getenv("EMAIL"), email, "Verify your account here:")