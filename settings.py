import os

from dotenv import load_dotenv

load_dotenv()

email = os.getenv('valid_email')
passwd = os.getenv('valid_password')
