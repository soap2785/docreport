import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://egrul.nalog.ru/index.html'

def suggest_fsn(inn, surname, name, patronymic):
    driver.get(url)
    inp = driver.find_element(By.XPATH, '//*[@id="query"]')
    inp.send_keys(inn)
    inp.send_keys(Keys.ENTER)
    time.sleep(1)
    try:
        nothing_result = driver.find_element(By.XPATH, '//*[@id="noDataFound"]/div/div/p')
        for x in inn:
            inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(surname + ' ' + name + ' ' + patronymic)
        inp.send_keys(Keys.ENTER)
        time.sleep(1)
        try:
            nothing_result = driver.find_element(By.XPATH, '//*[@id="noDataFound"]/div/div/p')
            return "Человека нету в базе данных"
        except:
            ...
    except:
        ...


if __name__ == "__main__":
    print(suggest_fsn('490018495', 'a', 'a', 'a'))