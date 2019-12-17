class GeneralExceptionHandling:
    def getJsonData(self, keyValue, jsonFileData):
        try:
            if keyValue not in jsonFileData:
                print('json key ' + keyValue + ' not in ', jsonFileData)
                return False
            else:
                return jsonFileData[keyValue]
        except Exception as e:
            print('error in jsonFileHandling in GeneralExceptionHandling', e)
            return False

    def regularExpressionHandling(self, data, flag):
        try:
            if flag == 0:
                data = data.replace('\\', '\\\\')
                data = data.replace('(', '\(')
                data = data.replace(')', '\)')
                data = data.replace('.', '\.')
                data = data.replace('+', '\+')
                data = data.replace('[', '\[')
                data = data.replace(']', '\]')
                data = data.replace('|', '\|')
                data = data.replace('/', '\/')
                data = data.replace('?', '\?')
                data = data.replace('"', '\\"')
                data = data.replace('*', '\*')

                return data
            if flag == 1:
                data = data.replace('\(', '(')
                data = data.replace('\)', ')')
                data = data.replace('\.', '.')
                data = data.replace('\+', '+')
                data = data.replace('\[', '[')
                data = data.replace('\]', ']')
                data = data.replace('\|','|')
                data = data.replace('\/', '/')
                data = data.replace('\?','?')
                data = data.replace('\\"', '"')
                data = data.replace('\*', '*')
                data = data.replace('\\\\', '\\')

                return data
            else:
                print('invalid flag in regularExpressionHandling')
                return False
        except Exception as e:
            print('error in regularExpressionHandling in GeneralExceptoinHandling', e)
            return False