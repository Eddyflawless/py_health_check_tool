import os
import time
import requests
from dotenv import load_dotenv
from pathlib import Path
import smtplib, ssl
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.utils import COMMASPACE, formatdate

SERVER_URL = "https://icdpghana2.org/#/" #server to monitor
GRACE_PERIOD = 2 #check to higer for better telemetry eg..5
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
TO_EMAIL_ADDRESS = os.environ.get("TO_EMAIL_USER")

wait_minutes = 2
wait_factor = 1

def cool_off_exponentially():
    global wait_minutes, wait_factor
    wait_minutes *= 1.2
    wait_factor +=1
    return wait_minutes * wait_factor

def ping_server():
    r = None
    try:
        r = requests.get(SERVER_URL, timeout=5)
    except:
        print("Couldnot find server")
    finally:
        return r   

def add_attachment():
    pass  


def build_multipart_message(): 
    pass

def build_simple_message():

    subject = 'YOUR SITE IS DOWN'
    body = 'Make sure the server restarted and it is backed up'
    #msg = f'Subject : {subject}\n\n{body}'
    # msg = "Subject: " + subject + "\n" + body
    msg = f"""
    Subject: Hi there, {subject}

    {body}
    
    """

    return msg


def send_email(message_type="simple"):

    # Create a secure SSL context
    # context = ssl.create_default_context()
        
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls() #secure the connection
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = build_simple_message()

        smtp.sendmail(EMAIL_ADDRESS, [TO_EMAIL_ADDRESS], msg)
        # close connection
        smtp.quit()
        smtp.close()



def run_health_check():

    count = 0
    response = ping_server()

    if response is None:

        while count < GRACE_PERIOD:

            time_to_wait = cool_off_exponentially()

            print(f"wait for {time_to_wait}")
            time.sleep(time_to_wait) #delay abit time_to_wait * 60 to get seconds
            response = ping_server()
            count += 1

        print("send email after grace period")
        send_status = send_email() # finally send an emaol
        print("email sent")
    
    else:
        print("All systems green....")  
        print(f"reponse {response.status_code}")


if __name__ == "__main__":
    load_dotenv(dotenv_path = Path('.env'))
    print(build_simple_message())
    run_health_check()

