import json
import sys

def fireFOx(options):
    try:
        print(options['firefox']['firefoxPath'])
        try:
            sys.path.insert(0, options['firefox']['firefoxPath'])
            from firefoxWeb import FireFox

            firefox = FireFox(options['firefox'])
            firefox.fireFox()
        except Exception as e:
            print('Exception in mian/firefox opening firefox ', e)

        return True
    except Exception as e:
        print('Exception in main/firefox ', e)

        return False

def run(options):
    try:
        print('Oppening RPA')
        path = json.loads(open('path.json').read())[options]
        print(path)

        if fireFOx(path['web']):
            print('FireFox enabling')
        else:
            print('FireFox failed')


        return True
    except Exception as e:
        print('Exception in main/run', e)

        return False

if __name__ == '__main__':
    option = 'windows'
    run(option)