import json
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class LocatorValidation:
    def __init__(self, path):
        self.path = path
        self.locatorValidationArray = dict()

        self.dataFetchingValidationLocatorPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'DataFetching', self.path)
        self.dataFetchingValidationLocatorPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'validationLocator', self.dataFetchingValidationLocatorPath)

        self.dataFetchingFilesPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'DataFetching', self.path)
        self.dataFetchingFilesPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'filesPath', self.dataFetchingFilesPath)

    def patternCheck(self, pattern, string):
        try:
            import re
            searchPattern = re.search(pattern, string)

            if searchPattern:
                # print('pattern match')
                return True
            else:
                # print('pattern no match')
                return False
        except Exception as e:
            print('error in pattern check in validation', e)
            return False

    def getValidity(self, locatorId, locatorData, locatorValidationDirectoryPath):
        try:
            validatorDirectory = GeneralExceptionHandling.getFileData(GeneralExceptionHandling, locatorValidationDirectoryPath)

            if not validatorDirectory:
                return False
            else:
                validatorDirectory = json.loads(validatorDirectory)
                for flag, seperatedValidation in validatorDirectory.items():
                    # print('seperatedvalidation ', seperatedValidation, locatorId)
                    if locatorId in seperatedValidation:
                        validatorPatternArray = seperatedValidation[locatorId]
                        # print('validation: ', locatorId,flag, validatorPatternArray)
                        for validatorPattern in validatorPatternArray:
                            patternValidation = self.patternCheck(validatorPattern, locatorData)

                            if flag == 'True':
                                if not patternValidation:
                                    return False
                            elif flag == 'False':
                                if patternValidation:
                                    return False

                    # return True
                # self.locatorValidationArray[locatorId] = status

                return True
        except Exception as e:
            print('error in assignValidationStatus in validation', e)
            return False

    def addValidation(self, locatorValidationDirectoryPath, locatorId, validation, flag):
        try:
            # locatorValidationDirectoryPath = self.dataFetchingFilesPath + self.dataFetchingValidationLocatorPath + '.json'
            if locatorValidationDirectoryPath:
                validatorData =  GeneralExceptionHandling.getFileData(GeneralExceptionHandling, locatorValidationDirectoryPath)
                validationArray = []

                if not validatorData:
                    validatorDirectory = dict()
                    seperatedValidation = dict()
                else:
                    validatorDirectory = json.loads(validatorData)

                    if flag in validatorDirectory:
                        seperatedValidation = validatorDirectory[flag]
                        if locatorId in seperatedValidation:
                            validationArray = seperatedValidation[locatorId]
                    else:
                        seperatedValidation = dict()

                validationArray.append(validation)
                seen = set()

                validationArray[:] = [item for item in validationArray
                                   if item not in seen and not seen.add(item)]
                seperatedValidation[locatorId] = validationArray
                validatorDirectory[flag] = seperatedValidation

                fp = open(locatorValidationDirectoryPath, 'w')
                fp.write(json.dumps(validatorDirectory))
                fp.close()
                return True
            else:
                print('no locatorValidationDirectoryPath')
                return False
        except Exception as e:
            print('error in addvalidation in validation', e)
            print(locatorId, validation, flag)
            return False
