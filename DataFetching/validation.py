import json
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class LocatorValidation:
    def __init__(self, path):
        self.path = path
        self.locatorValidationArray = dict()

    def patternCheck(self, pattern, string):
        try:
            import re
            searchPattern = re.search(pattern, string)

            if searchPattern:
                print('pattern match')
                return True
            else:
                print('pattern no match')
                return False
        except Exception as e:
            print('error in pattern check in validation', e)
            return False

    def getValidity(self, locatorId, locatorData):
        try:
            locatorValidationDirectoryPath = self.path['DataFetching']['filesPath']+self.path['DataFetching']['validationLocator']+'.json'
            validatorDirectory = GeneralExceptionHandling.getFileData(GeneralExceptionHandling, locatorValidationDirectoryPath)

            if not validatorDirectory:
                return False
            else:
                validatorDirectory = json.loads(validatorDirectory)
                for flag, seperatedValidation in validatorDirectory.items():
                    # print('seperatedvalidation ', seperatedValidation, locatorId)
                    if locatorId in seperatedValidation:
                        validatorPatternArray = seperatedValidation[locatorId]
                        print('validation: ', locatorId,flag, validatorPatternArray)
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

    def addValidation(self, locatorId, validation, flag):
        try:
            locatorValidationDirectoryPath = self.path['DataFetching']['filesPath'] + self.path['DataFetching'][
                'validationLocator'] + '.json'
            validatorData =  GeneralExceptionHandling.getFileData(GeneralExceptionHandling, locatorValidationDirectoryPath)
            validationArray = []

            if not validatorData:
                validatorDirectory = dict()
                seperatedValidation = dict()
            else:
                validatorDirectory = json.loads(validatorData)
                if flag in validatorDirectory:
                    seperatedValidation = validatorDirectory[flag]
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
        except Exception as e:
            print('error in addvalidation in validation', e)

    # def getValidationStatus(self, locatorId):
    #     try:
    #         if locatorId in self.locatorValidationArray:
    #             status = self.locatorValidationArray[locatorId]
    #             return status
    #         else:
    #             return True
    #     except Exception as e:
    #         print('error in getValidationStatus', e)
    #         return False
    #
    # def absoluteValidation(self, locatorId, validationValue, pattern):
    #     try:
    #         if locatorId in self.locatorValidationArray:
    #             validation = self.locatorValidationArray[locatorId]
    #         else:
    #             validation = dict()
    #             validation[validationValue] = pattern
    #         self.locatorValidationArray[locatorId] = validation
    #
    #         return True
    #     except Exception as e:
    #         print('error in assignValidationTrue', e)
    #         return False
    # def assignValidationTrue(self, locatorId, pattern):
    #     try:
    #         if self.absoluteValidation(locatorId, 'True', pattern):
    #             return True
    #         else:
    #             return False
    #     except Exception as e:
    #         print('error in assignValidationTrue in validation', e)
    #         return False
    #
    # def assignValidationFalse(self, locatorId, pattern):
    #     try:
    #         if self.absoluteValidation(locatorId, 'False', pattern):
    #             return True
    #         else:
    #             return False
    #     except Exception as e:
    #         print('error in assignValidationTrue in validation', e)
    #         return False
    #
    # def addValidation(self, locatorId, validationPattern, validationFlag):
    #     try:
    #         if validationFlag == 'True':
    #             self.assignValidationTrue(locatorId, validationPattern)
    #             return True
    #         elif validationFlag == 'False':
    #             self.assignValidationFalse(locatorId, validationPattern)
    #             return True
    #         else:
    #             print('invalid validationFlag', validationFlag)
    #             return False
    #     except Exception as e:
    #         print('error in addValidation in validation', e)
    #         return False