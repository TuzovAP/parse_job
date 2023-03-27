import requests
from fake_useragent import UserAgent
import codecs
from bs4 import BeautifulSoup as bs

ua = UserAgent()
headers = {'User-Agent': ua.random}
url = 'https://spb.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=Python&from=suggest_post'
resp = requests.get(url, headers=headers)
vacancy_list = []
er = []  # список для ошибок
if resp.status_code == 200:
    soup = bs(resp.content, 'lxml')  # html.parser
    main_div = soup.find('div', id='a11y-main-content')  # a11y-main-content
    if main_div:
        vacancy_tbl = main_div.find_all('div', class_='vacancy-serp-item__layout')
        # vacancy_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
        for vacancy in vacancy_tbl:
            title = vacancy.find('a', class_='serp-item__title').text
            link = vacancy.find('a', class_='serp-item__title').get('href')
            company = vacancy.find('div', class_='vacancy-serp-item__meta-info-company').text
            link = link.split('?')[0]
            try:
                # salary = vacancy.find('span data-qa', class_='vacancy-serp__vacancy-compensation').text
                salary = vacancy.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            except Exception as ex:
                print(f'Salary not find, er: {ex}')
                salary = ''
            city = vacancy.find(attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text  # Минск, Купаловская и еще 2
            city = city.split(',')[0]
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
else:
    er.append({
        'url': url,
        'er': resp.status_code,
    })
# print(resp.text)
print(vacancy_list, file=codecs.open('vacancy_list.json', 'w', 'utf-8'))
print(resp.text, file=codecs.open('resp_text.html', 'w', 'utf-8'))
