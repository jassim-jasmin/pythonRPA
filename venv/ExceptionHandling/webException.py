import os
import wget
import re

class ExceptionHandling:
    def geckodriverException(self, path):
        try:
            os.chdir(path['web']['firefox']['firefoxPath'])
            if self.installGeckodriver(path):
                print('geckodriver installation complete')
                return True
            else:
                print('installation failed')
                return False
        except Exception as e:
            print(e)
            return False
        # print('geckodriverException')
        # print('wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip')
        # print('rm geckodriver')
        # print('tar -xvzf geckodriver-v0.20.0-linux64.tar.gz')


    def installGeckodriver(self, path):
        print('windows geckodriver installing')
        #
        try:
            os.system(path['delCommand']+'geckodriver*')
        except Exception as e:
            print('cant delete')
        wget.download('https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip')
        # os.system('cmd /c tar -xf geckodriver*')
        files = os.listdir()
        for file in files:
            if re.search('geckodriver', file):
                geckoDriver = file
                break

        if geckoDriver:
            try:
                print(geckoDriver)
                os.system(path['unzip'] + geckoDriver)
                return True
            except Exception as e:
                return False
        else:
            return False
        # print('path',os.getcwd())