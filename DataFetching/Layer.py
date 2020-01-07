from ExceptionHandling.DirecotryHandling import DrectoryHandling
# from DataFetching.StringHandling import StringHandling
from DataFetching.validation import LocatorValidation
from DataFetching.Locator import Locator
from ExceptionHandling.CSVHandling import CsvHandling

class Layer(LocatorValidation, DrectoryHandling, Locator):
    def __init__(self, path):
        """
        :todo: need to add profile for Layer
        :todo: cannot map two parent locator to a single child locator
        :param path: Basic argument
        """
        self.path = path
        # StringHandling.__init__(self, path)
        LocatorValidation.__init__(self, path)
        DrectoryHandling.__init__(self)
        Locator.__init__(self, path)
        self.mainLocator = dict()
        self.DataFetchingFilesPath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)

    def addLayerProfile(self, profileName):
        try:
            return self.createDirectory(self.DataFetchingFilesPath+profileName)
        except Exception as e:
            print('error in addLayerProfile in Locator', e)
            return False

    def processLayerAndGetDataFromFile(self, locatorFilePathWithFileName, sourceData):
        """
        Single file layer processing
        :param locatorFilePathWithFileName: Layer name with path extension
        :param sourceData: Source data
        :return: Layer data and locator array with ',' seperated
        :todo: processLocatorData return first match modify to priorites
        """
        try:
            if sourceData:
                try:
                    import re

                    sourceDataProcessed = sourceData.upper()
                    sourceDataProcessed = sourceDataProcessed.replace('\n', ' ')
                    locatorDataDictionary = dict()

                    locatorDictionary = self.getLocatorDataArray(locatorFilePathWithFileName)
                    locatorArray = []

                    if locatorDictionary:
                        for locatorId, locatorDataArray in locatorDictionary.items():
                            locatorArray.append(locatorId)
                            """ From locator array first matching will return """
                            locatorData = self.processLocatorData(locatorDataArray, sourceDataProcessed, sourceData, 'stringLength')

                            if locatorData:
                                locatorDataDictionary[locatorId] = locatorData
                        return locatorDataDictionary, locatorArray
                    else:
                        print('error Layer ', locatorFilePathWithFileName, ' has no data', locatorDictionary, locatorFilePathWithFileName)
                        exit()

                except Exception as e:
                    print('error in processLayerAndGetDataFromFile in Locator ',e)
                    return False
                return True
            else:
                print('error in source file Layer sourceData', sourceData)
                return False
        except Exception as e:
            print('errror in processLayerrAndGetDataFromFile in locator', e)
            return False

    def processLayerAndGetDataFromFileAll(self, layerName, sourceDataPath) -> dict:
        """
        Layer arrangement
        :param layerName: Name of layer
        :param sourceDataPath: location of directory
        :return: Locator directory :return: False if error
        """
        try:
            import sys
            layerFilePath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            locatorFilePathWithFileName = layerFilePath+layerName+'.json'

            if sourceDataPath:
                fileNameArray = self.getDirectoryElementBykey(sourceDataPath, 'txt')

                if fileNameArray:
                    locatorDirectoryWithFileName = dict()
                    layerDictionary = dict()
                    locatorArrayMain = []

                    for eachTextFile in fileNameArray:
                        textFileData = self.getFileData(sourceDataPath+eachTextFile)
                        if textFileData:
                            locatorDataDictionary, locatorArray = self.processLayerAndGetDataFromFile(locatorFilePathWithFileName, textFileData)
                            locatorArrayMain.extend(locatorArray)
                            if locatorDataDictionary:
                                fileNameSplit = eachTextFile.split('.')
                                if len(fileNameSplit)>0:
                                    locatorDirectoryWithFileName[fileNameSplit[0]] = locatorDataDictionary
                        else:
                            exit()
                        # print('Test break')
                        # break
                    """ If validation file available then only need of validation """
                    validationStatus = self.fileStatus(layerFilePath+layerName+'_validation.json')
                    if validationStatus:
                        self.validateLayer(locatorDirectoryWithFileName, layerName)
                    else:
                        locatorArrayMain = self.removeArrayDuplicate(locatorArrayMain)
                        layerDictionary['locator'] = locatorArrayMain
                        layerDictionary['locatorData'] = locatorDirectoryWithFileName
                        return layerDictionary
                else:
                    print('error no data in ', sourceDataPath, ' Processing layer failed')
                    return False
            else:
                print('error in argument sourceDataPath in processLayerAndGetDataFromFileAll')
                return False

        except Exception as e:
            print('errror in processLayerAndGetDataFromFileAll in locator', e)
            return False

    def getValidatedLocatorData(self, locatorDataDirectory, validation) -> dict:
        try:
            locatorDirectry = dict()
            for fileName, locatorData in locatorDataDirectory.items():
                locatorArray = dict()
                if fileName in validation:
                    validationDirectory = validation[fileName]
                    for locatorId, validationStatus in validationDirectory.items():
                        if validationStatus:
                            if locatorId in locatorData:
                                locatorArray[locatorId] = locatorData[locatorId]
                                locatorDirectry[fileName] = locatorArray.copy()
            return locatorDirectry
        except Exception as e:
            print('error in printLocatorDataWithLocatorId in locator', e)
            return False

    def processLayerFromLayer(self, processLayerName, layerDictionary, connectorKeys) -> dict:
        """
        Locator selection on another layer
        :param processLayerName: new layer name
        :param layerDictionary: Already processed layer dictionary
        :param connectorKeys: connector for new layer and existing dictionary layer
        :return: new layer data
        :Todo: if existing dictionary has no data then new layer further process is no need
        :Todo: Locator id is always appending to the dictionary can avoid that
        :todo: locator array and locator data in layer need to optimize, it is updating after checking validation can modify either from validation or before giving to validation
        :todo: dictionary is creating unecessorly, need to find other methodes to replace this strategy
        """
        try:
            locatorFilePath = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            layerPath = locatorFilePath+processLayerName+'.json'
            locatorArray = []
            layerDataMain = dict()

            if 'locatorData' in layerDictionary:
                layerData = layerDictionary['locatorData']
            else:
                layerData = False

            if layerData:
                try:
                    """ Collecting existing layer DATA dictionary """
                    dataDictionary = layerData  # primary dictionary
                    if 'locator' in layerDictionary:
                        locatorArray = layerDictionary['locator']
                    locatorDataDictionary = dict()

                    """ Collecting new layer dictionary """
                    locatorDictionary = self.getLocatorDataArray(layerPath)
                    if locatorDictionary and dataDictionary:
                        locatorDictionaryMain = dict()

                        for fileName, locatorData in dataDictionary.items():# main
                            for loactorIdInData, eachLocatorInData in locatorData.items():# new
                                if eachLocatorInData:
                                    """ Converting to upper case and removing new line for regular expression processing """
                                    sourceDataProcessed = eachLocatorInData.upper()
                                    sourceDataProcessed = sourceDataProcessed.replace('\n', ' ')

                                    for locatorId, locatorDataArray in locatorDictionary.items():
                                        locatorDataDictionary = dict()
                                        """ new layer locator id is available in connector keys """
                                        if locatorId in connectorKeys:
                                            """
                                                new layer id equals existing layer data dictionary id
                                                only then need to process locator
                                            """
                                            if connectorKeys[locatorId] == loactorIdInData:
                                                locatorArray.append(locatorId)
                                                locatorFinalData = self.processLocatorData(locatorDataArray,
                                                                                           sourceDataProcessed,
                                                                                           eachLocatorInData, 'stringLength')
                                                if locatorFinalData:
                                                    locatorDataDictionary[locatorId] = locatorFinalData
                                                    locatorDictionaryMain[fileName] = dict(locatorDataDictionary)# need correction
                                                    locatorArray.append(locatorId)
                                        else:
                                            print('invalid locator connector ', locatorId , ' not in ', connectorKeys)
                                            return False

                        if bool(locatorDictionaryMain):
                            validatedLayer = self.validateLayer(locatorDictionaryMain, processLayerName)
                            """ validation performs """
                            if validatedLayer:
                                return validatedLayer
                            else:
                                locatorArray = self.removeArrayDuplicate(locatorArray)
                                layerDictionaryFinal = dict()
                                layerDictionaryFinal['locator'] = locatorArray
                                layerDictionaryFinal['locatorData'] = locatorDictionaryMain
                                return layerDictionaryFinal
                        else:
                            print('empty layer:', processLayerName, locatorDictionaryMain)
                            return False
                    else:
                        print('layer ' + processLayerName + ' is not defined')
                        return False

                except Exception as e:
                    print('error in  processLocatorAndGetDataFromDictionary in Locator',e)
                    return False
                # return True
            else:
                print('error in source dictionary Layer sourceData', layerData, layerDictionary)
                return False
        except Exception as e:
            print('errror in processLocatorAndGetDataFromDictionary in locator', e)
            return False

    def fetchDataOverLayers(self, layerArray):
        """
        Merging multiple layer to one
        :param layerArray: Array of layer
        :return: Merged single layer
        :todo: multiple layer connector not applayed
        """
        try:
            mainLayerData = dict()
            locatorArray = []

            if len(layerArray)>0:
                """ Multiple layer ditected """
                for eachLayer in layerArray:
                    flag = True
                    """ Need to connector inside locator """
                    if 'locator' in eachLayer:
                        locatorArray.extend(eachLayer['locator'])

                    if 'locatorData' in eachLayer:
                        eachLayerData = eachLayer['locatorData']

                        for fileName, eachLocator in eachLayerData.items():
                            """ file name having different id is comming then old will be replaced by old """
                            if fileName in mainLayerData:
                                mainLayerData[fileName].update(eachLocator)
                            else:
                                mainLayerData[fileName] = eachLocator
                    else:
                        print('error locatorData not found in dictionary ', eachLayer)
                        return False
                locatorArray = self.removeArrayDuplicate(locatorArray)

                return {'locator': locatorArray, 'locatorData' : mainLayerData}
            else:
                """ Layer array zeror """
                return False

            return True
        except Exception as e:
            print('error in fetchSpecificDataOverLayer in Layer', e)
            return False
