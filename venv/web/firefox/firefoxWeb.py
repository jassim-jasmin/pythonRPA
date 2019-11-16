#!/usr / bin / env python
from selenium import webdriver
import time
import json
import sys
import os

# sys.path.insert(1,'browserOperationFunction')
# from basicOperations import BasicOptions

class FireFox():
    def __init__(self, path):
        try:
            self.path = path
            os.chdir(path['firefoxPath'])
        except Exception as e:
            print('FireFox !! ' + path['firefoxPath'] + ' !! has issue (minor)')

    def fireFox(self):
        try:
            self.browser = webdriver.Firefox(executable_path=self.path['geckodriver']+'geckodriver')

            return True
        except Exception as e:
            error = str(e).strip()
            if error == 'Message: newSession':
                return 'newSessionError'
            else:
                print('browser error :', e)
                return False

# print(os.getcwd())
# test = webdriver.Firefox(executable_path='/root/Documents/mj/python/rpaPython/venv/web/firefox/geckodriver')
# test.get("https://stackoverflow.com")