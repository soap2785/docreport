import asyncio
import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from businessLogic.classForParsers import CompiledData
from mainDIR.bot.src.config import proxies
from businessLogic.driverClass import DriverClass

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = DriverClass.driver
url = "https://fedsfm.ru/documents/terrorists-catalog-portal-add"


async def terroristCheck(fullname):
    """
    Возвращает состояние нахождения лица в базе террористов
    :param fullname:
    :return: str
    """
    print(datetime.datetime.now(), "TER")
    try:
        driver.get(url)
        try:
            passWarning = driver.find_element(By.XPATH, '//*[@id="details-button"]')
            passWarning.click()
            passWarning = driver.find_element(By.XPATH, '//*[@id="proceed-link"]')
            passWarning.click()
        except NoSuchElementException:
            pass

        TableTwoOpen = driver.find_element(By.XPATH, '//*[@id="bodyContent"]/div/div/div/div/div/div[1]/div/div[1]/h4/a')
        TableTwoOpen.click()
        await asyncio.sleep(1)

        TableRestOpen = driver.find_element(By.XPATH, '//*[@id="NationalPart"]/div/div[2]/div/div[1]/h4/a')
        TableRestOpen.click()

        table = driver.find_element(By.XPATH, '//*[@id="russianFL"]/div/ol')
        StringsInTable = table.find_elements(By.TAG_NAME, 'li')
        terrorists = []
        await asyncio.sleep(1)
        for String in StringsInTable:
            FIO = String.text.split()
            terrorists.append(FIO[1] + ' ' + FIO[2] + ' ' + FIO[3].replace('*', '').replace(',', ''))
        if fullname.upper() in terrorists:
            CompiledData.ter = "Человек есть в базе данных"
        else:
            CompiledData.ter = "Человека нет в базе данных"
    except Exception as e:
        print(e)
        return None
    finally:
        print(datetime.datetime.now(), "TER")
