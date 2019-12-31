from fuzzywuzzy import process
import re

from ExceptionHandling.DirecotryHandling import DrectoryHandling
from DataFetching.StringHandling import StringHandling
from DataFetching.validation import LocatorValidation

class Locator(LocatorValidation, DrectoryHandling, StringHandling):
    def __init__(self, path):
        self.path = path
        StringHandling.__init__(self, path)
        LocatorValidation.__init__(self, path)
        DrectoryHandling.__init__(self)
        self.mainLocator = dict()
        self.locatorMissMatchFlag = True
        self.locatorMissMatchDictionary = dict()
        self.locatorId = []
        self.DataFetchingFilesPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
        self.dataFetchingLocatorMissMatch = self.getJsonDataRecurssive('DataFetching,locatorMissMatch', self.path)

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

    def buildLocatorPattern(self, eachLocatorArray, sourceDataProcessed) -> str:
        """
        This one does the core logic of pattern build, need lot of improvement need to perform better
        :param eachLocatorArray: Locator array
        :param sourceDataProcessed: Processed locator data
        :return: pattern if match else False
        :Todo: Need more optimaization can improve speed and accurate
        """
        try:
            patternBuild = '('
            for i in range(0, len(eachLocatorArray)):
                eachLocator = eachLocatorArray[i].upper()
                """considering if a string contains number, prevent it for fuzzy search"""
                # searchOnlyNumAndCharObj = re.search(r'^[0-9-`!@#$%^&*()_+=\\|}\]\[{\';:\/\?>\.,<~ ]+$', eachLocator)
                searchOnlyNumAndCharObj = re.search(r'[0-9]', eachLocator)
                if searchOnlyNumAndCharObj:
                    bestMatch = re.sub('\d', '\d+', eachLocator)
                    # print('pattern found', bestMatch)

                    if i == 0:
                        patternBuild = patternBuild + bestMatch
                    else:
                        patternBuild = patternBuild + '(.*)' + bestMatch
                else:
                    """ Get fuzzy matching string array """
                    matchingFuzzyWord = self.getFuzzySearchData(eachLocator, sourceDataProcessed)
                    if len(process.extractBests(eachLocator, matchingFuzzyWord)) > 0:
                        """ Find the best amoung them """
                        bestMatch, confidence = process.extractBests(eachLocator, matchingFuzzyWord)[0]


                        if len(matchingFuzzyWord) > 0:
                            bestMatch = self.regularExpressionHandling(bestMatch, 0)
                            if i == 0:
                                patternBuild = patternBuild + bestMatch
                            else:
                                patternBuild = patternBuild + '(.*)' + bestMatch
                    elif len(matchingFuzzyWord) == 0 and i == 0:
                        """ if first locator doesnot match then no need for further process (Improvement in searching) """
                        return False

            patternBuild = patternBuild + ')'
            return patternBuild
        except Exception as e:
            print('error in buildLocatorPattern', e)
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
                    self.locatorId = []

                    if locatorDictionary:
                        for locatorId, locatorDataArray in locatorDictionary.items():
                            self.locatorId.append(locatorId)
                            locatorArray = self.processLocatorData(locatorDataArray, sourceDataProcessed, sourceData)

                            if locatorArray:
                                locatorDataDictionary[locatorId] = locatorArray
                            else:
                                if self.locatorMissMatchFlag:
                                    self.locatorMissMatchArray.append(locatorId)
                        return locatorDataDictionary
                    else:
                        print('error Layer ', locatorFilePathWithFileName, ' has no data', locatorDictionary)
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
        try:
            import sys
            locatorFilePath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            locatorFilePathWithFileName = locatorFilePath+layerName+'.json'

            if sourceDataPath:
                fileNameArray = self.getDirectoryElementBykey(sourceDataPath, 'txt')

                if fileNameArray:
                    locatorDirectoryWithFileName = dict()

                    for eachTextFile in fileNameArray:
                        textFileData = self.getFileData(sourceDataPath+eachTextFile)
                        if textFileData:
                            locatorDataDictionary = self.processLocatorAndGetDataFromFile(locatorFilePathWithFileName, textFileData)
                            if locatorDataDictionary:
                                if self.locatorMissMatchFlag:
                                    if len(self.locatorMissMatchArray)>0:
                                         self.locatorMissMatchDictionary[eachTextFile] = self.locatorMissMatchArray[:]
                                    else:
                                        self.locatorMissMatchDictionary[eachTextFile] = ['no match']
                                fileNameSplit = eachTextFile.split('.')
                                if len(fileNameSplit)>0:
                                    locatorDirectoryWithFileName[fileNameSplit[0]] = locatorDataDictionary
                        else:
                            exit()

                    validation = LocatorValidation(self.path)
                    return validation.validateLayer(locatorDirectoryWithFileName, layerName)
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
                    fieldNames = ['file name', 'no match']
                    if 'locator' in layerDictionary:
                        fieldNames.extend(layerDictionary['locator'])
                    else:
                        fieldNames.extend(self.locatorId[:])

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
                    dataDictionary = layerData  # primary dictionary
                    if 'locator' in layerDictionary:
                        locatorArray = layerDictionary['locator']

                    import re
                    locatorDataDictionary = dict()

                    locatorDictionary = self.getLocatorDataArray(layerPath) # new dictionary
                    if locatorDictionary and dataDictionary:
                        self.locatorMissMatchArray = []
                        self.locatorId = []
                        locatorDictionaryMain = dict()

                        for fileName, locatorData in dataDictionary.items():# main
                            for loactorIdInData, eachLocatorInData in locatorData.items():# new
                                for locatorId, locatorDataArray in locatorDictionary.items():
                                    if locatorId in connectorKeys:
                                        if connectorKeys[locatorId] == loactorIdInData:
                                            sourceDataProcessed = eachLocatorInData.upper()
                                            sourceDataProcessed = sourceDataProcessed.replace('\n', ' ')
                                            self.locatorId.append(eachLocatorInData)
                                            locatorArray.append(locatorId)
                                            # print(sourceDataProcessed)
                                        else:
                                            if connectorKeys[
                                                    locatorId] == locatorId:  # the data is in final locator
                                                sourceDataProcessed = eachLocatorInData.upper()
                                                sourceDataProcessed = sourceDataProcessed.replace('\n', ' ')
                                                self.locatorId.append(locatorId)
                                                locatorArray.append(locatorId)

                                        if sourceDataProcessed and eachLocatorInData:
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
                            """
                            validation performs
                            """
                            if validatedLayer:
                                return validatedLayer
                            else:
                                return locatorDictionaryMain
                        else:
                            print('empty layer:', processLayerName)
                            return False
                    else:
                        return False

                except Exception as e:
                    print('error in  processLocatorAndGetDataFromDictionary in Locator',e)
                    return False
                return True
            else:
                print('error in source dictionary Locator sourceData', layerDataMain)
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