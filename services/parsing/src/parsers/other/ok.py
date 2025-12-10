from asyncio import sleep as asleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


class OK:
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
        self.__info_logger.info('OK', 1)
        hrefs = []
        try:
            self.__driver.get('https://m.ok.ru/alexei')
            await asleep(2)
            (
                self.__driver.find_element(By.CLASS_NAME, 'base-button_target')
                .click()
            )
            await asleep(2)
            (
                self.__driver.find_element(
                    By.ID, 'AnonymGlobalAllSearchFormField'
                )
                .send_keys(fullname, Keys.ENTER)
            )
            await asleep(2)
            (
                self.__driver.find_element(By.CLASS_NAME, 'clickarea').click()
            )
            await asleep(2)
            for card in (
                self.__driver.find_element(By.ID, 'user-list')
                .find_elements(By.CLASS_NAME, 'item')
            ):
                if len(hrefs) == 5:
                    break
                hrefs.append(
                    card.find_element(By.CLASS_NAME, 'clickarea')
                    .get_attribute('href')
                )
            if hrefs:
                classObject.ok = hrefs
        except Exception as error:
            self.__error_logger.error(str(error) + ' OK')

    def __del__(self):
        self.__info_logger.info('OK', 2)
        self.__driver.quit()
