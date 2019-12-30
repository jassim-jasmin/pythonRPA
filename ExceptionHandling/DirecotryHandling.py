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

    def getTextFileFromDiffDirectory(self, mainDirectoryPath,osDirectorySeperator):
        try:
            allFolder =  self.getDirectoryElements(mainDirectoryPath)
            allTextFilePath = []

            for eachFolder in allFolder:
                insideEachFolder = mainDirectoryPath+osDirectorySeperator+eachFolder
                textFiles = self.getDirectoryElementBykey(insideEachFolder, 'txt')
                if textFiles:
                    for eachTextFile in textFiles:
                        allTextFilePath.append(insideEachFolder+osDirectorySeperator+eachTextFile)

            return allTextFilePath
        except Exception as e:
            print('error in getTextFileFromDiffDirectory in DirectoryHandling', e)
            return False

    def copyToAnotherDirectory(self, destinationFolder, copyFile):
        """
        copy content of copy files to another folder
        :param destinationFolder: path of destination
        :param copyFile: file with path and extension
        :return: True if success else :return: False
        """
        try:
            import shutil
            shutil.copy2(copyFile, destinationFolder)

            return True
        except Exception as e:
            print('error in copyToAnotherDirectory in DirectoryHandling', e)
            return False

# import json
# obj = DrectoryHandling()
# fp = open('../path.json')
# path = json.loads(fp.read())['linux']
# fp.flush()
# fp.close()
#
#
# textFileArray = obj.getTextFileFromDiffDirectory('/root/Documents/Test/all_files', path['directorySeperator'])
#
# if textFileArray:
#     for eachTextFileArray in textFileArray:
#         obj.copyToAnotherDirectory(path['imagProcessing']['ocrTextPath'], eachTextFileArray)
#     print('File copied to ', path['imagProcessing']['ocrTextPath'])