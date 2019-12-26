import json
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class LocatorValidation(GeneralExceptionHandling):
    def __init__(self, path):
        GeneralExceptionHandling.__init__(self)
        self.path = path
        self.locatorValidationArray = dict()

        self.dataFetchingValidationLocatorPath = self.getJsonDataRecurssive('DataFetching,validationLocator', self.path)
        self.dataFetchingFilesPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)

    def patternCheck(self, pattern, string):
        try:
            import re
            searchPattern = re.search(pattern, string, re.IGNORECASE)

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
            validatorDirectory = self.getFileData(locatorValidationDirectoryPath)

            if validatorDirectory:
                validatorDirectory = json.loads(validatorDirectory)
                for flag, seperatedValidation in validatorDirectory.items():
                    if locatorId in seperatedValidation:
                        validatorPatternArray = seperatedValidation[locatorId]
                        for validatorPattern in validatorPatternArray:
                            patternValidation = self.patternCheck(validatorPattern, locatorData)
                            # print('final validity', validatorPattern, '::', locatorData,'::', patternValidation)

                            if flag == 'True':
                                if not patternValidation:
                                    return False
                            elif flag == 'False':
                                if patternValidation:
                                    return False
                    else:
                        return True

            return True
        except Exception as e:
            print('error in assignValidationStatus in validation', e)
            return False

    def addValidation(self, locatorValidationDirectoryPath, locatorId, validation, flag):
        try:
            if locatorValidationDirectoryPath:
                validatorData = self.getFileData(locatorValidationDirectoryPath)
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
                print('no locatorValidationData')
                return False
        except Exception as e:
            print('error in addvalidation in validation', e)
            print(locatorId, validation, flag)
            return False

    def addValidationLayer(self, layerName, validationArray):
        try:
            filesPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            fileName = filesPath +layerName + '_validation.json'
            fp = open(fileName, 'w')
            fp.flush()
            fp.close()
            # print(validationArray, 'validation')

            for eachLocaotrData in validationArray:
                # print('length:', len(eachLocaotrData))
                if len(eachLocaotrData) == 3:
                    locatorId, pattern, flag = eachLocaotrData
                    if not self.addValidation(fileName, locatorId, pattern, flag):
                        print('error in adding locator validation')
                        return False
                else:
                    print('error in validation should contain locator, pattern, flag', eachLocaotrData)
                    return False

            return True
        except Exception as e:
            print('error in addValidationLayer in validation', e)
            return False

    def validateLayer(self, layerDictionaryOrData, layerName):
        try:
            dataFetchingFilesPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            validationLayer = dataFetchingFilesPath + layerName + '_validation.json'
            layerDictionaryMain  = dict()

            if 'locatorData' in layerDictionaryOrData:
                layerData  = layerDictionaryOrData['locatorData']
            else:
                layerData = layerDictionaryOrData

            locatorArray = []
            if 'locator' in layerDictionaryOrData:
                locatorArray = layerDictionaryOrData['locator']

            if layerData:
                validDictionary = dict()
                for fileName, locatorDirectory in layerData.items():
                    valid = []
                    for locatorId, locatorData in locatorDirectory.items():
                        if self.getValidity(locatorId, locatorData, validationLayer):
                            # print('validity::', locatorId, locatorData, validationLayer)
                            valid.append(locatorId)
                            locatorArray.append(locatorId)
                        # else:
                            # print('rejected', fileName, locatorId, locatorData, validationLayer)
                            # print('vald::::', valid)
                    validDictionary[fileName] = valid
                    # print('dicitionary::', validDictionary)

                #final out
                validatedLayer = dict()
                locatorArray = []
                for fileName, locatorData in layerData.items():
                    layerDictionary = dict()
                    if fileName in validDictionary:
                        for locatorIdMain, locatorDataMain in locatorData.items():
                            if locatorIdMain in validDictionary[fileName]:
                                layerDictionary[locatorIdMain] = locatorDataMain
                                locatorArray.append(locatorIdMain)
                        # print('locatorData', locatorData)
                        # print('locatorArray', layerDictionary)
                        validatedLayer[fileName] = layerDictionary.copy()
                        # print('values::', locatorData, validDictionary[fileName])
                    # else:
                    #     validatedLayer[fileName] = locatorData.copy()
                # print('dataa:::::', validatedLayer)

                layerDictionaryMain['locator'] = self.removeArrayDuplicate(locatorArray)
                layerDictionaryMain['locatorData'] = validatedLayer
                return layerDictionaryMain
            return False

        except Exception as e:
            print('error in validatinglocator in validation', e)
            return False

    def processLayerFromLayer(self, layerDirectory, processLayerName):
        try:
            dataFetchingFilesPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            processLayerPath = dataFetchingFilesPath+processLayerName+'_validation.json'

            if 'locatorData' in layerDirectory:
                layerData = layerDirectory['locatorData']
            else:
                layerData = False

            if layerData:
                validationDictionary = dict()
                for fileName, locatorDirectory in layerData.items():
                    # print(fileName)
                    validity = dict()
                    for locatorId, locatorData in locatorDirectory.items():
                        validity[locatorId] = self.getValidity(locatorId, locatorData,
                                                               processLayerPath)
                    validationDictionary[fileName] = validity
                return validationDictionary
            return False

        except Exception as e:
            print('error in validatinglocator in validation', e)
            return False