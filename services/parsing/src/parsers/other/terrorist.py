from asyncio import sleep as asleep

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


url = "https://fedsfm.ru/documents/terrorists-catalog-portal-add"


class Terrorist:
    __error_logger = Logger('error')
    __info_logger = Logger()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )

    def __init__(self) -> None:
        self.__driver = webdriver.Chrome(options=self.chrome_options)

    async def check(self, fullname: str, classObject: ResponseData) -> None:
        self.__info_logger.info('TER', 1)
        try:
            self.__driver.get(url)
            try:
                (
                    self.__driver.find_element(By.ID, 'details-button').click()
                ), (
                    self.__driver.find_element(By.ID, 'proceed-link').click()
                )
            except Exception:
                pass
            await asleep(1)
            (
                self.__driver.find_element(By.CLASS_NAME, 'panel-title')
                .find_element(By.TAG_NAME, 'a').click()
            )
            await asleep(1)
            (
                self.__driver.find_elements(By.CLASS_NAME, 'panel-group')[2]
                .find_element(By.TAG_NAME, 'a').click()
            )
            await asleep(1)
            StringsInTable = (
                self.__driver.find_element(By.ID, 'russianFL')
                .find_elements(By.TAG_NAME, 'li')
            )
            terrorists = []
            await asleep(1)
            for String in StringsInTable:
                FIO = String.text.split()
                FIO = FIO[1] + ' ' + FIO[2] + ' ' + FIO[3]
                terrorists.append(FIO.replace('*', '').replace(',', ''))
            if fullname.upper() in terrorists:
                classObject.ter = "Человек есть в базе данных"
        except Exception as error:
            self.__error_logger.error(str(error) + ' TER')

    def __del__(self):
        self.__driver.quit()
        self.__info_logger.info('TER', 2)
