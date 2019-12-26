import json

from fuzzywuzzy import process

from ExceptionHandling.DirecotryHandling import DrectoryHandling
from DataFetching.StringHandling import StringHandling
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.validation import LocatorValidation

class Locator:
    def __init__(self, path):
        self.path = path
        self.mainLocator = dict()
        self.locatorMissMatchFlag = True
        self.locatorMissMatchDictionary = dict()
        self.locatorId = []
        self.DataFetchingFilesPath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                                       'DataFetching,filesPath',
                                                                                       self.path)
        self.dataFetchingLocatorMissMatch = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                                       'DataFetching,locatorMissMatch',
                                                                                       self.path)

    def addLocatorToDictionary(self, locationStringArray, locatorId, locatorJsonFileName, locatorDirectory):
        try:

            if locatorDirectory and locationStringArray:
                for i in range(0,len(locationStringArray)):
                    if i == 0:
                        locationString = locationStringArray[i].replace(':','-:-')
                    else:
                        locationString = locationString + '::' + locationStringArray[i].replace('::',':|:')

                stringHandling = StringHandling(self.path)
                DrectoryHandling.createDirectory(DrectoryHandling, locatorDirectory)
                locatorJsonFileNamewithPath = ''

                locatorJsonFileNamewithPath = locatorDirectory + locatorJsonFileName + '.json'

                locatorData = GeneralExceptionHandling.getFileData(GeneralExceptionHandling, locatorJsonFileNamewithPath)
                if locatorData:
                    locatorData = json.loads(locatorData)

                    if locatorId in locatorData:
                        fileData = locatorData[locatorId]
                        data = stringHandling.getMathcFromSetInverse(locationString, fileData, stringHandling.stringMatchConfidence+10)
                        if data:
                            if stringHandling.addStringWriteFile(locationString, locatorJsonFileName, locatorId, locatorDirectory):
                                return True
                            else:
                                return False
                        else:
                            print('locator adding failed, similar pattern available', locationString, fileData)
                            return False
                    elif stringHandling.addStringWriteFile(locationString, locatorJsonFileName, locatorId, locatorDirectory):
                        return True
                    else:
                        print('write error', locatorJsonFileName)
                        return False
                else:
                    if stringHandling.addStringWriteFile(locationString, locatorJsonFileName, locatorId, locatorDirectory):
                        return True
                    else:
                        return False
            else:
                print('error in locatorDirectory in addLocatorToDictionary in Locator')
        except Exception as e:
            print('error in addNewStringToDictionary in Locator', e)
            return False

    def getLocatorDataArray(self, locatorFilePathWithFileName):
        try:
            fp = open(locatorFilePathWithFileName, 'r')
            locatorJson = json.loads(fp.read())
            locator = []
            locatorDictionary = dict()

            for locatorId, locatorArray in locatorJson.items():
                # print(locatorId, locatorArray)
                for locatorData in locatorArray:
                    indeces = locatorData.split('::')
                    for i in range(0,len(indeces)):
                        indeces[i] = indeces[i].replace('-:-', ':')
                    locator.append(indeces)
                locatorDictionary[locatorId] = locator
                locator = []

            return locatorDictionary
        except Exception as e:
            print('error in getLocatorDataArray in Locator', e)
            return False
        finally:
            try:
                fp.close()
            except Exception as e:
                return False

    def buildLocatorPattern(self, eachLocatorArray, sourceDataProcessed):
        try:
            patternBuild = '('
            for i in range(0, len(eachLocatorArray)):
                stringHandling = StringHandling(self.path)
                import re
                eachLocator = eachLocatorArray[i].upper()
                searchOnlyNumAndCharObj = re.search(r'^[0-9-`!@#$%^&*()_+=\\|}\]\[{\';:\/\?>\.,<~ ]+$', eachLocator)
                # print('each locator: ', eachLocator, searchOnlyNumAndCharObj)
                if searchOnlyNumAndCharObj:
                    bestMatch = re.sub('\d', '\d+', eachLocator)
                    # print('pattern found', bestMatch)

                    if i == 0:
                        patternBuild = patternBuild + bestMatch
                    else:
                        patternBuild = patternBuild + '(.*)' + bestMatch
                else:
                    matchingFuzzyWord = stringHandling.getFuzzySearchData(eachLocator, sourceDataProcessed)
                    if len(process.extractBests(eachLocator, matchingFuzzyWord)) > 0:
                        bestMatch, confidence = process.extractBests(eachLocator, matchingFuzzyWord)[0]


                        if len(matchingFuzzyWord) > 0:
                            bestMatch = GeneralExceptionHandling.regularExpressionHandling(GeneralExceptionHandling,bestMatch,0)
                            # print(eachLocatorArray[i].upper(), 'fu::::', matchingFuzzyWord, 'best match:::', bestMatch)
                            if i == 0:
                                patternBuild = patternBuild + bestMatch
                            else:
                                patternBuild = patternBuild + '(.*)' + bestMatch

            patternBuild = patternBuild + ')'
            return patternBuild
        except Exception as e:
            print('error in buildLocatorPattern', e)
            return False

    def processLocatorData(self, locatorDataArray, sourceDataProcessed, sourceData):
        try:
            if locatorDataArray:
                for eachLocatorArray in locatorDataArray:
                    patternBuild = self.buildLocatorPattern(eachLocatorArray, sourceDataProcessed)
                    if patternBuild:
                        stringHandling = StringHandling(self.path)
                        # print('pattern build: ', patternBuild)
                        locatorData = stringHandling.reSelect(patternBuild, sourceDataProcessed, sourceData)

                        if locatorData:
                            # print('processLocatorData: ',locatorData, patternBuild)
                            return locatorData
                        else:
                            return False

        except Exception as e:
            print('error in processLocatorData in Locator', e)
            return False

    def processLocatorAndGetDataFromFile(self, locatorFilePathWithFileName, sourceData):
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

                    for locatorId, locatorDataArray in locatorDictionary.items():
                        self.locatorId.append(locatorId)
                        locatorArray = self.processLocatorData(locatorDataArray, sourceDataProcessed, sourceData)

                        if locatorArray:
                            locatorDataDictionary[locatorId] = locatorArray
                        else:
                            if self.locatorMissMatchFlag:
                                self.locatorMissMatchArray.append(locatorId)
                    return locatorDataDictionary

                except Exception as e:
                    print('error in processLocatorAndGetDataFromFile in Locator ',e)
                    # print('patter: ', patternMatch)
                    # print('patter other: ', sourceData, 'exception data')
                    return False
                return True
            else:
                print('error in source file Locator sourceData', sourceData)
                return False
        except Exception as e:
            print('errror in processLocatorAndGetDataFromFile in locator', e)
            return False

    def processLocatorAndGetDataFromFileAll(self, layerName, sourceDataPath):
        try:
            locatorFilePath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                             'DataFetching,filesPath', self.path)
            locatorFilePathWithFileName = locatorFilePath+layerName+'.json'
            from ExceptionHandling.DirecotryHandling import DrectoryHandling
            drectoryHandling = DrectoryHandling()

            if sourceDataPath:
                fileNameArray = drectoryHandling.getDirectoryElementBykey(sourceDataPath, 'txt')

                if fileNameArray:

                    locatorDirectoryWithFileName = dict()

                    for eachTextFile in fileNameArray:
                        textFileData = GeneralExceptionHandling.getFileData(GeneralExceptionHandling, sourceDataPath+eachTextFile)
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

                    validation = LocatorValidation(self.path)
                    # print('locator', locatorDirectoryWithFileName)
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
        finally:
            if self.locatorMissMatchFlag:
                self.saveMissMatch()

    def saveMissMatch(self):
        try:
            if self.locatorMissMatchDictionary:
                saveMissMatchData = json.dumps(self.locatorMissMatchDictionary)
                fileName = self.dataFetchingLocatorMissMatch

                if fileName and self.DataFetchingFilesPath:
                    print('saving file ', self.DataFetchingFilesPath+fileName+'.json')
                    fp = open(self.DataFetchingFilesPath+fileName+'.json', 'w')
                    fp.write(saveMissMatchData)
                    fp.close()

                    csvNameWithPath = self.DataFetchingFilesPath + 'missmatch.csv'
                    headData = 'Locator miss match\n'
                    locatorMissMatchDictionary = self.locatorMissMatchDictionary
                    # self.saveAsCsv(csvNameWithPath, headData, locatorMissMatchDictionary)

                    return True
                else:
                    print('error in source file or file name in locatorMissmatch')
                    return False
                    # print('data: ', saveMissMatchData)
        except Exception as e:
            print('error in saveMissMatch', e)
            # print('data: ', saveMissMatchData)
            return False

    def saveAsCsv(self, csvNameWithPath, tag,layerDictionary):
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
                            # print('csv data', fileName, locatorData)
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
                print('error in csv dictionary in saveAsCsv in Locator')
                return False
        except Exception as e:
            print("error in saveAsCsv in Locator", e)

    def getValidatedLocatorData(self, locatorDataDirectory, validation):
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

    def processLayerFromLayer(self, processLayerName, layerDictionary, connectorKeys):
        try:
            locatorFilePath = GeneralExceptionHandling.getJsonDataRecurssive(GeneralExceptionHandling,
                                                                             'DataFetching,filesPath',
                                                                             self.path)
            layerPath = locatorFilePath+processLayerName+'.json'
            locatorArray = []
            # print('layer path: ', layerPath)
            layerDataMain = dict()
            # print(layerDictionary)

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
                            locatorFinalData = False
                            for loactorIdInData, eachLocatorInData in locatorData.items():# new
                                for locatorId, locatorDataArray in locatorDictionary.items():
                                    if locatorId in connectorKeys:
                                        # print('locatorrrrr:::', locatorId,connectorKeys[locatorId], loactorIdInData)
                                        if connectorKeys[locatorId] == loactorIdInData:
                                            sourceDataProcessed = eachLocatorInData.upper()
                                            sourceDataProcessed = sourceDataProcessed.replace('\n', ' ')
                                            self.locatorId.append(eachLocatorInData)
                                            locatorArray.append(locatorId)
                                            locatorFinalData = self.processLocatorData(locatorDataArray,
                                                                                       sourceDataProcessed,
                                                                                       eachLocatorInData)
                                            # print('data;;', locatorFinalData)
                                        else:
                                            if connectorKeys[
                                                    locatorId] == locatorId:  # the data is in final locator
                                                sourceDataProcessed = eachLocatorInData.upper()
                                                sourceDataProcessed = sourceDataProcessed.replace('\n', ' ')
                                                self.locatorId.append(locatorId)
                                                locatorFinalData = self.processLocatorData(locatorDataArray, sourceDataProcessed, eachLocatorInData)
                                                # print('locatorFinalData', locatorFinalData)
                                                locatorArray.append(locatorId)

                                        if locatorFinalData:
                                            locatorDataDictionary[locatorId] = locatorFinalData
                                            locatorFinalData = False
                                            locatorDictionaryMain[fileName] = dict(locatorDataDictionary)# need correction
                                            locatorArray.append(locatorId)

                        validation = LocatorValidation(self.path)
                        data =  validation.validateLayer(locatorDictionaryMain, processLayerName)

                        return data

                except Exception as e:
                    print('error in  processLocatorAndGetDataFromDictionary in Locator',e)
                    # print('patter: ', patternMatch)
                    # print('patter other: ', sourceData, 'exception data')
                    return False
                return True
            else:
                print('error in source dictionary Locator sourceData', layerDataMain)
                return False
        except Exception as e:
            print('errror in processLocatorAndGetDataFromDictionary in locator', e)
            return False