import os
from dotenv import load_dotenv

load_dotenv(".env")

TOKEN_BOT = os.environ.get("TOKEN_BOT")
CHANNEL_ID = os.environ.get("CHANNEL_ID")