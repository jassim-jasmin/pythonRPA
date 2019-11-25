import json
import sys
import os
class MainRPA:
    def openFirefox(self, options):
        print('firefox')
        sys.path.insert(0, options['firefox']['firefoxPath'])
        from firefoxWeb import FireFox

        return FireFox(options['firefox'])

    def fireFOx(self, options):
        try:
            try:
                firefoxObj = self.openFirefox(self, options)
                firefox = firefoxObj.fireFox()
                if firefox:
                    if (firefox == 'pathError' or firefox == 'newSessionError') and self.runCount == 1:
                        if self.webException(self, 'geckodriverException'):
                            print('Opening Fire Fox')
                            self.runCount = self.runCount + 1
                            self.fireFOx(self, options)

                        else:
                            return False
                    elif firefox == 'pathError' or firefox == 'pathError':
                        exit()
                    else:
                        print('FireFox openning success')
                        try:
                            firefoxObj.browser.close()
                            return True
                        except Exception as e:
                            print(e)
                            return False
                else:
                    print('FireFox opening error')
                    return False

            except Exception as e:
                print('Exception in mian/firefox opening firefox ', e)

            return True
        except Exception as e:
            print('Exception in main/firefox ', e)

            return False

    def webException(self, option):
        if option == 'geckodriverException':
            try:
                os.chdir(os.getcwd().replace(self.path['web']['firefox']['firefoxPath'], ''))
                sys.path.insert(1,'ExceptionHandling')
                from webException import ExceptionHandling

                exceptionHandling = ExceptionHandling()
                if exceptionHandling.geckodriverException(self.path):
                    return True
                else:
                    return False
            except Exception as e:
                print('class ExceptionHandling has issue', e)
        else:
            print('Exception not handling and exiting')
            return False

    def run(self, options, path):
        try:
            print('Oppening RPA')
            self.runCount = 1
            self.os = options
            self.path = path[options]

            if self.fireFOx(self, self.path['web']):
                print('FireFox enabling')
                return True
            else:
                print('FireFox failed')
                return True

        except Exception as e:
            print('Exception in main/run (json file issue)', e)

            return False

if __name__ == '__main__':
    try:
        pathFile = open('path.json', 'r')
        path = json.loads(pathFile.read())
        pathFile.close()
        if MainRPA.run(MainRPA, sys.argv[1], path):
            print('Process complete')
        else:
            print('Process exit with error')
    except Exception as e:
        print(e)