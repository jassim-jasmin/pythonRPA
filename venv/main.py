import json
import sys
import os

class MainRPA:
    def openFirefox(self, options):
        sys.path.insert(0, options['web']['firefox']['firefoxPath'])
        from firefoxWeb import FireFox

        return FireFox(options)

    def run(self, os, option, path):
        try:
            print('Oppening RPA')
            self.runCount = 1
            self.os = os
            self.path = path[os]

            if option == 'firefox':
                print('FireFox enabling')
                firefoxObj = self.openFirefox(self, self.path)

                if firefoxObj.openWebAddress('http://www.google.com', self.runCount):
                    firefoxObj.saveScreenshot('imageLocation', 'test.png')
                    firefoxObj.browser.close()
                    return True
                else:
                    print('process failed')
            else:
                print('Invalid browser option')
                return False

        except Exception as e:
            print('Exception in main/run (json file issue)', e)

            return False

if __name__ == '__main__':
    try:
        if len(sys.argv) == 3:
            pathFile = open('path.json', 'r')
            path = json.loads(pathFile.read())
            pathFile.close()

            if MainRPA.run(MainRPA, sys.argv[1], sys.argv[2], path):
                print('Process complete')
            else:
                print('Process exit with error')
        else:
            print('Error: Proper argument need to run the program')
    except Exception as e:
        print(e)