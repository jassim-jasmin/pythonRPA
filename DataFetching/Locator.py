import json
from fuzzywuzzy import process

from ExceptionHandling.DirecotryHandling import DrectoryHandling

class Locator:
    def addNewStringToDictionary(self, string, fileName, locatorId):
        try:
            DrectoryHandling.createDirectory(DrectoryHandling, self.path['DataFetching']['filesPath'])
            fileData = self.getFileData(self.path['DataFetching']['filesPath'] + fileName, locatorId)
            if fileData:
                data = self.getMathcFromSetInverse(string, fileData, self.stringMatchConfidence)
                if data:
                    if self.addStringWriteFile(string, fileName, locatorId):
                        return True
                    else:
                        return False
                else:
                    return False
            elif self.addStringWriteFile(string, fileName, locatorId):
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
                    # self.addNewStringToDictionary(locationStringArray[i], self.path['DataFetching']['startStringFiles'])
                else:
                    locationString = locationString + '::' + locationStringArray[i].replace('::',':|:')
                    # self.addNewStringToDictionary(locationStringArray[i], self.path['DataFetching']['endStringFiles'])
                    # if i != len(locationStringArray)-1:
                    #     self.addNewStringToDictionary(locationStringArray[i],
                    #                                 self.path['DataFetching']['startStringFiles'])
            # print(locationString)
            self.addNewStringToDictionary(locationString, self.path['DataFetching']['locatorDictionary'], locatorId)
        except Exception as e:
            print('excecption in addLocatorToDictionary', e)
            return False

    def getLocatorDataArray(self, locatorFilePathWithFileName):
        try:
            # fp = open(, 'r')
            fp = open(locatorFilePathWithFileName+'.json', 'r')
            # locatorArray = fp.read().split(',')
            locatorJson = json.loads(fp.read())
            locator = []
            locatorDictionary = dict()

            # print(locatorJson)
            for locatorId, locatorArray in locatorJson.items():
                print(locatorId, locatorArray)
                for locatorData in locatorArray:
                    indeces = locatorData.split('::')
                    for i in range(0,len(indeces)):
                        indeces[i] = indeces[i].replace('-:-', ':')
                    locator.append(indeces)
                locatorDictionary[locatorId] = locator
                locator = []

            return locatorDictionary
        except Exception as e:
            print('error in getLocatorData in stringHandling', e)
            return False
        finally:
            try:
                fp.close()
            except Exception as e:
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
                        for eachLocatorArray in locatorDataArray:
                            patternBuild = '('
                            for i in range(0,len(eachLocatorArray)):
                                matchingFuzzyWord = self.getFuzzySearchData(eachLocatorArray[i].upper(), sourceDataProcessed)
                                bestMatch,confidence = process.extractBests(eachLocatorArray[i].upper(), matchingFuzzyWord)[0]
                                # print(eachLocatorArray[i].upper(), 'fu::::', matchingFuzzyWord)

                                if len(matchingFuzzyWord)>0:
                                    if i == 0:
                                        patternBuild = patternBuild+bestMatch
                                    else:
                                        patternBuild = patternBuild + '(.*)' + bestMatch

                            patternBuild = patternBuild + ')'
                            locatorData = self.searchDataInFuzzySearch(patternBuild, sourceDataProcessed, sourceData)

                            if locatorData:
                                locatorArray.append(locatorData)

                        locatorDataDictionary[locatorId] = locatorArray
                    return locatorDataDictionary

                except Exception as e:
                    print('exception ',e)
                    # print('patter: ', patternMatch)
                    # print('patter other: ', sourceData, 'exception data')
                    return False
                return True
            else:
                print('error in source file')
                return False
        except Exception as e:
            print('errror in processLocatorAndGetDataFromFile in locator', e)
            return False