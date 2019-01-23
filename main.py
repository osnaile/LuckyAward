# coding:utf-8
import wx
import random
import threading
import time
import os
import codecs
import PanelMain

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=u"抽奖", style=wx.MAXIMIZE | wx.DEFAULT_FRAME_STYLE)

        self.panel = PanelMain.PanelMain(self)
        self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

        countForThisTimeStr = u"本次抽出"
        self.countForThisTime = wx.StaticText(self.panel, label=countForThisTimeStr, pos=(80, 900))
        self.countForThisTime.SetBackgroundColour(wx.Colour(0, 0, 0, 255))
        self.countForThisTime.SetForegroundColour(wx.Colour(255, 255, 255, 255))
        self.inputForCount = wx.TextCtrl(self.panel, -1, u"50", size=(40, -1), style=wx.TE_CENTRE, pos=(150, 900))
        self.inputForCount.SetInsertionPoint(0)

        self.stopRollNumber = wx.Button(self.panel, label=u"停", pos=(1200, 900), size=(150, 50))
        self.Bind(wx.EVT_BUTTON, self.OnStopRollNumber, self.stopRollNumber)

        btnSize = (100, 30)
        self.GetForthButton = wx.Button(self.panel, label=u"抽取幸运奖", pos=(300, 910), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetForthButton, self.GetForthButton)

        self.GetThirdButton = wx.Button(self.panel, label=u"抽取三等奖", pos=(420, 910), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetThirdButton, self.GetThirdButton)

        self.GetSecondButton = wx.Button(self.panel, label=u"抽取二等奖", pos=(540, 910), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetSecondButton, self.GetSecondButton)

        self.GetFirstButton = wx.Button(self.panel, label=u"抽取一等奖", pos=(660, 910), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetFirstButton, self.GetFirstButton)

        self.GetSpecialButton = wx.Button(self.panel, label=u"抽取特等奖", pos=(780, 910), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetSpecialButton, self.GetSpecialButton)

        self.btnShowResultPanel = wx.Button(self.panel, label=u"显示上次结果", pos=(900, 950), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnBtnShowResultPanel, self.btnShowResultPanel)

        self.btnHideResultPanel = wx.Button(self.panel, label=u"关闭结果显示", pos=(1020, 950), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnBtnHideResultPanel, self.btnHideResultPanel)

        self.GetForthButton.Enable(True)
        self.GetThirdButton.Enable(True)
        self.GetSecondButton.Enable(True)
        self.GetFirstButton.Enable(True)
        self.GetSpecialButton.Enable(True)
        self.stopRollNumber.Enable(False)

        self.Bind(wx.EVT_CHAR_HOOK, self.OnKey)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.rollCount = 0

        self.LoadBGMain()
        self.LoadBGResult()
        self.bmp = self.bmpMain

        self.Show(True)
        self.ShowFullScreen(True, wx.FULLSCREEN_ALL)

        self.HCenter(self.panel.showNumber)
        self.HCenter(self.panel.txtTitle)

    def OnKey(self, event):
        code = event.GetKeyCode()
        print(code)
        if (code == 366) or (code == 367) or (code == 66):
            self.StopRoll()
        else:
            event.Skip()
        
    def ChangeBGToMain(self):
        self.bmp = self.bmpMain
        self.Refresh()

    def ChangeBGToResult(self):
        self.bmp = self.bmpResult
        self.Refresh()

    def LoadBGMain(self):
        image_file = "background.jpg"
        self.bmpMain = wx.Bitmap(image_file)

    def LoadBGResult(self):
        image_file = "bg_result.jpg"
        self.bmpResult = wx.Bitmap(image_file)

    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
            dc.Clear()
        bbr = wx.Brush(wx.Colour(0, 0, 0, 255), wx.BRUSHSTYLE_SOLID)
        dc.SetBackground(bbr)
        dc.SetBackgroundMode(wx.SOLID)
        dc.Clear()
        x, y = self.bmp.Size
        frame_width, frame_height = self.GetSize()
        x = frame_width / 2 - x / 2
        y = frame_height / 2 - y / 2
        dc.DrawBitmap(self.bmp, x, y)
        
    def OnStopRollNumber(self, e):
        self.StopRoll()
        
    def StopRoll(self):
        global bRolling
        if not bRolling:
            # print(u"Not Rolling")
            return

        self.timer.Stop()
        self.panel.showNumber.SetLabel(u"恭喜中奖")
        bRolling = False
        
        global currentLevel
        global currentMaxCount
        allNumberDisplay = getThisDegreeResult(currentLevel, currentMaxCount)
        self.showResult(currentLevel)
        currentMaxCount = 0
        self.GetForthButton.Enable(True)
        self.GetThirdButton.Enable(True)
        self.GetSecondButton.Enable(True)
        self.GetFirstButton.Enable(True)
        self.GetSpecialButton.Enable(True)
        self.stopRollNumber.Enable(False)
        
    def startRoll(self, degree, limit):
        global currentLevel
        global currentMaxCount
        global candidateList

        self.rollCount = len(candidateList)
        if self.rollCount == 0:
            dlg = wx.MessageDialog(self, u"所有人都已抽中", u"提示", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
            

        currentLevel = degree
        currentMaxCount = limit
        
        self.rollCount = len(candidateList)

        self.hideResult()
        
        self.timer.Start(100)
        self.stopRollNumber.Enable(True)
        self.GetForthButton.Enable(False)
        self.GetThirdButton.Enable(False)
        self.GetSecondButton.Enable(False)
        self.GetFirstButton.Enable(False)
        self.GetSpecialButton.Enable(False)

        global bRolling
        bRolling = True

    def HCenter(self, obj):
        frame_width, frame_height = self.GetSize()
        obj_width, obj_height = obj.GetSize()
        obj_pos = obj.GetPosition()
        x = frame_width / 2 - obj_width / 2
        obj_pos.x = x
        obj.SetPosition(obj_pos)
        
    def OnBtnShowResultPanel(self, event):
        global currentLevel
        self.showResult(currentLevel)

    def OnBtnHideResultPanel(self, event):
        self.hideResult()

    def getInputCount(self):
        return int(self.inputForCount.GetValue())

    def OnGetForthButton(self, e):
        self.startRoll(4, self.getInputCount())

    def OnGetThirdButton(self, e):
        self.startRoll(3, self.getInputCount())

    def OnGetSecondButton(self, e):
        self.startRoll(2, self.getInputCount())

    def OnGetFirstButton(self, e):
        self.startRoll(1, self.getInputCount()) 

    def OnGetSpecialButton(self, e):
        self.startRoll(0, self.getInputCount())

    def showResult(self, level):
        global arrLevel
        global showList
        lenShowList = len(showList)
        title = arrLevel[level][1]
        self.panel.showNumber.Hide()
        self.panel.txtTitle.SetLabel(u"获得" + title + u"的是")
        self.HCenter(self.panel.txtTitle)
        self.panel.txtTitle.Show()
        if lenShowList > 10:
            self.HCenter(self.panel.gridResult)
            self.panel.gridResult.ClearGrid()
            self.panel.gridResult.Show()
            row = 0
            col = 0
            if lenShowList <= 25:
                row = 2
            for item in showList:
                self.panel.gridResult.SetCellValue(row, col, item)
                col = col + 1
                if col == 5:
                    col = 0
                    row = row + 1
        else:
            txtToShow = u""
            for item in showList:
                txtToShow = txtToShow + item + "\n"
            self.panel.txtResult.SetLabel(txtToShow)
            willFontSize = 20
            if lenShowList < 4:
                willFontSize = 60
            elif lenShowList < 6:
                willFontSize = 40
            elif lenShowList < 7:
                willFontSize = 32 
            elif lenShowList < 9:
                willFontSize = 28
            else:
                willFontSize = 20
            print (lenShowList, willFontSize)
            txtResultFont = wx.Font(willFontSize, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="楷体")
            self.panel.txtResult.SetFont(txtResultFont)
            willHeight = txtResultFont.GetPixelSize().Height * len(showList)
            print ("willHeight = " + str(willHeight))
            self.panel.txtResult.SetSize(920, willHeight)
            self.panel.txtResult.SetPosition(wx.Point(120, 455 + (135 - willHeight / 2)))
            self.HCenter(self.panel.txtResult)
            self.panel.txtResult.Show()
        self.ChangeBGToResult()

    def hideResult(self):
        self.panel.gridResult.Hide()
        self.panel.txtTitle.Hide()
        self.panel.txtResult.Hide()
        showNumberFont = wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="楷体")
        self.panel.showNumber.SetFont(showNumberFont)
        self.panel.showNumber.Size = (610, 100)
        self.panel.showNumber.SetPosition(wx.Point(0, 500))
        self.HCenter(self.panel.showNumber)
        self.panel.showNumber.SetLabel(u"祝大家中大奖")
        self.panel.showNumber.Show()
        self.ChangeBGToMain()

    def showRandomNumber(self):
        global candidateList
        currentNumber = getRandom(self.rollCount)
        willDisplay = candidateList[currentNumber - 1]
        self.panel.showNumber.SetLabel(willDisplay)

    def OnTimer(self, e):
        self.showRandomNumber()

def getRandom(maxNumber):
    theRandom = random.randint(1, maxNumber)
    return theRandom

def getThisDegreeResult(degree, limit):
    global candidateList
    global preList
    global showList
    global thisLevelList
    global exceptList
    
    allNumberDisplay = ""
    trueDegree = degree - 1
    showList = []

    thisLevelList = []
    for item in candidateList:
        thisLevelList.append(item)
    for item in exceptList[trueDegree]:
        if (item in thisLevelList):
            thisLevelList.remove(item)

    for i in (range(0, limit)):
        if (len(preList[trueDegree]) > 0):
            theNumberDisplay = preList[trueDegree][0]
            del preList[trueDegree][0]
            if theNumberDisplay in thisLevelList:
                thisLevelList.remove(theNumberDisplay)
        else:
            if len(thisLevelList) == 0:
                break
            theNumber = getRandom(len(thisLevelList))
            theNumberDisplay = thisLevelList[theNumber - 1]
            del thisLevelList[theNumber - 1]
        if theNumberDisplay in candidateList:
            candidateList.remove(theNumberDisplay)
        showList.append(theNumberDisplay)
    SaveResult(degree)

def OpenList():
    global candidateList
    global preList
    global candidateCount
    fp = codecs.open("data/list.txt", "r", "utf-8")
    for oneLine in fp.readlines():
        txt = oneLine[:-1].rstrip()
        if (txt.count(',') == 1):
            degree = int(txt[-1]) - 1
            preNumber = txt[:-2]
            preList[degree].append(preNumber)
        else:
            candidateList.append(txt)
    fp.close()

def ReadExceptList():
    global exceptList

    if (not os.path.isfile("data/except.txt")):
        return

    fp = codecs.open("data/except.txt", "r", "utf-8")
    for oneLine in fp.readlines():
        txt = oneLine[:-1].rstrip()
        if (txt.count(',') == 1):
            degree = int(txt[-1]) - 1
            preNumber = txt[:-2]
            exceptList[degree].append(preNumber)
    fp.close()

def ReadResultList():
    global resultList
    global candidateList

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
        resultList[degree - 1].append(resultNumber)
        if (resultNumber in candidateList):
            candidateList.remove(resultNumber)
    fp.close()

def SaveResult(degree):
    global showList
    global resultList
    fp = codecs.open("data/result.txt", "a", "utf-8")
    for item in showList:
        resultList[degree-1].append(item)
        #print str(degree) + "," + theNumberDisplay
        fp.write(str(degree) + "," + item + "\n")
    fp.close()

candidateList = []              # 待抽奖列表
preList = [[], [], [], [], []]      # 预计中奖列表
resultList = [[], [], [], [], []]   # 已中奖列表
showList = []                   # 抽完后显示用列表
exceptList = [[], [], [], [], []]           # 不参与奖项列表
thisLevelList = [[], []]        # 本次抽取时待抽列表，第一列是名字，第二列是在 candidateList 中的位置
OpenList()
ReadResultList()
ReadExceptList()
#print showList
#print candidateList
#print preList
#print resultList

arrLevel = [[0, u"特等奖"], [1, u"一等奖"], [2, u"二等奖"], [3, u"三等奖"], [4, u"幸运奖"]]

currentMaxCount = 0
currentLevel = 0
bRolling = False

app = wx.App(False)
frame = MainFrame(None)
app.MainLoop()

