# coding:utf-8
import wx
import threading
import time
import PanelMain
from AwardModal import AwardModal
from config import config
from math import trunc

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=u"抽奖", style=wx.MAXIMIZE | wx.DEFAULT_FRAME_STYLE)

        self.panel = PanelMain.PanelMain(self)
        self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

        countForThisTimeStr = u"本次抽出"
        self.countForThisTime = wx.StaticText(self.panel, label=countForThisTimeStr, pos=(80, 1040))
        self.countForThisTime.SetBackgroundColour(wx.Colour(0, 0, 0, 255))
        self.countForThisTime.SetForegroundColour(wx.Colour(255, 255, 255, 255))
        self.inputForCount = wx.TextCtrl(self.panel, -1, u"50", size=(40, -1), style=wx.TE_CENTRE, pos=(150, 1040))
        self.inputForCount.SetInsertionPoint(0)

        self.CandidateCount = wx.StaticText(self.panel, label=u"/", pos=(200, 1040))
        self.CandidateCount.SetBackgroundColour(wx.Colour(0, 0, 0, 255))
        self.CandidateCount.SetForegroundColour(wx.Colour(255, 255, 255, 255))

        self.stopRollNumber = wx.Button(self.panel, label=u"停", pos=(1200, 1040), size=(150, 30))
        self.Bind(wx.EVT_BUTTON, self.OnStopRollNumber, self.stopRollNumber)

        btnSize = (100, 30)
        btnTitle = u"抽取" + AwardModal.AwardLevel[4][1]
        self.GetForthButton = wx.Button(self.panel, label=btnTitle, pos=(300, 1040), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetForthButton, self.GetForthButton)

        btnTitle = u"抽取" + AwardModal.AwardLevel[3][1]
        self.GetThirdButton = wx.Button(self.panel, label=btnTitle, pos=(420, 1040), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetThirdButton, self.GetThirdButton)

        btnTitle = u"抽取" + AwardModal.AwardLevel[2][1]
        self.GetSecondButton = wx.Button(self.panel, label=btnTitle, pos=(540, 1040), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetSecondButton, self.GetSecondButton)

        btnTitle = u"抽取" + AwardModal.AwardLevel[1][1]
        self.GetFirstButton = wx.Button(self.panel, label=btnTitle, pos=(660, 1040), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetFirstButton, self.GetFirstButton)

        btnTitle = u"抽取" + AwardModal.AwardLevel[0][1]
        self.GetSpecialButton = wx.Button(self.panel, label=btnTitle, pos=(780, 1040), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnGetSpecialButton, self.GetSpecialButton)

        self.btnShowResultPanel = wx.Button(self.panel, label=u"显示上次结果", pos=(900, 1040), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnBtnShowResultPanel, self.btnShowResultPanel)

        self.btnHideResultPanel = wx.Button(self.panel, label=u"关闭结果显示", pos=(1020, 1040), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnBtnHideResultPanel, self.btnHideResultPanel)
        
        self.btnCancelRoll = wx.Button(self.panel, label=u"取消抽奖", pos=(1400, 1040), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnBtnCancelRoll, self.btnCancelRoll)

        self.btnSaveLeftList = wx.Button(self.panel, label=u"导出剩余人员", pos=(1600, 1040), size=btnSize)
        self.Bind(wx.EVT_BUTTON, self.OnBtnSaveLeftList, self.btnSaveLeftList)

        self.GetForthButton.Enable(True)
        self.GetThirdButton.Enable(True)
        self.GetSecondButton.Enable(True)
        self.GetFirstButton.Enable(True)
        self.GetSpecialButton.Enable(True)
        self.stopRollNumber.Enable(False)

        self.Bind(wx.EVT_CHAR_HOOK, self.OnKey)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        self.CandidateCount.SetLabel(u"/" + str(len(AwardModal.candidateList)))

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
        # code 66 是字母 "b"，也是罗技翻页器的黑屏按钮
        # code 366 和 367 分别是罗技翻页器上的左和右
        # code 306 是罗技翻页器上播放按钮
        if (code == 366) or (code == 367) or (code == 66) or (code == 306):
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
        image_file = "resources/background.jpg"
        self.bmpMain = wx.Bitmap(image_file)

    def LoadBGResult(self):
        image_file = "resources/bg_result.jpg"
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
        x = trunc(frame_width / 2 - x / 2)
        y = trunc(frame_height / 2 - y / 2)
        dc.DrawBitmap(self.bmp, x, y)
        

    def OnBtnSaveLeftList(self, event):
        AwardModal.SaveLeftList()

    def OnBtnCancelRoll(self, event):
        global bRolling

        if not bRolling:
            # print(u"Not Rolling")
            return

        self.timer.Stop()
        self.panel.showNumber.SetLabel(u"好 运 连 连")
        bRolling = False
        
        global currentLevel
        global currentMaxCount

        currentMaxCount = 0
        
        self.GetForthButton.Enable(True)
        self.GetThirdButton.Enable(True)
        self.GetSecondButton.Enable(True)
        self.GetFirstButton.Enable(True)
        self.GetSpecialButton.Enable(True)
        self.stopRollNumber.Enable(False)
        
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
        currentMaxCount = self.getInputCount()
        AwardModal.getThisDegreeResult(currentLevel, currentMaxCount)
        self.showResult(currentLevel)
        currentMaxCount = 0

        self.CandidateCount.SetLabel(u"/" + str(len(AwardModal.candidateList)))
        
        self.GetForthButton.Enable(True)
        self.GetThirdButton.Enable(True)
        self.GetSecondButton.Enable(True)
        self.GetFirstButton.Enable(True)
        self.GetSpecialButton.Enable(True)
        self.stopRollNumber.Enable(False)
        
    def startRoll(self, degree, limit):
        global currentLevel
        global currentMaxCount

        rollCount = len(AwardModal.candidateList)
        if rollCount == 0:
            dlg = wx.MessageDialog(self, u"所有人都已抽中", u"提示", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return

        currentLevel = degree
        currentMaxCount = limit

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
        x = trunc(frame_width / 2 - obj_width / 2)
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
        self.startRoll(5, self.getInputCount())

    def OnGetThirdButton(self, e):
        self.startRoll(4, self.getInputCount())

    def OnGetSecondButton(self, e):
        self.startRoll(3, self.getInputCount())

    def OnGetFirstButton(self, e):
        self.startRoll(2, self.getInputCount()) 

    def OnGetSpecialButton(self, e):
        self.startRoll(1, self.getInputCount())

    def showResult(self, level):
        self.panel.txtBG.Show()
        self.HCenter(self.panel.txtBG)

        lenShowList = len(AwardModal.showList)
        title = AwardModal.AwardLevel[level-1][1]
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
            for item in AwardModal.showList:
                self.panel.gridResult.SetCellValue(row, col, item)
                col = col + 1
                if col == 5:
                    col = 0
                    row = row + 1
        else:
            txtToShow = u""
            for item in AwardModal.showList:
                txtToShow = txtToShow + item + "\n"
            self.panel.txtResult.SetLabel(txtToShow)
            willFontSize = 20
            if lenShowList < 4:
                willFontSize = 100
            elif lenShowList < 6:
                willFontSize = 68
            elif lenShowList < 7:
                willFontSize = 58
            elif lenShowList < 8:
                willFontSize = 50
            elif lenShowList < 9:
                willFontSize = 40
            elif lenShowList < 10:
                willFontSize = 38
            else:
                willFontSize = 34
            print (lenShowList, willFontSize)
            txtResultFont = wx.Font(willFontSize, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName=config.ListFont)
            self.panel.txtResult.SetFont(txtResultFont)
            willHeight = (txtResultFont.GetPixelSize().Height + 2) * len(AwardModal.showList)
            print ("willHeight = " + str(willHeight))
            self.panel.txtResult.SetSize(920, willHeight)
            self.panel.txtResult.SetPosition(wx.Point(120, 455 + (135 - trunc(willHeight / 2))))
            self.HCenter(self.panel.txtResult)
            self.panel.txtResult.Show()
        self.ChangeBGToResult()

    def hideResult(self):
        self.panel.gridResult.Hide()
        self.panel.txtTitle.Hide()
        self.panel.txtResult.Hide()
        self.panel.txtBG.Hide()

        showNumberFont = wx.Font(120, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName=config.TitleFont)
        self.panel.showNumber.SetFont(showNumberFont)
        self.panel.showNumber.Size = (1200, 180)
        self.panel.showNumber.SetPosition(wx.Point(0, 450))
        self.HCenter(self.panel.showNumber)
        self.panel.showNumber.SetLabel(u"好 运 连 连")
        self.panel.showNumber.Show()
        self.ChangeBGToMain()

    def showRandomNumber(self):
        willDisplay = AwardModal.getRandomCandicate()
        self.panel.showNumber.SetLabel(willDisplay)

    def OnTimer(self, e):
        self.showRandomNumber()

if __name__ == '__main__':
    # 初始化
    AwardModal.get_data_from_file() # 读人员清单
    AwardModal.ReadResultList() # 读已保存的抽奖结果
    AwardModal.ReadExceptList() # 读例外清单
    AwardModal.ReadAwardLevel() # 读奖项设置

    config.ReadConfig() # 读取配置文件

    currentMaxCount = 0
    currentLevel = 0
    bRolling = False

    app = wx.App(False)
    frame = MainFrame(None)
    app.MainLoop()
