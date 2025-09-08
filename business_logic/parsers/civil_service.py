import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from mainDIR.bot.config import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)


async def checkCivserv(fullname) -> list | str:
    """
    Возвращает состояние нахождения лица в базе госслужащих

    Args:
        fullname: полное ФИО интересующего лица

    Returns:
        Список, содержащий данные таблицы с сайта или строку, которая гласит что лица нет в базе
    """
    fullname = fullname.split()
    surname = fullname[0]
    name = fullname[1]
    patronymic = fullname[2]

    url = f'https://gossluzhba.gov.ru/reestr?filters=%7B"fullName":"{surname}%20{name}%20{patronymic}"%7D&page=1'

    if surname == ' ' and name == ' ' and patronymic == ' ':
        url = 'https://gossluzhba.gov.ru/reestr?filters=%7B"fullName":null%7D&page=1'

    try:
        driver.get(url)
        await asyncio.sleep(2)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'table.text-center.table-hover.text-xs.line-height-xs')))
        table = driver.find_element(By.XPATH, '/html/body/app-root/div/section[4]/app-trust-loss-dismissal-records-list/div/app-trust-loss-dismissal-records-table/app-loader/div/div/table/tbody')
        linesOfTable = table.find_elements(By.TAG_NAME, 'tr')
        listAbs = []

        for iteration_number, nothing_matters in enumerate(linesOfTable):
            listTemp = []
            columnsOfLine = linesOfTable[iteration_number].find_elements(By.TAG_NAME, 'td')

            for column in (2, 3, 4, 5, 6):
                listTemp.append(columnsOfLine[column].text)

            listAbs.append(listTemp)

        return listAbs

    except IndexError:
        return "Человека нет в базе данных"
    except Exception as e:
        print(e)
        return "Произошла ошибка со стороны ресурса или сервиса"