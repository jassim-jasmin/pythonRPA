import json
from main import MainRPA
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class Automation:
    def processLine(self, process):
        for key, action in process.items():
            # print(key)
            if key == 'web':
                for eachAction in action:
                    if not self.automateFirefox(eachAction):
                        return False
            elif key == 'imageProcessing':
                for eachAction in action:
                    if not self.automateImageProcessing(eachAction):
                        return False
            elif key == 'ocr':
                for eachAction in action:
                    if not self.automateOcrProcess(eachAction):
                        return False
        return True

    def automateOcrProcess(self, values):
        from imageProcessing.imageProcessing import ImageProcessing

        for imageName, imageExtension, ocrDocumentName, filePath in values:
            if not ImageProcessing.ocrImage(ImageProcessing, imageName,imageExtension, ocrDocumentName, filePath):
                return False

    def automateFirefox(self, values):
        try:
            path = self.openPathFile()

            openValue = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'open', values)
            if openValue:
                if len(openValue) >3:
                    if MainRPA.run(MainRPA, openValue[0], openValue[1], path, openValue[2], openValue[3]):
                        print('image processing complete')
                        return True
                    else:
                        print('image processing faild')
                        return False
                else:
                    print('open  array size should be 4', values)
                    return False
            else:
                print('json error in automateFirefox in automation')
                return False
        except Exception as e:
            print('error in auromatefirefox')

    def automateImageProcessing(self, eachAction):
        try:
            path = self.openPathFile()
            eachActionValue = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'open', eachAction)

            if eachActionValue:
                if len(eachActionValue)>1:
                    pathValue = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling
                                                                 , eachActionValue[0], path)
                    if pathValue:
                        if MainRPA.imageProcessing(MainRPA, pathValue, eachActionValue[1]):
                            print('image processing complete')
                            return True
                        else:
                            print('image processing faild')
                        return False
                    else:
                        print('json error in automateImageProcessing')

                        return False
                else:
                    print('error in array size in automateImageProcessing greater than 1', eachActionValue)
            else:
                print('json error in automateImageProcessing')
                return False
        except Exception as e:
            print('error in automateImageProcessing', e)
            return False

    def automate(self, option):
        try:
            processFile = open('process.json', 'r')
            # process = json.loads(processFile.read())[option]
            process = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, option, json.loads(processFile.read()))
            processFile.close()

            if process:
                for eachProcessLine in process:
                    if not self.processLine(eachProcessLine):
                        return False
                return True
            else:
                print('json error in automate in automation')
                return False
        except Exception as e:
            print('error in automate', e)
            return False

    def openPathFile(self):
        pathFile = open('path.json', 'r')
        path = json.loads(pathFile.read())
        pathFile.close()
        return path

