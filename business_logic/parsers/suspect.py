from selenium import webdriver
from config import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies


url = "https://r49.fssp.gov.ru/iss/suspect_info"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def check_suspect():
    ...