#!/usr / bin / env python
from selenium import webdriver
import time

browser = webdriver.Firefox(executable_path="/root/Documents/mj/python/rpaPython/venv/geckodriver")
website_URL ='https://www.zomato.com/ncr'
browser.get(website_URL)

time.sleep(3)

username = "test"
password = "test"

# signin element clicked
browser.find_element_by_xpath("//a[@id ='signin-link']").click()
time.sleep(2)

# Login clicked
browser.find_element_by_xpath("//a[@id ='login-email']").click()

# username send
a = browser.find_element_by_xpath("//input[@id ='ld-email']")
a.send_keys(username)

# password send
b = browser.find_element_by_xpath("//input[@id ='ld-password']")
b.send_keys(password)

# submit button clicked
browser.find_element_by_xpath("//input[@id ='ld-submit-global']").click()

print('Login Successful')
browser.close()