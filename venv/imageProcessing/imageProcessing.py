import cv2
import numpy as np

def ocrImage(imageName, imageExtension, ocrFileName, filePath):
    try:
        from PIL import Image
    except ImportError:
        import Image
    import pytesseract

    try:
        # fp = open('../ocrText/' + ocrFileName,'w')
        fp = open(filePath + ocrFileName, 'w')
    except Exception as e:
        import os

        os.mkdir(filePath)
        fp = open(filePath + ocrFileName, 'w')

    try:
        fp.write(pytesseract.image_to_string(filePath + imageName + '.' + imageExtension))
        fp.close()
    except Exception as e:
        print('Error in ocrImage', e)
        return False

def getContours(image):
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

def cropContors(contours, contorIndex, imagePath):
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
                print('Error in cropContors imread',e)
                return False
        else:
            return False
    except Exception as e:
        print('Error in cropContors main',e)
        return False

def openCVdrawContours():
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

image = cv2.imread('../images/test.png')
contors = getContours(image)
for i in range(0, len(contors)):
    outputImage = cropContors(getContours(image), i, '../images/test.png')
    print(outputImage.shape)
    height, width = outputImage.shape
    if width == 33:
        cv2.imshow('Output', outputImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# ocrImage('test', 'png', 'test_ocr.txt')
# print(pytesseract.image_to_string('../images/test.png'))