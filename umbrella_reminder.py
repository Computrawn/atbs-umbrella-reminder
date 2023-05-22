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

EMAIL_SMTP = os.environ.get("SENDER_SMTP")  # Get smtp address from env vars
EMAIL_USER = os.environ.get("SENDER_USER")  # Get email address from env vars
EMAIL_PASS = os.environ.get("SENDER_PASS")  # Get email password from env vars


def get_my_weather():
    """Scrape current weather forecast and location information from site."""
    user_zip = os.environ.get("USER_ZIP")  # Get user zipcode from env vars
    user_weather = f"https://www.weather.gov/{user_zip}"

    session = HTMLSession()
    res = session.get(user_weather, timeout=10)
    res.raise_for_status()
    site_status = res.status_code

    if site_status == 200:
        now_selector = ".myforecast-current"
        forecast_today = res.html.find(now_selector, first=True).text
        detail_selector = "div.row-odd:nth-child(1) > div:nth-child(2)"
        first_detailed = res.html.find(detail_selector, first=True).text
        location_selector = "#seven-day-forecast > div.panel-heading > h2"
        zipcode_location = res.html.find(location_selector, first=True).text
    else:
        print(f"Something went wrong: Error {site_status}")
    logging.info("%s — %s: %s", zipcode_location, forecast_today, first_detailed)
    return forecast_today, first_detailed, zipcode_location


def check_for_rain():
    """Checks for rain keywords in forecast."""
    current_forecast, current_details, zipcode_location = get_my_weather()
    rain_chance = ["shower", "thunderstorm", "rain", "sprinkle"]
    it_is_raining = False
    for weather_condition in rain_chance:
        if weather_condition in current_details:
            it_is_raining = True
    return it_is_raining, current_forecast, current_details, zipcode_location


def send_email(subject, content, location):
    """Send umbrella reminder email."""
    weather_message = EmailMessage()
    weather_message["Subject"] = f"Right now in {location}: {subject}"
    weather_message["From"] = EMAIL_USER
    weather_message["To"] = EMAIL_USER
    weather_message.set_content(
        f"""You might want to pack an umbrella before heading out the door.
        
Forecast details: {content}"""
    )

    # combined_info = f"Now in {location}: {subject} | Details: {content}"
    # logging.info(combined_info)

    with SMTP(EMAIL_SMTP, 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(weather_message)


is_raining, subject_info, content_details, user_location = check_for_rain()
if is_raining:
    send_email(subject_info, content_details, user_location)
