from datetime import datetime
import requests
from fake_useragent import UserAgent
import codecs
from bs4 import BeautifulSoup as bs
import urllib.request
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# создаю браузер
def get_browser(headless=True):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # result = requests.get('https://www.avito.ru/all/avtomobili?cd=1&f=ASgBAgICAUTyCrCKAQ', headers=headers)
    service = Service(executable_path=ChromeDriverManager().install())
    options = Options()
    # выключаю экранный режим
    if headless:
        options.add_argument("--headless")
    browser = webdriver.Chrome(service=service, options=options)
    browser.implicitly_wait(5)
    print(f'Create browser {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}')
    return browser

# закрываю браузер
def browser_close(browser):
    browser.close()
    browser.quit()
    print(f'Browser close {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}')

# создаю объект супа
def get_soup(browser):
    '''
    передаю браузер (страницу открытую в selenium)
    '''
    # browser.get(url)
    # sleep(random.randint(3, 6))
    # pyautogui.hotkey('ctrl', 's')
    # sleep(1)
    # pyautogui.typewrite('page.html')
    # pyautogui.hotkey('enter')
    # with open('page.txt', 'w', encoding='UTF-8') as f:  # encoding='cp1251'
    #     f.write(browser.page_source)
    soup = bs(browser.page_source, 'lxml')
    # print(soup)
    return soup

def parse_rabota(url):
    '''
    :param url: ссылка на страницу поиска
    :return: два списка: vacancy_list и er
    '''
    # создаю объект браузера
    browser = get_browser()
    # открываю ссылку в селениуме
    browser.get(url)
    # получаю суп
    soup = get_soup(browser)
    vacancy_list = []
    er = []  # список для ошибок
    main_div = soup.find('div', class_='home-vacancies__infinity-list')  # a11y-main-content
    if main_div:
        vacancy_tbl = main_div.find_all(attrs={'itemtype': 'http://schema.org/JobPosting'})
        for vacancy in vacancy_tbl:
            title = vacancy.find('h3', class_='vacancy-preview-card__title').text.strip()
            link = vacancy.find('a').get('href').split('?')[0]  # /vacancy/47298372/?search_id=1680030580507mv7cwb9kbim
            link = f'https://spb.rabota.ru{link}'
            company = vacancy.find('span', class_='vacancy-preview-card__company-name').text.strip()
            salary = vacancy.find('div', class_='vacancy-preview-card__salary').text.strip()
            city = vacancy.find('span', class_='vacancy-preview-location__address-text').text.strip()
            vacancy_list.append({
                'title': title,
                'link': link,
                'company': company,
                'salary': salary,
                'city': city,
            })
            print(f'title: {title}, link: {link}, company: {company}, salary: {salary}, city: {city}')
    else:
        er.append({
            'url': url,
            'er': 'main_div not find',
        })
    # print(vacancy_list, file=codecs.open('vacancy_list_rabota.json', 'w', 'utf-8'))
    # закрываю браузер
    browser_close(browser)
    return vacancy_list, er


def main():
    url = 'https://spb.rabota.ru/?query=python&sort=relevance&all_regions=1'
    parse_rabota(url=url)

if __name__ == '__main__':
    main()
