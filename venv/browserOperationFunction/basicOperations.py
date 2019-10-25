class BasicOptions:
    def buttonClick(self, butonId):
        browser.find_element_by_xpath("//button[@id ='" + butonId + "']").click()

    def findInputAndInsert(self, fieldIdName, inputValue):
        a = browser.find_element_by_xpath("//input[@id ='" + fieldIdName + "']")
        a.send_keys(inputValue)

    def loginAdmin(self):
        findInputAndInsert('username', 'admin')
        findInputAndInsert('password', 'donotusethispassword')
        buttonClick('login')