from selenium import webdriver
from selenium.common import NoSuchElementException
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
url = 'https://fsin.gov.ru/criminal/'


def criminal(region, fullname):
    fullname = fullname.split()
    surname = fullname[0]
    name = fullname[1]
    patronymic = fullname[2]

    driver.get(url)
    try:
        driver.find_element(By.XPATH, '//*[@id="cookiesBtn"]').click()
    except NoSuchElementException:
        pass
    driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div/form/div[1]/div/div[2]/div/div[1]/div').click()
    targetElements = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div/form/div[1]/div/div[2]/div/div[2]/div/div/ul').find_elements(By.TAG_NAME, "li")

    for target_element in targetElements:
        if target_element.text == region + ' (УФСИН)':
            driver.execute_script("arguments[0].scrollIntoView();", target_element)
            target_element.click()
            break

    driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div/form/div[2]/div[1]/div[2]/div/input').send_keys(surname + ' ' + name + ' ' + patronymic, Keys.ENTER)

    try:
        driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[6]').find_elements(By.CLASS_NAME, 'sl-item')
        return "Человек присутствует в базе"
    except:
        return "Человека нет в базе данных"