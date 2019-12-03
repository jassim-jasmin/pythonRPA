def ocrImage(image, extension, ocrFileName):
    try:
        from PIL import Image
    except ImportError:
        import Image
    import pytesseract

    try:
        fp = open('../ocrText/' + ocrFileName,'w')
    except Exception as e:
        import os

        os.mkdir('../ocrText')
        fp = open('../ocrText/' + image + '_ocr.txt', 'w')

    fp.write(pytesseract.image_to_string('../images/'+image + '.' + extension))

    fp.close()

def openCV():
    import cv2

    print(cv2.__version__)

openCV()
# ocrImage('test', 'png', 'test_ocr.txt')
# print(pytesseract.image_to_string('../images/test.png'))
# print(pytesseract.image_to_boxes(Image.open('../images/test.png')))
#
# import cv2

# img = cv2.imread(r'../images/test.png')
# print(pytesseract.image_to_string(img))