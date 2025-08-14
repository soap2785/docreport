import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
url = "https://fedsfm.ru/documents/terrorists-catalog-portal-add"


def terrorist(surname, name, patronymic):
    driver.get(url)

    pass_warning = driver.find_element(By.XPATH, '//*[@id="details-button"]')
    pass_warning.click()
    pass_warning = driver.find_element(By.XPATH, '//*[@id="proceed-link"]')
    pass_warning.click()

    TableTwoOpen = driver.find_element(By.XPATH, '//*[@id="bodyContent"]/div/div/div/div/div/div[1]/div/div[1]/h4/a')
    TableTwoOpen.click()
    time.sleep(1)

    TableRestOpen = driver.find_element(By.XPATH, '//*[@id="NationalPart"]/div/div[2]/div/div[1]/h4/a')
    TableRestOpen.click()

    table = driver.find_element(By.XPATH, '//*[@id="russianFL"]/div/ol')
    StringsInTable = table.find_elements(By.TAG_NAME, 'li')
    terrorists = []
    for String in StringsInTable:
        FIO = String.text.split()
        terrorists.append(FIO[1] + ' ' + FIO[2] + ' ' + FIO[3].replace('*', '').replace(',', ''))
    print(terrorists)
    if surname + " " + name + " " + patronymic in terrorists:
        return "Человек в базе террористов присутствует"
    else:
        return "Человек отстуствует в базе террористов"
