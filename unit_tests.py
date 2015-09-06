import logging, utilsReddit, db, sqlite3, os
import getPicturesReddit

CLR_FAIL = '\033[91m'
CLR_INFO = '\033[94m'
CLR_OK   = '\033[92m'
CLR_END  = '\033[0m'

def _assertTest(elementToTest, elementResult, errorMsg):
    try:
        assert(elementToTest == elementResult), errorMsg
    except AssertionError as e:
        print(CLR_INFO, "test ", e, CLR_FAIL, " not passed", CLR_END, sep='')
        return False
    else:
        print(CLR_INFO, "test ", elementToTest, CLR_OK, " passed", CLR_END, sep='')
        return True

def printInfo(msg):
    print(CLR_INFO, msg, CLR_END, sep='')

def testRegexExtractAnime():
    print("______________________")
    printInfo("testRegexExtractAnime {}started".format(CLR_OK))
    error = True
    lstStart = ["Double docking [Kantai Collection][x-post from /r/kanmusu]",
           "Double dockin[g",
           "Double docki]g",
           "Double docking [x-post from /r/kanmusu] [Kantai Collection]"]
    lstAssert = ["Kantai Collection",
                 False,
                 False,
                 "Kantai Collection"]
    for i, elt in enumerate(lstStart):
        res = utilsReddit.extractAnimeName(elt)
        ret = _assertTest(res, lstAssert[i], "Extraction failed for {}'{}'{}".format(CLR_INFO, elt, CLR_END))
        error = ret if error == True else True
    if not error:
        print(CLR_INFO, "testRegexExtractAnime ", CLR_FAIL, "not ok", CLR_END, sep='')
    else:
        print(CLR_INFO, "testRegexExtractAnime ", CLR_OK, "passed", CLR_END, sep='')
    print("______________________")

def testCreateFolder():
    print("______________________")
    printInfo("testCreateFolder {}started".format(CLR_OK))
    folderName = 'createFolderTest'
    if not utilsReddit.createFolder('./' + folderName):
        printInfo("testCreateFolder {}not ok".format(CLR_FAIL))
    else:
        printInfo("test 1 {}passed".format(CLR_OK))
        if utilsReddit.createFolder('./' + folderName) != None:
            printInfo("testCreateFolder {}not ok".format(CLR_FAIL))
        else:
            os.rmdir('./' + folderName)
    printInfo("testCreationDatabase {}passed".format(CLR_OK))
    print("______________________")

def testCreationDatabase():
    try:
        print("______________________")
        printInfo("testCreationDatabase {}started".format(CLR_OK))
        mydb = db.Database('unit_tests.db')
        print("Database unit_tests.db created")
        print("anime table created")
        print("pictures table created")
        printInfo("testCreationDatabase {}passed".format(CLR_OK))
        print("______________________")
        return mydb
    except sqlite3.OperationalError:
        print("unable to create")
        printInfo("testCreationDatabase {}not ok".format(CLR_FAIL))
        print("______________________")
        return False

def testAddEntryAnime(mydb):
    print("______________________")
    printInfo("testAddEntryAnime {}started".format(CLR_OK))
    name = "Zero no Tsukaima"
    myId = mydb._addEntryAnime(name, 0)
    if not myId:
        print("Unable to add {} in anime".format(name))
        printInfo("testAddEntryAnime {}not ok".format(CLR_FAIL))
        print("______________________")
        return False
    else:
        print("{} in anime added with id: ".format(name), myId)
    sameId = mydb._addEntryAnime(name, 1)
    if not sameId:
        print("Error for the same one")
        printInfo("testAddEntryAnime {}not ok".format(CLR_FAIL))
        print("______________________")
        return False
    if myId != sameId:
        print("sameId({}) isn't equal to myId({})".format(sameId, myId))
        printInfo("testAddEntryAnime {}not ok".format(CLR_FAIL).format(CLR_FAIL))
        print("______________________")
        return False
    else:
        print("sameId({}) = myId({})".format(sameId, myId))
    printInfo("testAddEntryAnime {}passed".format(CLR_OK))
    print("______________________")

def testAddEntryPictures(mydb):
    print("______________________")
    printInfo("testAddEntryPictures {}started".format(CLR_OK))
    name = "Yukina Himeragi is the female protagonist"
    filename = "testAddEntryPictures.jpg"
    url = "http://testAddEntryPictures.jpg"
    anime = "Strike The Blood"
    idAnime = mydb._addEntryAnime(anime, 0)
    if not idAnime:
        print("Unable to add {} in anime".format(anime))
        printInfo("testAddEntryPictures {}not ok".format(CLR_FAIL))
        print("______________________")
        return False
    myId = mydb._addEntryPictures(name, filename, url, idAnime)
    if not myId:
        print("Unable to add {} in pictures".format(name))
        printInfo("testAddEntryPictures {}not ok".format(CLR_FAIL))
        print("______________________")
        return False
    printInfo("testAddEntryPictures {}passed".format(CLR_OK))
    print("______________________")

def testCheckEntryAnime(mydb):
    print("______________________")
    printInfo("testCheckEntryAnime {}started".format(CLR_OK))
    myId = mydb._addEntryAnime("Sword Art Online", 0)
    if not myId:
        print("Unable to add Sword Art Online in anime")
        printInfo("testCheckEntryAnime {}not ok".format(CLR_FAIL))
        print("______________________")
        return False
    nbEntries = mydb.checkEntryAnime("Sword Art Online")
    if not nbEntries:
        print("Unable to execute select in anime")
        printInfo("testCheckEntryAnime {}not ok".format(CLR_FAIL))
        print("______________________")
        return False
    elif nbEntries == 1:
        print("Sword Art Online entry found in anime table")
        printInfo("testCheckEntryAnime {}passed".format(CLR_OK))
        print("______________________")
    else:
        print("multi entries found for Sword Art Online in anime table")
        printInfo("testCheckEntryAnime {}not ok".format(CLR_FAIL))
        print("______________________")
        return False

def testCheckEntryPictures(mydb):
    print("______________________")
    printInfo("testCheckEntryPictures {}started".format(CLR_OK))
    name = "Sora and his sister, Shiro"
    filename = "image_test.jpg"
    url = "http://image.com/image_test.jpg"
    anime = "No Game No Life"
    idAnime = mydb._addEntryAnime(anime, 0)
    if not idAnime:
        print("Unable to add {} in anime".format(anime))
        printInfo("testCheckEntryPictures {}not ok".format(CLR_FAIL))
        print("______________________")
        return False
    myId = mydb._addEntryPictures(name, filename, url, idAnime)
    if not myId:
        print("Unable to add {} in pictures".format(name))
        printInfo("testCheckEntryPictures {}not ok".format(CLR_FAIL))
        print("______________________")
        return False
    nbEntries = mydb.checkEntryPictures(url)
    if not nbEntries:
        print("Unable to execute select in pictures")
        printInfo("testCheckEntryPictures {}not ok".format(CLR_FAIL))
        print("______________________")
        return False
    elif nbEntries == 1:
        print("{} entry found in pictures table".format(name))
        printInfo("testCheckEntryPictures {}passed".format(CLR_OK))
        print("______________________")
    else:
        print("Error: multi entries found for {} in anime table".format(name))
        printInfo("testCheckEntryPictures {}not ok".format(CLR_FAIL))
        print("______________________")
        return False


def main():
    if os.path.exists('./logs/unit_tests.log'):
        os.remove('./logs/unit_tests.log')
    logging.basicConfig(filename='unit_tests.log', format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    testRegexExtractAnime()
    testCreateFolder()
    mydb = testCreationDatabase()
    testAddEntryAnime(mydb)
    testAddEntryPictures(mydb)
    testCheckEntryAnime(mydb)
    testCheckEntryPictures(mydb)
    del mydb
    os.remove('unit_tests.db')

if __name__ == '__main__':
    main()
