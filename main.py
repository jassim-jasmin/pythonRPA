import json
import sys
import os

class MainRPA:
    def openFirefox(self, options):
        sys.path.insert(0, options['web']['firefox']['firefoxPath'])
        from firefoxWeb import FireFox

        return FireFox(options)

    def imageProcessing(self, options):
        try:
            os.chdir(options['imagProcessing']['path'])
            from imageProcessing import imageProcessing
            return True
        except Exception as e:
            print('error from imageProcessing', e)
            return False

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
        pathFile = open('path.json', 'r')
        path = json.loads(pathFile.read())
        pathFile.close()

        if len(sys.argv) == 4:
            if sys.argv[3] == 'rpa':
                if MainRPA.run(MainRPA, sys.argv[1], sys.argv[2], path):
                    print('Process complete')
            else:
                print('Process exit with error')
        elif len(sys.argv) == 3:
            print('imageProcessing', sys.argv)
            path = path[sys.argv[1]]
            if MainRPA.imageProcessing(MainRPA, path):
                print('image processing complete')
            else:
                print('image processing faild')
        else:
            print('Error: Proper argument need to run the program')
    except Exception as e:
        print(e)