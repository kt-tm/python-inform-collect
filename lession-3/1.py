from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['vacancies']
vacancydb = db.vacancies

# задание 2
salary = int(input('Ввведите желаемую зарплату '))
def check_salary(salary):
    for vacancy in vacancydb.find({'$or': [{'salary_max':{'$gte': salary}},
                                    {'salary_min':{'$gte': salary}}]}):
        pprint(vacancy)
check_salary(salary)

# задание 3
data = {'currency': 'руб.',
 'link': 'https://www.superjob.ru/vakansii/menedzher-po-prodazham-dop-35086698.html',
 'salary_max': 180000,
 'salary_min': None,
 'site': 'https://www.superjob.ru',
 'vacancy': 'Менеджер по продажам доп. оборудования для автомобилей'}
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
print(insert_uniq(data))
