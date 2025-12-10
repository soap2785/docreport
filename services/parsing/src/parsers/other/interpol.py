from asyncio import sleep as asleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from transliterate import translit

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


class Interpol:
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
        self.__info_logger.info('INTER', 1)
        url = 'https://www.interpol.int/How-we-work/Notices/Red-Notices/'
        'View-Red-Notices'
        try:
            self.__driver.get(url)
            (
                self.__driver.find_element(By.ID, 'nationality')
                .send_keys('Russia')
            )
            await asleep(0.5)
            translitquery = translit(fullname, 'ru', reversed=True)
            (
                self.__driver.find_element(By.ID, 'nationality')
                .send_keys(Keys.ENTER)
            ), (
                self.__driver.find_element(By.ID, 'name')
                .send_keys(translitquery.split()[0].upper())
            ), (
                self.__driver.find_element(By.ID, 'forename')
                .send_keys(translitquery.split()[1].upper())
            ), (
                self.__driver.find_element(By.ID, 'submit').click()
            )
            await asleep(1)
            if (
                self.__driver.find_element(By.ID, 'searchResults').text
            ) != "0":
                classObject.inter = 'Числится в Интерполе'
        except Exception as error:
            self.__error_logger(str(error) + ' INTER')

    def __del__(self):
        self.__info_logger.info('INTER', 2)
        self.__driver.quit()
