#! python3
# umbrella_reminder.py — An exercise in sending SMS messages based on info craped from a website.
# For more information, see project_details.txt.

import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
# logging.disable(logging.CRITICAL) # Note out to enable logging.