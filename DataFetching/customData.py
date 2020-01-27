def connectingLocator() -> dict:
    """
    Connector for each locator in different layers
    :return: connector dictionary
    """
    try:
        connectorKeys = dict()

        # first locator key      = final locator key
        connectorKeys['parcel_number'] = 'parcel'
        connectorKeys['parcel_number_new'] = 'parcel_1'
        connectorKeys['formated_parcel_number'] = 'parcel_1'
        connectorKeys['titleName'] = 'title_search'
        # connectorKeys['parcel_data_2'] = 'parcel_2'

        # connectorKeys['parcel_number_1'] = 'parcel'
        # connectorKeys['lot'] = 'legal'
        # connectorKeys['block'] = 'legal'
        # connectorKeys['lot_1'] = 'legal'

        return connectorKeys
    except Exception as e:
        print('error in connectingLocator in DataFetching', e)
        return False


def getLayer1() -> list:
    """
    Custom locator asigning
    :return: locator array
    :Todo: Direct regular expression need to add (To improve fetching)
    """
    data = []
    # data.append(['legal', ['lot', 'block', 'plat']])
    # data.append(['legal', ['lot', 'block', 'plat', 'county']])
    # data.append(['legal', ['lot', 'plat', 'thereof']])
    # data.append(['parcel', ['271-02171-0101', 'parcel']])
    # data.append(['parcel', ['APN #;', 'R0235662']])
    # data.append(['parcel', ['A.P.N.', 'R1605212']])
    # data.append(['parcel', ['APN ', '17-02421']])
    data.append(['parcel_1', ['Parcel 1D Number:', 'R0235659 / 4009138524369']])
    data.append(['parcel_1', ['APN #:', '4-010-129-090-012']])
    data.append(['parcel_1', ['PARCEL NUMBER:', '4016159029035']])

    # data.append(['parcel_1', ['Parcel Number: 114-150-49-06']])
    data.append(['parcel_1', ['APN: 594-020-17-00']])
    data.append(['parcel_1', ['APN: 108-505-34']])
    data.append(['parcel_1', ['A.P.N.: 6205200200']])
    data.append(['parcel_1', ['A.P. # 278-424-31-00']])
    data.append(['parcel_1', ['APN/Parcel ID(s):', '465-192-06-00']])
    data.append(['parcel_1', ['APN No. 186-270-35']])
    data.append(['parcel_1', ['A.P.N.: 501-174-60-08']])
    data.append(['parcel_1', ['Assessor’s Parcel No. 624-440-33-00']])
    data.append(['parcel_1', ['Parcel N', '595-221-08-41']])
    data.append(['parcel_1', ['Tax Parcel/Bill No. 380-243-11-00']])
    data.append(['parcel_1', ['APN: 1876400500']])
    data.append(['parcel_1', ['Parcel/Account Number: 582-420-16-00']])
    data.append(['parcel_1', ['APN 254 - 222 -20-60']])
    data.append(['parcel_1', ['Tax ID No: 001516 (Map No.) 496-040-20-00 (Parcel No.)']])
    data.append(['parcel_1', ['A. P N. 447-390-11']])
    data.append(['parcel_1', ['A. P. N.: 216-53 1-15-00']])
    data.append(['parcel_2', ['594-020-17-00']])

    return data


def getValidation1() -> list:
    """
    Custom validation asigning
    :return: validation array
    :Todo: Pattern build need to add, only direct regular expressions are allowed
    """
    data = []
    # data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'))
    # data.append(('legal', '^ *\d', 'False'))
    # data.append(('parcel', '\d\d\d-\d\d\d\d\d-\d\d\d\d \d\d\d-\d\d\d\d\d-\d\d\d\d', 'False'))
    # data.append(('parcel', '\d\d\d\d\d\d\d\d', 'True'))
    # data.append(('parcel', '^A', 'True'))

    return data


def getLayer2() -> list:
    """
    Custom locator asigning
    :return: locator array
    """
    data = []

    # data.append(['parcel_number', ['271-02171-0101']])
    # data.append(['lot', ['LOT 1']])
    # data.append(['lot_1', ['lot three', 'LOT FOUR', 'LOT SIXTEEN', 'lots four']])
    # data.append(['block', ['BLOCK ELEVEN']])
    # data.append(['parcel_number', ['R0242052']])
    # data.append(['parcel_number', ['RO242052']])
    # data.append(['parcel_number', ['02-34000']])
    # data.append(['parcel_number_new', ['108-505-34']])

    data.append(['parcel_number_new', ['186-270-35']])
    data.append(['parcel_number_new', ['254 - 222 -20-60']])
    data.append(['parcel_number_new', ['6205200200']])
    data.append(['formated_parcel_number', ['4-010-129-090-012']])
    data.append(['formated_parcel_number', ['114-150-49-06']])
    # data.append(['parcel_data_2', ['594-020-17-00']])
    # data.append(['parcel_number', ['10-33009']])

    return data


def getValidation2() -> list:
    """
    Custom validation asigning
    :return: validation array
    """
    data = []
    # data.append(('lot', 'LOT [A-Z]$', 'False'))
    # data.append(('lot_1', '^[0-9]', 'False'))
    # data.append(('lot_1', 'LOT THREE \(3\)', 'False'))
    # data.append(('lot_1', 'STATE BAR', 'False'))
    # data.append(('lot', 'lot *[\\"]+', 'False'))
    # data.append(('lot', 'lot \w{2,}', 'False'))
    # data.append(('lot', '^[0-9]', 'False'))
    # data.append(('lot', 'one', 'true'))
    # data.append(('parcel_number','\d\d\d-\d\d\d\d\d-\d\d\d\d', 'True'))
    # data.append(('parcel_number', '\d\d\d\d\d\d', 'True'))

    return data


def getLayer3():
    data = []
    data.append(['title_search', ['RECORDING REQUESTED BY:', 'ABOVE THIS LINE FOR RECORDER']])
    data.append(['title_search', ['RECORDING REQUESTED', 'OFFICIAL RECORDS']])
    data.append(['title_search', ['RECORDING REQUESTED', 'RECORDER\'S USE ONLY']])
    data.append(['title_search_2', ['PRELIMINARY REPORT', 'YOUR REFERENCE']])
    return data

def getLayer4():
    data = []
    data.append(['titleName', ['CALIFORNIA MEMBERS TITLE CO']])
    data.append(['titleName', ['CALIFORNIA TITLE CO']])
    data.append(['titleName', ['Corinthian Title Company']])
    data.append(['titleName', ['CORINTHIAN TITLE']])
    data.append(['titleName', ['CORINTHIAN TITLE COMPANY INC']])
    data.append(['titleName', ['LANDWOOD TITLE COMPANY']])
    data.append(['titleName', ['Innovative Title Company']])
    data.append(['titleName', ['TicorTitle']])
    data.append(['titleName', ['AMERICAN COAST TITLE COMPANY']])
    data.append(['titleName', ['Fidelity National Title Company']])
    data.append(['titleName', ['TicoF Title']])
    data.append(['titleName', ['Ticor Tile Company']])
    data.append(['titleName', ['WEG National Tile Company']])
    data.append(['titleName', ['National Commercial Services']])
    data.append(['titleName', ['First American Title Insurance Company']])
    data.append(['titleName', ['AMERICAN COAST TITLE COMPANY']])
    data.append(['titleName', ['Fidelity National Title Company']])
    data.append(['titleName', ['Ticor Title Company']])
    data.append(['titleName', ['Ticor Title Company of California']])
    data.append(['titleName', ['Corinthian Title Company']])
    data.append(['titleName', ['Western Resources Title Company']])
    data.append(['titleName', ['Corinthian Title Company']])
    data.append(['titleName', ['WFG Tile Company']])
    data.append(['titleName', ['WEG Title Company']])
    data.append(['titleName', ['Ticor Title Company']])

    return data

def getValidation4():
    data = []
    data.append(('titleName', '^and title$', 'False'))
    data.append(('titleName', '^th title$', 'False'))

    return data

def getLayer5():
    data = []
    data.append(['accFlag', ['accommodation']])

    return data