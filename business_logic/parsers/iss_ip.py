import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from business_logic.parsers.captcha import solve_captcha
from config import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
url = 'https://fssp.gov.ru/iss/ip'
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)


def iss_ip(region, surname, name, patronymic, birthdate):
    try:
        driver.get(url)

        # 1. Кликаем на поле "Территориальные органы", чтобы открыть список
        dropdown_element = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/div/div/div[5]/div/form/div/div[2]/div/div/div/div/input')
        dropdown_element.click()

        # 2. Вводим название региона, чтобы отфильтровать список
        region_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body/div[2]/main/section/div/div/div[5]/div/form/div/div[2]/div/div/div/ul")  # Здесь лучше использовать более точный селектор для самого поля ввода, если есть
            )
        )
        region_input = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/div/div/div[5]/div/form/div/div[2]/div/div/div/div/input')
        region_input.send_keys(region)
        region_input.send_keys(Keys.ENTER)

        # 4. Вводим фамилию
        surname_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/main/section/div/div/div[5]/div/form/div/div[3]/div/input"))
        )
        surname_input.send_keys(surname)

        # 5. Вводим имя
        name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/main/section/div/div/div[5]/div/form/div/div[4]/div/input')
            )
        )
        name_input.send_keys(name)

        # 6. Вводим отчество
        patronymic_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/main/section/div/div/div[5]/div/form/div/div[7]/div[1]/div/input')
            )
        )
        patronymic_input.send_keys(patronymic)

        # 7. Вводим дату рождения
        birthdate_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '/html/body/div[2]/main/section/div/div/div[5]/div/form/div/div[7]/div[2]/div/div/input[1]')
            )
        )
        birthdate_input.send_keys(birthdate)

        #8. Кликаем на кнопку поиска
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/main/section/div/div/div[5]/div/form/div/div[8]/div/input')
            )
        )
        element_outside_menu = driver.find_element(By.XPATH, "/html/body/div[2]/main")
        element_outside_menu.click()
        button.click()
        time.sleep(1)
        image = driver.find_element(By.XPATH, '//*[@id="capchaVisual"]')
        url_captcha = image.get_attribute("src")
        solve = solve_captcha(url_captcha).get('code')
        captcha_input = driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[2]/div/div/div/form/div[2]/input[1]')
        captcha_input.send_keys(solve)
        captcha_button = driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[2]/div/div/div/form/div[2]/input[2]')
        captcha_button.click()
        time.sleep(1)
        try:
            table = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[3]/div/div/div[2]/table/tbody')
            trs = table.find_elements(By.TAG_NAME, "tr")
            data_abs = []
            for tr in trs:
                tds = tr.find_elements(By.TAG_NAME, 'td')
                data_cur = []
                for index, td in enumerate(tds):
                    if index not in (0, 3, 4, 7):
                        data_cur.append(td.text)
                    data_abs.append(data_cur)
            return data_abs
        except:
            return ('Ничего не найдено')


    except Exception as e:
        print('Произошла ошибка')
        if input() == 'y':
            print(e)

    finally:
        driver.quit()
