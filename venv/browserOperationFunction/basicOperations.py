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
        return "https://www.google.com/search?client=ubuntu&channel=fs&q=" +text+ "&ie=utf-8&oe=utf-8"