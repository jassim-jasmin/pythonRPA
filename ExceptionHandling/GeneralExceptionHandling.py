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