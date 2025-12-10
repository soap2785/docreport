from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from mainDIR import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
url = "https://r49.fssp.gov.ru/iss/suspect_info"

def checkSuspect(fullname):
    driver.get(url)
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div[2]/div[2]/div/div/div/div[4]/div/div/'
                                  'div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/'
                                  'div/div[1]/div/div/input').send_keys(fullname, Keys.ENTER)

