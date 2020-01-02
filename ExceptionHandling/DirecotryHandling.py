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
                else:
                    return False

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
# import json
# obj = DrectoryHandling()
# fp = open('../path.json')
# path = json.loads(fp.read())['linux']
# fp.flush()
# fp.close()



# textFileArray = obj.getTextFileFromDiffDirectory('/root/Documents/Test/ocr/diago', path['directorySeperator'])
# textFileArray = obj.getTextFileFromDiffDirectory('/run/user/0/gvfs/smb-share:server=192.168.15.65,share=aishare/result_data/CA/SAN_DIEGO/CASANDIEGO_20191212', '/')
#
# print(textFileArray)
# print('finally')
# #
# if textFileArray:
#     for eachTextFileArray in textFileArray:
#         obj.copyToAnotherDirectory(path['imagProcessing']['ocrTextPath'], eachTextFileArray)
#     print('File copied to ', path['imagProcessing']['ocrTextPath'])
#
# textFileArray = obj.getDirectoryElementBykey('/root/Documents/Test/ocr/diago', 'txt')
#
# obj.deleteFileWithKey(path['imagProcessing']['ocrTextPath'],'pdf','/')

# list = ['SD-2019_00570756.txt','SD-2019_00570714.txt','SD-2019_00570711.txt','SD-2019_00570690.txt','SD-2019_00570570.txt','SD-2019_00570558.txt','SD-2019_00570554.txt','SD-2019_00570511.txt','SD-2019_00570618.txt','SD-2019_00570516.txt','SD-2019_00570504.txt','SD-2019_00570500.txt','SD-2019_00570749.txt','SD-2019_00570738.txt','SD-2019_00570747.txt','SD-2019_00570625.txt','SD-2019_00570538.txt','SD-2019_00570515.txt','SD-2019_00570517.txt','SD-2019_00570521.txt','SD-2019_00570510.txt','SD-2019_00570505.txt','SD-2019_00570503.txt','SD-2019_00570620.txt','SD-2019_00570557.txt','SD-2019_00570895.txt','SD-2019_00570733.txt','SD-2019_00570636.txt','SD-2019_00570599.txt','SD-2019_00570556.txt','SD-2019_00570512.txt','SD-2019_00570539.txt','SD-2019_00570522.txt','SD-2019_00570530.txt','SD-2019_00570745.txt','SD-2019_00570650.txt','SD-2019_00570652.txt','SD-2019_00570616.txt','SD-2019_00570606.txt','SD-2019_00570614.txt','SD-2019_00570578.txt','SD-2019_00570555.txt','SD-2019_00570715.txt','SD-2019_00570647.txt','SD-2019_00570609.txt','SD-2019_00570742.txt','SD-2019_00571291.txt','SD-2019_00571252.txt','SD-2019_00571122.txt','SD-2019_00571060.txt','SD-2019_00571467.txt','SD-2019_00571469.txt','SD-2019_00571413.txt','SD-2019_00571384.txt','SD-2019_00571373.txt','SD-2019_00571211.txt','SD-2019_00571079.txt','SD-2019_00571476.txt','SD-2019_00571385.txt','SD-2019_00571387.txt','SD-2019_00571360.txt','SD-2019_00571357.txt','SD-2019_00571180.txt','SD-2019_00571081.txt','SD-2019_00571436.txt','SD-2019_00571181.txt','SD-2019_00571083.txt','SD-2019_00571474.txt','SD-2019_00571184.txt','SD-2019_00571472.txt','SD-2019_00571119.txt','SD-2019_00571457.txt','SD-2019_00571215.txt','SD-2019_00571075.txt','SD-2019_00571473.txt','SD-2019_00571451.txt','SD-2019_00571449.txt','SD-2019_00571439.txt','SD-2019_00571435.txt','SD-2019_00571411.txt','SD-2019_00571109.txt','SD-2019_00571859.txt','SD-2019_00571784.txt','SD-2019_00571753.txt','SD-2019_00571740.txt','SD-2019_00571643.txt','SD-2019_00571624.txt','SD-2019_00571580.txt','SD-2019_00571503.txt','SD-2019_00571529.txt','SD-2019_00571530.txt','SD-2019_00571501.txt','SD-2019_00571504.txt','SD-2019_00571508.txt','SD-2019_00571511.txt','SD-2019_00571658.txt','SD-2019_00571577.txt','SD-2019_00571562.txt','SD-2019_00571521.txt','SD-2019_00571514.txt','SD-2019_00571519.txt','SD-2019_00571506.txt','SD-2019_00571507.txt','SD-2019_00571509.txt','SD-2019_00571510.txt','SD-2019_00571937.txt','SD-2019_00571757.txt','SD-2019_00571537.txt','SD-2019_00571802.txt','SD-2019_00571642.txt','SD-2019_00571617.txt','SD-2019_00571610.txt','SD-2019_00571578.txt','SD-2019_00571536.txt','SD-2019_00571838.txt','SD-2019_00571792.txt','SD-2019_00571609.txt','SD-2019_00571592.txt','SD-2019_00571616.txt','SD-2019_00571613.txt','SD-2019_00571968.txt','SD-2019_00571793.txt','SD-2019_00571741.txt','SD-2019_00571628.txt','SD-2019_00571611.txt','SD-2019_00572433.txt','SD-2019_00572422.txt','SD-2019_00572303.txt','SD-2019_00572159.txt','SD-2019_00572076.txt','SD-2019_00572081.txt','SD-2019_00572036.txt','SD-2019_00572037.txt','SD-2019_00572034.txt','SD-2019_00572480.txt','SD-2019_00572316.txt','SD-2019_00572274.txt','SD-2019_00572224.txt','SD-2019_00572222.txt','SD-2019_00572214.txt','SD-2019_00572216.txt','SD-2019_00572210.txt','SD-2019_00572198.txt','SD-2019_00572191.txt','SD-2019_00572182.txt','SD-2019_00572108.txt','SD-2019_00572091.txt','SD-2019_00572145.txt','SD-2019_00572105.txt','SD-2019_00572103.txt','SD-2019_00572075.txt','SD-2019_00572060.txt','SD-2019_00571999.txt','SD-2019_00571998.txt','SD-2019_00572486.txt','SD-2019_00572472.txt','SD-2019_00572310.txt','SD-2019_00572285.txt','SD-2019_00572089.txt','SD-2019_00572086.txt','SD-2019_00572082.txt','SD-2019_00572059.txt','SD-2019_00572464.txt','SD-2019_00572420.txt','SD-2019_00572320.txt','SD-2019_00572272.txt','SD-2019_00572259.txt','SD-2019_00572261.txt','SD-2019_00572193.txt','SD-2019_00572028.txt','SD-2019_00572040.txt','SD-2019_00572032.txt','SD-2019_00572467.txt','SD-2019_00572431.txt','SD-2019_00572421.txt','SD-2019_00572409.txt','SD-2019_00572419.txt','SD-2019_00572346.txt','SD-2019_00572291.txt','SD-2019_00572270.txt','SD-2019_00572269.txt','SD-2019_00572240.txt','SD-2019_00572228.txt','SD-2019_00572157.txt','SD-2019_00572329.txt','SD-2019_00572172.txt','SD-2019_00572174.txt','SD-2019_00572166.txt','SD-2019_00572160.txt','SD-2019_00572148.txt','SD-2019_00572095.txt','SD-2019_00572077.txt','SD-2019_00572083.txt','SD-2019_00572074.txt','SD-2019_00572078.txt','SD-2019_00572263.txt','SD-2019_00572267.txt','SD-2019_00572245.txt','SD-2019_00572205.txt','SD-2019_00572185.txt','SD-2019_00572061.txt','SD-2019_00572052.txt','SD-2019_00572134.txt','SD-2019_00572919.txt','SD-2019_00572810.txt','SD-2019_00572765.txt','SD-2019_00572697.txt','SD-2019_00572685.txt','SD-2019_00572612.txt','SD-2019_00572608.txt','SD-2019_00572576.txt','SD-2019_00572572.txt','SD-2019_00572914.txt','SD-2019_00572908.txt','SD-2019_00572869.txt','SD-2019_00572843.txt','SD-2019_00572734.txt','SD-2019_00572713.txt','SD-2019_00572709.txt','SD-2019_00572650.txt','SD-2019_00572627.txt','SD-2019_00572620.txt','SD-2019_00572498.txt','SD-2019_00572653.txt','SD-2019_00572648.txt','SD-2019_00572646.txt','SD-2019_00572622.txt','SD-2019_00572521.txt','SD-2019_00572952.txt','SD-2019_00572945.txt','SD-2019_00572944.txt','SD-2019_00572838.txt','SD-2019_00572807.txt','SD-2019_00572804.txt','SD-2019_00572776.txt','SD-2019_00572768.txt','SD-2019_00572733.txt','SD-2019_00572717.txt','SD-2019_00572727.txt','SD-2019_00572700.txt','SD-2019_00572663.txt','SD-2019_00572586.txt','SD-2019_00572558.txt','SD-2019_00572549.txt','SD-2019_00572922.txt','SD-2019_00572880.txt','SD-2019_00572904.txt','SD-2019_00572892.txt','SD-2019_00572881.txt','SD-2019_00572808.txt','SD-2019_00572770.txt','SD-2019_00572767.txt','SD-2019_00572719.txt','SD-2019_00572614.txt','SD-2019_00572603.txt','SD-2019_00572942.txt','SD-2019_00572929.txt','SD-2019_00572927.txt','SD-2019_00572877.txt','SD-2019_00572849.txt','SD-2019_00572844.txt','SD-2019_00572833.txt','SD-2019_00572826.txt','SD-2019_00572781.txt','SD-2019_00572917.txt','SD-2019_00572915.txt','SD-2019_00572912.txt','SD-2019_00572905.txt','SD-2019_00572893.txt','SD-2019_00572890.txt','SD-2019_00572828.txt','SD-2019_00572742.txt','SD-2019_00572977.txt','SD-2019_00573333.txt','SD-2019_00573339.txt','SD-2019_00573300.txt','SD-2019_00573245.txt','SD-2019_00573181.txt','SD-2019_00573160.txt','SD-2019_00573154.txt','SD-2019_00573354.txt','SD-2019_00573289.txt','SD-2019_00573176.txt','SD-2019_00573084.txt','SD-2019_00573080.txt','SD-2019_00573026.txt','SD-2019_00573013.txt','SD-2019_00573007.txt','SD-2019_00573000.txt','SD-2019_00573282.txt','SD-2019_00573277.txt','SD-2019_00573224.txt','SD-2019_00573229.txt','SD-2019_00573046.txt','SD-2019_00573025.txt','SD-2019_00573335.txt','SD-2019_00573318.txt','SD-2019_00573272.txt','SD-2019_00573264.txt','SD-2019_00573270.txt','SD-2019_00573253.txt','SD-2019_00573231.txt','SD-2019_00573212.txt','SD-2019_00573172.txt','SD-2019_00573170.txt','SD-2019_00573118.txt','SD-2019_00573358.txt','SD-2019_00573346.txt','SD-2019_00573337.txt','SD-2019_00573330.txt','SD-2019_00573324.txt','SD-2019_00573322.txt','SD-2019_00573095.txt','SD-2019_00573028.txt','SD-2019_00573017.txt','SD-2019_00573024.txt','SD-2019_00573267.txt','SD-2019_00573261.txt','SD-2019_00573256.txt','SD-2019_00573237.txt','SD-2019_00573242.txt','SD-2019_00573189.txt','SD-2019_00573094.txt','SD-2019_00573058.txt']
#
# for each in list:
#     print(each)
#     textFileArray.remove(each)
#
# print(textFileArray)
# if textFileArray:
#     for item in textFileArray:
#         obj.deleteFileWithKey('/root/Documents/Test/ocr/diago', item, '/')