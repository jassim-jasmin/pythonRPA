import os

class DrectoryHandling:
    def createDirectory(self, path):
        try:
            import os
            os.mkdir(path)

            return True
        except Exception as e:
            return True