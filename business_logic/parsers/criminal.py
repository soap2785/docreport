from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://fsin.gov.ru/criminal/'


def criminal(region, surname, name, patronymic):
    driver.get(url)
    cookies = driver.find_element(By.XPATH, '//*[@id="cookiesBtn"]')
    cookies.click()
    inp_region = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div/form/div[1]/div/div[2]/div/div[1]/div')
    inp_region.click()
    dropdown_list = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div/form/div[1]/div/div[2]/div/div[2]/div/div/ul')
    target_elements = dropdown_list.find_elements(By.TAG_NAME, "li")
    for target_element in target_elements:
        if target_element.text == region + ' (УФСИН)':
            driver.execute_script("arguments[0].scrollIntoView();", target_element)
            target_element.click()
            break
    inp_fullname = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[5]/div/form/div[2]/div[1]/div[2]/div/input')
    inp_fullname.send_keys(surname + ' ' + name + ' ' + patronymic, Keys.ENTER)
    try:
        orientations_array = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[2]/div[1]/div/div/div[6]')
        orientations = orientations_array.find_elements(By.CLASS_NAME, 'sl-item')
        return "Человек присутствует в базе"
    except:
        return "Человека нет в базе данных"