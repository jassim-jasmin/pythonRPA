import json
import sys
import os
class MainRPA:
    def openFirefox(self, options):
        sys.path.insert(0, options['firefox']['firefoxPath'])
        from firefoxWeb import FireFox

        return FireFox(options['firefox'])

    def run(self, os, option, path):
        try:
            print('Oppening RPA')
            self.runCount = 1
            self.os = os
            self.path = path[os]

            if option == 'firefox':
                if self.openFirefox(self, self.path['web']).testFireFOx(self.path, self.runCount):
                    print('FireFox enabling')

                    firefoxObj = self.openFirefox(self, self.path['web'])
                    if firefoxObj.openWebAddress('http://www.google.com'):
                        return True
                    else:
                        print('process failed')
                else:
                    print('FireFox failed')
                    return True
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