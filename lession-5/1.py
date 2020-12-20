from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pprint import pprint
from pymongo import MongoClient
import time
from selenium.webdriver.chrome.options import Options
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
cnt_mail_page = 0
print(1)
time.sleep(10)
while cnt < 15:
    print(f"cnt={cnt}")
    elements = driver.find_elements_by_class_name('llc')
    actions = ActionChains(driver)
    actions.move_to_element(elements[-1])
    actions.perform()
    cnt_mail_page = 0
    print('perform')
    time.sleep(3)

    print(elements[cnt].text)
    elements[cnt].click()
    data = {}
    time.sleep(10)
    data['theme'] = driver.find_element_by_class_name('thread__subject').text
    data['sender'] = driver.find_element_by_class_name('letter__author').text
    data['date'] = driver.find_element_by_class_name('letter__date').text
    data['body'] = driver.find_element_by_class_name('letter-body').text
    print(insert_uniq(data))
    print('end')
    driver.back()
    cnt += 1
    cnt_mail_page += 1
    time.sleep(3)


driver.close()

for mail in maildb.find():
    pprint(mail)
