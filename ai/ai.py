from sklearn import  tree


def trainingSet1(self):
    X = [[181, 80, 44], [177, 70, 43], [160, 60, 38],
         [154, 54, 37], [166, 65, 40], [190, 90, 47], [175, 64, 39],
         [177, 70, 40], [159, 55, 37], [171, 75, 42],
         [181, 85, 43], [168, 75, 41], [168, 77, 41]]

    Y = ['male', 'male', 'female', 'female', 'male', 'male', 'female', 'female', 'female', 'male', 'male', 'female',
         'female']
    return X, Y


def testData1(self):
    return [[190, 70, 43], [154, 75, 38], [181, 65, 40]]


def trainingSet2(self):
    X = [['jassim', 'jasmin'], ['test1', 'test2']]
    Y = ['me', 'idontkonw']

    return X, Y


def testData2(self):
    return [['jassim', 'jasmin']]


def locatorDemo(self):
    try:
        print('locatorDemo')

    except Exception as e:
        print('error in locator demo', e)


def desisionTreeTest(self):
    X, Y = self.trainingSet1()
    test_data = self.testData1()

    test_labels = ['male', 'female', 'male']

    # dtc_clf = tree.DecisionTreeClassifier()
    # dtc_clf = dtc_clf.fit(X, Y)
    # dtc_prediction = dtc_clf.predict(test_data)
    # print(dtc_prediction)

    # stringHandling = StringHandling(self.path)

    # stringHandling.Test()
    # self.Test()