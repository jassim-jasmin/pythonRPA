#!/usr / bin / env python
from selenium import webdriver
import time
import json
import sys
import os
import re

class FireFox():
    def __init__(self, path):
        try:
            self.path = path
        except Exception as e:
            print('FireFox !! ' + path['firefoxPath'] + ' !! has issue (minor)')

    def fireFox(self):
        try:
            self.browser = webdriver.Firefox(executable_path=self.path['web']['firefox']['firefoxPath']+'geckodriver')

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

    def saveScreenshot(self, imageLocation, fileName):
        try:
            print('Image saving..', self.path[imageLocation]+fileName)
            try:
                os.mkdir(self.path[imageLocation])
            except Exception as e:
                print('Location "' + self.path[imageLocation] + '" already exist')

            try:
                self.browser.save_screenshot(self.path[imageLocation]+fileName)
            except Exception as e:
                print(e)

            return True
        except Exception as e:
            print('Error with image loacation\n', self.path, path)
            self.browser.close()
            return False

    def openWebAddress(self, address, runCount):
        try:
            print('opening address ', address)
            self.browser = webdriver.Firefox(executable_path=self.path['web']['firefox']['firefoxPath'] + 'geckodriver')
            self.browser.get(address)

            return True
        except Exception as e:
            try:
                self.browser.close()
            except Exception as e:
                print('clossing browser', e)
            if self.testFireFOx(self.path, runCount):
                return self.openWebAddress(address, runCount+1)


    def testFireFOx(self, options, runCount):
        try:
            self.path = options
            self.runCount = runCount
            try:
                firefox = self.fireFox()
                if firefox:
                    if (firefox == 'pathError' or firefox == 'newSessionError') and self.runCount == 1:
                        if self.webException('geckodriverException'):
                            print('Opening Fire Fox')
                            self.runCount = self.runCount + 1
                            # self.fireFOx(self, options)
                            return True

                        else:
                            return False
                    elif firefox == 'pathError' or firefox == 'pathError':
                        exit()
                    else:
                        print('FireFox openning success')
                        try:
                            self.browser.close()
                            return True
                        except Exception as e:
                            print('FireFox openning failed: ',e)
                            return False
                else:
                    print('FireFox opening error')
                    return False

            except Exception as e:
                print('Exception in firefoxWeb/testFirefox opening firefox ', e)
        except Exception as e:
            print('Exception in main/firefox ', e)

            return False

    def webException(self, option):
        if option == 'geckodriverException':
            try:
                sys.path.insert(1,'ExceptionHandling')
                from webException import ExceptionHandling

                exceptionHandling = ExceptionHandling()
                if exceptionHandling.geckodriverException(self.path):
                    print('web handled')
                    return True
                else:
                    return False
            except Exception as e:
                print('class ExceptionHandling has issue', e)
        else:
            print('Exception not handling and exiting')
            return False