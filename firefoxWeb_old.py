#!/usr / bin / env python
from selenium import webdriver
import time
import json
import sys
sys.path.insert(1,'browserOperationFunction')
from basicOperations import BasicOptions

def buttonClick(butonId):
    browser.find_element_by_xpath("//button[@id ='"+butonId+"']").click()

def findInputAndInsert(fieldIdName, inputValue):
    a = browser.find_element_by_xpath("//input[@id ='" + fieldIdName + "']")
    a.send_keys(inputValue)

def loginAdmin(data):
    findInputAndInsert('username','admin')
    findInputAndInsert(data['userName'], data['password'])
    buttonClick('login')

def custom():
    try:
        browser.find_element_by_xpath("//img[@id ='lu_map']")
        return True
    except Exception as e:
        print(e, 'in BasicOptions custom')
    return False

basicData = json.loads(open('PageData/basicData.json','r').read())['profile1']

# browser = webdriver.Firefox(executable_path=basicData['executable_path'])
browser = webdriver.Firefox(executable_path='geckodriver.exe')
# website_URL ='https://www.zomato.com/ncr'
# website_URL = 'http://localhost:4200/'
browser.get('http://www.google.com')
# browser.get('https://www.google.com/search?client=ubuntu&channel=fs&q=tree&ie=utf-8&oe=utf-8')


# browser.get(BasicOptions.searchGoogle(BasicOptions, '10976 LABRADOR AVE'))
# if custom():
#     print('address')
# else:
#     print('not an address')

browser.close()
# time.sleep(3)
# loginAdmin(basicData)
# time.sleep(3)




# username = "Test"
# password = "Test"
#
# # signin element clicked
# browser.find_element_by_xpath("//a[@id ='signin-link']").click()
# time.sleep(2)
#
# # Login clicked
# browser.find_element_by_xpath("//a[@id ='login-email']").click()
#
# # username send
# a = browser.find_element_by_xpath("//input[@id ='ld-email']")
# a.send_keys(username)
#
# # password send
# b = browser.find_element_by_xpath("//input[@id ='ld-password']")
# b.send_keys(password)
#
# # submit button clicked
# browser.find_element_by_xpath("//input[@id ='ld-submit-global']").click()
#
# print('Login Successful')
# browser.close()