from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pprint import pprint
from pymongo import MongoClient
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


client = MongoClient('127.0.0.1', 27017)
db = client['mail']
maildb = db.mail

def insert_uniq(data):
    if maildb.count_documents({'theme': data['theme'], 'sender': data['sender'], 'date': data['date']}) == 0:
        maildb.insert_one({
            "theme": data['theme'],
            "sender": data['sender'],
            "date": data['date'],
            "body": data['body']})
        return True
    else:
        return False

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://mail.ru/')


elem = driver.find_element_by_name('login')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

time.sleep(1)
elem = driver.find_element_by_name('password')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.ENTER)
cnt = 0
links = []
print(f"cnt={cnt}")
last_elem = None
pr_break = None
while True:
    time.sleep(4)
    elements = driver.find_elements_by_class_name('llc')
    if last_elem == elements[-1].get_attribute('href'):
        break
    for elem in elements:
        link = elem.get_attribute('href')
        last_elem = elem.get_attribute('href')
        links.append(link)
        cnt += 1
    actions = ActionChains(driver)
    actions.move_to_element(elements[-1])
    actions.perform()
print(f"cnt={cnt}")
links = list(set(links))

for l in links:
    print(l)
    driver.get(l)
    time.sleep(5)
    data = {}
    data['theme'] = driver.find_element_by_class_name('thread__subject').text
    data['sender'] = driver.find_element_by_class_name('letter__author').text
    data['date'] = driver.find_element_by_class_name('letter__date').text
    data['body'] = driver.find_element_by_class_name('letter-body').text
    print(insert_uniq(data))
driver.close()



cntm = 0
for mail in maildb.find():
    pprint(mail)
    cntm+=1
print(f"cntm={cntm}")
