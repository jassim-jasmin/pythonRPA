import json

class BasicOptions:
    def buttonClick(self, browser, butonId):
        try:
            browser.find_element_by_xpath("//button[@id ='" + butonId + "']").click()
            return True
        except Exception as e:
            print(e, 'in BasicOptions buttonClick')
            return False

    def findInputAndInsert(self, browser, fieldIdName, inputValue):
        try:
            a = browser.find_element_by_xpath("//input[@id ='" + fieldIdName + "']")
            a.send_keys(inputValue)
            return True
        except Exception as e:
            print(e, 'in BasicOptions findInputAndInsert')
            return False

    def loginAdmin(self):
        try:
            findInputAndInsert('username', 'admin')
            findInputAndInsert('password', 'donotusethispassword')
            buttonClick('login')
            return True
        except Exception as e:
            print(e, 'in BasicOptions loginAdmin')
            return False

    def searchGoogle(self,text):
        try:
            url = json.loads(open("/root/Documents/mj/python/rpaPython/venv/PageData/basicData.json","r").read())['profile1']["googleSearchUrl"]
            return url.replace('text',text)
        except Exception as e:
            print(e)

    def findMap(self, browser):
        try:
            browser.find_element_by_xpath("//img[@id ='lu_map']")
            return True
        except Exception as e:
            print(e, 'in BasicOptions custom')
        return False
