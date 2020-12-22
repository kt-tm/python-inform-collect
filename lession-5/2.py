from selenium import webdriver
from pprint import pprint
from pymongo import MongoClient
import time
from selenium.webdriver.chrome.options import Options
import json

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
mvideodb = db.mvideo

def insert_uniq(data):
    if mvideodb.count_documents({'productId': data['productId']}) == 0:
        mvideodb.insert_one({
            "productPriceLocal": data['productPriceLocal'],
            "productId": data['productId'],
            "productName": data['productName'],
            "href": data['href']})
        return True
    else:
        return False

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

result = []
driver.get('https://www.mvideo.ru/')
count = int(json.loads(driver.find_element_by_xpath("//div[@class='section']//div[contains(@class,'gallery-content accessories-new ')]//ul[contains(@class,'accessories-product-list')]").get_attribute('data-init-param'))['ajaxContentLoad']['total'])
while True:
    time.sleep(3)
    elements = driver.find_elements_by_xpath("//div[contains(text(),'Хиты продаж')]/ancestor::div[@class='section']//div[contains(@class,'gallery-content accessories-new ')]//ul[contains(@class,'accessories-product-list')]/li/div/div/div/a")
    for elem in elements:
        data = {}
        data = json.loads(elem.get_attribute("data-product-info"))
        data['href'] = elem.get_attribute("href")
        insert_uniq(data)
        result.append(data['href'])
    result = list(set(result))
    if count == len(result):
        break
    button = driver.find_element_by_xpath("//div[contains(text(),'Хиты продаж')]/ancestor::div[@class='section']//div[contains(@class,'gallery-content accessories-new ')]//a[contains(@class, 'next-btn')]")
    button.click()
driver.close()

cntm = 0
for good in mvideodb.find():
    pprint(good)
    cntm+=1
print(f"cntm={cntm}")