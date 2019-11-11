#!/usr / bin / env python
from selenium import webdriver
import time
import json
import sys
# sys.path.insert(1,'browserOperationFunction')
# from basicOperations import BasicOptions

class FireFox():
    def __init__(self, workingDirectory):
        print('fire fox constructor called', workingDirectory)
        sys.path(workingDirectory['firefoxPath'])

    def fireFox(self):
        browser = webdriver.Firefox(executable_path='geckodriver.exe')

        browser.get('http://www.google.com')

        browser.close()
