import os
import re

class DrectoryHandling:
    def createDirectory(self, path):
        try:
            import os
            os.mkdir(path)

            return True
        except Exception as e:
            return True

    def getDirectoryElements(self, pathToDirectoyr):
        try:
            files = os.listdir(pathToDirectoyr)

            return files
        except Exception as e:
            print('erron in getDrectoryElements in DirectoryHandling', e)
            return False

    def getDirectoryElementBykey(self, pathToDirecotory, searchKey):
        try:
            allElements = self.getDirectoryElements(pathToDirecotory)

            if allElements:
                allElementsArray = []
                for eachElements in allElements:
                    if re.search(searchKey, eachElements):
                        allElementsArray.append(eachElements)
            else:
                return False

            return allElementsArray
        except Exception as e:
            print('error in getDirectoryElementByKey', e)
            return False