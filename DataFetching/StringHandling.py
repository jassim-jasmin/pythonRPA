from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from ExceptionHandling.DirecotryHandling import DrectoryHandling

class StringHandling:
    print('string handling')
    def __init__(self, path):
        self.path = path
        self.stringMatchConfidence = 89

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
            fp = open(sourceFilePathWithDataFileName, 'r')
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
                return False

    def processLocatorAndGetDataFromFile(self, sourceFilePathWithDataFileName, locatorFilePathWithFileName):
        sourceData = self.getSourceFileData(sourceFilePathWithDataFileName)

        if sourceData:
            try:
                import re

                locatorDataArray = self.getLocatorDataArray(locatorFilePathWithFileName)
                for eachLocatorArray in locatorDataArray:
                    patternBuild = '('
                    # for eachLocator in eachLocatorArray:
                    for i in range(0,len(eachLocatorArray)):
                        if i == 0:
                            patternBuild = patternBuild+eachLocatorArray[i]
                        else:
                            patternBuild = patternBuild + '\n*.*' + eachLocatorArray[i]

                    patternBuild = patternBuild + ')'
                    searhcObj = re.search(patternBuild,sourceData)

                    # print('pattern:', patternBuild)
                    if searhcObj:
                        print('Pattern out: ', searhcObj.group())
                    else:
                        print('no match')


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
        testLocator2 = ['Dated:', 'April 18', '2019']
        testLocator3 = ['A.P.N.:', 'Title File']
        testLocator4 = ['The exclusive right to','above described']
        self.addLocatorToDictionary(testLocator)
        self.addLocatorToDictionary(testLocator2)
        self.addLocatorToDictionary(testLocator3)
        self.addLocatorToDictionary(testLocator4)

        # print(self.getLocatorData())
        sourceFilePathAndDataFileName = self.path['Data']['path'] + self.path['Data']['dataFileName']
        locatorFilePathWithFileName = self.path['DataFetching']['filesPath'] + self.path['DataFetching']['locatorDictionary']
        self.processLocatorAndGetDataFromFile(sourceFilePathAndDataFileName, locatorFilePathWithFileName)
    # def getPorttion(self, startString, endString):


