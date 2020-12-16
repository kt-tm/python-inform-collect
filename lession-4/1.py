import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

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

def get_news(url, xpath_gen, xpath_link, xpath_name, xpath_date_gen, xpath_date, xpath_source, pr_source):
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)
    items = dom.xpath(xpath_gen)
    news = []
    for item in items:
        new = {}
        source = url
        link = item.xpath(xpath_link)
        name = item.xpath(xpath_name)
        print(link)
        new['link'] = url + link[0].replace(url, '')
        new['name'] = name[0]

        response_date = requests.get(new['link'], headers=header)
        dom_date = html.fromstring(response_date.text)
        items_date = dom_date.xpath(xpath_date_gen)
        for item_date in items_date:
            date = item_date.xpath(xpath_date)
            if not pr_source:
                source = item_date.xpath(xpath_source)
        new['date'] = date[0]
        new['source'] = source
        news.append(new)
        # insert_uniq(new)
    # for new in newsdb.find():
    #     pprint(new)
    pprint(news)

# get_news('https://lenta.ru/', "//div[@class='b-yellow-box__wrap']/div[@class='item']", ".//a/@href", ".//a/text()", "//div[@class='b-topic__info']/time[@class='g-date']", "./@datetime", None, True)
get_news('https://news.mail.ru/', "//div[@name='clb20268335']//a[contains(@class,'photo_full')]", "//div[@name='clb20268335']//a[contains(@class,'photo_full')]//a/@href", ".//span[contains(@class,'photo__title')]/text()", "//div[contains(@class,'breadcrumbs')]", "./@datetime", "//div[contains(@class,'breadcrumbs')]//a/@href", True)