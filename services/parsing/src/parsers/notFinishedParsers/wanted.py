from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from businessLogic.parsers.captcha import solveCaptcha
from mainDIR import proxies

webdriver.DesiredCapabilities.CHROME['proxy'] = proxies
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
url = 'https://мвд.рф/wanted'
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


def get_image_data_url(driver, img_element):
    """Получает Data URL из элемента img с использованием JavaScript."""
    script = """
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    var img = arguments[0];

    console.log("IMG Element:", img);
    console.log("IMG Width:", img.width);
    console.log("IMG Height:", img.height);
    console.log("IMG NaturalWidth:", img.naturalWidth);
    console.log("IMG NaturalHeight:", img.naturalHeight);
    console.log("IMG Complete:", img.complete);

    if (!img.complete) {
        console.error("Изображение не загружено полностью (complete = false)!");
        return null;
    }

    if (img.naturalWidth === 0 || img.naturalHeight === 0) {
        console.error("Изображение не загружено (naturalWidth или naturalHeight = 0)!");
        return null;
    }

    if (img.width === 0 || img.height === 0) {
        console.warn("Ширина или высота элемента IMG равна нулю, используя naturalWidth и naturalHeight");
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
    } else {
        canvas.width = img.width;
        canvas.height = img.height;
    }


    try {
        ctx.drawImage(img, 0, 0);
        var dataURL = canvas.toDataURL('image/png');
        console.log("Data URL:", dataURL);
        return dataURL;
    } catch (e) {
        console.error("Ошибка при создании Data URL:", e);
        return null; // Или можно выбросить исключение
    }
    """
    return driver.execute_script(script, img_element)


def wanted(surname, name, patronymic, birthdate):
    driver.get(url)
    birthdate = datetime.strptime(birthdate, '%d.%m.%Y')
    space = driver.find_element(By.XPATH, '//*[@id="form-1"]')
    driver.find_element(By.XPATH, '//*[@id="search-form"]/div[1]/div[1]/div[1]/div/div/input').send_keys(surname)
    space.click()
    driver.find_element(By.XPATH, '//*[@id="search-form"]/div[1]/div[1]/div[2]/div/div/input').send_keys(name)
    space.click()
    driver.find_element(By.XPATH, '//*[@id="search-form"]/div[1]/div[1]/div[3]/div/div/input').send_keys(patronymic)
    space.click()
    driver.find_element(By.XPATH, '//*[@id="search-form"]/div[1]/div[2]/div[1]/div/div/span/span[1]/span').click()
    driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input').send_keys(str(birthdate.year), Keys.ENTER)
    driver.find_element(By.XPATH, '//*[@id="search-form"]/div[1]/div[2]/div[2]/div/div/span/span[1]/span').click()
    driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input').send_keys(str(months[birthdate.month - 1]), Keys.ENTER)
    driver.find_element(By.XPATH, '//*[@id="search-form"]/div[1]/div[2]/div[3]/div/div/span/span[1]/span').click()
    driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input').send_keys(str(birthdate.day), Keys.ENTER)
    driver.find_element(By.XPATH, '//*[@id="search-form"]/div[1]/div[3]/div[1]/div/div/input').send_keys('soap5220@gmail.com')
    img_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[5]/div[2]/div[5]/form/div[4]/div[1]/div/div[1]/img')
    WebDriverWait(driver, 10).until(lambda driver: driver.execute_script(
        "return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0",
        img_element
    ))
    data_url = get_image_data_url(driver, img_element)
    solved = solveCaptcha(data_url)
    driver.find_element(By.XPATH, '//*[@id="search-form"]/div[4]/div[1]/div/div[2]/div/input').send_keys(solved.get('code'))
    driver.find_element(By.XPATH, '//*[@id="search-form"]/div[4]/div[3]/button').click()