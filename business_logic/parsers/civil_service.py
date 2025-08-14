import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)


def check_civserv(surname, name, patronymic):
    url = f'https://gossluzhba.gov.ru/reestr?filters=%7B"fullName":"{surname}%20{name}%20{patronymic}"%7D&page=1'
    print(url)
    if surname == ' ' and name == ' ' and patronymic == ' ':
        url = 'https://gossluzhba.gov.ru/reestr?filters=%7B"fullName":null%7D&page=1'

    try:
        driver.get(url)
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'table.text-center.table-hover.text-xs.line-height-xs')))

        table = driver.find_element(By.XPATH, '/html/body/app-root/div/section[4]/app-trust-loss-dismissal-records-list/div/app-trust-loss-dismissal-records-table/app-loader/div/div/table/tbody')
        linesOfTable = table.find_elements(By.TAG_NAME, 'tr')
        list_abs = []
        for iteration_number, nothing_matters in enumerate(linesOfTable):
            list_temp = []
            columnsOfLine = linesOfTable[iteration_number].find_elements(By.TAG_NAME, 'td')
            for column in (2, 3, 4, 5, 6):
                list_temp.append(columnsOfLine[column].text)
            list_abs.append(list_temp)
        return list_abs

    except Exception as e:
        return f"Ошибка: {e}"



if __name__ == "__main__":
    print(check_civserv('Гилев', 'Станислав', 'Георгиевич'))
    print(check_civserv('Гилеа', 'Станислав', 'Георгиевич'))
    print(check_civserv(' ', ' ', ' '))