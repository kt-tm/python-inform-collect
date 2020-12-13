from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
vacancydb = db.vacancies

vacancy_input = 'менеджер по продажам авто'
    # input('Ввведите название вакансии ')  # 'менеджер по продажам авто'
# pr_reload_file = input('Введите yes, если необходимо перезаписать файл с результатами ')
main_link = 'https://hh.ru'
addit_params = f"/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&search_field=description&text={vacancy_input}"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
vacancies = []
cnt = 0
def insert_uniq(data):
    if vacancydb.count_documents({'link': data['link']}) == 0:
        vacancydb.insert_one({
            "site": data['site'],
            "vacancy": data['vacancy'],
            "link": data['link'],
            "currency": data['currency'],
            "salary_min": data['salary_min'],
            "salary_max": data['salary_max']})
        return True
    else:
        return False

while True:
    response = requests.get(main_link + addit_params, params={}, headers=headers)
    soup = bs(response.text, 'html.parser')
    if response.ok:
        vacancy_list = soup.findAll('div', {'class': 'vacancy-serp-item__row_header'})
        for vacancy in vacancy_list:
            data = {}
            cnt += 1
            vacancy_header = vacancy.find('a')
            data['site'] = 'https://hh.ru'
            data['vacancy'] = vacancy_header.text
            data['link'] = vacancy_header['href']
            data['currency'] = None
            data['salary_min'] = None
            data['salary_max'] = None
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            try:
                salary_text = ''.join(vacancy_salary.text.split()[:-1])
                data['currency'] = vacancy_salary.text.split()[-1]
                if salary_text.find('-') > -1:
                    data['salary_min'] = int(re.sub('\D', '', salary_text.split('-')[0]))
                    data['salary_max'] = int(re.sub('\D', '', salary_text.split('-')[-1]))
                elif salary_text.find('от') > -1:
                    data['salary_min'] = int(re.sub('\D', '', salary_text))
                    data['salary_max'] = None
                elif salary_text.find('до') > -1:
                    data['salary_min'] = None
                    data['salary_max'] = int(re.sub('\D', '', salary_text))
                else:
                    data['salary_min'] = int(re.sub('\D', '', salary_text))
                    data['salary_max'] = int(re.sub('\D', '', salary_text))
                vacancies.append(data)
                pprint(data)
                insert_uniq(data)
            except AttributeError:
                continue
        next_link = soup.find('a', {'data-qa': 'pager-next'})
        if next_link is None:
            break
        addit_params = next_link['href']
for t in vacancydb.find():
    pprint(t)

