from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.Locator import Locator

class DataFetchingMain(Locator, GeneralExceptionHandling):
    def __init__(self, path):
        """
        Class designed for fetching data
        :param path: General argument json file
        """
        self.path = path
        Locator.__init__(self, path)
        GeneralExceptionHandling.__init__(self)

    def generateOCR(self, imagesPath, ocrTextPath) -> bool:
        """
        For performing ocr
        :param imagesPath: Path of the image to convert
        :param ocrTextPath: Path for saving text
        :return: True if success else :return: False
        """
        try:
            from imageProcessing.imageProcessing import ImageProcessing
            imageProcessing = ImageProcessing(self.path)

            imageNameKey = 'tif'

            return imageProcessing.ocrAllImage(imageNameKey, imagesPath, ocrTextPath)
        except Exception as e:
            print('error in ocrgeneration in DataFetching', e)
            return False

    def pdfHandling(self, locatorFilePathWithFileName) -> bool:
        """
        For performing highlighting serachable pdf
        :param locatorFilePathWithFileName: json contains file name and locator
        :return: True if success else :return: False
        ":Todo: json file might contain locator connector and locator array confirm and sort it out
        """
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

    def addLoatorLayer(self, layerName, data) -> bool:
        """
        Dictionary generation with locator
        :param layerName: name of layer
        :param data: json data for a layer
        :return: True if sucess else :return: False
        """
        try:
            locatorDirectory = self.getJsonDataRecurssive('DataFetching,filesPath', self.path)
            print(locatorDirectory+layerName+'.json')
            fp = open(locatorDirectory+layerName+'.json', 'w')
            fp.flush()
            fp.close()

            for locatorId, locatorData in data:
                if not self.addLocatorToDictionary(locatorData, locatorId, layerName, locatorDirectory):
                    return False

            return True
        except Exception as e:
            print('error in addLocatorLayer in DataFetching', e)
            return False

    def imageDataProcessing(self) -> bool:
        """
        Collect images and  perform ocr for each images
        Locator initialization and performing
        Data fetching
        Processed out
        :return: True if success else :return: False
        """
        try:
            imagesPath = self.getJsonDataRecurssive('imagProcessing,imagePath', self.path)
            ocrTextDirectoryPath = self.getJsonDataRecurssive('imagProcessing,ocrTextPath', self.path)

            # if not self.generateOCR(imagesPath, ocrTextDirectoryPath):
            #     exit()

            if not self.addLoatorLayer('layer1', self.getLayer1()):
                return False

            if not self.addLoatorLayer('layer2', self.getLayer2()):
                return False

            self.addValidationLayer('layer1', self.getValidation1())
            self.addValidationLayer('layer2', self.getValidation2())

            layerData = self.processLocatorAndGetDataFromFileAll('layer1', ocrTextDirectoryPath)
            print('layer1 completed')

            # print('layer1 out', layerData)
            if not self.saveDataAsCSV('layer1Out', layerData, 'layer1Out'):
                print('error saving csv layer1')
                return False

            locatorDataDictionary = self.processLayerFromLayer('layer2', layerData, self.connectingLocator())

            print('layer2 out', locatorDataDictionary)
            if locatorDataDictionary:
                if not self.saveDataAsCSV('layer2Out', locatorDataDictionary, 'layer2Out'):
                    print('error saving csv layer2')
                    return False
            else:
                print('processing layer1 with layer2 failed')
                return False


            print('completed')

            # self.pdfHandling(locatorFilePathWithFileName)

            return True
        except Exception as e:
            print('error in imageDataProcessing in DataFetching', e)
            return False

    def connectingLocator(self) -> dict:
        """
        Connector for each locator in different layers
        :return: connector dictionary
        """
        try:
            connectorKeys = dict()

            #first locator key      = final locator key
            connectorKeys['parcel_number'] = 'parcel'
            # connectorKeys['parcel_number_1'] = 'parcel'
            # connectorKeys['lot'] = 'legal'
            # connectorKeys['block'] = 'legal'
            # connectorKeys['lot_1'] = 'legal'

            return connectorKeys
        except Exception as e:
            print('error in connectingLocator in DataFetching', e)
            return False

    def getLayer1(self) -> list:
        """
        Custom locator asigning
        :return: locator array
        :Todo: Direct regular expression need to add (To improve fetching)
        """
        data = []
        # data.append(['legal', ['lot', 'block', 'plat']])
        # data.append(['legal', ['lot', 'block', 'plat', 'county']])
        # data.append(['legal', ['lot', 'plat', 'thereof']])
        # data.append(['parcel', ['271-02171-0101', 'parcel']])
        data.append(['parcel', ['APN #;', 'R0235662']])
        data.append(['parcel', ['A.P.N.', 'R1605212']])
        data.append(['parcel', ['APN ', '17-02421']])

        return data

    def getValidation1(self) -> list:
        """
        Custom validation asigning
        :return: validation array
        :Todo: Pattern build need to add, only direct regular expressions are allowed
        """
        data = []
        # data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'))
        # data.append(('legal', '^ *\d', 'False'))
        # data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d \d\d\d-\d\d\d\d\d-\d\d\d\d', 'False'))
        # data.append(('parcel', '\d\d\d\d\d\d\d\d', 'True'))
        # data.append(('parcel', '^A', 'True'))

        return data

    def getLayer2(self) -> list:
        """
        Custom locator asigning
        :return: locator array
        """
        data = []

        # data.append(['parcel_number', ['271-02171-0101']])
        # data.append(['lot', ['LOT 1']])
        # data.append(['lot_1', ['lot three', 'LOT FOUR', 'LOT SIXTEEN', 'lots four']])
        # data.append(['block', ['BLOCK ELEVEN']])
        data.append(['parcel_number', ['R0242052']])
        data.append(['parcel_number', ['RO242052']])
        data.append(['parcel_number', ['02-34000']])
        # data.append(['parcel_number', ['10-33009']])

        return data

    def getValidation2(self) -> list:
        """
        Custom validation asigning
        :return: validation array
        """
        data = []
        # data.append(('lot', 'LOT [A-Z]$', 'False'))
        # data.append(('lot_1', '^[0-9]', 'False'))
        # data.append(('lot_1', 'LOT THREE \(3\)', 'False'))
        # data.append(('lot_1', 'STATE BAR', 'False'))
        # data.append(('lot', 'lot *[\\"]+', 'False'))
        # data.append(('lot', 'lot \w{2,}', 'False'))
        # data.append(('lot', '^[0-9]', 'False'))
        # data.append(('lot', 'one', 'true'))
        # data.append(('parcel_number','\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'))
        # data.append(('parcel_number', '\d\d\d\d\d\d', 'True'))

        return data

    def saveDataAsCSV(self, fileName, dataDictionary, tag) -> bool:
        """
        Convert data for General Exception saveAsCsv format
        :param fileName: Name
        :param dataDictionary: csv content
        :param tag: Heading for csv if any
        :return: True if success else :return: False
        """
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