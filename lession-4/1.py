import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
import datetime

client = MongoClient('127.0.0.1', 27017)
db = client['news']
newsdb = db.news

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

def insert_uniq(data):
    if newsdb.count_documents({'link': data['link']}) == 0:
        newsdb.insert_one({
            "source": data['source'],
            "link": data['link'],
            "name": data['name'],
            "date": data['date']})
        return True
    else:
        return False

def get_news(url, xpath_gen, xpath_link, xpath_name, xpath_page_gen, xpath_date, xpath_source, pr_source, pr_current_page_dt, pr_current_page_src):
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)
    items = dom.xpath(xpath_gen)
    news = []
    date = None

    for item in items:
        new = {}
        link = item.xpath(xpath_link)
        name = item.xpath(xpath_name)
        source = None if xpath_source is None else item.xpath(xpath_source)

        date = item.xpath(xpath_date)
        new['link'] = url + link[0] if pr_source else link[0]
        new['name'] = name[0]
        new['source'] = source[0] if pr_current_page_src and xpath_source is not None else url
        new['date'] = date[0] if pr_current_page_dt else None


        if not pr_current_page_dt or not pr_current_page_src:
            response_date = requests.get(new['link'], headers=header)
            dom_date = html.fromstring(response_date.text)
            items_date = dom_date.xpath(xpath_page_gen)

            for item_date in items_date:
                date = item_date.xpath(xpath_date)
                source = None if xpath_source is None else item_date.xpath(xpath_source)
                new['source'] = source[0] if not pr_current_page_src and xpath_source is not None else new['source']
                new['date'] = date[0] if not pr_current_page_dt else new['date']
        news.append(new)
        insert_uniq(new)


get_news('https://lenta.ru/', "//div[@class='b-yellow-box__wrap']/div[@class='item']", ".//a/@href", ".//a/text()", "//div[@class='b-topic__info']/time[@class='g-date']", "./@datetime", None, True, False, None)
get_news('https://news.mail.ru/', "//div[@name='clb20268335']//li[contains(@class,'list__item')] | //div[@name='clb20268335']//div[contains(@class,'daynews__item')]", "//a[contains(@class,'photo_full')]/@href | //a[@class='list__text']/@href", ".//span[contains(@class,'photo__title')]/text() | //a[@class='list__text']/text()", "//div[contains(@class,'breadcrumbs')]", "//@datetime", "//a[contains(@class,'breadcrumbs__link')]/@href", False, False, False)
get_news('https://yandex.ru/news/', "//div[contains(@class,'mg-grid__col_sm_9')]/div[position()=5]//article", ".//a/@href", ".//a/h2/text()", "//div[@class='news-story__head']", ".//span[@class='mg-card-source__time']/text()", "./a/@href", False, True, False)
for new in newsdb.find():
    pprint(new)
