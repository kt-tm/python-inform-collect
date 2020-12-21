from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pprint import pprint
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json



chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

result = []
driver.get('https://www.mvideo.ru/')
# elem = driver.find_element_by_xpath("//div[@class='section']//div[contains(@class,'gallery-content accessories-new ')]")
# print(elem.text)
cnt = 0
count = int(json.loads(driver.find_element_by_xpath("//div[@class='section']//div[contains(@class,'gallery-content accessories-new ')]//ul[contains(@class,'accessories-product-list')]").get_attribute('data-init-param'))['ajaxContentLoad']['total'])
# print(count)
while count >= 0:
    count-=1
    elements = driver.find_elements_by_xpath("//div[@class='section']//div[contains(@class,'gallery-content accessories-new ')]//ul[contains(@class,'accessories-product-list')]//li//a")
    for elem in elements:
        data = {}
        print(elem.text)
        data = elem.get_attribute("data-product-info")
        print(data)
        # data = elem.get_attribute("data-product-info")
        result.append(data)
        cnt += 1
        print(f"cnt={cnt}")
    print(f"cnt2={cnt}")
    # print(result)
    # print(count)
    button = driver.find_element_by_class_name("//div[@class='section']//div[contains(@class,'gallery-content accessories-new ')]//a[contains(@class, 'next-btn')]")
    button.click()

# pprint(result)
# //div[@class='u-mb-12 u-mt-24 gallery-layout__title-block']
# //ul[contains(@class,'accessories-product-list')]
driver.close()