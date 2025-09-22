import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from businessLogic.captcha import solveCaptcha
from businessLogic.classForParsers import CompiledData
from mainDIR.bot.src.config import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://egrul.nalog.ru/index.html'


def captchaForEgrul():
    try:
        WebDriverWait(driver, 1).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="uniDialogContainer"]')))
        iframe = driver.find_element(By.ID, "uniDialogFrame")
        driver.switch_to.frame(iframe)
        elementInsideIframe = driver.find_element(By.XPATH, '//*[@id="dialogContent"]/div/div/div/div/img')
        imgSource = elementInsideIframe.get_attribute('src')
        solved = solveCaptcha(imgSource)
        inp = driver.find_element(By.XPATH, '//*[@id="captcha"]')
        inp.send_keys(solved.get('code'))
        inp.send_keys(Keys.ENTER)
        driver.switch_to.default_content()
        WebDriverWait(driver, 3).until(ec.invisibility_of_element_located((By.XPATH, '//*[@id="uniDialogContainer"]')))
    except TimeoutException:
        return TimeoutException


def checkFNS(inn, fullname):
    """
    Возвращает состояние нахождения лица в ЕГРЮЛ/ЕГРИП

    Args:
        inn: ИНН интересующего лица (получено из suggestINNPost)
        fullname: полное ФИО интересующего лица

    Returns: str
    """
    print(datetime.datetime.now(), "FNS")
    try:
        driver.get(url)
        if driver.find_element(By.XPATH, '//*[@id="uniPageSubtitle"]').text == 'Технологические работы':
            return None
        fullname = fullname.split()
        surname = fullname[0]
        name = fullname[1]
        patronymic = fullname[2]

        if inn:

            inp = driver.find_element(By.XPATH, '//*[@id="query"]')
            inp.send_keys(inn, Keys.ENTER)

            try:
                captchaForEgrul()
            except TimeoutException:
                pass

            WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.CLASS_NAME, 'blockUI')))
            time.sleep(0.3)

            try:
                WebDriverWait(driver, 1).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="noDataFound"]/div/div/p')))
                pass

            except TimeoutException:
                CompiledData.fns = "Человек есть в базе данных"

            checkbox = driver.find_element(By.XPATH, '//*[@id="unichk_0"]')
            checkbox.click()

            inp.send_keys(Keys.CONTROL, 'a', surname + ' ' + name + ' ' + patronymic, Keys.ENTER)

            try:
                captchaForEgrul()
            except TimeoutException:
                pass

            try:
                WebDriverWait(driver, 1).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="resultContent"]')))
                CompiledData.fns = "Человек есть в базе данных"
            except TimeoutException or NoSuchElementException:
                CompiledData.fns = "Человека нет в базе данных"
        else:
            inp = driver.find_element(By.XPATH, '//*[@id="query"]')
            WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.CLASS_NAME, 'blockUI')))
            time.sleep(0.3)

            try:
                WebDriverWait(driver, 1).until(
                    ec.visibility_of_element_located((By.XPATH, '//*[@id="noDataFound"]/div/div/p')))
                pass

            except TimeoutException:
                CompiledData.fns = "Человек есть в базе данных"

            checkbox = driver.find_element(By.XPATH, '//*[@id="unichk_0"]')
            checkbox.click()

            inp.send_keys(Keys.CONTROL, 'a', surname + ' ' + name + ' ' + patronymic, Keys.ENTER)

            try:
                captchaForEgrul()
            except TimeoutException:
                pass

            try:
                WebDriverWait(driver, 1).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="resultContent"]')))
                CompiledData.fns = "Человек есть в базе данных"

            except TimeoutException or NoSuchElementException:
                CompiledData.fns = "Человека нет в базе данных"

    except NoSuchElementException:
        CompiledData.fns = "На ресурсе технические работы"
    except Exception as e:
        print(e)
        return None
    finally:
        print(datetime.datetime.now(), "FNS")