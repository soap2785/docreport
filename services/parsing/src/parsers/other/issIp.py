import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger
from ..captcha import solveCaptcha


class ISS:
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

    def check(
            self,
            fullname: str,
            birthdate: str,
            region: str
    ) -> None:
        self.__info_logger.info('ISS')
        url = 'https://fssp.gov.ru/iss/ip'
        wd = WebDriverWait(self.__driver, 2)
        ResponseData.iss = 'Ничего не найдено'
        try:
            self.__driver.get(url)
            time.sleep(1)

            try:
                self.__driver.find_element(By.CLASS_NAME, 't-warning')
                ResponseData.iss = "Сервис недоступен"
                self.__driver.quit()
                return None

            except NoSuchElementException:
                pass

            regInp = self.__driver.find_element(
                By.ID, 'region_id_chosen'
            ).find_element(
                By.TAG_NAME, 'input'
            )
            regInp.click()
            wd.until(
                ec.presence_of_element_located(
                    (By.CLASS_NAME, 'chosen-results')
                )
            )
            regInp.send_keys(region, Keys.ENTER)

            ToBeClickable((By.ID, 'input01')).send_keys(fullname.split()[0])
            ToBeClickable((By.ID, 'input02')).send_keys(fullname.split()[1])
            ToBeClickable((By.ID, 'input03')).send_keys(fullname.split()[2])
            ToBeClickable((By.ID, 'input04')).send_keys(birthdate)
            self.__driver.find_element(By.XPATH, '//*[@id="app"]/main').click()
            ToBeClickable((By.ID, 'btn-sbm')).click()
            try:
                img = ToBeClickable((By.ID, 'capchaVisual'))
                print(img)
                image = self.__driver.find_element(By.ID, 'capchaVisual')
                print(image)
                solve = solveCaptcha(image.get_attribute("src"))['code']
                self.__driver.find_element(
                    By.ID,
                    'captcha-popup-code'
                ).send_keys(solve, Keys.ENTER)
                wd.until(
                    ec.invisibility_of_element_located((
                        By.XPATH, '/html/body/div[5]/div[1]/div[2]')
                    )
                )
            except Exception:
                pass
            try:
                trs = self.__driver.find_element(
                    By.ID, 'content'
                ).find_element(
                    By.TAG_NAME, 'tbody'
                ).find_elements(
                    By.TAG_NAME, 'tr'
                )
                dataAbs = []
                for tr in trs:
                    tds = tr.find_elements(
                        By.TAG_NAME,
                        'td'
                    )
                    dataCur = []
                    for index, td in enumerate(tds):
                        if index not in (0, 3, 4, 7):
                            dataCur.append(td.text)
                    if dataCur:
                        dataAbs.append(dataCur)
                ResponseData.iss = dataAbs
            except NoSuchElementException:
                ResponseData.iss = "Ничего не найдено"

        except NoSuchElementException:
            ResponseData.iss = "Ничего не найдено"

        except Exception as error:
            self.__error_logger.error(str(error) + ' ISS')

        finally:
            self.__info_logger.info('ISS')
            self.__driver.quit()


def ToBeClickable(driver, pointer: set[str, str]) -> any:
    return WebDriverWait(driver, 2).until(ec.element_to_be_clickable(pointer))
