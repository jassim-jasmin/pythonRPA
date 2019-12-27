import os
import json

class GeneralExceptionHandling:
    def getFileData(self, fileNameWithPath):
        """
        :argument fileNameWithPath is coplete file name extension with path
        :returns file data :returns false if file is empty"""
        try:
            fp = open(fileNameWithPath, 'r')
            data = fp.read()
            fp.flush()
            fp.close()
            if os.stat(fileNameWithPath).st_size == 0:
                return False
            else:
                return data
        except Exception as e:
            print('error in getFileData in GeneralExceptionHandlig', e)
            return False

    def getJsonData(self, keyValue, jsonFileData):
        """Check key available in a dictionary :returns dictionary value if available else :returns False"""
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
        """
        Convert special characters for processing regualar expression
        :var flag is for selecting conversion
        :arg flag = 0 for conversion
        :arg self = 1 for undo the conversion
        """
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
        """:argument keyValueWithComma is json key with coma seperated
        key value itrate over json data and final out put returns
        :returns value if all key values are available in json else False"""
        try:
            keyValueArray = keyValueWithComma.split(',')

            for keyValue in keyValueArray:
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

    def removeArrayDuplicate(self, array):
        """General way of removing duplicate entry from array :returns distinct array elements"""
        try:
            seen = set()

            array[:] = [item for item in array
                                  if item not in seen and not seen.add(item)]
            return array
        except Exception as e:
            print('error in removeArrayDuplicate', e)
            return False

    def returnsDictionaryFromString(self, data):
        try:
            if data:
                return json.loads(data)
            else:
                return False
        except Exception as e:
            print('error in returnsDictionaryFromString in GeneralExceptionHandling', e)
            return False

    def readFileAndReturnJson(self, fileNameWithPath):
        try:
            if fileNameWithPath:

                return self.returnsDictionaryFromString(self.getFileData(fileNameWithPath))
            else:
                print('error json file name with path is error')
                return False
        except Exception as e:
            print('error in readFileAndReturnJson in GeneralExceptionHandling', e)
            return False

    def writeJsonDataToFile(self, data, nameWithPath):
        try:
            fp = open(nameWithPath, 'w')
            fp.write(json.dumps(data))
            fp.flush()
            fp.close()

            return True
        except Exception as e:
            print('error in writeJsonDataToFile in GeneralExceptionHandling', e)
            return False
        finally:
            try:
                fp.close()
            except Exception as e:
                pass
