import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
def check_civserv(surname, name, patronymic):
    url = f'https://gossluzhba.gov.ru/reestr?filters=7B"fullName":"{surname}%20{name}%20{patronymic}"%7D&page=1'
    response = requests.get(url, headers = headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        result = soup.find('')
        print(result)


if __name__ == "__main__":
    print(check_civserv('Гилев', 'Станислав', 'Георгиевич'))
    print(check_civserv('Гилеа', 'Станислав', 'Георгиевич'))