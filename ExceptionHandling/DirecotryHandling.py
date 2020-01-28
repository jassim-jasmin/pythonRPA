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
#
# dpath = '/run/user/0/gvfs/smb-share:server=192.168.15.65,share=aishare/result_data/CA/RIVERSIDE/CARIVERSIDE_20200109'
# opath = '/root/Documents/Test/cariver/ocr'
# opath = '/root/Documents/Test/cariver/Test/ocr/'
#
# # textFileArray = obj.getTextFileFromDiffDirectory('/root/Documents/Test/CASANDIEGO_20191109', path['directorySeperator'])
# textFileArray = obj.getTextFileFromDiffDirectory(dpath, '/')
# if textFileArray:
#     for eachTextFileArray in textFileArray:
#         obj.copyToAnotherDirectory(opath, eachTextFileArray)
#     print('File copied to ', opath)
#
# textFileArray = obj.getDirectoryElementBykey(opath, 'txt')[:]
# print(textFileArray)
# obj.deleteFileWithKey(opath,'pdf','/')

# list = ['RV-2020_00001505.txt','RV-2020_00001493.txt','RV-2020_00001452.txt','RV-2020_00002377.txt','RV-2020_00002257.txt', 'RV-2020_00002261.txt',
#         'RV-2020_00002249.txt','RV-2020_00002222.txt','RV-2020_00002385.txt','RV-2020_00002264.txt','RV-2020_00002265.txt','RV-2020_00002229.txt',
#         'RV-2020_00001949.txt','RV-2020_00002438.txt','RV-2020_00002444.txt','RV-2020_00002442.txt','RV-2020_00002431.txt','RV-2020_00002239.txt',
#         'RV-2020_00002141.txt','RV-2020_00002012.txt','RV-2020_00002426.txt','RV-2020_00002340.txt','RV-2020_00002324.txt','RV-2020_00002221.txt',
#         'RV-2020_00002206.txt','RV-2020_00002441.txt','RV-2020_00002430.txt','RV-2020_00002435.txt','RV-2020_00002428.txt','RV-2020_00002347.txt',
#         'RV-2020_00002348.txt','RV-2020_00002266.txt','RV-2020_00002266.txt','RV-2020_00002237.txt','RV-2020_00002236.txt','RV-2020_00002220.txt',
#         'RV-2020_00002204.txt','RV-2020_00002152.txt','RV-2020_00002838.txt','RV-2020_00002822.txt','RV-2020_00002742.txt','RV-2020_00002738.txt',
#         'RV-2020_00002733.txt','RV-2020_00002665.txt','RV-2020_00002667.txt','RV-2020_00002657.txt','RV-2020_00002629.txt','RV-2020_00002608.txt',
#         'RV-2020_00002619.txt','RV-2020_00002607.txt','RV-2020_00002448.txt','RV-2020_00002846.txt','RV-2020_00002817.txt','RV-2020_00002797.txt',
#         'RV-2020_00002793.txt','RV-2020_00002795.txt','RV-2020_00002696.txt','RV-2020_00002652.txt','RV-2020_00002603.txt','RV-2020_00002602.txt',
#         'RV-2020_00002597.txt','RV-2020_00002466.txt','RV-2020_00002462.txt','RV-2020_00002455.txt','RV-2020_00002920.txt','RV-2020_00002907.txt',
#         'RV-2020_00002881.txt','RV-2020_00002862.txt','RV-2020_00002870.txt','RV-2020_00002788.txt','RV-2020_00002758.txt','RV-2020_00002769.txt',
#         'RV-2020_00002751.txt','RV-2020_00002744.txt','RV-2020_00002703.txt','RV-2020_00002673.txt','RV-2020_00002666.txt','RV-2020_00002642.txt',
#         'RV-2020_00002636.txt','RV-2020_00002633.txt','RV-2020_00002626.txt','RV-2020_00002617.txt','RV-2020_00002611.txt','RV-2020_00002491.txt',
#         'RV-2020_00002486.txt','RV-2020_00002628.txt','RV-2020_00002620.txt','RV-2020_00002718.txt','RV-2020_00002718.txt','RV-2020_00002709.txt',
#         'RV-2020_00002692.txt','RV-2020_00002672.txt','RV-2020_00002640.txt','RV-2020_00002631.txt','RV-2020_00002496.txt','RV-2020_00002496.txt',
#         'RV-2020_00002488.txt','RV-2020_00003354.txt','RV-2020_00003224.txt','RV-2020_00003231.txt','RV-2020_00003032.txt','RV-2020_00003001.txt',
#         'RV-2020_00002999.txt','RV-2020_00002966.txt','RV-2020_00003255.txt','RV-2020_00003166.txt','RV-2020_00003149.txt','RV-2020_00003116.txt',
#         'RV-2020_00003086.txt','RV-2020_00003436.txt','RV-2020_00003419.txt','RV-2020_00003293.txt','RV-2020_00003267.txt','RV-2020_00003196.txt',
#         'RV-2020_00003119.txt','RV-2020_00003090.txt','RV-2020_00003045.txt','RV-2020_00003039.txt','RV-2020_00003017.txt','RV-2020_00003010.txt',
#         'RV-2020_00002991.txt','RV-2020_00002987.txt','RV-2020_00002955.txt','RV-2020_00003432.txt','RV-2020_00003430.txt','RV-2020_00003368.txt',
#         'RV-2020_00003363.txt','RV-2020_00003046.txt','RV-2020_00003034.txt','RV-2020_00003676.txt','RV-2020_00003672.txt','RV-2020_00003610.txt',
#         'RV-2020_00003457.txt','RV-2020_00003455.txt','RV-2020_00003471.txt','RV-2020_00003450.txt','RV-2020_00003502.txt','RV-2020_00003788.txt',
#         'RV-2020_00003788.txt','RV-2020_00003788.txt','RV-2020_00003780.txt','RV-2020_00003627.txt','RV-2020_00003569.txt','RV-2020_00003507.txt',
#         'RV-2020_00003708.txt','RV-2020_00003656.txt','RV-2020_00003660.txt','RV-2020_00003862.txt','RV-2020_00003669.txt','RV-2020_00003671.txt',
#         'RV-2020_00003611.txt','RV-2020_00003603.txt','RV-2020_00003997.txt','RV-2020_00003987.txt','RV-2020_00004372.txt','RV-2020_00004348.txt',
#         'RV-2020_00004420.txt','RV-2020_00004423.txt','RV-2020_00004418.txt','RV-2020_00004364.txt','RV-2020_00004358.txt','RV-2020_00004265.txt',
#         'RV-2020_00004038.txt','RV-2020_00004780.txt','RV-2020_00004728.txt','RV-2020_00005401.txt','RV-2020_00005347.txt','RV-2020_00005350.txt',
#         'RV-2020_00005345.txt','RV-2020_00005343.txt','RV-2020_00005163.txt','RV-2020_00005160.txt','RV-2020_00005079.txt','RV-2020_00005051.txt',
#         'RV-2020_00005218.txt','RV-2020_00005198.txt','RV-2020_00005142.txt','RV-2020_00005126.txt','RV-2020_00005119.txt','RV-2020_00005122']
#
# print(len(textFileArray))
#
# for each in list:
#     # print(each)
#     if each in textFileArray:
#         textFileArray.remove(each)
#
# print(len(textFileArray))
# print(textFileArray)
# if textFileArray:
#     for item in textFileArray:
#         obj.deleteFileWithKey(opath, item, '/')