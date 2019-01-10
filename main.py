# coding:utf-8
import wx
import random
import threading
import time
import os
import codecs

class MainFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, title=u"抽奖", size=(800, 600))
		self.CreateStatusBar()

		filemenu = wx.Menu()

		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this")
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		filemenu.AppendSeparator()
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		self.SetMenuBar(menuBar)

		panel = MainPanel(self, -1)

		self.Show(True)

	def OnAbout(self, event):
		dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnExit(self, event):
		self.Close(True)


class MainPanel(wx.Panel):
	def __init__(self, parent, id):
		wx.Panel.__init__(self, parent, id)

		image_file = "background.jpg"
		to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))

		awardMemoStr = u"幸运大抽奖"
		self.awardMemo = wx.StaticText(self, label=awardMemoStr, pos=(20, 30))
		self.awardMemo.SetForegroundColour("Red")
		awardMemoFont = wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)
		self.awardMemo.SetFont(awardMemoFont)

		countForThisTimeStr = u"本次抽出"
		self.countForThisTime = wx.StaticText(self, label=countForThisTimeStr, pos=(80, 400))
		self.inputForCount = wx.TextCtrl(self, -1, u"50", size=(40, -1), style=wx.TE_CENTRE, pos=(150, 400))
		self.inputForCount.SetInsertionPoint(0)

		self.stopRollNumber = wx.Button(self, label=u"停", pos=(200, 400))
		self.Bind(wx.EVT_BUTTON, self.OnStopRollNumber, self.stopRollNumber)

		self.GetThirdButton = wx.Button(self, label=u"抽取三等奖", pos=(120, 450))
		self.Bind(wx.EVT_BUTTON, self.OnGetThirdButton, self.GetThirdButton)

		self.GetSecondButton = wx.Button(self, label=u"抽取二等奖", pos=(240, 450))
		self.Bind(wx.EVT_BUTTON, self.OnGetSecondButton, self.GetSecondButton)

		self.GetFirstButton = wx.Button(self, label=u"抽取一等奖", pos=(360, 450))
		self.Bind(wx.EVT_BUTTON, self.OnGetFirstButton, self.GetFirstButton)

		self.GetSpecialButton = wx.Button(self, label=u"抽取特等奖", pos=(480, 450))
		self.Bind(wx.EVT_BUTTON, self.OnGetSpecialButton, self.GetSpecialButton)

		self.showNumber = wx.StaticText(self, label="0000", pos=(80, 220))
		showNumberFont = wx.Font(98, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)
		self.showNumber.SetForegroundColour("Red")
		self.showNumber.SetFont(showNumberFont)

		self.GetThirdButton.Enable(True)
		self.GetSecondButton.Enable(True)
		self.GetFirstButton.Enable(True)
		self.GetSpecialButton.Enable(True)
		self.stopRollNumber.Enable(False)

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

	def OnStopRollNumber(self, e):
		global currentLevel
		global currentMaxCount
		allNumberDisplay = self.getThisDegreeResult(currentLevel, currentMaxCount)
		self.showResult(currentLevel, allNumberDisplay)
		currentLevel = 0
		currentMaxCount = 0
		self.GetThirdButton.Enable(True)
		self.GetSecondButton.Enable(True)
		self.GetFirstButton.Enable(True)
		self.GetSpecialButton.Enable(True)
		self.stopRollNumber.Enable(False)

	def getThisDegreeResult(self, degree, limit):
		global candidateList
		global preList
		global resultList
		self.timer.Stop()

		allNumberDisplay = ""
		trueDegree = degree - 1

		for i in (range(0, limit)):
			if (len(preList[trueDegree]) > 0):
				theNumberDisplay = preList[trueDegree][0]
				del preList[trueDegree][0]
			else:
				theNumber = self.getRandom(len(candidateList))
				theNumberDisplay = candidateList[theNumber - 1]
				del candidateList[theNumber - 1]
			allNumberDisplay = allNumberDisplay + "\n\n" + theNumberDisplay
			SaveResult(degree, theNumberDisplay)
			self.showNumber.SetLabel(theNumberDisplay)
		return allNumberDisplay

	def startRoll(self, degree, limit):
		global currentLevel
		global currentMaxCount
		currentLevel = degree
		currentMaxCount = limit
		self.timer.Start(100)
		self.stopRollNumber.Enable(True)
		self.GetThirdButton.Enable(False)
		self.GetSecondButton.Enable(False)
		self.GetFirstButton.Enable(False)
		self.GetSpecialButton.Enable(False)

	def getInputCount(self):
		return int(self.inputForCount.GetValue())

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

	def getRandom(self, maxNumber):
		theRandom = random.randint(1, maxNumber)
		return theRandom

	def showCurrentRollNumber(self):
		global showList
		currentNumber = self.getRandom(len(candidateList))
		willDisplay = candidateList[currentNumber - 1]
		self.showNumber.SetLabel(willDisplay)

	def OnTimer(self, e):
		self.showCurrentRollNumber()

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

app = wx.App(False)
frame = MainFrame(None)
app.MainLoop()

