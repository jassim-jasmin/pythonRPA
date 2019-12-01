#!/usr / bin / env python
from selenium import webdriver
import time
import json
import sys
import os
import re

# sys.path.insert(1,'browserOperationFunction')
# from basicOperations import BasicOptions

class FireFox():
    def __init__(self, path):
        try:
            self.path = path
        except Exception as e:
            print('FireFox !! ' + path['firefoxPath'] + ' !! has issue (minor)')

    def fireFox(self):
        try:
            self.browser = webdriver.Firefox(executable_path=self.path['firefoxPath']+'geckodriver')

            return True
        except Exception as e:
            error = str(e).strip()
            print(e)
            if error == 'Message: newSession':
                return 'newSessionError'
            elif re.search('needs to be in PATH',error):
                return 'pathError'
            else:
                return False

    def saveScreenshot(self, path, fileName):
        try:
            print('Image saving..', self.path[path]+fileName)
            try:
                os.mkdir(self.path[path])
            except Exception as e:
                print('Location ' + self.path[path] + ' already exist')

            self.browser.save_screenshot(self.path[path]+fileName)

            return True
        except Exception as e:
            print('Error with image loacation')
            self.browser.close()
            return False

    def openWebAddress(self, address):
        try:
            print('opening address ', address)
            self.browser = webdriver.Firefox(executable_path=self.path['firefoxPath'] + 'geckodriver')
            self.browser.get(address)
            if self.saveScreenshot('imageLocation','test.png'):
                self.browser.close()
                
                return True
            else:
                return False
        except Exception as e:
            print(e)
            self.browser.close()
            return False