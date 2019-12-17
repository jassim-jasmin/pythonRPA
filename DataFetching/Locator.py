import json

from fuzzywuzzy import process

from ExceptionHandling.DirecotryHandling import DrectoryHandling
from DataFetching.StringHandling import StringHandling
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class Locator:
    def __init__(self, path):
        self.path = path
        self.mainLocator = dict()
        self.locatorMissMatchFlag = True
        self.locatorMissMatchDictionary = dict()
        self.locatorId = []

        self.DataFetchingFilesPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'DataFetching',
                                                                          self.path)
        self.DataFetchingFilesPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'filesPath',
                                                                          self.DataFetchingFilesPath)

        self.dataFetchingLocatorDictionary = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'DataFetching', self.path)
        self.dataFetchingLocatorDictionary = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'locatorDictionary', self.dataFetchingLocatorDictionary)

        self.locatorFileName = self.DataFetchingFilesPath+self.dataFetchingLocatorDictionary+'.json'

        fileName = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'DataFetching', self.path)
        self.dataFetchingLocatorMissMatch =  GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'locatorMissMatch', fileName)

    def getLocatorProfile(self):
        try:
            locatorData = GeneralExceptionHandling.getFileData(GeneralExceptionHandling, self.locatorFileName)
            locatorData = json.loads(locatorData)
            # print(sourceDataPath+eachTextFile, 'file')
            return locatorData

        except Exception as e:
            print('error in getLocatorProfile', e)
            return False

    def getLocatorDataFromID(self, locatorData, locatorId):
        try:
            if locatorId in locatorData:
                return locatorData[locatorId]
            else:
                print('getLocatorDataFromID has not matching ', locatorData, locatorId)
                return False
        except Exception as e:
            print('error in getFileData', e)
            return False

    def addNewStringToDictionary(self, string, fileName, locatorId):
        try:
            stringHandling = StringHandling(self.path)
            DrectoryHandling.createDirectory(DrectoryHandling, self.DataFetchingFilesPath)
            locatorData = self.getLocatorProfile()

            if locatorData:
                fileData = self.getLocatorDataFromID(locatorData, locatorId)

                if fileData:
                    data = stringHandling.getMathcFromSetInverse(string, fileData, stringHandling.stringMatchConfidence)
                    if data:
                        if stringHandling.addStringWriteFile(string, fileName, locatorId):
                            return True
                        else:
                            return False
                    else:
                        return False
                elif stringHandling.addStringWriteFile(string, fileName, locatorId):
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print('error in addNewStringToDictionary in StringHandling', e)
            return False

    def addLocatorToDictionary(self, locationStringArray, locatorId):
        try:
            for i in range(0,len(locationStringArray)):
                if i == 0:
                    locationString = locationStringArray[i].replace(':','-:-')
                else:
                    locationString = locationString + '::' + locationStringArray[i].replace('::',':|:')
            # print(locationString)
            self.addNewStringToDictionary(locationString, self.dataFetchingLocatorDictionary, locatorId)
        except Exception as e:
            print('excecption in addLocatorToDictionary', e)
            return False

    def getLocatorDataArray(self, locatorFilePathWithFileName):
        try:
            fp = open(locatorFilePathWithFileName+'.json', 'r')
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
                    bestMatch = re.sub('\d', '\d', eachLocator)
                    # print('pattern found', bestMatch)

                    if i == 0:
                        patternBuild = patternBuild + bestMatch
                    else:
                        patternBuild = patternBuild + '(.*)' + bestMatch
                else:
                    matchingFuzzyWord = stringHandling.getFuzzySearchData(eachLocator, sourceDataProcessed)
                    if len(process.extractBests(eachLocator, matchingFuzzyWord)) > 0:
                        bestMatch, confidence = process.extractBests(eachLocator, matchingFuzzyWord)[0]
                        # print(eachLocatorArray[i].upper(), 'fu::::', matchingFuzzyWord)

                        if len(matchingFuzzyWord) > 0:
                            bestMatch = GeneralExceptionHandling.regularExpressionHandling(GeneralExceptionHandling,bestMatch,0)
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
                        locatorData = stringHandling.searchDataInFuzzySearch(patternBuild, sourceDataProcessed, sourceData)

                        if locatorData:
                            # print('processLocatorData: ',locatorData)
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
                    locatorArray = []
                    locatorDataDictionary = dict()

                    locatorDictionary = self.getLocatorDataArray(locatorFilePathWithFileName)
                    self.locatorMissMatchArray = []
                    self.locatorId = []

                    for locatorId, locatorDataArray in locatorDictionary.items():
                        self.locatorId.append(locatorId)
                        # print('locatorId',locatorDataArray)
                        locatorArray = self.processLocatorData(locatorDataArray, sourceDataProcessed, sourceData)

                        if locatorArray:
                            locatorDataDictionary[locatorId] = locatorArray
                            # print('locator success')
                        else:
                            if self.locatorMissMatchFlag:
                                self.locatorMissMatchArray.append(locatorId)
                            # print('locator failed')
                    return locatorDataDictionary

                except Exception as e:
                    print('exception ',e)
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

    def processLocatorAndGetDataFromFileAll(self, locatorFilePathWithFileName, sourceDataPath):
        try:
            from ExceptionHandling.DirecotryHandling import DrectoryHandling
            drectoryHandling = DrectoryHandling()

            if sourceDataPath:
                fileNameArray = drectoryHandling.getDirectoryElementBykey(sourceDataPath, 'txt')

                if fileNameArray:

                    locatorDirectoryWithFileName = dict()

                    for eachTextFile in fileNameArray:
                        textFileData = GeneralExceptionHandling.getFileData(GeneralExceptionHandling, sourceDataPath+eachTextFile)
                        # print(sourceDataPath+eachTextFile, 'file')
                        if textFileData:
                            locatorDataDictionary = self.processLocatorAndGetDataFromFile(locatorFilePathWithFileName, textFileData)
                            if locatorDataDictionary:
                                if self.locatorMissMatchFlag:
                                    # print('locator misss match ;;;', self.locatorMissMatchArray)
                                    if len(self.locatorMissMatchArray)>0:
                                         self.locatorMissMatchDictionary[eachTextFile] = self.locatorMissMatchArray[:]
                                    else:
                                        self.locatorMissMatchDictionary[eachTextFile] = ['no match']
                                fileNameSplit = eachTextFile.split('.')
                                if len(fileNameSplit)>0:
                                    locatorDirectoryWithFileName[fileNameSplit[0]] = locatorDataDictionary

                    # print('finally ', self.locatorMissMatchDictionary)

                    return locatorDirectoryWithFileName
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
                # print('missmatch data: complete ::', saveMissMatchData)

                if fileName and self.DataFetchingFilesPath:
                    print('saving file ', self.DataFetchingFilesPath+fileName+'.json')
                    fp = open(self.DataFetchingFilesPath+fileName+'.json', 'w')
                    fp.write(saveMissMatchData)
                    fp.close()
                    # print('file name:: ', fileName)

                    csvNameWithPath = self.DataFetchingFilesPath + 'missmatch.csv'
                    headData = 'Locator miss match\n'
                    locatorMissMatchDictionary = self.locatorMissMatchDictionary
                    self.saveAsCsv(csvNameWithPath, headData, locatorMissMatchDictionary)

                    return True
                else:
                    print('error in source file or file name in locatorMissmatch')
                    return False
                    # print('data: ', saveMissMatchData)
        except Exception as e:
            print('error in saveMissMatch', e)
            # print('data: ', saveMissMatchData)
            return False

    def saveAsCsv(self, csvNameWithPath, headData,locatorMissMatchDictionary, csvHead=False):
        try:
            import csv

            with open(csvNameWithPath, 'w') as csvfile:
                csvfile.write(headData)
                fieldNames = ['file name', 'no match']
                if csvHead:
                    fieldNames.extend(csvHead)
                else:
                    fieldNames.extend(self.locatorId[:])
                writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
                writer.writeheader()
                print('csv save file:', csvNameWithPath)
                for fileName, missmatchFieldData in locatorMissMatchDictionary.items():
                    # print('csv data: ', fileName, missmatchFieldData)
                    csvEacRowLocator = dict()
                    csvEacRowLocator['file name'] = fileName

                    for data in missmatchFieldData:
                        array = []
                        dictionary = dict()

                        if type(missmatchFieldData) is  type(array):
                            csvEacRowLocator[data] = data
                        elif type(missmatchFieldData) is type(dictionary):
                            if data in missmatchFieldData:
                                csvEacRowLocator[data] = missmatchFieldData[data]
                            else:
                                print('Error json error key' + data + ' not in ')
                                print(missmatchFieldData)
                                return False
                        else:
                            return False

                        # csvEacRowLocator[data] = data

                    writer.writerow(csvEacRowLocator)
                    # print('csv ', csvEacRowLocator)
        except Exception as e:
            print("I/O error", e)

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
                                # print('file name: ', fileName, 'locator id: ', locatorId, '\nData: ', locatorData[locatorId])
                                locatorArray[locatorId] = locatorData[locatorId]
                                locatorDirectry[fileName] = locatorArray.copy()
            return locatorDirectry
        except Exception as e:
            print('error in printLocatorDataWithLocatorId in locator', e)
            return False

    def selectData(self, locatorDataWithValidation):
        try:
            print('select')
            return True
        except Exception as e:
            print('error in select data in Locator', e)
            return False