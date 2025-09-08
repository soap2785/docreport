import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from business_logic.parsers.captcha import solveCaptcha
from mainDIR.bot.config import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://fssp.gov.ru/iss/ip'
wd = WebDriverWait(driver, 10)


async def iss_ip(region, fullname, birthdate) -> list | str:
    fullname = fullname.split()
    surname = fullname[0]
    name = fullname[1]
    patronymic = fullname[2]
    birthdate = datetime.datetime.strftime(birthdate, '%d.%m.%Y')

    try:
        driver.get(url)

        regInp = driver.find_element(By.XPATH, '//*[@id="region_id_chosen"]/div/div/input')
        regInp.click()
        wd.until(ec.presence_of_element_located((By.XPATH, '//*[@id="region_id_chosen"]/div/ul')))
        regInp.send_keys(region, Keys.ENTER)

        wd.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="input01"]'))).send_keys(surname)
        wd.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="input02"]'))).send_keys(name)
        wd.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="input05"]'))).send_keys(patronymic)
        wd.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="input06"]'))).send_keys(birthdate)
        driver.find_element(By.XPATH, '//*[@id="app"]/main').click()
        wd.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="btn-sbm"]'))).click()

        wd.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="capchaVisual"]')))
        image = driver.find_element(By.XPATH, '//*[@id="capchaVisual"]')
        solve = solveCaptcha(image.get_attribute("src")).get('code')
        driver.find_element(By.XPATH, '//*[@id="captcha-popup-code"]').send_keys(solve, Keys.ENTER)
        wd.until(ec.invisibility_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[2]')))
        try:
            table = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[3]/div/div/div[2]/table/tbody')
            trs = table.find_elements(By.TAG_NAME, "tr")
            dataAbs = []
            for tr in trs:
                tds = tr.find_elements(By.TAG_NAME, 'td')
                dataCur = []
                for index, td in enumerate(tds):
                    if index not in (0, 3, 4, 7):
                        dataCur.append(td.text)
                if dataCur:
                    dataAbs.append(dataCur)
            return dataAbs
        except NoSuchElementException:
            return 'Ничего не найдено 101'

    except Exception as e:
        print(e)
        return "Ничего не найдено"
    finally:
        driver.quit()
