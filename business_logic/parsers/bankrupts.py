from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from oldconfig import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://bankrot.fedresurs.ru/bankrupts'
wd = WebDriverWait(driver, 10)


def bankrupt(inn, fullname) -> str | None:
    fullname = fullname.split()
    surname = fullname[0]
    name = fullname[1]
    patronymic = fullname[2]

    driver.get(url)
    inp = wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/section/div[1]/app-bankrupt/div/'
                                                               'div[1]/div/app-bankrupt-form/div/form/'
                                                               'app-form-search-string/div/form/div/div/el-input/div/'
                                                               'div/div/input')))
    inp.send_keys(inn, Keys.ENTER)
    try:
        wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/section/div[1]/app-bankrupt/div/'
                                                             'div[2]/div/app-loader/div[1]/app-bankrupt-result/'
                                                             'el-tab-panel/div[2]')))
        individual = driver.find_element(By.XPATH, '/html/body/app-root/section/div[1]/app-bankrupt/div/div[2]/'
                                                   'div/app-loader/div[1]/app-bankrupt-result/el-tab-panel/div[1]/ul/'
                                                   'li[2]/div/span[2]')
        if int(individual.text) >= 1:
            return "Человек в базе присутствует"

        elif individual.text == '0':
            return "Физлиц нет"
    except:
        for number in inn:
            inp.send_keys(Keys.BACKSPACE)
        try:
            driver.find_element(By.XPATH,'/html/body/app-root/section/div[1]/app-bankrupt/div/div[2]/div/'
                                         'app-loader/div/div/div[1]')
            inp.send_keys(surname + ' ' + name + ' ' + patronymic)
            inp.send_keys(Keys.ENTER)
            wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/section/div[1]/app-bankrupt/div/'
                                                                 'div[2]/div/app-loader/div[1]/app-bankrupt-result/'
                                                                 'el-tab-panel/div[2]')))
            individual = driver.find_element(By.XPATH,'/html/body/app-root/section/div[1]/app-bankrupt/div/div[2]/'
                                                      'div/app-loader/div[1]/app-bankrupt-result/el-tab-panel/div[1]/ul/'
                                                      'li[2]/div/span[2]')
            if int(individual.text) >= 1:
                return "Человек в базе присутствует"
            else:
                return "Человек в базе отсутствует"
        except:
            return "Человек в базе отсутствует"