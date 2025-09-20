import asyncio
import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from businessLogic.classForParsers import CompiledData
from mainDIR.bot.src.config import proxies
from businessLogic.driverClass import DriverClass

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = DriverClass.driver
url = 'https://bankrot.fedresurs.ru/bankrupts'


async def bankrupt(inn):
    """
    Возвращает состояние нахождения лица в базе банкротов

    Args:
        inn: ИНН лица (получается в suggestINNPost)
    """
    print(datetime.datetime.now(), "BANK")
    try:
        driver.get(url)
        await asyncio.sleep(3)
        inp = driver.find_element(By.XPATH, '/html/body/app-root/section/div[1]/app-bankrupt/div/'
                                                                   'div[1]/div/app-bankrupt-form/div/form/'
                                                                   'app-form-search-string/div/form/div/div/el-input/div/'
                                                                   'div/div/input')
        inp.send_keys(inn, Keys.ENTER)
        try:
            individual = driver.find_element(By.XPATH, '/html/body/app-root/section/div[1]/app-bankrupt/div/div[2]/'
                                                       'div/app-loader/div[1]/app-bankrupt-result/el-tab-panel/div[1]/ul/'
                                                       'li[2]/div/span[2]')
            if individual.text:
                CompiledData.bank = "Человек есть в базе данных"

            elif individual.text == '0':
                CompiledData.bank = "Человека нет в базе данных"

        except NoSuchElementException:
            CompiledData.bank = "Человека нет в базе данных"

        CompiledData.bank = "Человека нет в базе данных"
    except Exception as e:
        print(e)
        CompiledData.bank = "Произошла ошибка на стороне ресурса или сервиса"
    finally:
        print(datetime.datetime.now(), "BANK")