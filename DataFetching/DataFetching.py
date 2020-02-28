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

            # layer3Data = self.processLayerAndGetDataFromFileAll('layer3', ocrTextDirectoryPath)
            layer4Direct = self.processLayerAndGetDataFromFileAll('locator', ocrTextDirectoryPath)
            # layer5 = self.processLayerAndGetDataFromFileAll('layer5', ocrTextDirectoryPath)
            # titleCompay = self.processLayerFromLayer('title_lookup', layer3Data, 'layer3')

            # self.writeJsonDataToFile(titleCompay, self.getJsonDataRecurssive('DataFetching,filesPath', self.path)+'layer4Out.json')

            # if layer3Data:
            #     if not self.saveDataAsCSV('layer3Data_Out', layer3Data, 'layer3Data'):
            #         print('error saving csv layer3Data')
            #         return False
            #
            # if titleCompay:
            #     if not self.saveDataAsCSV('title_lookup_Out', titleCompay, 'Title Company'):
            #         print('error saving csv layer4Out')
            #         return False

            test = self.locatorDataSearchAndReplace(layer4Direct, 'locator')

            if test:
                if not self.saveDataAsCSV('rematched', test, 'rematched'):
                    print('errror saving rematches')
                    return False

            if layer4Direct:
                if not self.saveDataAsCSV('allData', layer4Direct, 'Direct Matching'):
                    print("error in saving csv layer 4 direct")
                    return False
            else:
                print('no data in layer4')
                return False


            # if layer4Direct and titleCompay:
            #     allData = self.fetchDataOverLayers([layer4Direct, titleCompay])
            #
            #     if allData:
            #         if not self.saveDataAsCSV('allData', allData, 'Compained data'):
            #             print('error compaining data')
            # else:
            #     print('layer4 and title empty')
            #
            # if layer5:
            #     if not self.saveDataAsCSV('layer5', layer5, 'final'):
            #         print('error saving layer5')
            #         return False

            # self.validateLayerBylayer('allData', 'layer5')

            # if not self.getUnprocessedFiles('allData'):
            #     return False
            # print('completed')

            # self.pdfHandling(locatorFilePathWithFileName)

            end = time.time()
            print("Complete execution time: ", end - start)

            return True
        except Exception as e:
            print('error in imageDataProcessing in DataFetching', e)
            return False