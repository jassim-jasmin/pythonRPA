import json
import sys
import os

from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class MainRPA:

    def openFirefox(self, options):
        try:
            from web.Firefox.firefoxWeb import FireFox

            return FireFox(options)
        except Exception as e:
            print('error in mainRPA in main', e)
            return False

    def imageProcessing(self, options, imageName):
        try:
            from imageProcessing.imageProcessing import ImageProcessing

            imageProcessingObj =  ImageProcessing()

            imageLocation = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'imageLocation', options)

            if imageLocation:
                openCvImage= imageProcessingObj.openCVReadImage(imageLocation, imageName)
                contors = imageProcessingObj.getContours(imageProcessingObj.openCVReadImage(imageLocation, imageName))
                if imageProcessingObj.drawContours(openCvImage,contors):
                    return True
                else:
                    return False
            else:
                print('json error image location')
                return False
        except Exception as e:
            print('error from imageProcessing', e)
            return False

    def run(self, os, option, path, address='https://cityofmidlandmi.gov/275/Parcel-Identification-Numbers', imageName='apn'):
        try:
            print('Oppening RPA')
            self.runCount = 1
            self.os = os
            self.path = path[os]

            if option == 'firefox':
                print('FireFox enabling')
                firefoxObj = self.openFirefox(self, self.path)

                if firefoxObj:
                    if firefoxObj.openWebAddress(address, self.runCount):
                        if firefoxObj.saveScreenshot('imageLocation', imageName + '.tif'):
                            firefoxObj.browser.close()
                        return True
                    else:
                        print('process failed')
                else:
                    print('error opening firefox')
                    return False
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
            if sys.argv[2] == 'imageProcessing':
                print('imageProcessing', sys.argv)
                # path = path[sys.argv[1]]
                path = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, sys.argv[1], path)

                if path:
                    if MainRPA.imageProcessing(MainRPA, path, 'geek'):
                        print('image processing complete')
                    else:
                        print('image processing faild')
                else:
                    exit()
            elif sys.argv[2] == 'dataFetching':
                try:
                    from DataFetching.DataFetching import DataFetchingMain

                    pathValues = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, sys.argv[1], path)
                    if pathValues:
                        df = DataFetchingMain(pathValues)
                        df.imageDataProcessing()
                        # from DataFetching.StringHandling import StringHandling

                    else:
                        exit()
                except Exception as e:
                    print('error in dataFetching in main', e)
            elif sys.argv[2] == 'test':
                try:
                    from DataFetching.test import *
                except Exception as e:
                    print('error in test main in main', e)

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
        print('error in main', e)

"""
    python3 main.py linux dataFetching
    python3 main.py linux   (works based on process file)
    python3 main.py linux imageProcessing
    python3 main.py linux firefox rpa
"""