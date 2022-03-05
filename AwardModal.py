import os
import codecs
import random

class AwardModal():
    # 待抽奖名单
    candidateList = []
    
    # 预订中奖名单
    preList = [[], [], [], [], []]
    
    # 每个奖项不参与抽奖名单
    exceptList = [[], [], [], [], []]
    
    # 抽奖结果名单
    resultList = [[], [], [], [], []]
    
    showList = []                   # 抽完后显示用列表
    
    thisLevelList = [[], []]        # 本次抽取时待抽列表，第一列是名字，第二列是在 candidateList 中的位置
    
    allNumberDisplay = ""
    
    # 从文件中读取所有抽奖名单数据及预订奖项数据
    def get_data_from_file():
        fp = codecs.open("data/list.txt", "r", "utf-8")
        for oneLine in fp.readlines():
            txt = oneLine[:-1].rstrip()
            if (txt.count(',') == 1):
                degree = int(txt[-1]) - 1
                preNumber = txt[:-2]
                AwardModal.preList[degree].append(preNumber)
            else:
                AwardModal.candidateList.append(txt)
        fp.close()
     
    # 从文件中读取每个奖项不参与抽奖名单数据   
    def ReadExceptList():
        if (not os.path.isfile("data/except.txt")):
            return

        fp = codecs.open("data/except.txt", "r", "utf-8")
        for oneLine in fp.readlines():
            txt = oneLine[:-1].rstrip()
            if (txt.count(',') == 1):
                degree = int(txt[-1]) - 1
                preNumber = txt[:-2]
                AwardModal.exceptList[degree].append(preNumber)
        fp.close()

    # 从文件中读取前次已经抽奖的结果数据
    def ReadResultList():
        if (not os.path.isfile("data/result.txt")):
            #print "No Result File!"
            return

        fp = codecs.open("data/result.txt", "r+", "utf-8")
        for oneLine in fp.readlines():
            if oneLine == "":
                continue
            txt = oneLine[:-1]
            degree = int(txt[0])
            resultNumber = txt[2:]
            AwardModal.resultList[degree - 1].append(resultNumber)
            if (resultNumber in AwardModal.candidateList):
                AwardModal.candidateList.remove(resultNumber)
        fp.close()

    # 保存本次抽奖结果到文件
    def SaveResult(degree):
        fp = codecs.open("data/result.txt", "a", "utf-8")
        for item in AwardModal.showList:
            AwardModal.resultList[degree-1].append(item)
            #print str(degree) + "," + theNumberDisplay
            fp.write(str(degree) + "," + item + "\n")
        fp.close()
        
    def getRandom(maxNumber):
        theRandom = random.randint(1, maxNumber)
        return theRandom

    def getRandomCandicate():
        currentNumber = AwardModal.getRandom(len(AwardModal.candidateList))
        return AwardModal.candidateList[currentNumber - 1]
        
    def getThisDegreeResult(degree, limit):
        trueDegree = degree - 1
        print("trueDegree: ", trueDegree)
        AwardModal.showList = []

        AwardModal.thisLevelList = []
        for item in AwardModal.candidateList:
            AwardModal.thisLevelList.append(item)
        for item in AwardModal.exceptList[trueDegree]:
            if (item in AwardModal.thisLevelList):
                AwardModal.thisLevelList.remove(item)

        for i in (range(0, limit)):
            if (len(AwardModal.preList[trueDegree]) > 0):
                theNumberDisplay = AwardModal.preList[trueDegree][0]
                del AwardModal.preList[trueDegree][0]
                if theNumberDisplay in AwardModal.thisLevelList:
                    AwardModal.thisLevelList.remove(theNumberDisplay)
            else:
                if len(AwardModal.thisLevelList) == 0:
                    break
                theNumber = AwardModal.getRandom(len(AwardModal.thisLevelList))
                theNumberDisplay = AwardModal.thisLevelList[theNumber - 1]
                del AwardModal.thisLevelList[theNumber - 1]
            if theNumberDisplay in AwardModal.candidateList:
                AwardModal.candidateList.remove(theNumberDisplay)
            AwardModal.showList.append(theNumberDisplay)
        AwardModal.SaveResult(degree)