from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def check_civserv(surname, name, patronymic):
    """Ищет данные о государственных служащих, используя Selenium."""

    url = f'https://gossluzhba.gov.ru/reestr?filters=%7B"fullName":"{surname}%20{name}%20{patronymic}"%7D&page=1'
    print(url)
    if surname == ' ' and name == ' ' and patronymic == ' ':
        url = 'https://gossluzhba.gov.ru/reestr?filters=%7B"fullName":null%7D&page=1'
        print(url)
    # Настройка опций Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Инициализация драйвера
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Явное ожидание загрузки таблицы
        wait = WebDriverWait(driver, 10)
        table = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table.text-center.table-hover.text-xs.line-height-xs')) #Селектор таблицы
        )

        # Находим tbody
        tbody = driver.find_elements(By.CSS_SELECTOR, 'tbody')
        tr_elements = tbody[0].find_elements(By.CSS_SELECTOR, 'tr')

        if tr_elements:
            # Обрабатываем каждую строку
            for tr in tr_elements:
                print(tr)
                td_elements = tr.find_elements(By.TAG_NAME, 'td')
                print(td_elements)
                print(101)
                if td_elements:
                    for td in td_elements:
                        ...
                else:
                    try:
                        th = tr.find_element(By.CSS_SELECTOR, 'th')
                        print(th.text)
                    except:
                        print('Ничего не найдено')
        else:
             print("Строки в таблице не найдены")

    except TimeoutException:
        print("Время ожидания истекло, таблица не загрузилась.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

    return None


if __name__ == "__main__":
    print("Searching for Гилев Станислав Георгиевич:")
    check_civserv('Гилев', 'Станислав', 'Георгиевич')
    print("\nSearching for Гилеа Станислав Георгиевич:")
    check_civserv('Гилеа', 'Станислав', 'Георгиевич')
    check_civserv(' ', ' ', ' ')