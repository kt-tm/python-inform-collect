from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint

# https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&search_field=description&text=Postgresql java script python oracle
vacancy_input = input('Ввведите название вакансии ')  # 'Postgresql java script python oracle'
main_link = 'https://hh.ru'
addit_params = f"/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&search_field=description&text={vacancy_input}"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
vacancies = []
cnt = 0
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
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if vacancy_salary is None:
                data['currency'] = None
                data['salary_min'] = None
                data['salary_max'] = None
                vacancies.append(data)
                continue
            salary_text = vacancy_salary.text.replace(' ' + vacancy_salary.text.split()[-1], '')
            data['currency'] = vacancy_salary.text.split()[-1]
            if salary_text.find('-') > -1:
                data['salary_min'] = re.sub('\D', '', salary_text.split('-')[0])
                data['salary_max'] = re.sub('\D', '', salary_text.split('-')[-1])
            elif salary_text.find('от') > -1:
                data['salary_min'] = re.sub('\D', '', salary_text)
                data['salary_max'] = None
            elif salary_text.find('до') > -1:
                data['salary_min'] = None
                data['salary_max'] = re.sub('\D', '', salary_text)
            vacancies.append(data)
            next_link = soup.find('a', {'data-qa': 'pager-next'})
        if next_link is None:
            break
        addit_params = next_link['href']
pprint(vacancies)
print(cnt)
print(len(vacancies))





