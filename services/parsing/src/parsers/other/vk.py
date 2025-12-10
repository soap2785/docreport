from asyncio import sleep as asleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


class VK:
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
        classObject.vk = 'Данные не обнаружены'
        hrefs = []
        self.__info_logger.info('VK', 1)
        try:
            self.__driver.get('https://vk.com')
            await asleep(3)
            (
                self.__driver.find_element(By.ID, 'search-:r0:')
                .send_keys(fullname, Keys.ENTER)
            )
            await asleep(3)
            self.__driver.find_elements(
                By.CLASS_NAME, 'vkuiButton__content'
            )[1].click()
            await asleep(3)
            for card in self.__driver.find_elements(
                By.CLASS_NAME, 'vkitUserRichCell__container--9XWzm'
            ):
                if len(hrefs) == 5:
                    break
                hrefs.append(
                    card.find_element(By.CLASS_NAME, 'vkitLink__link--4toGC')
                    .get_attribute('href')
                )
            if hrefs:
                classObject.vk = hrefs
        except Exception as error:
            self.__error_logger.error(str(error) + ' VK')

    def __del__(self):
        self.__info_logger.info('VK', 2)
        self.__driver.quit()
