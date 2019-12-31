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

    def deleteFileWithKey(self, location, key, osFileSeperator):
        try:
            print('deletion')
            files =self.getDirectoryElementBykey(location, key)

            for eachFile in files:
                print('removeing', eachFile)
                os.remove(location+osFileSeperator+eachFile)

            return True
        except Exception as e:
            print('error in deleteFileWithKey in DirectoryHandling', e)
            return False
import json
obj = DrectoryHandling()
fp = open('../path.json')
path = json.loads(fp.read())['linux']
fp.flush()
fp.close()



textFileArray = obj.getTextFileFromDiffDirectory('/root/Documents/Test/ocr/diago', path['directorySeperator'])
# print(textFileArray)
# print('finally')
# #
# if textFileArray:
#     for eachTextFileArray in textFileArray:
#         obj.copyToAnotherDirectory(path['imagProcessing']['ocrTextPath'], eachTextFileArray)
#     print('File copied to ', path['imagProcessing']['ocrTextPath'])

# obj.deleteFileWithKey('/root/Documents/Test/ocr/diago','pdf','/')
list = ['SD-2019_00570756', 'SD-2019_00570714', 'SD-2019_00570711', 'SD-2019_00570690', 'SD-2019_00570570', 'SD-2019_00570558', 'SD-2019_00570554', 'SD-2019_00570511', 'SD-2019_00570618', 'SD-2019_00570516', 'SD-2019_00570504', 'SD-2019_00570500', 'SD-2019_00570749', 'SD-2019_00570738', 'SD-2019_00570747', 'SD-2019_00570625', 'SD-2019_00570538', 'SD-2019_00570515', 'SD-2019_00570517', 'SD-2019_00570521', 'SD-2019_00570510', 'SD-2019_00570505', 'SD-2019_00570503', 'SD-2019_00570620', 'SD-2019_00570557', 'SD-2019_00570895', 'SD-2019_00570733', 'SD-2019_00570636', 'SD-2019_00570599', 'SD-2019_00570556', 'SD-2019_00570512', 'SD-2019_00570539', 'SD-2019_00570522','SD-2019_00570530','SD-2019_00570745','SD-2019_00570650','SD-2019_00570652','SD-2019_00570616','SD-2019_00570606','SD-2019_00570614','SD-2019_00570578','SD-2019_00570555','SD-2019_00570715','SD-2019_00570647','SD-2019_00570609','SD-2019_00570742','SD-2019_00571291','SD-2019_00571252','SD-2019_00571122','SD-2019_00571060','SD-2019_00571467','SD-2019_00571469','SD-2019_00571413','SD-2019_00571384','SD-2019_00571373','SD-2019_00571211','SD-2019_00571079','SD-2019_00571476','SD-2019_00571385','SD-2019_00571387','SD-2019_00571360','SD-2019_00571357','SD-2019_00571180','SD-2019_00571081','SD-2019_00571436','SD-2019_00571181','SD-2019_00571083','SD-2019_00571474','SD-2019_00571184','SD-2019_00571472','SD-2019_00571119','SD-2019_00571457','SD-2019_00571215','SD-2019_00571075','SD-2019_00571473','SD-2019_00571451','SD-2019_00571449','SD-2019_00571439','SD-2019_00571435','SD-2019_00571411','SD-2019_00571109','SD-2019_00571859','SD-2019_00571784','SD-2019_00571753','SD-2019_00571740','SD-2019_00571643','SD-2019_00571624','SD-2019_00571580','SD-2019_00571503','SD-2019_00571529','SD-2019_00571530','SD-2019_00571501','SD-2019_00571504','SD-2019_00571508','SD-2019_00571511','SD-2019_00571658','SD-2019_00571577','SD-2019_00571562','SD-2019_00571521','SD-2019_00571514','SD-2019_00571519','SD-2019_00571506','SD-2019_00571507','SD-2019_00571509','SD-2019_00571510','SD-2019_00571937','SD-2019_00571757','SD-2019_00571537','SD-2019_00571802','SD-2019_00571642','SD-2019_00571617','SD-2019_00571610','SD-2019_00571578','SD-2019_00571536','SD-2019_00571838','SD-2019_00571792','SD-2019_00571609','SD-2019_00571592','SD-2019_00571616','SD-2019_00571613','SD-2019_00571968','SD-2019_00571793','SD-2019_00571741','SD-2019_00571628','SD-2019_00571611','SD-2019_00572433','SD-2019_00572422','SD-2019_00572303','SD-2019_00572159','SD-2019_00572076','SD-2019_00572081','SD-2019_00572036','SD-2019_00572037','SD-2019_00572034','SD-2019_00572480','SD-2019_00572316','SD-2019_00572274','SD-2019_00572224','SD-2019_00572222','SD-2019_00572214','SD-2019_00572216','SD-2019_00572210','SD-2019_00572198','SD-2019_00572191','SD-2019_00572182','SD-2019_00572108','SD-2019_00572091','SD-2019_00572145','SD-2019_00572105','SD-2019_00572103','SD-2019_00572075','SD-2019_00572060','SD-2019_00571999','SD-2019_00571998','SD-2019_00572486','SD-2019_00572472','SD-2019_00572310','SD-2019_00572285','SD-2019_00572089','SD-2019_00572086','SD-2019_00572082','SD-2019_00572059','SD-2019_00572464','SD-2019_00572420','SD-2019_00572320','SD-2019_00572272','SD-2019_00572259','SD-2019_00572261','SD-2019_00572193','SD-2019_00572028','SD-2019_00572040','SD-2019_00572032','SD-2019_00572467','SD-2019_00572431','SD-2019_00572421','SD-2019_00572409','SD-2019_00572419','SD-2019_00572346','SD-2019_00572291','SD-2019_00572270','SD-2019_00572269','SD-2019_00572240','SD-2019_00572228','SD-2019_00572157','SD-2019_00572329','SD-2019_00572172','SD-2019_00572174','SD-2019_00572166','SD-2019_00572160','SD-2019_00572148','SD-2019_00572095','SD-2019_00572077','SD-2019_00572083','SD-2019_00572074','SD-2019_00572078','SD-2019_00572263','SD-2019_00572267','SD-2019_00572245','SD-2019_00572205','SD-2019_00572185','SD-2019_00572061','SD-2019_00572052','SD-2019_00572134','SD-2019_00572919','SD-2019_00572810','SD-2019_00572765','SD-2019_00572697','SD-2019_00572685','SD-2019_00572612','SD-2019_00572608','SD-2019_00572576','SD-2019_00572572','SD-2019_00572914','SD-2019_00572908','SD-2019_00572869','SD-2019_00572843','SD-2019_00572734','SD-2019_00572713','SD-2019_00572709','SD-2019_00572650','SD-2019_00572627','SD-2019_00572620','SD-2019_00572498','SD-2019_00572653','SD-2019_00572648','SD-2019_00572646','SD-2019_00572622','SD-2019_00572521','SD-2019_00572952','SD-2019_00572945','SD-2019_00572944','SD-2019_00572838','SD-2019_00572807','SD-2019_00572804','SD-2019_00572776','SD-2019_00572768','SD-2019_00572733','SD-2019_00572717','SD-2019_00572727','SD-2019_00572700','SD-2019_00572663','SD-2019_00572586','SD-2019_00572558','SD-2019_00572549','SD-2019_00572922','SD-2019_00572880','SD-2019_00572904','SD-2019_00572892','SD-2019_00572881','SD-2019_00572808','SD-2019_00572770','SD-2019_00572767','SD-2019_00572719','SD-2019_00572614','SD-2019_00572603','SD-2019_00572942','SD-2019_00572929','SD-2019_00572927','SD-2019_00572877','SD-2019_00572849','SD-2019_00572844','SD-2019_00572833','SD-2019_00572826','SD-2019_00572781','SD-2019_00572917','SD-2019_00572915','SD-2019_00572912','SD-2019_00572905','SD-2019_00572893','SD-2019_00572890','SD-2019_00572828','SD-2019_00572742','SD-2019_00572977','SD-2019_00573333','SD-2019_00573339','SD-2019_00573300','SD-2019_00573245','SD-2019_00573181','SD-2019_00573160','SD-2019_00573154','SD-2019_00573354','SD-2019_00573289','SD-2019_00573176','SD-2019_00573084','SD-2019_00573080','SD-2019_00573026','SD-2019_00573013','SD-2019_00573007','SD-2019_00573000','SD-2019_00573282','SD-2019_00573277','SD-2019_00573224','SD-2019_00573229','SD-2019_00573046','SD-2019_00573025','SD-2019_00573335','SD-2019_00573318','SD-2019_00573272','SD-2019_00573264','SD-2019_00573270','SD-2019_00573253','SD-2019_00573231','SD-2019_00573212','SD-2019_00573172','SD-2019_00573170','SD-2019_00573118','SD-2019_00573358','SD-2019_00573346','SD-2019_00573337','SD-2019_00573330','SD-2019_00573324','SD-2019_00573322','SD-2019_00573095','SD-2019_00573028','SD-2019_00573017','SD-2019_00573024','SD-2019_00573267','SD-2019_00573261','SD-2019_00573256','SD-2019_00573237','SD-2019_00573242','SD-2019_00573189','SD-2019_00573094','SD-2019_00573058']

for each in list:
    textFileArray.remove(each)

for item in textFileArray:
    obj.deleteFileWithKey('/root/Documents/Test/ocr/diago', item, '/')