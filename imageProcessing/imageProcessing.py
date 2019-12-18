import cv2
import numpy as np
import json

from ExceptionHandling.GeneralExceptionHandling import GeneralExceptionHandling

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

class ImageProcessing():
    def __init__(self, path):
        self.path = path

    """
    image image data
    """
    def getOcr(self, image):
        import pytesseract
        try:
            return pytesseract.image_to_string(image)
        except Exception as e:
            print('Exception in imageProcessing getOcr ',e)
            return False

    """
    image @image data
    return valid non empty text
    """
    def getValidOcr(self, image):
        try:
            if image.any():
                invalidCondition = ['']
                ocrText = pytesseract.image_to_string(image)

                for invalid in invalidCondition:
                    if ocrText == invalid:
                        return False
                return ocrText
            else:
                return False
        except Exception as e:
            print('Error in imageProcessing getValidOcr() ', e)
            return False

    def ocrAllImage(self, imageExtensionOrKey, filePath):
        try:
            from ExceptionHandling.DirecotryHandling import DrectoryHandling
            drectoryHandling = DrectoryHandling()

            imageList = drectoryHandling.getDirectoryElementBykey(filePath, imageExtensionOrKey)

            ocrTextPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'imagProcessing', self.path)
            ocrTextPath = GeneralExceptionHandling.getJsonData(GeneralExceptionHandling, 'ocrTextPath', ocrTextPath)
            print('ocr image saving to ', ocrTextPath)

            for eachImage in imageList:
                splitImageName = eachImage.split('.')
                imageName = splitImageName[0]
                extension = splitImageName[1]
                if not self.ocrImage(imageName, extension,imageName, filePath, ocrTextPath):
                    print(eachImage, ' failed')

            print('ocr completed')

            return True
        except Exception as e:
            print('error in ocrAllImage', e)
            return False

    def ocrImage(self, imageName, imageExtension, ocrDocumentName, imageFilePath, ocrFilePath):
        try:
            fp = open(ocrFilePath + ocrDocumentName+'.txt', 'w')
        except Exception as e:
            import os

            os.mkdir(ocrFilePath)
            fp = open(ocrFilePath + ocrDocumentName, 'w')

        try:
            fp.write(pytesseract.image_to_string(imageFilePath + imageName + '.' + imageExtension))
            fp.close()
            return True
        except Exception as e:
            print('Error in ocrImage', e)
            return False

    """
    image @opencv image object
    returns contours or False when error occured
    """
    def getContours(self, image):
        try:
            # Grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Find Canny edges
            edged = cv2.Canny(gray, 30, 200)
            cv2.waitKey(0)

            # Finding Contours
            # Use a copy of the imageName e.g. edged.copy()
            # since findContours alters the imageName
            contours, hierarchy = cv2.findContours(edged,
                                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            return contours
        except Exception as e:
            print('Error in getContours', e)
            return False

    """
    contours @array
    contorIndex @num data contain index of contours
    imagePath @string path to the image file
    """
    def cropContors(self, contours, contorIndex, imagePath):
        try:
            if contours:
                idx = contorIndex
                try:
                    image = cv2.imread(imagePath, 0)
                    mask = np.zeros_like(image)  # Create mask where white is what we want, black otherwise
                    cv2.drawContours(mask, contours, idx, 255, -1)  # Draw filled contour in mask
                    out = np.zeros_like(image)  # Extract out the object and place into output imageName
                    out[mask == 255] = image[mask == 255]

                    # Now crop
                    (y, x) = np.where(mask == 255)
                    (topy, topx) = (np.min(y), np.min(x))
                    (bottomy, bottomx) = (np.max(y), np.max(x))
                    out = out[topy:bottomy + 1, topx:bottomx + 1]

                    return out
                except Exception as e:
                    # print('Error in cropContors imread',e)
                    return False
            else:
                return False
        except Exception as e:
            print('Error in cropContors main',e)
            return False

    def showImage(self, imagetag, image):
        cv2.imshow(imagetag, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def drawContours(self, openCvImage, contors, contourldx=-1, color = (0, 255, 0), thickness = 3):
        try:
            cv2.drawContours(openCvImage, contors, contourldx, color, thickness, lineType=-1)
            # print(imageName)
            cv2.imshow('drawContours', openCvImage)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return True
        except Exception as e:
            print('errorn in draw contrours', e)
            return False

    def openCVReadImage(self, imageLoaction, imageName, arg=None):
        try:
            import os
            # print('open',os.getcwd(), imageLoaction + imageName + '.png')
            if arg == None:
                image = cv2.imread(imageLoaction + imageName + '.png')
            else:
                image = cv2.imread(imageLoaction + imageName + '.png', arg)
            return image
        except Exception as e:
            print('opencvreadimage',e)
            return False

    def openCVdrawContours(self):
        import cv2
        import numpy as np

        print(cv2.__version__)
        image = cv2.imread('../images/test.png')
        cv2.waitKey(0)

        # Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find Canny edges
        edged = cv2.Canny(gray, 30, 200)
        cv2.waitKey(0)

        # Finding Contours
        # Use a copy of the imageName e.g. edged.copy()
        # since findContours alters the imageName
        contours, hierarchy = cv2.findContours(edged,
                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # cv2.imshow('Canny Edges After Contouring', edged)
        # cv2.waitKey(0)

        print("Number of Contours found = " + str(len(contours)))

        # Draw all contours
        # -1 signifies drawing all contours
        # cv2.drawContours(imageName, contours[190], -1, (0, 255, 0), 3)

        # print(contours[190])
        # print(contours[190][0][0])
        # # , contours[190][len(contours[190])][0])
        # print(len(contours[190]))
        # print(contours[190][len(contours[190])-1][0])
        # cv2.imshow('Contours', imageName)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


        idx = 190
        image = cv2.imread('../images/test.png', 0)
        mask = np.zeros_like(image)  # Create mask where white is what we want, black otherwise
        cv2.drawContours(mask, contours, idx, 255, -1)  # Draw filled contour in mask
        out = np.zeros_like(image)  # Extract out the object and place into output imageName
        out[mask == 255] = image[mask == 255]

        # Now crop
        (y, x) = np.where(mask == 255)
        (topy, topx) = (np.min(y), np.min(x))
        (bottomy, bottomx) = (np.max(y), np.max(x))
        out = out[topy:bottomy + 1, topx:bottomx + 1]

        cv2.imshow('Output', out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#
# obj = imageProcessing()
#
# image = cv2.imread('../images/test.png')
#
# contors = obj.getContours(image)
#
# obj.drawContours(image,contors)
# for i in range(0, len(contors)):
#     outputImage = obj.cropContors(obj.getContours(image), i, '../images/test.png')
#     # print(outputImage.shape)
#     try:
#         height, width = outputImage.shape
#
#         # print('!' +getOcr(outputImage) + '!')
#         if obj.getValidOcr(outputImage):
#             confidence = pytesseract.image_to_data(outputImage, output_type='data.frame')
#             # print(type(confidence))
#             confidence =  confidence[confidence.conf != -1]
#             print(confidence)
#             # obj.drawContours(image,contors)
#             # cv2.imshow('Output', outputImage)
#             # cv2.waitKey(0)
#             # cv2.destroyAllWindows()
#     except Exception as e:
#         # print((e))
#         continue
#
# cv2.imshow('final', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# # ocrImage('test', 'png', 'test_ocr.txt')
# # print(pytesseract.image_to_string('../images/test.png'))