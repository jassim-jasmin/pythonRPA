from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.validation import LocatorValidation
from DataFetching.Locator import Locator

class DataFetchingMain(Locator, GeneralExceptionHandling):
    def __init__(self, path):
        self.path = path
        Locator.__init__(self, path)
        GeneralExceptionHandling.__init__(self)

    def generateOCR(self, imagesPath, ocrTextPath):
        try:
            from imageProcessing.imageProcessing import ImageProcessing
            imageProcessing = ImageProcessing(self.path)

            imageNameKey = 'tif'

            return imageProcessing.ocrAllImage(imageNameKey, imagesPath, ocrTextPath)
        except Exception as e:
            print('error in ocrgeneration in DataFetching', e)
            return False

    def pdfHandling(self, locatorFilePathWithFileName):
        try:
            from PdfHandling.PdfHandling import PdfHanling
            pdfHandling = PdfHanling()
            pdfPath = self.getJsonDataRecurssive('imagProcessing,pdfPath', self.path)
            imagePath = self.getJsonDataRecurssive('imagProcessing,imagePath', self.path)

            for fileName, locatorDataDictionary in locatorFilePathWithFileName.items():
                print('filename: ', fileName)
                for locatorFinalId, locatorDataArray in locatorDataDictionary.items():
                    pdfHandling.pdfGenerator(imagePath, fileName, '.tif', pdfPath)
                    pdfHandling.highlihtPDF(pdfPath, fileName, locatorDataArray)

            return True
        except Exception as e:
            print('error in pdfHandling in DataFetching', e)
            return False

    def addLoatorLayer(self, layerName, data):
        try:
            locatorDirectory = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            fp = open(locatorDirectory+layerName+'.json', 'w')
            fp.flush()
            fp.close()

            # locator = Locator(self.path)

            for locatorId, locatorData in data:
                if not self.addLocatorToDictionary(locatorData, locatorId, layerName, locatorDirectory):
                    return False

            return True
        except Exception as e:
            print('error in addLocatorLayer in DataFetching', e)
            return False

    def imageDataProcessing(self):
        try:
            imagesPath = self.getJsonDataRecurssive('imagProcessing,imagePath', self.path)
            ocrTextDirectoryPath = self.getJsonDataRecurssive('imagProcessing,ocrTextPath', self.path)

            # if not self.generateOCR(imagesPath, ocrTextDirectoryPath):
            #     exit()

            if not self.addLoatorLayer('layer1', self.getLayer1()):
                return False

            if not self.addLoatorLayer('layer2', self.getLayer2()):
                return False

            validation = LocatorValidation(self.path)
            # locator = Locator(self.path)

            validation.addValidationLayer('layer1', self.getValidation1())
            validation.addValidationLayer('layer2', self.getValidation2())

            # locatorDataDirectory = self.processLayerFromSourceFile('layer1', ocrTextDirectoryPath)
            layerData = self.processLocatorAndGetDataFromFileAll('layer1', ocrTextDirectoryPath)

            # print('layer1 out', layerData)
            if not self.saveDataAsCSV('layer1Out', layerData, 'layer1Out'):
                print('error saving csv layer1')
                return False

            locatorDataDictionary = self.processLayerFromLayer('layer2', layerData, self.connectingLocator())

            # print('layer2 out', locatorDataDictionary)
            if not self.saveDataAsCSV('layer2Out', locatorDataDictionary, 'layer2Out'):
                print('error saving csv layer2')
                return False

            print('completed')

            # self.pdfHandling(locatorFilePathWithFileName)

            return True
        except Exception as e:
            print('error in imageDataProcessing in DataFetching', e)
            return False

    def connectingLocator(self):
        try:
            connectorKeys = dict()

            #first locator key      = final locator key
            connectorKeys['parcel_number'] = 'parcel'
            connectorKeys['lot'] = 'legal'
            connectorKeys['block'] = 'legal'
            connectorKeys['lot_1'] = 'legal'

            return connectorKeys
        except Exception as e:
            print('error in connectingLocator in DataFetching', e)
            return False

    def getLayer1(self):
        data = []
        data.append(['legal', ['lot', 'block', 'plat']])
        # data.append(['legal', ['lot', 'block', 'plat', 'county']])
        # data.append(['legal', ['lot', 'plat', 'thereof']])
        data.append(['parcel', ['271-02171-0101', 'parcel']])

        return data



    def getValidation1(self):
        data = []
        data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'))
        data.append(('legal', '^ *\d', 'False'))
        data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d \d\d\d-\d\d\d\d\d-\d\d\d\d', 'False'))

        return data

    def getLayer2(self):
        data = []

        data.append(['parcel_number', ['271-02171-0101']])
        data.append(['lot', ['LOT 1']])
        data.append(['lot_1', ['lot three', 'LOT FOUR', 'LOT SIXTEEN']])
        # data.append(['block', ['BLOCK ELEVEN']])

        return data

    def getValidation2(self):
        data = []
        data.append(('lot', 'LOT [A-Z]$', 'False'))
        data.append(('lot_1', '^[0-9]', 'False'))
        data.append(('lot_1', 'LOT THREE \(3\)', 'False'))
        data.append(('lot_1', 'STATE BAR', 'False'))
        # data.append(('lot', 'lot *[\\"]+', 'False'))
        # data.append(('lot', 'lot \w{2,}', 'False'))
        # data.append(('lot', '^[0-9]', 'False'))
        # data.append(('lot', 'one', 'true'))
        # data.append(('parcel_number','\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'))

        return data

    def saveDataAsCSV(self, fileName, dataDictionary, tag):
        try:
            csvName = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            csvName = csvName+fileName+'.csv'
            fp = open(csvName, 'w')
            fp.flush()
            fp.close()

            if self.saveAsCsv(csvName, tag+'\n', dataDictionary):
                return True
            else:
                return False
        except Exception as e:
            print('error in saveDataAsCSV in DataFetching', e)
            return False