import os
import time
import requests
import smtplib

SERVER_URL = "https://icdpghana2.org/#/"
GRACE_PERIOD = 5
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

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


def send_email():
        
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = 'YOUR SITE IS DOWN'
        body = 'Make sure the server restarted and it is backed up'
        #msg = f'Subject : {subject}\n\n{body}'
        msg = "Subject: " + subject + "\n" + body

        smtp.sendmail(EMAIL_ADDRESS, 'edjonorh@gmail.com', msg)

        return True

    return False    


def run_health_check():

    count = 0
    response = ping_server()

    if response is None:

        while count < GRACE_PERIOD:

            time_to_wait = cool_off_exponentially()

            print(f"wait for {time_to_wait}")
            condition = (count <= GRACE_PERIOD)
            print(f" loop state { condition }")
            print(f"count {count}")
            time.sleep(time_to_wait) #delay abit time_to_wait * 60 to get seconds
            response = ping_server()
            count += 1

        print("send email after grace period")
        send_status = send_email() # finally send an emaol
        if send_email == False:
            print("couldnot send email")
    
    else:
        print("All systems green....")  
        print(f"reponse {response.status_code}")


if __name__ == "__main__":
    run_health_check()

