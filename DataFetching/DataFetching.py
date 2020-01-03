from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.Locator import Locator
from DataFetching.customData import *

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

            if data:
                for locatorId, locatorData in data:
                    if not self.addLocatorToDictionary(locatorData, locatorId, layerName, locatorDirectory):
                        return False

                return True
            else:
                print('json data input for layer ' + layerName + ' is empty')
                return False
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

            # if not self.addLoatorLayer('layer1', getLayer1()):
            #     return False
            #
            # if not self.addLoatorLayer('layer2', getLayer2()):
            #     return False

            if not self.addLoatorLayer('layer3', getLayer3()):
                return False

            # self.addValidationLayer('layer1', getValidation1())
            # self.addValidationLayer('layer2', getValidation2())
            self.addValidationLayer('layer3', [])
            self.addValidationLayer('layer4', [])

            # layerData = self.processLocatorAndGetDataFromFileAll('layer1', ocrTextDirectoryPath)
            # print('layer1 completed')
            #
            layer3Data = self.processLocatorAndGetDataFromFileAll('layer3', ocrTextDirectoryPath)

            # print('layer1 out', layerData)
            # if not self.saveDataAsCSV('layer1Out', layerData, 'layer1Out'):
            #     print('error saving csv layer1')
            #     return False
            #
            if not self.saveDataAsCSV('layer3Out', layer3Data, 'layer3'):
                print('error saving csv layer1')
                return False

            # locatorDataDictionary = self.processLayerFromLayer('layer2', layerData, connectingLocator())

            titleCompay = self.processLayerFromLayer('layer4', layer3Data, connectingLocator())

            # print('layer2 out', locatorDataDictionary)
            # if locatorDataDictionary:
            #     if not self.saveDataAsCSV('layer2Out', locatorDataDictionary, 'layer2Out'):
            #         print('error saving csv layer2')
            #         return False
            # else:
            #     print('processing layer1 with layer2 failed')
            #     return False

            if titleCompay:
                if not self.saveDataAsCSV('layer4Out', titleCompay, 'Title Company'):
                    print('error saving csv layer2')
                    return False
            else:
                print('no data in layer4')
                return False


            print('completed')

            # self.pdfHandling(locatorFilePathWithFileName)

            return True
        except Exception as e:
            print('error in imageDataProcessing in DataFetching', e)
            return False

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