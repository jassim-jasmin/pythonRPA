import fitz
import pytesseract

imagePathWithName = 'Data/sample.tif'
path = 'Data/'
name = 'sample'
class PdfHanling:
    def imageToText(self, imagePath, name, extension):
        pytesseract.image_to_string(imagePath+name+extension)

    def pdfGenerator(self, imagePath, name, extension):
        try:
            pdf = pytesseract.image_to_pdf_or_hocr(imagePath+name+extension, extension='pdf')
            f = open(imagePath+name+".pdf", "w+b")
            f.write(bytearray(pdf))
            f.close()
        except Exception as e:
            print(e)

    def highlihtPDF(self, pdfPath, pdfName, highlightTextArray):
        print('highlight ', highlightTextArray)
        if highlightTextArray:
            doc = fitz.open(pdfPath+pdfName+'.pdf')

            # page = doc[0]

            for page in doc:
                for highlightText in highlightTextArray:
                    # highlightText = 'QUIT CLAIM DEED  Document Number 010-00532-0000 Parcel Identification Number'
                    instance = page.searchFor(highlightText)

                    for ins in instance:
                        highlight = page.addHighlightAnnot(ins)

            doc.save(pdfPath+pdfName+'_highlightened.pdf', garbage=4, deflate=True, clean=True)
        else:
            print('hightlight failed')
            return False

# imageToText('Data/', 'sample','.tif')
# pdfGenerator(imagePathWithName)
# print(com)