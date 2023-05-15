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
    """Scrape current weather forecast from site."""
    session = HTMLSession()
    res = session.get(MY_WEATHER, timeout=10)
    res.raise_for_status()
    site_status = res.status_code

    if site_status == 200:
        now_selector = ".myforecast-current"
        forecast_today = res.html.find(now_selector, first=True).text
        detail_selector = "div.row-odd:nth-child(1) > div:nth-child(2)"
        first_detailed = res.html.find(detail_selector, first=True).text
    print(f"Something went wrong: Error {site_status}")
    return forecast_today, first_detailed


def check_for_rain():
    """Checks for rain keywords in forecast."""
    current_forecast, current_details = get_my_weather()
    rain_chance = ["shower", "thunderstorm", "rain", "sprinkle"]

    for weather_condition in rain_chance:
        if weather_condition in current_details:
            return True, current_forecast, current_details


def send_email(subject, content):
    """Send umbrella reminder email."""
    weather_message = EmailMessage()
    weather_message["Subject"] = f"Right now in Decatur: {subject}"
    weather_message["From"] = EMAIL_USER
    weather_message["To"] = EMAIL_USER
    weather_message.set_content(
        f"""You might want to pack an umbrella.
        
Forecast details: {content}"""
    )

    combined_info = f"Now: {subject} | Details: {content}"
    logging.info(combined_info)

    with SMTP(EMAIL_SMTP, 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(weather_message)


is_raining, subject_info, content_details = check_for_rain()
if is_raining:
    send_email(subject_info, content_details)
