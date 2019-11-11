import sys
from selenium import webdriver
import time
import json
import re

# try:
#     from googlesearch import search
# except ImportError:
#     print("No module named 'google' found")

sys.path.insert(0,'../browserOperationFunction')
from basicOperations import BasicOptions

sys.path.insert(0,'../sql')
from sqlDB import sqlDB

# def SearchGoogle(search):
#     try:
#         browser = webdriver.Firefox(executable_path=basicData['executable_path'])
#         browser.get(BasicOptions.searchGoogle(BasicOptions, search))
#         if BasicOptions.findMap(BasicOptions, browser):
#             data.append(search)
#             print('find address')
#         else:
#             print('no address')
#         browser.close()
#         return True
#     except Exception as e:
#         browser.close()
#         print(e)
#         return False


start = time.time()

basicData = json.loads(open('../PageData/basicData.json','r').read())['profile1']
# browser = webdriver.Firefox(executable_path=basicData['executable_path'])


obj = sqlDB()
obj.defaultZillow()
obj.connectSchema('testj')
noMatch = sqlDB.sqlSelect(obj, 'name', 'Addr_1_no_match', 'Addr_1_no_match is not null limit 10')

data = []
for name in noMatch:
    data.append(name[0])
#     # query = "http://maps.google.com/?q=2+SEASIDE+LN+#801" + name[0].replace(' ', '+')
#     #
#     # for j in search(query, tld="com", num=10, stop=2, pause=2):
#     #     if re.search('mapques',j):
#     #         print('found', j, name[0])
#     #         data.append(j)
#     #     else:
#     #         print('not found ', j,name[0])
#
#     print(name[0])
#     if SearchGoogle(name[0]):
#         print('Completed search')
#     else:
#         print('Search failed')

# print(data,len(data))


# if SearchGoogle():
#     print('Completed search')
# else:
#     print('Search failed')

# browser.close()


def SearchGoogleLimit(search, address, limit):
    try:
        for i in range(len(search)):
            print(search[i])
            if (i%limit) == 0:
                if i != 0:
                    browser.close()
                browser = webdriver.Firefox(executable_path=basicData['executable_path'])

            browser.get(BasicOptions.searchGoogle(BasicOptions, search[i]))
            if BasicOptions.findMap(BasicOptions, browser):
                address.append(search[i])
                print('find address')
            else:
                print('no address')
        browser.close()
        return True
    except Exception as e:
        browser.close()
        print(e)
        return False

address = []
SearchGoogleLimit(data, address, 3)

print(address)
end = time.time()
print("Complete execution time: ", end - start)

