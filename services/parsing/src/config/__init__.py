from dotenv import load_dotenv
from os import getenv

load_dotenv('config/.env')

TWOCAPTCHA_TOKEN = getenv('TWOCAPTCHA_TOKEN')
