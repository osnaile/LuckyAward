# coding:utf-8
import wx
import random
import threading
import time
import os
import codecs
import TransparentText
import PanelMain

class MainFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, title=u"抽奖", style=wx.MAXIMIZE | wx.DEFAULT_FRAME_STYLE)

		self.panel = PanelMain.PanelMain(self)
		self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

		#awardMemoStr = u"幸运大抽奖"
		#awardMemo = TransparentText.TransparentText(self.panel, label=awardMemoStr, style=wx.ALIGN_CENTRE_HORIZONTAL)
		#awardMemo.SetForegroundColour(wx.Colour(255, 255, 0, 255))
		#awardMemoFont = wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="黑体")
		#awardMemo.SetFont(awardMemoFont)

		countForThisTimeStr = u"本次抽出"
		self.countForThisTime = TransparentText.TransparentText(self.panel, label=countForThisTimeStr, pos=(80, 900))
		self.countForThisTime.SetForegroundColour(wx.Colour(255, 255, 255, 255))
		self.inputForCount = wx.TextCtrl(self.panel, -1, u"50", size=(40, -1), style=wx.TE_CENTRE, pos=(150, 900))
		self.inputForCount.SetInsertionPoint(0)

		self.stopRollNumber = wx.Button(self.panel, label=u"停", pos=(1200, 900))
		self.Bind(wx.EVT_BUTTON, self.OnStopRollNumber, self.stopRollNumber)

		btnSize = (100, 30)
		self.GetForthButton = wx.Button(self.panel, label=u"抽取四等奖", pos=(300, 910), size=btnSize)
		self.Bind(wx.EVT_BUTTON, self.OnGetForthButton, self.GetForthButton)

		self.GetThirdButton = wx.Button(self.panel, label=u"抽取三等奖", pos=(420, 910), size=btnSize)
		self.Bind(wx.EVT_BUTTON, self.OnGetThirdButton, self.GetThirdButton)

		self.GetSecondButton = wx.Button(self.panel, label=u"抽取二等奖", pos=(540, 910), size=btnSize)
		self.Bind(wx.EVT_BUTTON, self.OnGetSecondButton, self.GetSecondButton)

		self.GetFirstButton = wx.Button(self.panel, label=u"抽取一等奖", pos=(660, 910), size=btnSize)
		self.Bind(wx.EVT_BUTTON, self.OnGetFirstButton, self.GetFirstButton)

		self.GetSpecialButton = wx.Button(self.panel, label=u"抽取特等奖", pos=(780, 910), size=btnSize)
		self.Bind(wx.EVT_BUTTON, self.OnGetSpecialButton, self.GetSpecialButton)

		self.btnShowResultPanel = wx.Button(self.panel, label=u"显示上次结果", pos=(900, 910), size=btnSize)
		self.Bind(wx.EVT_BUTTON, self.OnBtnShowResultPanel, self.btnShowResultPanel)

		self.btnHideResultPanel = wx.Button(self.panel, label=u"关闭结果显示", pos=(1020, 910), size=btnSize)
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
		self.showResult(currentLevel, allNumberDisplay)
		currentLevel = 0
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
		
		currentLevel = degree
		currentMaxCount = limit
		
		self.rollCount = len(candidateList)
		
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
		self.panel.showNumber.SetLabel("")
		showNumberFont = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="楷体")
		self.panel.showNumber.SetFont(showNumberFont)
		self.panel.showNumber.Size = (920, 338)
		self.panel.showNumber.SetPosition(wx.Point(0, 415))
		self.HCenter(self.panel.showNumber)
		self.panel.showNumber.SetLabel(u"我我我1234\t你你你\t他他他\t22222\t33333\n我我我\t你你你\t他34f他他\t22222\t33333\n我我我\t你你你\t他他他\t22222\t33333\n谁我我我\t你你你\t他他他\t22222\t33333\n谁我我我\t你你你-34131\t他他他\t22222\t33333\n谁我我我\t你你你\t他他他\t22222\t33333\n谁我我我\t你你你\t他他他\t22222\t33333\n谁我我我\t你你你\t他他他\t22222\t33333\n谁我我我\t你你你\t他他他\t22222\t33333\n谁我我我\t你你你\t他他他\t22222\t33333")
		self.ChangeBGToResult()

	def OnBtnHideResultPanel(self, event):
		self.panel.showNumber.SetLabel("")
		showNumberFont = wx.Font(80, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="楷体")
		self.panel.showNumber.SetFont(showNumberFont)
		self.panel.showNumber.Size = (610, 118)
		self.panel.showNumber.SetPosition(wx.Point(0, 484))
		self.HCenter(self.panel.showNumber)
		self.panel.showNumber.SetLabel(u"- - - -")
		self.ChangeBGToMain()

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

	def showResult(self, level, msg):
		global arrLevel;
		title = arrLevel[level][1]
		dlg = wx.MessageDialog(self, msg, title, wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def showRandomNumber(self):
		global candidateList
		currentNumber = getRandom(self.rollCount)
		willDisplay = candidateList[currentNumber - 1]
		self.panel.showNumber.SetLabel(willDisplay)

	def OnTimer(self, e):
		self.showRandomNumber()

	def OnAbout(self, event):
		dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnExit(self, event):
		self.Close(True)
		
def getRandom(maxNumber):
	theRandom = random.randint(1, maxNumber)
	return theRandom

def getThisDegreeResult(degree, limit):
	global candidateList
	global preList
	global resultList
	
	allNumberDisplay = ""
	trueDegree = degree - 1

	for i in (range(0, limit)):
		if (len(preList[trueDegree]) > 0):
			theNumberDisplay = preList[trueDegree][0]
			del preList[trueDegree][0]
		else:
			theNumber = getRandom(len(candidateList))
			theNumberDisplay = candidateList[theNumber - 1]
			del candidateList[theNumber - 1]
		allNumberDisplay = allNumberDisplay + "\n\n" + theNumberDisplay
		SaveResult(degree, theNumberDisplay)
	return allNumberDisplay

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
			showList.append(preNumber)
		else:
			candidateList.append(txt)
			showList.append(txt)
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

def SaveResult(degree, theNumberDisplay):
	global resultList
	resultList[degree - 1].append(theNumberDisplay)
	fp = codecs.open("data/result.txt", "a", "utf-8")
	#print str(degree) + "," + theNumberDisplay
	fp.write(str(degree) + "," + theNumberDisplay)
	fp.write("\n")
	fp.close()

candidateList = []
preList = [[], [], [], []]
resultList = [[], [], [], []]
showList = []
OpenList()
ReadResultList()
#print showList
#print candidateList
#print preList
#print resultList

arrLevel = [[0, u"特等奖"], [1, u"一等奖"], [2, u"二等奖"], [3, u"三等奖"], [4, u"四等奖"]]

currentMaxCount = 0
currentLevel = 0
bRolling = False

app = wx.App(False)
frame = MainFrame(None)
app.MainLoop()

