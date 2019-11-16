import json
import sys
import os

def fireFOx(options):
    try:
        print(options['firefox']['firefoxPath'])
        try:
            sys.path.insert(0, options['firefox']['firefoxPath'])
            from firefoxWeb import FireFox

            firefox = FireFox(options['firefox']).fireFox()
            if firefox:
                if firefox == 'newSessionError':
                    webException('geckodriverException')
                else:
                    print('FireFox openning success')
            else:
                print('FireFox opening error')

        except Exception as e:
            print('Exception in mian/firefox opening firefox ', e)

        return True
    except Exception as e:
        print('Exception in main/firefox ', e)

        return False

def webException(option):
    if option == 'geckodriverException':
        try:
            os.chdir(os.getcwd().replace('/web/firefox', ''))
            sys.path.insert(1,'ExceptionHandling')
            from webException import ExceptionHandling

            ExceptionHandling().geckodriverException()
        except Exception as e:
            print('class ExceptionHandling has issue', e)
    else:
        print('Exception not handling and exiting')
        return False

def run(options):
    try:
        print('Oppening RPA')
        path = json.loads(open('path.json').read())[options]

        if fireFOx(path['web']):
            print('FireFox enabling')
            return True
        else:
            print('FireFox failed')
            return True

    except Exception as e:
        print('Exception in main/run (json file issue)', e)

        return False

if __name__ == '__main__':
    if run(sys.argv[1]):
        print('Process complete')
    else:
        print('Process exit with error')