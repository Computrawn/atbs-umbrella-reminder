#! python3
# umbrella_reminder.py — An exercise in sending SMS messages based on info craped from a website.
# For more information, see project_details.txt.

import logging
import os
from smtplib import SMTP
from email.message import EmailMessage
from requests_html import HTMLSession

logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
logging.disable(logging.DEBUG)  # Note out to enable logging.


MY_WEATHER = os.environ.get("MY_WEATHER")  # Get site address from environment variables
EMAIL_SMTP = os.environ.get("ICLD_SMTP")  # Get smtp address from env vars
EMAIL_USER = os.environ.get("ICLD_USER")  # Get email address from env vars
EMAIL_PASS = os.environ.get("ICLD_PASS")  # Get email password from env vars


def get_my_weather():
    session = HTMLSession()
    res = session.get(MY_WEATHER, timeout=10)
    res.raise_for_status()
    site_status = res.status_code

    if site_status == 200:
        now_selector = ".myforecast-current"
        forecast_today = res.html.find(now_selector, first=True).text
        detail_selector = "div.row-odd:nth-child(1) > div:nth-child(2)"
        first_detailed = res.html.find(detail_selector, first=True).text
        return forecast_today, first_detailed
    print(f"Something went wrong: Error {site_status}")


def send_forecast_email():
    current_forecast, current_details = get_my_weather()
    rain_chance = ["shower", "thunderstorm", "rain", "sprinkle"]

    for weather_condition in rain_chance:
        if weather_condition in current_details:
            weather_message = EmailMessage()
            weather_message["Subject"] = f"Right now in Decatur: {current_forecast}"
            weather_message["From"] = EMAIL_USER
            weather_message["To"] = EMAIL_USER
            weather_message.set_content(
                f"You might want to pack an umbrella: {current_details}"
            )

            combined_info = f"Now: {current_forecast} | Details: {current_details}"
            logging.info(combined_info)

            with SMTP(EMAIL_SMTP, 587) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.send_message(weather_message)


send_forecast_email()
