import os
from dotenv import load_dotenv

load_dotenv("../.env")

URL_CHANNEL = os.environ.get("URL_CHANNEL")
URL_INVITE = os.environ.get("URL_INVITE")
SECRET_KEY_DJANGO = os.environ.get("SECRET_KEY_DJANGO")