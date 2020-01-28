import json
from fuzzysearch import find_near_matches
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Locator tag Test

def regularExpressionHandling(data, flag):
    """
    Convert special characters for processing regualar expression
    :param data:
    :param flag: selecting conversion, 0 for conversion, 1 for undo the conversion
    :return: data based on flag, False if error occured
    """
    try:
        if flag == 0:
            data = data.replace('\\', '\\\\')
            data = data.replace('(', '\(')
            data = data.replace(')', '\)')
            data = data.replace('.', '\.')
            data = data.replace('+', '\+')
            data = data.replace('[', '\[')
            data = data.replace(']', '\]')
            data = data.replace('|', '\|')
            data = data.replace('/', '\/')
            data = data.replace('?', '\?')
            data = data.replace('"', '\\"')
            data = data.replace('*', '\*')
            data = data.replace('$', '\$')
            data = data.replace('{', '\{')
            data = data.replace('}', '\}')

            return data
        if flag == 1:
            data = data.replace('\(', '(')
            data = data.replace('\)', ')')
            data = data.replace('\.', '.')
            data = data.replace('\+', '+')
            data = data.replace('\[', '[')
            data = data.replace('\]', ']')
            data = data.replace('\|', '|')
            data = data.replace('\/', '/')
            data = data.replace('\?', '?')
            data = data.replace('\\"', '"')
            data = data.replace('\*', '*')
            data = data.replace('\$', '$')
            data = data.replace('\{', '{')
            data = data.replace('\}', '}')
            data = data.replace('\\\\', '\\')

            return data
        else:
            print('invalid flag in regularExpressionHandling')
            return False
    except Exception as e:
        print('error in regularExpressionHandling in GeneralExceptoinHandling', e)
        return False
fuzzySearchOptimumLength = 6

def getFuzzySearchData(qs, ls, threshold=60) -> list:
    """
    Fuzzy search data,
    This part play major role of selecting fuzzy string amoung list
    String length less than optimum result need to process seperately
    :param qs: String for serching
    :param ls: Main set of string to search in
    :param threshold: threshold for fuzzy
    :return: Fuzzy array
    :Todo: qs length might getting verry low upto 1, need to check on it, This will get wrong result
    """
    try:
        fuzzyWordArray = []

        if len(qs)<fuzzySearchOptimumLength:
            processThreshold=90
            max_l_dist = 0
        else:
            processThreshold = threshold
            max_l_dist = 1

        processThreshold = 57

        print('extract bessss:', process.extractBests(qs, (ls,), score_cutoff=processThreshold))

        for word, confidence in process.extractBests(qs, (ls,), score_cutoff=processThreshold):
            # print('fuzzy', qs, confidence)
            # print('word {}'.format(word))
            print('word:', word, 'confidene', confidence)

            for match in find_near_matches(qs, word, max_l_dist=max_l_dist):
                match = word[match.start:match.end]
                fuzzyWordArray.append(match)



                # if word == 'RECORDING REQUESTED BY FIRST AMERICAN TITLE AND WHEN RECORDED MAIL DOCUMENT TO: MR. AND MRS. DAVID PARRISH 14216 HALPER ROAD POWAY, CA 92064 SPACE ABOVE THIS LINE FOR RECORDER':
                #     print(word, confidence, qs, match)
        return fuzzyWordArray
    except Exception as e:
        print('error in getFuzzySearchData in stringHandling', e)
        return False

def buildEachLocatorTagPattern(eachLocatorArray,i, sourceDataProcessed, patternBuild):
    try:
        import re

        eachLocator = eachLocatorArray.upper()
        """considering if a string contains number, prevent it for fuzzy search"""
        # searchOnlyNumAndCharObj = re.search(r'^[0-9-`!@#$%^&*()_+=\\|}\]\[{\';:\/\?>\.,<~ ]+$', eachLocator)
        searchOnlyNumAndCharObj = re.search(r'[0-9]', eachLocator)
        if searchOnlyNumAndCharObj:
            """ Converting number to coresponding regular expression """
            bestMatch = re.sub('\d', '\d', eachLocator)
            # print('pattern found', bestMatch)

            if i == 0:
                patternBuild = patternBuild + bestMatch
            else:
                patternBuild = patternBuild + '(.*)' + bestMatch
        else:
            """ Get fuzzy matching string array """
            matchingFuzzyWord = getFuzzySearchData(eachLocator, sourceDataProcessed)
            print('locator', eachLocator)
            print('fuzzy string; ', matchingFuzzyWord)
            print('extract best: ', process.extractBests(eachLocator, matchingFuzzyWord))
            if len(process.extractBests(eachLocator, matchingFuzzyWord)) > 0:
                """ 
                    Find the best amoung them
                    It is very importent for selecting appropriate confidence limit, one thing is based on string length
                    :todo: find other parameters for improving
                """
                if len(eachLocator) < 5:
                    confidenceLimit = 90
                else:
                    confidenceLimit = 80

                bestMatch, confidence = process.extractBests(eachLocator, matchingFuzzyWord, limit=1)[0]

                if len(matchingFuzzyWord) > 0 and confidenceLimit < confidence:
                    bestMatch = regularExpressionHandling(bestMatch, 0)
                    if i == 0:
                        patternBuild = patternBuild + bestMatch
                    else:
                        patternBuild = patternBuild + '(.*)' + bestMatch

                    return patternBuild
                else:
                    if i == 0 or len(eachLocatorArray) == i + 1:
                        """ if first or last locator doesnot match then no need for further process (Improvement in searching) """
                        print('i=0 index')
                        return False
            elif len(matchingFuzzyWord) == 0 and (i == 0 or len(eachLocatorArray) == i + 1):
                """ if first or last locator doesnot match then no need for further process (Improvement in searching) """
                print('less than index')
                return False
    except Exception as e:
        print('error in buildEachLocatorTagPattern in StringHandling', e)
        return False

# eachLocatorArray = 'TICOR TITLE COMPANY'
# patternBuild = '('
# sourceDataProcessed = 'RECORDING REQUESTED BY I | INU NA PELL AAN EARL THIS DOCUMENT PEE 09, SO EOOENE AND TAX STATEMENTS TO: EMOTE DENE AC OROS MANUEL PADILLA AND JUANITA PADILLA SAN DIEGO COUNTY RECORDER 1958 WIND RIVER ROAD FEES: EEE WEE AE $0.00) EL CAJON CA 92019 PAGES: 3 APN: 518-082-45-00 1 | ESCROW NO: SDL90684-LT147-SG . TITLE NO: 00645244-995-CC1 | _. SE 2 SPACE ABOVE THIS LINE FOR RECORDER\'S USE GRANT DEED THE UNDERSIGNED GRANTOR(S) DECLARE(S) DOCUMENTARY TRANSFER TAX IS $781.00, CITY TRANSFER TAX $ COMPUTED ON FULL VALUE OF PROPERTY CONVEYED , AND EER FOR A VALUABLE CONSIDERATION, RECEIPT OF WHICH IS HEREBY ACKNOWLEDGED, BRET A INGOLD AND AMY M INGOLD, HUSBAND AND WIFE AS JOINT TENANTS HEREBY GRANT(S) TO MANUEL A. PADILLA AND JUANITA T PADILLA , HUSBAND AND WIFE AS JOINT TENANTS THE FOLLOWING DESCRIBED REAL PROPERTY IN THE COUNTY OF SAN DIEGO, STATE OF CALIFORNIA: T FOR LEGAL DESCRIPTION OF THE REAL PROPERTY HEREIN, SEE EXHIBIT A ATTACHED HERETO AND - MADE A PART HEREOF. COMMONLY KNOWN AS: 1958 WIND RIVER ROAD, EL CAJON, CA 92019 DATED:_NOVEMBER¥I8, 2019... __ OS : BAT O.. BO | B: $ RET. A INGO! THIS DOCUMENT IS EXECUTED IN COUNTERPART | POR MEENERE AED AMY M INGOLD ’ [A NOTARY PUBLIC OR OTHER OFFICER COMPLETING THIS CERTIFICATE VERIFIES ONLY THE IDENTITY OF THE INDIVIDUAL WHO SIGNED THE I DOCUMENT TO WHICH THIS CERTIFICATE IS ATTACHED, AND NOT ‘THE TRUTHFULNESS, ACCURACY, OR VALIDITY OF THAT DOCUMENT. F STATE OF-CAHIFORNIZ “TSK AS ) JER, ) SS. COUNTY OF TARRAAN £ OP) ON AL / AE (19, . BEFORE ME, BEF’ AVY B-LWOOD . __, NOTARY PUBLIC, PERSONALLY APPEARED BRET A. TW ALD |. _ . _ _- - WHO PROVED TO ME ON THE BASIS OF SATISFACTORY EVIDENCE) TO BE THE PERSON(S) WHOSE NAME(S) IS/ARE SUBSCRIBED TO - THE WITHIN INSTRUMENT AND ACKNOWLEDGED TO ME THAT HE/SHE/THEY EXECUTED THE SAME IN HIS/HER/THEIR AUTHORIZED CAPACITY(LES), AND THAT BY HIS/HER/THEIR SIGNATURE(S) ON THE INSTRUMENT THE PERSON(S), OR THE ENTITY UPON BEHALF OF WHICH THE PERSON(S) ACTED, EXECUTED THE INSTRUMENT. I CERTIFY UNDER PENALTY OF PERJURY UNDER THE LAWS OF THE STATE OF CALIFORNIA THAT THE FOREGOING PARAGRAPH IS TRUE . . AND CORRECT. & BY TEXAS DRIVES LICENSE. WITNESS MY HAND AND OFFICIAL SEAL. I = KEP JEFFREY G WOOD 4 AOA) NOTARY ID 4129004307 ¢ E IE} BY COMMISSION EXPIRES QX MAY 24, 2020 EWW WE WW OW WW EWW SIGNATURE +++++-----+++++RECORDING REQUESTED BY | TICOR TITLE COMPANY | WHEN RECORDED MAIL THIS DOCUMENT . AND TAX STATEMENTS TO: | MANUEL PADILLA AND JUANITA PADILLA 1958 WIND RIVER ROAD EL CAJON CA 92019 APN: 518-082-45-00 ESCROW NO: SDL90684-LT147-SG TITLE NO: 00645244-995-CC1_ GRANT DEED THE UNDERSIGNED GRANTOR(S) DECLARE(S) DOCUMENTARY TRANSFER TAX IS $#84-00, CITY TRANSFER TAX $ {& COMPUTED ON FULL VALUE OF PROPERTY CONVEYED , AND SPACE ABOVE THIS LINE FOR RECORDER'
# patternBuild = buildEachLocatorTagPattern(eachLocatorArray,0, sourceDataProcessed, patternBuild)
# print(patternBuild)