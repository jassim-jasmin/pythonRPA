import json
from main import MainRPA

class Automation:
    def automateFirefox(self, values):
        try:
            path = self.openPathFile()

            if MainRPA.run(MainRPA, values['open'][0], values['open'][1], path, values['open'][2], values['open'][3]):
                print('image processing complete')
            else:
                print('image processing faild')
        except Exception as e:
            print('error in auromatefirefox')

    def automateImageProcessing(self, eachAction):
        try:
            print(eachAction)
            path = self.openPathFile()
            path = path[eachAction['open'][0]]
            if MainRPA.imageProcessing(MainRPA, path, eachAction['open'][1]):
                print('image processing complete')
            else:
                print('image processing faild')
            return True
        except Exception as e:
            print('error in automateImageProcessing', e)
            return False

    def processLine(self, process):
        for key, action in process.items():
            # print(key)
            if key == 'web':
                for eachAction in action:
                    self.automateFirefox(eachAction)
            elif key == 'imageProcessing':
                for eachAction in action:
                    self.automateImageProcessing(eachAction)

    def automate(self, option):
        try:
            processFile = open('process.json', 'r')
            process = json.loads(processFile.read())[option]
            processFile.close()

            for eachProcessLine in process:
                self.processLine(eachProcessLine)
            return True
        except Exception as e:
            print('error in automate', e)
            return False

    def openPathFile(self):
        pathFile = open('path.json', 'r')
        path = json.loads(pathFile.read())
        pathFile.close()
        return path