from DataFetching.StringHandling import StringHandling
from DataFetching.LocatorFromDB import SqlConnect
from copy import deepcopy

class Locator(StringHandling):
    def __init__(self, path):
        StringHandling.__init__(self, path)

    def addLocatorTag(self, layerName, locator, tag, group) -> bool:
        """
        Adding new tag to data set
        :param locationStringArray:
        :param locatorId:
        :param locatorJsonFileName:
        :param locatorDirectory:
        :return:
        """
        try:
            print('Layer name:', layerName, 'Locator:', locator, 'tag:', tag, 'group:', group)
            print('table:', group+layerName)
            return True
        except Exception as e:
            print('error in addNewStringToDictionary in Locator', e)
            return False

    def addLocatorToDictionary(self, locationStringArray, locatorId, locatorJsonFileName, locatorDirectory) -> bool:
        """
        todo getMathcFromSetInverse need to sync with locator data fetch
        :param locationStringArray:
        :param locatorId:
        :param locatorJsonFileName:
        :param locatorDirectory:
        :return:
        """
        try:

            if locatorDirectory and locationStringArray:
                for i in range(0,len(locationStringArray)):
                    if i == 0:
                        locationString = locationStringArray[i].replace(':','-:-')
                    else:
                        locationString = locationString + '::' + locationStringArray[i].replace('::',':|:')

                self.createDirectory(locatorDirectory)

                locatorJsonFileNamewithPath = locatorDirectory + locatorJsonFileName + '.json'

                """ If file has already data then need to append or else data is set as False for insertion """
                if self.fileStatus(locatorJsonFileNamewithPath):
                    locatorData = self.readFileAndReturnJson(locatorJsonFileNamewithPath)
                else:
                    locatorData = False

                if locatorData:
                    if locatorId in locatorData:
                        fileData = locatorData[locatorId]
                        """
                        stringMatchConfidence = 90
                        + 10 will result 100%
                        """
                        data = self.getMathcFromSetInverse(locationString, fileData, self.stringMatchConfidence+10)
                        if data:
                            if not self.addStringWriteFile(locationString, locatorJsonFileName, locatorId, locatorDirectory):
                                return False
                            """ If similar pattern already there then no need to add or send errror response Send only error response of write """
                        else:
                            print('locator adding failed, similar pattern available', locationString)
                        #     return False
                        return True
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

    def addLoatorLayer(self, layerName, data) -> bool:
        """
        Dictionary generation with locator
        :param layerName: name of layer
        :param data: json data for a layer
        :return: True if sucess else :return: False
        """
        try:
            locatorDirectory = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)

            if data:
                for locatorId, locatorData in data:
                    if not self.addLocatorToDictionary(locatorData, locatorId, layerName, locatorDirectory):
                        return False

                return True
            else:
                print('json data input for layer ' + layerName + ' is empty')
                return False
        except Exception as e:
            print('error in addLocatorLayer in Locator', e)
            return False

    def getLocatorDataArray(self, layer_name) -> dict:
        try:
            locator = []
            locatorDictionary = dict()

            # locatorJson = self.readFileAndReturnJson(locatorFilePathWithFileName)# mj

            # print('getlocatordataarray', layer_name)
            sqlConnect = SqlConnect(self.path)
            locatorJson = sqlConnect.buildLocatorJsonFileFromDb(layer_name)

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

    def processLocatorData(self, locatorDataArray, sourceDataProcessed, sourceData, priority=None):
        """
        pattern match math source file
        :param locatorDataArray: loactor array
        :param sourceDataProcessed: processed source data, that is capitalize, remove new line...
        :param sourceData: original source file
        :return: match data if error then :return: False
        :todo: Prioritize
        """
        try:
            if locatorDataArray:
                if priority == None:
                    for eachLocatorArray in locatorDataArray:
                        # print('array',eachLocatorArray)
                        patternBuild = self.buildLocatorPattern(eachLocatorArray, sourceDataProcessed)

                        if patternBuild:
                            locatorData = self.reSelect(patternBuild, sourceDataProcessed, sourceData)

                            if locatorData:
                                # print('found;;;;', locatorData)
                                return locatorData
                else:
                    index = 0
                    locatorIndexArray = []
                    for eachLocatorArray in locatorDataArray:
                        index = index + 1
                        # print('locator array', eachLocatorArray)
                        patternBuild = self.buildLocatorPattern(eachLocatorArray, sourceDataProcessed)

                        if patternBuild:
                            locatorData = self.reSelect(patternBuild, sourceDataProcessed, sourceData)

                            if locatorData:
                                # print('found;;;;', locatorData)
                                locatorIndexArray.append((locatorData, index))
                    if len(locatorIndexArray):
                        filterData = self.filterLocatorArray(locatorIndexArray, priority)
                        if filterData:
                            return filterData
            return False

        except Exception as e:
            print('error in processLocatorData in Locator', e)
            return False

    def filterLocatorArray(self, locatorIndexArray, priority):
        """
        To avoid terminating the first occurence of multiple locator
        :param locatorIndexArray: For futer index wise prioritizing
        :param priority: prioirty method flag
        :return: priority result
        :todo: only prioritizing string length is done. If necessory of other methode add the logic
        """
        try:
            string = False
            length = 0
            if priority == 'stringLength':
                for locator, index in locatorIndexArray:
                    locatorLength = len(locator)
                    # print(locator, index)
                    if locatorLength > length:
                        string = locator
                        length = locatorLength
                        # print(locator, length, 'max')
                return string
        except Exception as e:
            print('error in filterLcatorArray in Locator',e)
            return False

    def locatorDataSearchAndReplace(self, layerDataMain, searchLayer):
        try:
            searchLocatorDictionary = self.getLocatorDataArray(searchLayer)
            # layerData = layerDataMain.copy()

            """ Since the dictionary has nested dictionary, it will always copy by refernce for inner dictionary """
            layerData = deepcopy(layerDataMain)
            if 'locatorData' in layerData:
                locatorDictionaryProcessed = layerData['locatorData']

                for fileName, locator in list(locatorDictionaryProcessed.items()):
                    if locator:
                        for locatorId, locatorData in list(locator.items()):
                            match = False
                            if searchLocatorDictionary:
                                for searchLocatorId, searchLocatorDataArray in searchLocatorDictionary.items():
                                    if locatorId == searchLocatorId:
                                        matchTouple = self.getMathcFromSet(locatorData.strip(), searchLocatorDataArray, 90)
                                        if matchTouple:
                                            match = matchTouple[0]

                            if match:
                                locator[locatorId] = match[0]
                            else:
                                locator.pop(locatorId)
                        if not locator:
                            locatorDictionaryProcessed.pop(fileName)
                if layerData:
                    return layerData
                else:
                    return False
            else:
                print('Layer structure error, locatorData is not there')
                return False
        except Exception as e:
            print('error in locatorDataSearchAndReplace in Locator', e)
            return False