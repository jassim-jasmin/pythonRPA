class GeneralExceptionHandling:
    def getFileData(self, fileNameWithPath):
        try:
            fp = open(fileNameWithPath, 'r')
            data = fp.read()
            fp.close()
            return data
        except Exception as e:
            print('error in getFileData in GeneralExceptionHandlig', e)
            return False

    def getJsonData(self, keyValue, jsonFileData):
        try:
            if jsonFileData:
                if keyValue in jsonFileData:
                    return jsonFileData[keyValue]
                else:
                    print('error in json \ninputkey:'+keyValue+'\njson:')
                    print(jsonFileData)
                    return False
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
                data = data.replace('$', '\$')
                data = data.replace('{', '\{')
                data = data.replace('}', '\}')

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
                data = data.replace('\$', '$')
                data = data.replace('\{', '{')
                data = data.replace('\}', '}')
                data = data.replace('\\\\', '\\')

                return data
            else:
                print('invalid flag in regularExpressionHandling')
                return False
        except Exception as e:
            print('error in regularExpressionHandling in GeneralExceptoinHandling', e)
            return False

    def getJsonDataRecurssive(self, keyValueWithComma, jsonFileData):
        try:
            keyValueArray = keyValueWithComma.split(',')

            for keyValue in keyValueArray:
                print(keyValue)
                if jsonFileData:
                    if keyValue in jsonFileData:
                        jsonFileData = jsonFileData[keyValue]
                    else:
                        print('error in json \ninputkey:' + keyValue + '\njson:')
                        print(jsonFileData)
                        return False
                else:
                    return False

            return jsonFileData

        except Exception as e:
            print('error in getJsonDataRecurssive in GeneralExceptionHandling', e)
            return False