# from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling
from DataFetching.Layer import Layer
from DataFetching.analyse import Analyse
from DataFetching.customData import *

class DataFetchingMain(Layer, Analyse):
    def __init__(self, path):
        """
        Class designed for fetching data
        :param path: General argument json file
        """
        self.path = path
        Layer.__init__(self, path)
        # GeneralExceptionHandling.__init__(self)
        Analyse.__init__(self, path)

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

    def imageDataProcessing(self) -> bool:
        """
        Collect images and  perform ocr for each images
        Locator initialization and performing
        Data fetching
        Processed out
        :return: True if success else :return: False
        """
        try:
            import time
            start = time.time()

            # imagesPath = self.getJsonDataRecurssive('imagProcessing,imagePath', self.path)
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

            if not self.addLoatorLayer('layer4', getLayer4()):
                print('error adding locator')
                return False
            #
            if not self.addLoatorLayer('layer5', getLayer5()):
                print('error adding layer5')
                return False

            # self.addValidationLayer('layer1', getValidation1())
            # self.addValidationLayer('layer2', getValidation2())

            # layerData = self.processLayerAndGetDataFromFileAll('layer1', ocrTextDirectoryPath)
            # print('layer1 completed')
            #
            layer3Data = self.processLayerAndGetDataFromFileAll('layer3', ocrTextDirectoryPath)

            # print('layer1 out', layerData)
            # if not self.saveDataAsCSV('layer1Out', layerData, 'layer1Out'):
            #     print('error saving csv layer1')
            #     return False
            #
            if not self.saveDataAsCSV('layer3Out', layer3Data, 'layer3'):
                print('error saving csv layer1')
                return False

            layer4Direct = self.processLayerAndGetDataFromFileAll('layer4', ocrTextDirectoryPath)
            layer5 = self.processLayerAndGetDataFromFileAll('layer5', ocrTextDirectoryPath)

            # locatorDataDictionary = self.processLayerFromLayer('layer2', layerData, connectingLocator())

            titleCompay = self.processLayerFromLayer('layer4', layer3Data, connectingLocator())

            self.writeJsonDataToFile(titleCompay, self.getJsonDataRecurssive('DataFetching,filesPath', self.path)+'layer4Out.json')

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
                    print('error saving csv layer4Out')
                    return False

            if layer4Direct:
                if not self.saveDataAsCSV('layer4Direct', layer4Direct, 'Direct Matching'):
                    print("error in saving csv layer 4 direct")
                    return False
            else:
                print('no data in layer4')
                return False

            #test
            # test = self.readFileAndReturnJson('/root/Documents/Test/layer4Out.json')
            # print(test)


            if layer4Direct and titleCompay:
                allData = self.fetchDataOverLayers([layer4Direct, titleCompay])

                if allData:
                    if not self.saveDataAsCSV('allData', allData, 'Compained data'):
                        print('error compaining data')
            else:
                print('layer4 and title empty')

            # if layer4Direct:
            #     if not self.saveDataAsCSV('allData', layer4Direct, 'final'):
            #         print('error saving all data layer 4')
            #         return False

            if layer5:
                if not self.saveDataAsCSV('layer5', layer5, 'final'):
                    print('error saving layer5')
                    return False
            #     else:
            #         self.validateLayerBylayer('allData', 'layer5')

            self.validateLayerBylayer('allData', 'layer5')

            if not self.getUnprocessedFiles('allData'):
                return False
            print('completed')

            # self.pdfHandling(locatorFilePathWithFileName)

            end = time.time()
            print("Complete execution time: ", end - start)

            return True
        except Exception as e:
            print('error in imageDataProcessing in DataFetching', e)
            return False