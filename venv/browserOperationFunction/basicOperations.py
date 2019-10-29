import json

class BasicOptions:
    def buttonClick(self, butonId):
        try:
            browser.find_element_by_xpath("//button[@id ='" + butonId + "']").click()
            return True
        except Exception as e:
            print(e)
            return False

    def findInputAndInsert(self, fieldIdName, inputValue):
        try:
            a = browser.find_element_by_xpath("//input[@id ='" + fieldIdName + "']")
            a.send_keys(inputValue)
            return True
        except Exception as e:
            print(e)
            return False

    def loginAdmin(self):
        try:
            findInputAndInsert('username', 'admin')
            findInputAndInsert('password', 'donotusethispassword')
            buttonClick('login')
            return True
        except Exception as e:
            print(e)
            return False

    def searchGoogle(self,text):
        url = json.loads(open("/root/Documents/mj/python/rpaPython/venv/PageData/basicData.json","r").read())['profile1']["googleSearchUrl"]
        return url.replace('text',text)