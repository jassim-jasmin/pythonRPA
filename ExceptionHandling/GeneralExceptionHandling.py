import os
import json

class GeneralExceptionHandling:
    def fileStatus(self, fileNameWithPath):
        """ For checking file is empty or not """
        try:
            fp = open(fileNameWithPath, 'r')
            if os.stat(fileNameWithPath).st_size == 0:
                fp.flush()
                fp.close()
                return False
            fp.flush()
            fp.close()
            return True
        except Exception as e:
            return False

    def getFileData(self, fileNameWithPath):
        """

        :param fileNameWithPath: coplete file name extension with path
        :return: file data :returns false if file is empty
        """
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
        """
        Check key available in a dictionary
        :param keyValue: json key
        :param jsonFileData: json data
        :return: dictionary value if available else :returns False
        """
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
        :param data:
        :param flag: selecting conversion, 0 for conversion, 1 for undo the conversion
        :return: data based on flag, False if error occured
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
        """
        key value itrate over json data and final out put returns
        :param keyValueWithComma: json key with coma seperated
        :param jsonFileData: key value pair json
        :return: value if all key values are available in json else False
        """
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
        """
        General way of removing duplicate entry from array
        :param array: array with elements
        :return: distinct array elements
        """
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
        """
        Read text from file and returns as json
        :param fileNameWithPath: file which is going to convert
        :return: json data, if error then :returns: False
        """
        try:
            if fileNameWithPath:
                fileData = self.getFileData(fileNameWithPath)

                if fileData:
                    return self.returnsDictionaryFromString(fileData)
            else:
                print('error json file name with path is error')
                return False
        except Exception as e:
            print('error in readFileAndReturnJson in GeneralExceptionHandling', e)
            return False

    def writeJsonDataToFile(self, data, nameWithPath) -> bool:
        """
        convert json to text file
        :param data: json data
        :param nameWithPath: out file
        :return: True if success else False
        """
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