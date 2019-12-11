import json
import sys
import os

class MainRPA:
    def openFirefox(self, options):
        sys.path.insert(0, options['web']['firefox']['firefoxPath'])
        from firefoxWeb import FireFox

        return FireFox(options)

    def imageProcessing(self, options, imageName):
        try:
            # print(os.getcwd())
            # print('image prcessing',options['imagProcessing']['path'])
            # os.chdir(options['imagProcessing']['path'])
            # print(os.getcwd())
            from imageProcessing.imageProcessing import ImageProcessing
            # from imageProcessing import ImageProcessing
            # from imageProcessing import ImageProcessing

            imageProcessingObj =  ImageProcessing()

            imageProcessingObj.drawContours(imageProcessingObj.openCVReadImage(options['imageLocation'],imageName), imageProcessingObj.getContours(imageProcessingObj.openCVReadImage(options['imageLocation'],imageName)))
            return True
        except Exception as e:
            print('error from imageProcessing', e)
            return False

    def run(self, os, option, path, address='http://www.google.com', imageName='google'):
        try:
            print('Oppening RPA')
            self.runCount = 1
            self.os = os
            self.path = path[os]

            if option == 'firefox':
                print('FireFox enabling')
                firefoxObj = self.openFirefox(self, self.path)

                if firefoxObj.openWebAddress(address, self.runCount):
                    firefoxObj.saveScreenshot('imageLocation', imageName + '.png')
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
                if MainRPA.run(MainRPA, sys.argv[1], sys.argv[2], path[sys.argv[1]]):
                    print('Process complete')
            else:
                print('Process exit with error')
        elif len(sys.argv) == 3:
            print('imageProcessing', sys.argv)
            path = path[sys.argv[1]]
            if MainRPA.imageProcessing(MainRPA, path, 'geek'):
                print('image processing complete')
            else:
                print('image processing faild')
        elif len(sys.argv) == 2:
            from automation.automation import Automation

            automation = Automation()
            if automation.automate(sys.argv[1]):
                print('completed')
            else:
                print('failed')
        else:
            print('Error: Proper argument need to run the program')
    except Exception as e:
        print(e)