import json

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

    def test3(self):
        self.addStringWriteFile('test2', 'testFile', 'id1')

    def addStringWriteFile(self, writeData, fileName, locatorId):
        try:
            try:
                readFile = open(self.path['DataFetching']['filesPath'] + fileName+'.json', 'r')
                jsonData = json.loads(readFile.read())
                readFile.close()

                if locatorId in jsonData:
                    jsonData[locatorId].append(writeData)
                else:
                    jsonData[locatorId] = [writeData]
            except Exception as e:
                jsonData = dict()
                jsonData[locatorId] = [writeData]

            arrayElement = jsonData[locatorId]
            seen = set()

            arrayElement[:] = [item for item in arrayElement
                                if item not in seen and not seen.add(item)]
            jsonData[locatorId] = arrayElement

            fp  = open(self.path['DataFetching']['filesPath'] + fileName+'.json', 'w')

            if fp.writable():
                # fp.write(',' + writeData)
                jsonObj = json.dumps(jsonData)
                fp.write(jsonObj)
                fp.close()
                return True
            else:
                return False
        except Exception as e:
            print('error in addStringWriteFile', e)
            return False

    def getFileData(self, file, locatorId):
        try:
            fp = open(file+'.json', 'r')
            fileData = json.loads(fp.read())
            # fileData = fp.read().split(',')
            if locatorId in fileData:
                return fileData[locatorId]
            else:
                print('no data')
                return False
        except Exception as e:
            print('error in getFileData', e)
            return False

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

    def regularExpressionHandling(self, data, flag):
        if flag == 0:
            data = data.replace('\\', '\\\\')
            data = data.replace('(', '\(')
            data = data.replace(')', '\)')
            data = data.replace('.', '\.')
            data = data.replace('+', '\+')
            data = data.replace('[', '\[')
            data = data.replace(']', '\]')
            data = data.replace('|', '\|')
            data = data.replace('/', '\/')
            data = data.replace('?', '\?')
            data = data.replace('"', '\\"')
            data = data.replace('*', '\*')

            return data
        if flag == 1:
            data = data.replace('\(', '(')
            data = data.replace('\)', ')')
            data = data.replace('\.', '.')
            data = data.replace('\+', '+')
            data = data.replace('\[', '[')
            data = data.replace('\]', ']')
            data = data.replace('\|','|')
            data = data.replace('\/', '/')
            data = data.replace('\?','?')
            data = data.replace('\\"', '"')
            data = data.replace('\*', '*')
            data = data.replace('\\\\', '\\')

            return data
        else:
            print('invalid flag in regularExpressionHandling')
            return False

    def searchDataInFuzzySearch(self, patternBuild, sourceDataProcessed, sourceData):
        try:
            import re

            patternBuild = re.sub(r'\d', '\d', patternBuild)
            print(patternBuild)
            searhcObj = re.search(patternBuild, sourceDataProcessed)

            # print('pattern:', patternBuild)
            if searhcObj:
                # print('Pattern out: ', searhcObj.group())
                patternMatch = searhcObj.group()
                # print('patternMatch', patternMatch)
                patternMatch = self.regularExpressionHandling(patternMatch, 0)
                # sourceData = self.regularExpressionHandling(sourceData, 0)
                sourceData = sourceData.replace('\n', ' ')
                # print('pattern: ', patternMatch)
                # print('matching string = ', sourceData)
                sourceFileMatch = re.search(patternMatch, sourceData, re.IGNORECASE)

                if sourceFileMatch:
                    sourceFileMatchString = sourceFileMatch.group()
                    sourceFileMatchString = self.regularExpressionHandling(sourceFileMatchString, 1)
                    # print('Pattern from source file:', sourceFileMatchString)
                    return sourceFileMatchString
                else:
                    print('no match in source file')
                    print('patter: ', patternMatch)
                    print('patter other: ', sourceData)
                    return False

            else:
                print('no match', patternBuild)
        except Exception as e:
            print('error in searchDataInFuzzySearch\n', e)
            print('patter: ', patternMatch)
            print('patter other: ', sourceData)

    def processLocatorAndGetDataFromFile(self, locatorFilePathWithFileName, sourceData):
        # sourceData = self.getSourceFileData(sourceFilePathWithDataFileName).replace('\n', ' ')

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
                        # for eachLocator in eachLocatorArray:
                        for i in range(0,len(eachLocatorArray)):
                            matchingFuzzyWord = self.getFuzzySearchData(eachLocatorArray[i].upper(), sourceDataProcessed)
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
                        locatorData = self.searchDataInFuzzySearch(patternBuild, sourceDataProcessed, sourceData)

                        if locatorData:
                            locatorArray.append(locatorData)

                        # patternBuild = re.sub(r'\d', '\d', patternBuild)
                        # print(patternBuild)
                        # searhcObj = re.search(patternBuild,sourceDataProcessed)
                        #
                        # # print('pattern:', patternBuild)
                        # if searhcObj:
                        #     # print('Pattern out: ', searhcObj.group())
                        #     patternMatch = searhcObj.group(0)
                        #     # print('patternMatch', patternMatch)
                        #     patternMatch = self.regularExpressionHandling(patternMatch, 0)
                        #     sourceData = self.regularExpressionHandling(sourceData, 0)
                        #     sourceData = sourceData.replace('\n', ' ')
                        #     print('pattern: ', patternMatch)
                        #     print('matching string = ', sourceData)
                        #     sourceFileMatch = re.search(patternMatch, sourceData, re.IGNORECASE)
                        #
                        #     if sourceFileMatch:
                        #         sourceFileMatchString = sourceFileMatch.group(0)
                        #         sourceFileMatchString = self.regularExpressionHandling(sourceFileMatchString, 1)
                        #         print('Pattern from source file:', sourceFileMatchString)
                        #     else:
                        #         print('no match in source file')
                        #         print('patter: ',patternMatch)
                        #         print('patter other: ',sourceData)
                        #
                        # else:
                        #     print('no match', patternBuild)
                    # print('finallyaaaa')
                    # print(locatorArray)
                    locatorDataDictionary[locatorId] = locatorArray
                    # return locatorArray
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

    def test(self):
        try:
            testLocator = ['QUIT','CLAIM', 'DEED', 'Document Number']
            testLocator = ['010-00532-0000', 'Parcel', 'Identification Number']
            testLocator = ['GRANTOR:']
            locatorId = 'head'
            self.addLocatorToDictionary(testLocator, locatorId)
            testLocator = ['010-00532-0000', 'Parcel', 'Identification Number']
            locatorId = 'parcel'
            self.addLocatorToDictionary(testLocator, locatorId)

            from imageProcessing.imageProcessing import ImageProcessing

            if ImageProcessing.ocrImage(ImageProcessing, self.path['Data']['imageFile'], 'tif',
                                        self.path['Data']['imageFile'], self.path['Data']['path']):
                fp = open(self.path['Data']['path']+self.path['Data']['imageFile']+'.txt', encoding="utf8")
                sourceData = fp.read()
                fp.close()
                locatorFilePathWithFileName = self.path['DataFetching']['filesPath'] + self.path['DataFetching'][
                    'locatorDictionary']
                locatorDataDictionary = self.processLocatorAndGetDataFromFile(locatorFilePathWithFileName, sourceData)

                from PdfHandling.PdfHandling import PdfHanling

                for locatorFinalId, locatorDataArray in locatorDataDictionary.items():
                    print(locatorId)
                    PdfHanling.pdfGenerator(PdfHanling,self.path['Data']['path'], self.path['Data']['imageFile'],'.tif')
                    PdfHanling.highlihtPDF(PdfHanling, self.path['Data']['path'], self.path['Data']['imageFile'], locatorDataArray)
                print('ocr complete')
            else:
                print('error')
        except Exception as e:
            print('error in test ', e)

    def test2(self):
        from imageProcessing.imageProcessing import ImageProcessing

        if ImageProcessing.ocrImage(ImageProcessing, self.path['Data']['imageFile'], 'tif', self.path['Data']['imageFile'], self.path['Data']['path']):
            print('ocr complete')
        else:
            print('error')

        # self.printAllFuzzyComparison()

        # if self.addNewStringToDictionary('somethingnew', self.path['DataFetching']['startStringFiles']):
        #     print('left added')
        # if self.addNewStringToDictionary('somethingnew', self.path['DataFetching']['endStringFiles']):
        #     print('right added')

################
    #     testLocator = ['GRANT','DEED','Grantor']
    #     testLocator2 = ['Dated:', 'April 18', '2019', 'AS ABOVE']
    #     testLocator3 = ['A.P.N.:', 'Title File']
    #     testLocator4 = ['The exclusive right to','above described']
    #     testLocator5 = ['Date:', '04/18/2019']
    #     self.addLocatorToDictionary(testLocator)
    #     self.addLocatorToDictionary(testLocator2)
    #     self.addLocatorToDictionary(testLocator3)
    #     self.addLocatorToDictionary(testLocator4)
    #     self.addLocatorToDictionary(testLocator5)
    #
    #     # print(self.getLocatorData())
    #     sourceFilePathAndDataFileName = self.path['Data']['path'] + self.path['Data']['dataFileName']
    #     locatorFilePathWithFileName = self.path['DataFetching']['filesPath'] + self.path['DataFetching']['locatorDictionary']
    #     fp = open(sourceFilePathAndDataFileName, encoding="utf8")
    #     sourceData = fp.read()#.upper().replace('\n', ' ')
    #     # print(sourceData)
    #     fp.close()
    #     self.processLocatorAndGetDataFromFile(locatorFilePathWithFileName, sourceData)
    #
    #     # self.getConfidence('April 18::2019', ['Dated: April 18, 2019 David von Jr. ae ma Mail Tax Statements To: SAME AS ABOVE'])
    #     #
    #     # fileData = open(sourceFilePathAndDataFileName)
    #     # self.fuzzyExtract('GRANT', fileData, self.stringMatchConfidence)
    #     # print('FUzzySearch')
    #     # string = 'manhattan'
    #     large_string = "thelargemanhatanproject is a great project in themanhattincity"
    #     # string = 'grnt'
    #     # large_string = 'blahfa dfgrant dfas'
    #     #
    #     # for match,index in self.fuzzyExtract(string, large_string, 30):
    #     #     print('match: {}\nindex: {}'.format(match, index))
    #     #
    #     # array = self.getFuzzySearchData('DEED', sourceData, 30)
    #     # best = process.extractBests('DEED', array)
    #     # print('finnaly ', array,best)
    #
    #     #     print('match: {}\nindex: {}'.format(match, index))
    # # def getPorttion(self, startString, endString):
    # #fuzzysearch number has limitation
#
# pathFile = open('path.json', 'r')
#
# path = json.loads(pathFile.read())
# pathFile.close()
# obj = StringHandling(path['linux'])
# obj.test3()