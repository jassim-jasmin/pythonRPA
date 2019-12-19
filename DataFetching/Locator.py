import json
from fuzzywuzzy import process

from ExceptionHandling.DirecotryHandling import DrectoryHandling
from DataFetching.StringHandling import StringHandling
from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class Locator:
    def __init__(self, path):
        self.path = path
        self.mainLocator = dict()

    def getLocatorProfile(self, profilePath):
        try:
            locatorPath = profilePath
            locatorPath = 'DataFetching/files/locatorDictionary.json'
            locatorData = GeneralExceptionHandling.getFileData(GeneralExceptionHandling, locatorPath)
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
            DrectoryHandling.createDirectory(DrectoryHandling, self.path['DataFetching']['filesPath'])
            locatorData = self.getLocatorProfile(profilePath='')
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
            self.addNewStringToDictionary(locationString, self.path['DataFetching']['locatorDictionary'], locatorId)
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

    def processLocatorAndGetDataFromFileAll(self, locatorFilePathWithFileName, sourceDataPath):
        try:
            from ExceptionHandling.DirecotryHandling import DrectoryHandling
            drectoryHandling = DrectoryHandling()

            textFileArray = drectoryHandling.getDirectoryElementBykey(sourceDataPath, 'txt')

            locatorDirectoryWithFileName = dict()

            for eachTextFile in textFileArray:
                textFileData = GeneralExceptionHandling.getFileData(GeneralExceptionHandling, sourceDataPath+eachTextFile)
                # print(sourceDataPath+eachTextFile, 'file')
                if textFileData:
                    locatorDataDictionary = self.processLocatorAndGetDataFromFile(locatorFilePathWithFileName, textFileData)
                    if locatorDataDictionary:
                        fileNameSplit = eachTextFile.split('.')
                        if len(fileNameSplit)>0:
                            locatorDirectoryWithFileName[fileNameSplit[0]] = locatorDataDictionary

            return locatorDirectoryWithFileName
        except Exception as e:
            print('errror in processLocatorAndGetDataFromFileAll in locator', e)
            return False

    def buildLocatorPattern(self, eachLocatorArray, sourceDataProcessed):
        try:
            patternBuild = '('
            for i in range(0, len(eachLocatorArray)):
                stringHandling = StringHandling(self.path)
                matchingFuzzyWord = stringHandling.getFuzzySearchData(eachLocatorArray[i].upper(), sourceDataProcessed)
                if len(process.extractBests(eachLocatorArray[i].upper(), matchingFuzzyWord)) > 0:
                    bestMatch, confidence = process.extractBests(eachLocatorArray[i].upper(), matchingFuzzyWord)[0]
                    # print(eachLocatorArray[i].upper(), 'fu::::', matchingFuzzyWord)

                    if len(matchingFuzzyWord) > 0:
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
                        print('pattern build: ', patternBuild)
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

                    for locatorId, locatorDataArray in locatorDictionary.items():
                        # print(locatorDataArray)
                        locatorArray = self.processLocatorData(locatorDataArray, sourceDataProcessed, sourceData)

                        if locatorArray:
                            locatorDataDictionary[locatorId] = locatorArray
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

# fp = open('../path.json', 'r')
# fileData = json.loads(fp.read())['linux']
# fp.close()
# obj = Locator(fileData)
# obj.getLocatorProfile('blah')