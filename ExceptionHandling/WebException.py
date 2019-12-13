import os
import wget
import re

class ExceptionHandling:
    def geckodriverException(self, path):
        try:
            os.chdir(path['web']['Firefox']['firefoxPath'])
            if self.installGeckodriver(path):
                print('geckodriver downloaded')
                return True
            else:
                print('Failed geckodriver downloading')
                return False
        except Exception as e:
            print(e)
            return False

    def installGeckodriver(self, path):
        print('geckodriver downloading...')
        #
        try:
            os.system(path['delCommand']+'geckodriver*')
        except Exception as e:
            print(e)

        try:
            wget.download(path['web']['Firefox']['geckodriver']['geckodriverDownloadPath'])
        except Exception as e:
            print(e, 'wget error')
            return False

        try:
            files = os.listdir()
            for file in files:
                if re.search('geckodriver', file):
                    geckoDriver = file
                    break

            if geckoDriver:
                try:
                    print(geckoDriver)
                    os.system(path['unzip'] + geckoDriver)
                    os.chdir('..')
                    os.chdir('..')
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                return False
        except Exception as e:
            print(e)
            return False