# coding:utf-8
import wx
import random
import threading
import time
import os

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

		#image_file = "background.jpg"
		#to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		#self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))

		awardMemoStr = u"奖项说明：\n\n三等奖3名：华为手机荣耀6Plus\n二等奖2名：华为手机MATE7\n一等奖1名：苹果iPad Air 2\n特等奖1名：神秘大礼"
		self.awardMemo = wx.StaticText(self, label=awardMemoStr, pos=(20, 30))
		self.awardMemo.SetForegroundColour("Red")

		self.startRollNumber = wx.Button(self, label=u"开始", pos=(0, 0))
		self.Bind(wx.EVT_BUTTON, self.OnStartRollNumber, self.startRollNumber)

		self.GetThirdButton = wx.Button(self, label=u"抽取三等奖", pos=(120, 500))
		self.Bind(wx.EVT_BUTTON, self.OnGetThirdButton, self.GetThirdButton)

		self.GetSecondButton = wx.Button(self, label=u"抽取二等奖", pos=(240, 500))
		self.Bind(wx.EVT_BUTTON, self.OnGetSecondButton, self.GetSecondButton)

		self.GetFirstButton = wx.Button(self, label=u"抽取一等奖", pos=(360, 500))
		self.Bind(wx.EVT_BUTTON, self.OnGetFirstButton, self.GetFirstButton)

		self.GetSpecialButton = wx.Button(self, label=u"抽取特等奖", pos=(480, 500))
		self.Bind(wx.EVT_BUTTON, self.OnGetSpecialButton, self.GetSpecialButton)

		self.showNumber = wx.StaticText(self, label="0000", pos=(240, 220))
		showNumberFont = wx.Font(128, wx.FONTFAMILY_DEFAULT, wx.ITALIC, wx.FONTWEIGHT_BOLD)
		self.showNumber.SetForegroundColour("Red")
	        self.showNumber.SetFont(showNumberFont)

		#self.GetThirdButton.Enable(False)
		#self.GetSecondButton.Enable(False)
		#self.GetFirstButton.Enable(False)

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

	def OnStartRollNumber(self, e):
		self.timer.Start(100)
		self.GetThirdButton.Enable(True)
		self.GetSecondButton.Enable(True)
		self.GetFirstButton.Enable(True)

	def getThisDegreeResult(self, degree, limit):
		global candidateList
		global preList
		global resultList
		self.timer.Stop()
		self.GetThirdButton.Enable(False)
		self.GetSecondButton.Enable(False)
		self.GetFirstButton.Enable(False)

		allNumberDisplay = ""
		trueDegree = degree - 1

		if (len(resultList[trueDegree]) > 0):
			for i in (range(0, len(resultList[trueDegree]))):
				theNumberDisplay = resultList[trueDegree][i]
				allNumberDisplay = allNumberDisplay + "\n" + theNumberDisplay
			return allNumberDisplay

		for i in (range(0, limit)):
			if (len(preList[trueDegree]) > 0):
				theNumberDisplay = preList[trueDegree][0]
				del preList[trueDegree][0]
			else:
				theNumber = self.getRandom(len(candidateList))
				theNumberDisplay = candidateList[theNumber - 1]
				del candidateList[theNumber - 1]
			allNumberDisplay = allNumberDisplay + "\n" + theNumberDisplay
			SaveResult(degree, theNumberDisplay)
			self.showNumber.SetLabel(theNumberDisplay)
		return allNumberDisplay

	def OnGetThirdButton(self, e):
		allNumberDisplay = self.getThisDegreeResult(3, 3)
		self.showResult(u"三等奖", allNumberDisplay)

	def OnGetSecondButton(self, e):
		allNumberDisplay = self.getThisDegreeResult(2, 2)
		self.showResult(u"二等奖", allNumberDisplay)

	def OnGetFirstButton(self, e):
		allNumberDisplay = self.getThisDegreeResult(1, 1)
		self.showResult(u"一等奖", allNumberDisplay)

	def OnGetSpecialButton(self, e):
		dlg = wx.MessageDialog(self, "dd", "dd", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def showResult(self, title, msg):
		dlg = wx.MessageDialog(self, msg, title, wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def getRandom(self, maxNumber):
		theRandom = random.randint(1, maxNumber)
		return theRandom

	def showCurrentRollNumber(self):
		global showList
		currentNumber = self.getRandom(len(showList))
		willDisplay = showList[currentNumber - 1]
		self.showNumber.SetLabel(willDisplay)

	def OnTimer(self, e):
		self.showCurrentRollNumber()

def OpenList():
	global candidateList
	global preList
	global candidateCount
	fp = open("list.txt", "r")
	for oneLine in fp.readlines():
		txt = oneLine[:-1]
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

	if (not os.path.isfile("result")):
		return

	fp = open("result.txt", "r+")
	for oneLine in fp.readlines():
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
	fp = open("result.txt", "a")
	fp.writelines(str(degree) + "," + theNumberDisplay + "\n")
	fp.close()

candidateList = []
preList = [[], [], []]
resultList = [[], [], []]
showList = []
OpenList()
ReadResultList()
print showList
print candidateList
print preList
print resultList
app = wx.App(False)
frame = MainFrame(None)
app.MainLoop()

