from fuzzywuzzy import process
import re

from ExceptionHandling.DirecotryHandling import DrectoryHandling
from DataFetching.StringHandling import StringHandling
from DataFetching.validation import LocatorValidation

class Locator(LocatorValidation, DrectoryHandling, StringHandling):
    def __init__(self, path):
        """
        :todo: need to add profile for locator,
        :todo: rename Locator to profile layer
        :todo: cannot map two parent locator to a single child locator
        :param path: Basic argument
        """
        self.path = path
        StringHandling.__init__(self, path)
        LocatorValidation.__init__(self, path)
        DrectoryHandling.__init__(self)
        self.mainLocator = dict()
        self.locatorMissMatchFlag = True
        self.locatorMissMatchDictionary = dict()
        self.DataFetchingFilesPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
        self.dataFetchingLocatorMissMatch = self.getJsonDataRecurssive('DataFetching,locatorMissMatch', self.path)

    def addLayerProfile(self, profileName):
        try:
            return self.createDirectory(self.DataFetchingFilesPath+profileName)
        except Exception as e:
            print('error in addLayerProfile in Locator', e)
            return False


    def addLocatorToDictionary(self, locationStringArray, locatorId, locatorJsonFileName, locatorDirectory) -> bool:
        try:

            if locatorDirectory and locationStringArray:
                for i in range(0,len(locationStringArray)):
                    if i == 0:
                        locationString = locationStringArray[i].replace(':','-:-')
                    else:
                        locationString = locationString + '::' + locationStringArray[i].replace('::',':|:')

                self.createDirectory(locatorDirectory)

                locatorJsonFileNamewithPath = locatorDirectory + locatorJsonFileName + '.json'

                locatorData = self.readFileAndReturnJson(locatorJsonFileNamewithPath)
                if locatorData:
                    if locatorId in locatorData:
                        fileData = locatorData[locatorId]
                        data = self.getMathcFromSetInverse(locationString, fileData, self.stringMatchConfidence+10)
                        if data:
                            if self.addStringWriteFile(locationString, locatorJsonFileName, locatorId, locatorDirectory):
                                return True
                            else:
                                return False
                        else:
                            print('locator adding failed, similar pattern available', locationString, fileData)
                            return False
                    elif self.addStringWriteFile(locationString, locatorJsonFileName, locatorId, locatorDirectory):
                        return True
                    else:
                        print('write error', locatorJsonFileName)
                        return False
                else:
                    if self.addStringWriteFile(locationString, locatorJsonFileName, locatorId, locatorDirectory):
                        return True
                    else:
                        return False
            else:
                print('error in locatorDirectory in addLocatorToDictionary in Locator')
        except Exception as e:
            print('error in addNewStringToDictionary in Locator', e)
            return False

    def getLocatorDataArray(self, locatorFilePathWithFileName) -> dict:
        try:
            locator = []
            locatorDictionary = dict()

            locatorJson = self.readFileAndReturnJson(locatorFilePathWithFileName)

            if locatorJson:
                for locatorId, locatorArray in locatorJson.items():
                    for locatorData in locatorArray:
                        indeces = locatorData.split('::')
                        for i in range(0,len(indeces)):
                            indeces[i] = indeces[i].replace('-:-', ':')
                        locator.append(indeces)
                    locatorDictionary[locatorId] = locator
                    locator = []

                if bool(locatorDictionary):
                    return locatorDictionary
                else:
                    return False
            else:
                return False
        except Exception as e:
            print('error in getLocatorDataArray in Locator', e)
            return False

    def processLocatorData(self, locatorDataArray, sourceDataProcessed, sourceData):
        """
        pattern match math source file
        :param locatorDataArray: loactor array
        :param sourceDataProcessed: processed source data, that is capitalize, remove new line...
        :param sourceData: original source file
        :return: match data if error then :return: False
        :Todo: reSelect() might take too long for unstructured pattern build, need to rectify it
        """
        try:
            if locatorDataArray:
                for eachLocatorArray in locatorDataArray:
                    patternBuild = self.buildLocatorPattern(eachLocatorArray, sourceDataProcessed)

                    if patternBuild:
                        locatorData = self.reSelect(patternBuild, sourceDataProcessed, sourceData)

                        if locatorData:
                            # print('found;;;;', locatorData)
                            return locatorData
            return False

        except Exception as e:
            print('error in processLocatorData in Locator', e)
            return False

    def processLocatorAndGetDataFromFile(self, locatorFilePathWithFileName, sourceData) -> dict:
        try:
            if sourceData:
                try:
                    import re

                    sourceDataProcessed = sourceData.upper()
                    sourceDataProcessed = sourceDataProcessed.replace('\n', ' ')
                    locatorDataDictionary = dict()

                    locatorDictionary = self.getLocatorDataArray(locatorFilePathWithFileName)
                    self.locatorMissMatchArray = []
                    locatorArray = []

                    if locatorDictionary:
                        for locatorId, locatorDataArray in locatorDictionary.items():
                            locatorArray.append(locatorId)
                            locatorDataArray = self.processLocatorData(locatorDataArray, sourceDataProcessed, sourceData)

                            if locatorDataArray:
                                locatorDataDictionary[locatorId] = locatorDataArray
                            else:
                                if self.locatorMissMatchFlag:
                                    self.locatorMissMatchArray.append(locatorId)
                        return locatorDataDictionary, locatorArray
                    else:
                        print('error Layer ', locatorFilePathWithFileName, ' has no data', locatorDictionary, locatorFilePathWithFileName)
                        exit()

                except Exception as e:
                    print('error in processLocatorAndGetDataFromFile in Locator ',e)
                    return False
                return True
            else:
                print('error in source file Locator sourceData', sourceData)
                return False
        except Exception as e:
            print('errror in processLocatorAndGetDataFromFile in locator', e)
            return False

    def processLocatorAndGetDataFromFileAll(self, layerName, sourceDataPath) -> dict:
        """

        :param layerName: Name of layer
        :param sourceDataPath: location of directory
        :return: Locator directory :return: False if error
        :todo: miss match logic need to change
        """
        try:
            import sys
            locatorFilePath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            locatorFilePathWithFileName = locatorFilePath+layerName+'.json'

            if sourceDataPath:
                fileNameArray = self.getDirectoryElementBykey(sourceDataPath, 'txt')

                if fileNameArray:
                    locatorDirectoryWithFileName = dict()
                    layerDictionary = dict()
                    locatorArrayMain = []

                    for eachTextFile in fileNameArray:
                        textFileData = self.getFileData(sourceDataPath+eachTextFile)
                        if textFileData:
                            locatorDataDictionary, locatorArray = self.processLocatorAndGetDataFromFile(locatorFilePathWithFileName, textFileData)
                            locatorArrayMain.extend(locatorArray)
                            if locatorDataDictionary:
                                fileNameSplit = eachTextFile.split('.')
                                if len(fileNameSplit)>0:
                                    locatorDirectoryWithFileName[fileNameSplit[0]] = locatorDataDictionary
                        else:
                            exit()
                    """ If validation file available then only need of validation """
                    validationStatus = self.fileStatus(locatorFilePath+layerName+'_validation.json')
                    if validationStatus:
                        self.validateLayer(locatorDirectoryWithFileName, layerName)
                    else:
                        locatorArrayMain = self.removeArrayDuplicate(locatorArrayMain)
                        layerDictionary['locator'] = locatorArrayMain
                        layerDictionary['locatorData'] = locatorDirectoryWithFileName
                        return layerDictionary
                else:
                    print('error no data in ', sourceDataPath, ' Processing locator failed')
                    return False
            else:
                print('error in argument sourceDataPath in processLocatorAndGetDataFromFileAll')
                return False

        except Exception as e:
            print('errror in processLocatorAndGetDataFromFileAll in locator', e)
            return False

    def saveAsCsv(self, csvNameWithPath, tag,layerDictionary) -> bool:
        try:
            import csv

            if layerDictionary:
                with open(csvNameWithPath, 'w') as csvfile:
                    # print('opening csv', layerDictionary)
                    csvfile.write(tag)
                    fieldNames = ['file name']
                    if 'locator' in layerDictionary:
                        fieldNames.extend(layerDictionary['locator'])

                    if 'locatorData' in layerDictionary:
                        layerData = layerDictionary['locatorData']
                        # print('layer data: ', layerData)
                        csvfile.newlines
                        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
                        writer.writeheader()
                        print('csv save file:', csvNameWithPath)
                        for fileName, locatorData in layerData.items():
                            csvEacRowLocator = dict()
                            csvEacRowLocator['file name'] = fileName

                            for data in locatorData:
                                array = []
                                dictionary = dict()

                                if type(locatorData) is  type(array):
                                    csvEacRowLocator[data] = data
                                elif type(locatorData) is type(dictionary):
                                    if data in locatorData:
                                        csvEacRowLocator[data] = locatorData[data]
                                    else:
                                        print('Error json error key' + data + ' not in ')
                                        print(locatorData)
                                        return False
                                else:
                                    print('not a dictionary', locatorData)
                                    return False

                            writer.writerow(csvEacRowLocator)
                        return True
                    else:
                        print('error creating csv invalid layer data')
                        return False
            else:
                print('error in csv dictionary in saveAsCsv in Locator', layerDictionary)
                return False
        except Exception as e:
            print("error in saveAsCsv in Locator", e)

    def getValidatedLocatorData(self, locatorDataDirectory, validation) -> dict:
        try:
            locatorDirectry = dict()
            for fileName, locatorData in locatorDataDirectory.items():
                locatorArray = dict()
                if fileName in validation:
                    validationDirectory = validation[fileName]
                    for locatorId, validationStatus in validationDirectory.items():
                        if validationStatus:
                            if locatorId in locatorData:
                                locatorArray[locatorId] = locatorData[locatorId]
                                locatorDirectry[fileName] = locatorArray.copy()
            return locatorDirectry
        except Exception as e:
            print('error in printLocatorDataWithLocatorId in locator', e)
            return False

    def processLayerFromLayer(self, processLayerName, layerDictionary, connectorKeys) -> dict:
        """
        Locator selection on another layer
        :param processLayerName: new layer name
        :param layerDictionary: Already processed layer dictionary
        :param connectorKeys: connector for new layer and existing dictionary layer
        :return: new layer data
        :Todo: if existing dictionary has no data then new layer further process is no need
        :Todo: Locator id is always appending to the dictionary can avoid that
        :todo: locator array and locator data in layer need to optimize, it is updating after checking validation can modify either from validation or before giving to validation
        :todo: dictionary is creating unecessorly, need to find other methodes to replace this strategy
        """
        try:
            locatorFilePath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            layerPath = locatorFilePath+processLayerName+'.json'
            locatorArray = []
            layerDataMain = dict()

            if 'locatorData' in layerDictionary:
                layerData = layerDictionary['locatorData']
            else:
                layerData = False

            if layerData:
                try:
                    """ Collecting existing layer DATA dictionary """
                    dataDictionary = layerData  # primary dictionary
                    if 'locator' in layerDictionary:
                        locatorArray = layerDictionary['locator']
                    locatorDataDictionary = dict()

                    """ Collecting new layer dictionary """
                    locatorDictionary = self.getLocatorDataArray(layerPath)
                    if locatorDictionary and dataDictionary:
                        self.locatorMissMatchArray = []
                        locatorDictionaryMain = dict()

                        for fileName, locatorData in dataDictionary.items():# main
                            for loactorIdInData, eachLocatorInData in locatorData.items():# new
                                if eachLocatorInData:
                                    """ Converting to upper case and removing new line for regular expression processing """
                                    sourceDataProcessed = eachLocatorInData.upper()
                                    sourceDataProcessed = sourceDataProcessed.replace('\n', ' ')

                                    for locatorId, locatorDataArray in locatorDictionary.items():
                                        locatorDataDictionary = dict()
                                        """ new layer locator id is available in connector keys """
                                        if locatorId in connectorKeys:
                                            """
                                                new layer id equals existing layer data dictionary id
                                                only then need to process locator
                                            """
                                            if connectorKeys[locatorId] == loactorIdInData:
                                                locatorArray.append(locatorId)
                                                locatorFinalData = self.processLocatorData(locatorDataArray,
                                                                                           sourceDataProcessed,
                                                                                           eachLocatorInData)
                                                if locatorFinalData:
                                                    locatorDataDictionary[locatorId] = locatorFinalData
                                                    locatorDictionaryMain[fileName] = dict(locatorDataDictionary)# need correction
                                                    locatorArray.append(locatorId)
                                        else:
                                            print('invalid locator connector ', locatorId , ' not in ', connectorKeys)
                                            return False

                        if bool(locatorDictionaryMain):
                            validatedLayer = self.validateLayer(locatorDictionaryMain, processLayerName)
                            """ validation performs """
                            if validatedLayer:
                                return validatedLayer
                            else:
                                locatorArray = self.removeArrayDuplicate(locatorArray)
                                layerDictionaryFinal = dict()
                                layerDictionaryFinal['locator'] = locatorArray
                                layerDictionaryFinal['locatorData'] = locatorDictionaryMain
                                return layerDictionaryFinal
                        else:
                            print('empty layer:', processLayerName, locatorDictionaryMain)
                            return False
                    else:
                        print('layer ' + processLayerName + ' is not defined')
                        return False

                except Exception as e:
                    print('error in  processLocatorAndGetDataFromDictionary in Locator',e)
                    return False
                return True
            else:
                print('error in source dictionary Locator sourceData', layerDataMain, layerDictionary)
                return False
        except Exception as e:
            print('errror in processLocatorAndGetDataFromDictionary in locator', e)
            return False

    def fetchSpecificDataOverLayer(self):
        try:
            pass
        except Exception as e:
            print('error in fetchSpecificDataOverLayer in Locator', e)
            return False