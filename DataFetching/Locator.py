from DataFetching.StringHandling import StringHandling

class Locator(StringHandling):
    def __init__(self, path):
        StringHandling.__init__(self, path)

    def processLocatorData(self, locatorDataArray, sourceDataProcessed, sourceData):
        """
        pattern match math source file
        :param locatorDataArray: loactor array
        :param sourceDataProcessed: processed source data, that is capitalize, remove new line...
        :param sourceData: original source file
        :return: match data if error then :return: False
        """
        try:
            if locatorDataArray:
                for eachLocatorArray in locatorDataArray:
                    patternBuild = self.buildLocatorPattern(eachLocatorArray, sourceDataProcessed)

                    if patternBuild:
                        locatorData = self.reSelect(patternBuild, sourceDataProcessed, sourceData)

                        if locatorData:
                            # print('found;;;;', locatorData)
                            return locatorData
            return False

        except Exception as e:
            print('error in processLocatorData in Locator', e)
            return False

    def addLocatorToDictionary(self, locationStringArray, locatorId, locatorJsonFileName, locatorDirectory) -> bool:
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

    def getLocatorDataArray(self, locatorFilePathWithFileName) -> dict:
        try:
            locator = []
            locatorDictionary = dict()

            locatorJson = self.readFileAndReturnJson(locatorFilePathWithFileName)

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