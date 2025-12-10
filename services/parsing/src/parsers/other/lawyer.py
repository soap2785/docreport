from asyncio import sleep as asleep

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


class Lawyer:
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

    def __init__(self):
        self.__driver = webdriver.Chrome(options=self.chrome_options)

    async def check(self, fullname: str, classObject: ResponseData) -> None:
        self.__info_logger.info('LAW', 1)
        url = "https://minjust.gov.ru/ru/pages/advokaty-rossijskoj-federacii/"
        try:
            self.__driver.get(url)
            await asleep(2)
            (
                self.__driver.find_element(By.CLASS_NAME, 'dt-icon-filter')
                .click()
            )
            await asleep(0.5)
            (
                self.__driver.find_element(
                    By.CLASS_NAME, 'registries_facet_window_search'
                )
                .send_keys(fullname)
            )
            await asleep(0.5)
            (
                self.__driver.find_element(
                    By.CLASS_NAME, 'registries_facet_window_raw'
                )
                .find_element(By.TAG_NAME, 'input').click()
            )
            await asleep(0.5)
            absList = []
            for row in (
                self.__driver.find_elements(By.CLASS_NAME, 'registry_grid_raw')
            ):
                tempList = []
                for col in (
                    row.find_elements(By.CLASS_NAME, 'registry_grid_cell')
                ):
                    if col.text != "":
                        tempList.append(col.text)
                absList.append(tempList)
            if absList:
                classObject.law = absList
        except Exception as error:
            self.__error_logger.error(str(error) + ' LAW')

    def __del__(self):
        self.__info_logger.info('LAW', 2)
        self.__driver.quit()
