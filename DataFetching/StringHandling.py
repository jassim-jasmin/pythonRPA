from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from ExceptionHandling.DirecotryHandling import DrectoryHandling

class StringHandling:
    print('string handling')
    def __init__(self, path):
        self.path = path
        self.stringMatchConfidence = 90

    def getMatchOfEach(self,string, stringSet, confidence):
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

    def getMathcFromSet(self,string, stringSet, confidence):
        try:
            match = process.extractOne(string, stringSet)

            if match[1]>confidence:
                return match
            else:
                return False
        except Exception as e:
            print('error in getMatchFromSet in StringHandling')

    def getConfidence(self, string, stringSet):
        try:
            print('extractone confidence: ', process.extractOne(string, stringSet))
            print('extract confidence: ', process.extract(string, stringSet))
            print('extractbests: ', process.extractBests(string, stringSet))
            print('extractwithoutorder: ', process.extractWithoutOrder(string, stringSet))
        except Exception as e:
            print(e)

    def getMathcFromSetInverse(self,string, stringSet, confidence):
        try:
            match = process.extractOne(string, stringSet)

            if match[1]<confidence:
                return match
            else:
                return False
        except Exception as e:
            print('error in getMatchFromSet in StringHandling')

    def fuzzComparison(self, mainText, compareText):
        print('mainText : %s, compareText : %s' %(mainText,compareText))
        print('ration : %f' %(fuzz.ratio(mainText,compareText)))
        print('partial_ratio : %f' %(fuzz.partial_ratio(mainText,compareText)))
        print('token_sort_ratio : %f' %(fuzz.token_sort_ratio(mainText,compareText)))
        print('token_set_ratio : %f' %(fuzz.token_set_ratio(mainText,compareText)))
        print('WRatio : %f\n' %(fuzz.WRatio('geeks for geeks', 'Geeks For Geeks')))

    def printAllFuzzyComparison(self):
        dataSet = ['test', 'geekodrive', 'geeksgeeks', 'Geeks For Geeks ', "geeks for geeks!", "geeks geeks",
                   "for geeks geeks", "geeks for for geeks", 'geeks for geeks!!!']

        compareText = 'geeksforgeeks'
        for data in dataSet:
            self.fuzzComparison(compareText, data)
        print(self.getMatchOfEach(compareText, dataSet, self.stringMatchConfidence))
        print(self.getMathcFromSet(compareText, dataSet, self.stringMatchConfidence))

    def addStringWriteFile(self, writeData, fileName):
        try:
            fp = open(self.path['DataFetching']['filesPath'] + fileName, 'a')

            if fp.writable():
                fp.write(',' + writeData)
                return True
            else:
                return False
        except Exception as e:
            print('error in addStringWriteFile')
            return False
        finally:
            fp.close()

    def getFileData(self, file):
        try:
            fp = open(file, 'r')

            fileData = fp.read().split(',')

            return fileData[1:]
        except Exception as e:
            return False

    def addNewStringToDictionary(self, string, fileName):
        try:
            DrectoryHandling.createDirectory(DrectoryHandling, self.path['DataFetching']['filesPath'])
            fileData = self.getFileData(self.path['DataFetching']['filesPath'] + fileName)
            if fileData:
                data = self.getMathcFromSetInverse(string, fileData, self.stringMatchConfidence)
                if data:
                    if self.addStringWriteFile(string, fileName):
                        return True
                    else:
                        return False
                else:
                    return False
            elif self.addStringWriteFile(string, fileName):
                return True
            else:
                return False
        except Exception as e:
            print('error in addNewStringToDictionary in StringHandling', e)
            return False

    def addLocatorToDictionary(self, locationStringArray):
        try:
            for i in range(0,len(locationStringArray)):
                if i == 0:
                    locationString = locationStringArray[i].replace(':','-:-')
                    self.addNewStringToDictionary(locationStringArray[i], self.path['DataFetching']['startStringFiles'])
                else:
                    locationString = locationString + '::' + locationStringArray[i].replace('::',':|:')
                    self.addNewStringToDictionary(locationStringArray[i], self.path['DataFetching']['endStringFiles'])
                    if i != len(locationStringArray)-1:
                        self.addNewStringToDictionary(locationStringArray[i],
                                                    self.path['DataFetching']['startStringFiles'])
            print(locationString)
            self.addNewStringToDictionary(locationString, self.path['DataFetching']['locatorDictionary'])
        except Exception as e:
            print('excecption in addLocatorToDictionary', e)
            return False

    def getLocatorDataArray(self, locatorFilePathWithFileName):
        try:
            # fp = open(, 'r')
            fp = open(locatorFilePathWithFileName, 'r')
            locatorArray = fp.read().split(',')

            locator = []

            for locatorData in locatorArray:
                indeces = locatorData.split('::')
                for i in range(0,len(indeces)):
                    indeces[i] = indeces[i].replace('-:-', ':')

                locator.append(indeces)

            return locator[1:]
        except Exception as e:
            print('error in getLocatorData in stringHandling', e)
            return False
        finally:
            try:
                fp.close()
            except Exception as e:
                return False

    def getSourceFileData(self, sourceFilePathWithDataFileName):
        try:
            fp = open(sourceFilePathWithDataFileName, encoding="utf8")
            # fp = open(self.path['Data']['path'] + self.path['Data']['dataFileName'])
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
        from fuzzysearch import find_near_matches

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

    def getFuzzySearchData(self, qs, ls, threshold=30):
        try:
            from fuzzysearch import find_near_matches

            '''fuzzy matches 'qs' in 'ls' and returns list of
            tuples of (word,index)
            '''

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

    def processLocatorAndGetDataFromFile(self, sourceFilePathWithDataFileName, locatorFilePathWithFileName, sourceData):
        # sourceData = self.getSourceFileData(sourceFilePathWithDataFileName).replace('\n', ' ')

        if sourceData:
            try:
                import re

                sourceData = sourceData.upper()
                sourceData = sourceData.replace('\n', ' ')

                locatorDataArray = self.getLocatorDataArray(locatorFilePathWithFileName)
                for eachLocatorArray in locatorDataArray:
                    patternBuild = '('
                    # for eachLocator in eachLocatorArray:
                    for i in range(0,len(eachLocatorArray)):
                        matchingFuzzyWord = self.getFuzzySearchData(eachLocatorArray[i].upper(), sourceData)
                        bestMatch,confidence = process.extractBests(eachLocatorArray[i].upper(), matchingFuzzyWord)[0]
                        # print(eachLocatorArray[i].upper(), 'fu::::', matchingFuzzyWord)

                        if len(matchingFuzzyWord)>0:
                            if i == 0:
                                patternBuild = patternBuild+bestMatch
                                # patternBuild = patternBuild+eachLocatorArray[i]
                                # patternBuild = patternBuild+matchingFuzzyWord[0]
                            else:
                                patternBuild = patternBuild + '(.*)' + bestMatch
                                # patternBuild = patternBuild + '(.*)' + matchingFuzzyWord[0]
                                # patternBuild = patternBuild + '(.*)' + eachLocatorArray[i]

                    patternBuild = patternBuild + ')'
                    patternBuild = re.sub(r'\d', '\d', patternBuild)
                    print(patternBuild)
                    searhcObj = re.search(patternBuild,sourceData)

                    # print('pattern:', patternBuild)
                    if searhcObj:
                        print('Pattern out: ', searhcObj.group())
                    else:
                        print('no match', patternBuild)


            except Exception as e:
                print(e)
                return False
            return True
        else:
            print('error in source file')
            return False


    def test(self):
        # self.printAllFuzzyComparison()

        # if self.addNewStringToDictionary('somethingnew', self.path['DataFetching']['startStringFiles']):
        #     print('left added')
        # if self.addNewStringToDictionary('somethingnew', self.path['DataFetching']['endStringFiles']):
        #     print('right added')

        testLocator = ['GRANT','DEED','Grantor']
        testLocator2 = ['Dated:', 'April 18', '2019', 'AS ABOVE']
        testLocator3 = ['A.P.N.:', 'Title File']
        testLocator4 = ['The exclusive right to','above described']
        testLocator5 = ['Date:', '04/18/2019']
        self.addLocatorToDictionary(testLocator)
        self.addLocatorToDictionary(testLocator2)
        self.addLocatorToDictionary(testLocator3)
        self.addLocatorToDictionary(testLocator4)
        self.addLocatorToDictionary(testLocator5)

        # print(self.getLocatorData())
        sourceFilePathAndDataFileName = self.path['Data']['path'] + self.path['Data']['dataFileName']
        locatorFilePathWithFileName = self.path['DataFetching']['filesPath'] + self.path['DataFetching']['locatorDictionary']
        fp = open(sourceFilePathAndDataFileName, encoding="utf8")
        sourceData = fp.read().upper().replace('\n', ' ')
        print(sourceData)
        fp.close()
        self.processLocatorAndGetDataFromFile(sourceFilePathAndDataFileName, locatorFilePathWithFileName, sourceData
                                              )

        # self.getConfidence('April 18::2019', ['Dated: April 18, 2019 David von Jr. ae ma Mail Tax Statements To: SAME AS ABOVE'])
        #
        # fileData = open(sourceFilePathAndDataFileName)
        # self.fuzzyExtract('GRANT', fileData, self.stringMatchConfidence)
        # print('FUzzySearch')
        # string = 'manhattan'
        large_string = "thelargemanhatanproject is a great project in themanhattincity"
        # string = 'grnt'
        # large_string = 'blahfa dfgrant dfas'
        #
        # for match,index in self.fuzzyExtract(string, large_string, 30):
        #     print('match: {}\nindex: {}'.format(match, index))
        #
        # array = self.getFuzzySearchData('DEED', sourceData, 30)
        # best = process.extractBests('DEED', array)
        # print('finnaly ', array,best)

        #     print('match: {}\nindex: {}'.format(match, index))
    # def getPorttion(self, startString, endString):
    #fuzzysearch number has limitation


