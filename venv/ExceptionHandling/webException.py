import os

class ExceptionHandling:
    def geckodriverException(self, path, option):
        self.path = path
        # print('geckodriverException')
        # print('wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip')
        # print('rm geckodriver')
        # print('tar -xvzf geckodriver-v0.20.0-linux64.tar.gz')
        self.installGeckodriver(option)

    def installGeckodriver(self, option):
        if option == 'windows':
            para = """echo jassim
            echo jasmin
            echo test"""
            print('windows geckodriver installing')
            os.system('cmd /c '+para)
            print('path',os.getcwd())