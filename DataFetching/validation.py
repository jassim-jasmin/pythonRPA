class LocatorValidation:
    def __init__(self):
        self.locatorValidationArray = dict()

    def assignValidationStatus(self, locatorId, status):
        try:
            self.locatorValidationArray[locatorId] = status

            return True
        except Exception as e:
            print('error in assignValidationStatus in validation', e)
            return False

    def getValidationStatus(self, locatorId):
        try:
            if locatorId in self.locatorValidationArray:
                status = self.locatorValidationArray[locatorId]
                return status
            else:
                return True
        except Exception as e:
            print('error in getValidationStatus', e)
            return False

    def absoluteValidation(self, locatorId, validationValue, status):
        try:
            if locatorId in self.locatorValidationArray:
                validation = self.locatorValidationArray[locatorId]
            else:
                validation = dict()
                validation[validationValue] = status
            self.locatorValidationArray[locatorId] = validation

            return True
        except Exception as e:
            print('error in assignValidationTrue', e)
            return False
    def assignValidationTrue(self, locatorId, status):
        try:
            if self.absoluteValidation(locatorId, 'True', status):
                return True
            else:
                return False
        except Exception as e:
            print('error in assignValidationTrue in validation', e)
            return False

    def assignValidationFalse(self, locatorId, status):
        try:
            if self.absoluteValidation(locatorId, 'False', status):
                return True
            else:
                return False
        except Exception as e:
            print('error in assignValidationTrue in validation', e)
            return False