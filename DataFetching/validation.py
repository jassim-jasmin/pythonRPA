from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from ExceptionHandling.CSVHandling import CsvHandling

class LocatorValidation(GeneralExceptionHandling, CsvHandling):
    def __init__(self, path):
        CsvHandling.__init__(self)
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
                return True
            else:
                return False
        except Exception as e:
            print('error in pattern check in validation', e)
            return False

    def getValidity(self, locatorId, locatorData, locatorValidationDirectoryPath):
        try:
            validatorDirectory = self.readFileAndReturnJson(locatorValidationDirectoryPath)


            if validatorDirectory:
                for flag, seperatedValidation in validatorDirectory.items():
                    if locatorId in seperatedValidation:
                        validatorPatternArray = seperatedValidation[locatorId]
                        for validatorPattern in validatorPatternArray:
                            patternValidation = self.patternCheck(validatorPattern, locatorData)

                            if flag == 'True':
                                if not patternValidation:
                                    return False
                            elif flag == 'False':
                                if patternValidation:
                                    return False
                    else:
                        return True
                return True
            else:
                return False
        except Exception as e:
            print('error in assignValidationStatus in validation', e)
            return False

    def addValidation(self, locatorValidationDirectoryPath, locatorId, validation, flag):
        try:
            if locatorValidationDirectoryPath:
                validatorDirectory = self.readFileAndReturnJson(locatorValidationDirectoryPath)
                validationArray = []

                if not validatorDirectory:
                    validatorDirectory = dict()
                    seperatedValidation = dict()
                else:
                    if flag in validatorDirectory:
                        seperatedValidation = validatorDirectory[flag]
                        if locatorId in seperatedValidation:
                            validationArray = seperatedValidation[locatorId]
                    else:
                        seperatedValidation = dict()

                validationArray.append(validation)
                seperatedValidation[locatorId] = self.removeArrayDuplicate(validationArray)
                validatorDirectory[flag] = seperatedValidation

                return self.writeJsonDataToFile(validatorDirectory, locatorValidationDirectoryPath)
            else:
                print('no locatorValidationData')
                return False
        except Exception as e:
            print('error in addvalidation in validation', e)
            print(locatorId, validation, flag)
            return False

    def addValidationLayer(self, layerName, validationArray):
        """
        Adding validation dictionary
        :param layerName: name
        :param validationArray: each element of array having locator, pattern, flag
        :return:
        """
        try:
            filesPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            fileName = filesPath +layerName + '_validation.json'
            fp = open(fileName, 'w')
            fp.flush()
            fp.close()

            for eachLocaotrData in validationArray:
                if len(eachLocaotrData) == 3:
                    locatorId, pattern, flag = eachLocaotrData
                    if not self.addValidation(fileName, locatorId, pattern, flag):
                        print('error in adding locator validation')
                        return False
                else:
                    print('error in addValidationLayer, validation is not in the format locator, pattern, flag', eachLocaotrData)
                    exit()
                    # return False

            return True
        except Exception as e:
            print('error in addValidationLayer in validation', e)
            return False

    def validateLayer(self, layerDictionaryOrData, layerName):
        """
        todo validation file moved to db need to update
        :param layerDictionaryOrData:
        :param layerName:
        :return:
        """
        try:
            dataFetchingFilesPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            validationLayer = dataFetchingFilesPath + layerName + '_validation.json'
            layerDictionaryMain  = dict()

            if self.fileStatus(validationLayer):
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
                            if self.getValidity(locatorId, locatorData, validationLayer):# mj
                                valid.append(locatorId)
                                locatorArray.append(locatorId)

                        validDictionary[fileName] = valid

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

                            validatedLayer[fileName] = layerDictionary.copy()

                    layerDictionaryMain['locator'] = self.removeArrayDuplicate(locatorArray)
                    layerDictionaryMain['locatorData'] = validatedLayer
                    return layerDictionaryMain
            return False

        except Exception as e:
            print('error in validatinglocator in validation', e)
            return False

    def validateLayerBylayer(self, layer, validationLayer):
        '''
        todo optimize with  analyse and CSVHandling
        :param layer:
        :param validationLayer:
        :return:
        '''
        try:
            import pandas as pd
            import  csv

            csvPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)

            csvlayer = pd.read_csv(csvPath+layer+'.csv')
            csvValidationLayer = pd.read_csv(csvPath+validationLayer+'.csv')

            pendingFiles = csvlayer[~csvlayer['file_name'].isin(csvValidationLayer['file_name'])]

            pendingFiles.to_csv(csvPath+layer+'_'+validationLayer+'_validated.csv')

            pass
        except Exception as e:
            print('error in validtelayerByLayer in Layer', e)
            return False
