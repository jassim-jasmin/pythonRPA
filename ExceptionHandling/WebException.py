import os
import wget
import re

class ExceptionHandling:
    def geckodriverException(self, path):
        try:
            # os.chdir(path['web']['Firefox']['firefoxPath'])
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
            os.system(path['delCommand']+ path['web']['firefox']['firefoxPath'] +'geckodriver*')
        except Exception as e:
            print(e)

        try:
            wget.download(path['web']['firefox']['geckodriver']['geckodriverDownloadPath'],out=path['web']['firefox']['firefoxPath'])
        except Exception as e:
            print(e, 'wget error')
            return False

        try:
            files = os.listdir(path['web']['firefox']['firefoxPath'])
            for file in files:
                if re.search('geckodriver', file):
                    geckoDriver = file
                    break

            if geckoDriver:
                try:
                    os.system(path['unzip'] + path['web']['firefox']['firefoxPath'] + path['unzipOption'] + path['web']['firefox']['firefoxPath'] + geckoDriver)
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                return False
        except Exception as e:
            print(e)
            return False