import requests
from datetime import datetime
import smtplib
import time

# Send email notification
time_now = datetime.now()


def send_mail(email_receiver, mail):
    email_sender = 'masterpinak@gmail.com'
    password = 'oolqbcjuupfnflft'
    name = 'Pinak Mehta'

    connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
    # connection.ehlo()
    connection.starttls()
    connection.login(user=email_sender, password=password)

    connection.sendmail(from_addr=email_sender,
                        to_addrs=email_receiver, msg=f'Subject: ISS on top of you!!!\n\n{mail}'
                        )
    # email confirmation
    print(f'Email sent to {name} at {email_receiver}')
    connection.close()


# Toronto coordinates
MY_LAT = 43.653225  # Your latitude
MY_LONG = -79.383186  # Your longitude

# If the ISS is close to my current position


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    plus5_lat = MY_LAT + 5
    plus5_lng = MY_LONG + 5

    minus5_lat = MY_LAT - 5
    minus5_lng = MY_LONG - 5

    if iss_latitude >= minus5_lat and iss_latitude <= plus5_lat and iss_longitude >= minus5_lng and iss_longitude <= plus5_lng:
        return True


# and it is currently dark
def sunset_sunrise():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


# Then send me an email to tell me to look up.
while True:

    # BONUS: run the code every 60 seconds.
    time.sleep(60)
    if is_iss_overhead() and sunset_sunrise():
        email_receiver = "mehta.pinak@yahoo.com"
        mail = "ISS is above you. Look up!"
        send_mail(email_receiver, mail)
