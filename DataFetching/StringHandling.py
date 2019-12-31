import json
from fuzzysearch import find_near_matches
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

class StringHandling(GeneralExceptionHandling):
    def __init__(self, path):
        GeneralExceptionHandling.__init__(self)
        self.path = path
        self.stringMatchConfidence = 90

    def getMatchOfEach(self,string, stringSet, confidence) -> list:
        """It is a fuzzywuzzy process extract output only returns with confidence"""
        try:
            matchSet = process.extract(string, stringSet)

            matchArray = []

            for string,confidenceValue in matchSet:
                if confidenceValue > confidence:
                    matchArray.append((string,confidence))
            return matchArray
        except Exception as e:
            print('error in getMatchEach in StringHandling', e)
            return False

    def getMathcFromSet(self,string, stringSet, confidence) -> str:
        """It is a fuzzywuzzy process extractOne output only returns with confidence"""
        try:
            match = process.extractOne(string, stringSet)

            if match[1]>confidence:
                return match
            else:
                return False
        except Exception as e:
            print('error in getMatchFromSet in StringHandling')

    def getConfidence(self, string, stringSet):
        """Print each values of extractOne,extract,extractBests,extractWithoutOrder of fuzzywuzz process for visualizing the output"""
        try:
            print('extractone confidence: ', process.extractOne(string, stringSet))
            print('extract confidence: ', process.extract(string, stringSet))
            print('extractbests: ', process.extractBests(string, stringSet))
            print('extractwithoutorder: ', process.extractWithoutOrder(string, stringSet))
        except Exception as e:
            print('Error in getConfidence in StringHandling', e)

    def getMathcFromSetInverse(self,string, stringSet, confidence) -> str:
        """Fuzzywuzz process extractOne output with less confidence level"""
        try:
            match = process.extractOne(string, stringSet)

            if match[1]<confidence:
                return match
            else:
                return False
        except Exception as e:
            print('error in getMatchFromSet in StringHandling')

    def fuzzComparison(self, mainText, compareText):
        """Fuzzywuzz string comparison for each fuzzy options"""
        print('mainText : %s, compareText : %s' %(mainText,compareText))
        print('ration : %f' %(fuzz.ratio(mainText,compareText)))
        print('partial_ratio : %f' %(fuzz.partial_ratio(mainText,compareText)))
        print('token_sort_ratio : %f' %(fuzz.token_sort_ratio(mainText,compareText)))
        print('token_set_ratio : %f' %(fuzz.token_set_ratio(mainText,compareText)))
        print('WRatio : %f\n' %(fuzz.WRatio('geeks for geeks', 'Geeks For Geeks')))

    def printAllFuzzyComparison(self):
        """Testing each word with compare text Fuzzy monitoring"""
        dataSet = ['test', 'geekodrive', 'geeksgeeks', 'Geeks For Geeks ', "geeks for geeks!", "geeks geeks",
                   "for geeks geeks", "geeks for for geeks", 'geeks for geeks!!!']

        compareText = 'geeksforgeeks'
        for data in dataSet:
            self.fuzzComparison(compareText, data)
        print(self.getMatchOfEach(compareText, dataSet, self.stringMatchConfidence))
        print(self.getMathcFromSet(compareText, dataSet, self.stringMatchConfidence))

    def addStringWriteFile(self, writeData, fileName, locatorId, filePath) -> bool:
        """Read data in a json file and add write data to the existing file and remove duplicate"""
        try:
            try:
                jsonData = self.readFileAndReturnJson(filePath + fileName+'.json')

                if locatorId in jsonData:
                    jsonData[locatorId].append(writeData)
                else:
                    jsonData[locatorId] = [writeData]
            except Exception as e:
                jsonData = dict()
                jsonData[locatorId] = [writeData]

            arrayElement = jsonData[locatorId]
            jsonData[locatorId] = self.removeArrayDuplicate(arrayElement)

            if self.writeJsonDataToFile(jsonData, self.getJsonDataRecurssive('DataFetching,filesPath', self.path) + fileName+'.json'):
                return True
            else:
                return False
        except Exception as e:
            print('error in addStringWriteFile', e)
            return False

    def getSourceFileData(self, sourceFilePathWithDataFileName) -> str:
        try:
            fp = open(sourceFilePathWithDataFileName, encoding="utf8")
            sourceData = fp.read()

            return sourceData
        except Exception as e:
            print('error in getSourceFileData in stringHandling ', e)
            return False
        finally:
            try:
                fp.close()
            except Exception as e:
                print('error in cloasing file', e)
                return False

    def fuzzyExtract(self, qs, ls, threshold):
        '''fuzzy matches 'qs' in 'ls' and returns list of
        tuples of (word,index)
        '''
        for word, _ in process.extractBests(qs, (ls,), score_cutoff=threshold):
            print('word {}'.format(word))
            for match in find_near_matches(qs, word, max_l_dist=1):
                match = word[match.start:match.end]
                print('match {}'.format(match))
                index = ls.find(match)
                yield (match, index)

    def getFuzzySearchData(self, qs, ls, threshold=30) -> list:
        try:
            """fuzzy matches 'qs' in 'ls' and returns list of
            tuples of (word,index)
            """

            fuzzyWordArray = []
            for word, _ in process.extractBests(qs, (ls,), score_cutoff=threshold):
                # print('word {}'.format(word))
                for match in find_near_matches(qs, word, max_l_dist=1):
                    match = word[match.start:match.end]
                    fuzzyWordArray.append(match)
            return fuzzyWordArray
        except Exception as e:
            print('error in getFuzzySearchData in stringHandling', e)
            return False


    def reSelect(self, patternBuild, sourceDataProcessed, sourceData) -> str:
        """:returns regualr expression out put of :var patternBuild
        :argument patternBuild is a regular expression
        :argument sourceDataProcessed is regular expression applying data
        :argument sourceData is original data
        :returns matched string if not :returns False"""
        try:
            import re

            patternBuild = re.sub(r'\d', '\d', patternBuild)
            searhcObj = re.search(patternBuild, sourceDataProcessed)

            # print('pattern:', patternBuild)
            if searhcObj:
                patternMatch = searhcObj.group()
                patternMatch = self.regularExpressionHandling(patternMatch, 0)
                sourceData = sourceData.replace('\n', ' ')
                sourceFileMatch = re.search(patternMatch, sourceData, re.IGNORECASE)

                if sourceFileMatch:
                    sourceFileMatchString = GeneralExceptionHandling.regularExpressionHandling(GeneralExceptionHandling, patternMatch, 1)
                    return sourceFileMatchString
                else:
                    return False

            else:
                return False
        except Exception as e:
            print('error in searchDataInFuzzySearch\n', e)
            print(patternBuild)
            print('patter: ', patternMatch)
            print('patter other: ', sourceData)
