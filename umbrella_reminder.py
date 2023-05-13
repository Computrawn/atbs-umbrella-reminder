#! python3
# umbrella_reminder.py — An exercise in sending SMS messages based on info craped from a website.
# For more information, see project_details.txt.

import logging
import os
from requests_html import HTMLSession

logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
# logging.disable(logging.CRITICAL) # Note out to enable logging.


MY_WEATHER = os.environ.get("MY_WEATHER")  # Get weather info site page


def get_my_weather():
    session = HTMLSession()
    res = session.get(MY_WEATHER, timeout=10)
    res.raise_for_status()
    site_status = res.status_code

    if site_status == 200:
        css_selector = ".myforecast-current"
        forecast_today = res.html.find(css_selector, first=True).text
        return forecast_today


current_forecast = get_my_weather()
logging.info(current_forecast)
