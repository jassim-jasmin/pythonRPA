import csv
import pandas as pd

class CsvHandling:
    def readCsvAsDict(self, pathWithFileName):
        try:
            fp = open(pathWithFileName, mode='r')
            if fp.readable():
                csv_reader = csv.DictReader(fp.read())
                return csv_reader
            else:
                return False

        except Exception as e:
            print('error in readCsvAsDict in CSVHandling', e)
            return False
        finally:
            try:
                fp.close()
            except Exception as e:
                pass

    def readCsvColumn(self, pathWithFileName, columnName):
        try:
            df = pd.read_csv(pathWithFileName, engine='python')
            print(df.columns)
            if columnName in df:
                return df[columnName]
            else:
                return False
        except Exception as e:
            print('error in readCsvColumn in CSVHandling', e)
            return False