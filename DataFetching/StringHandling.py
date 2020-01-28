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
        self.fuzzySearchOptimumLength = 6
        """ threshold will set to 90 and l_dist will be 0 for precision while less than fuzzySearchOptimumLength """

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
        dataSet = ['Test', 'geekodrive', 'geeksgeeks', 'Geeks For Geeks ', "geeks for geeks!", "geeks geeks",
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
        '''
        todo fuzzy search seperation in words
        :param qs: query string
        :param ls: large string
        :param threshold: threshold
        :return:
        '''
        '''fuzzy matches 'qs' in 'ls' and returns list of
        tuples of (word,index)
        '''

        if len(qs) < self.fuzzySearchOptimumLength:
            processThreshold = 60
            max_l_dist = 0
        else:
            processThreshold = threshold
            max_l_dist = 1

        for word, confidence in process.extractBests(qs, (ls,), score_cutoff=processThreshold):
            print('word {}'.format(word), confidence)
            for match in find_near_matches(qs, word, max_l_dist=max_l_dist):
                match = word[match.start:match.end]
                print('match {}'.format(match))
                index = ls.find(match)
                # yield (match, index)

    def getFuzzySearchData(self, qs, ls, threshold=55) -> list:
        """
        Fuzzy search data,
        This part play major role of selecting fuzzy string amoung list
        String length less than optimum result need to process seperately
        :param qs: String for serching
        :param ls: Main set of string to search in
        :param threshold: threshold for fuzzy
        :return: Fuzzy array
        :Todo: qs length might getting verry low upto 1, need to check on it, This will get wrong result
        :raises False, threshold should be standardise, otherwise no data shold be getting !!LOCATOR TAG FETCHING!!
        """
        try:
            fuzzyWordArray = []

            if len(qs)<self.fuzzySearchOptimumLength:
                processThreshold=90
                max_l_dist = 0
            else:
                processThreshold = threshold
                max_l_dist = 1

            for word, confidence in process.extractBests(qs, (ls,), score_cutoff=processThreshold):
                # print('fuzzy', qs, confidence)
                # print('word {}'.format(word))

                for match in find_near_matches(qs, word, max_l_dist=max_l_dist):
                    match = word[match.start:match.end]
                    fuzzyWordArray.append(match)



                    # if word == 'RECORDING REQUESTED BY FIRST AMERICAN TITLE AND WHEN RECORDED MAIL DOCUMENT TO: MR. AND MRS. DAVID PARRISH 14216 HALPER ROAD POWAY, CA 92064 SPACE ABOVE THIS LINE FOR RECORDER':
                    #     print(word, confidence, qs, match)
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

    def buildEachLocatorTagPattern(self, eachLocatorArray, i, sourceDataProcessed, patternBuild):
        try:
            import re

            eachLocator = eachLocatorArray[i].upper()# mjj
            """considering if a string contains number, prevent it for fuzzy search"""
            # searchOnlyNumAndCharObj = re.search(r'^[0-9-`!@#$%^&*()_+=\\|}\]\[{\';:\/\?>\.,<~ ]+$', eachLocator)
            searchOnlyNumAndCharObj = re.search(r'[0-9]', eachLocator)
            if searchOnlyNumAndCharObj:
                """ Converting number to coresponding regular expression """
                bestMatch = re.sub('\d', '\d', eachLocator)
                # print('pattern found', bestMatch)

                if i == 0:
                    patternBuild = patternBuild + bestMatch
                else:
                    patternBuild = patternBuild + '(.*)' + bestMatch

                return patternBuild
            else:
                """ Get fuzzy matching string array """
                matchingFuzzyWord = self.getFuzzySearchData(eachLocator, sourceDataProcessed)
                if len(process.extractBests(eachLocator, matchingFuzzyWord)) > 0:
                    """ 
                        Find the best amoung them
                        It is very importent for selecting appropriate confidence limit, one thing is based on string length
                        :todo: find other parameters for improving
                    """
                    if len(eachLocator) < 5:
                        confidenceLimit = 90
                    else:
                        confidenceLimit = 80

                    bestMatch, confidence = process.extractBests(eachLocator, matchingFuzzyWord, limit=1)[0]

                    if len(matchingFuzzyWord) > 0 and confidenceLimit < confidence:
                        bestMatch = self.regularExpressionHandling(bestMatch, 0)
                        if i == 0:
                            patternBuild = patternBuild + bestMatch
                        else:
                            patternBuild = patternBuild + '(.*)' + bestMatch

                        return patternBuild
                    else:
                        if i == 0 or len(eachLocatorArray) == i + 1:
                            """ if first or last locator doesnot match then no need for further process (Improvement in searching) """
                            return False
                elif len(matchingFuzzyWord) == 0 and (i == 0 or len(eachLocatorArray) == i + 1):
                    """ if first or last locator doesnot match then no need for further process (Improvement in searching) """
                    return False
        except Exception as e:
            print('error in buildEachLocatorTagPattern in StringHandling', e)
            return False

    def buildLocatorPattern(self, eachLocatorArray, sourceDataProcessed) -> str:
        """
        This one does the core logic of pattern build, need lot of improvement need to perform better
        :param eachLocatorArray: Locator array
        :param sourceDataProcessed: Processed locator data
        :return: pattern if match else False
        :Todo: Need more optimaization can improve speed and accurate
        :Todo: if a number encounter then only the word contain that part need to process, not the whole string
        """
        try:
            import re
            patternBuild = '('
            for i in range(0, len(eachLocatorArray)):
                patternBuild = self.buildEachLocatorTagPattern(eachLocatorArray, i, sourceDataProcessed, patternBuild)
                # print(eachLocatorArray)
                # print('\n',sourceDataProcessed)
                if not patternBuild:
                    return False

            patternBuild = patternBuild + ')'
            return patternBuild
        except Exception as e:
            print('error in buildLocatorPattern in StringHandling', e)
            return False

# obj = StringHandling('')
#
# Test = obj.fuzzyExtract('FNT', "FNTG Builder Services", 30)
# print(Test)