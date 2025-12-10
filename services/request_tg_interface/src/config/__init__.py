from dotenv import load_dotenv
from os import getenv

load_dotenv("config/.env")

BOT_TOKEN = getenv('BOT_TOKEN')
PAY_TOKEN = getenv('PAY_TOKEN')
TWOCAPTCHA_TOKEN = getenv('TWOCAPTCHA_TOKEN')

ADMINS = list(map(int, getenv('ADMINS').split(',')))

REGIONS = [
    region.lower().rstrip() for region in
    open('config/regions.txt', 'r', encoding='utf-8').readlines()
]
PROXIES = {
    "proxyType": "manual",
    "httpProxy": getenv('HTTPPROXY'),
    "httpsProxy": getenv('HTTPSPROXY'),
}
