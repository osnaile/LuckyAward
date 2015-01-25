# coding=utf-8
import wx
import random
import threading
import time

class MainFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, title="抽奖", size=(800, 600))
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

		awardMemoStr = "奖项说明：\n\n三等奖3名：华为手机荣耀6Plus\n二等奖2名：华为手机MATE7\n一等奖1名：苹果iPad Air 2\n特等奖1名：神秘大礼"
		self.awardMemo = wx.StaticText(self, label=awardMemoStr, pos=(20, 30))
		self.awardMemo.SetForegroundColour("Yellow")

		self.startRollNumber = wx.Button(self, label="开始", pos=(120, 300))
		self.Bind(wx.EVT_BUTTON, self.OnStartRollNumber, self.startRollNumber)

		self.GetThirdButton = wx.Button(self, label="抽取三等奖", pos=(120, 500))
		self.Bind(wx.EVT_BUTTON, self.OnGetThirdButton, self.GetThirdButton)

		self.GetSecondButton = wx.Button(self, label="抽取二等奖", pos=(240, 500))
		self.Bind(wx.EVT_BUTTON, self.OnGetSecondButton, self.GetSecondButton)

		self.GetFirstButton = wx.Button(self, label="抽取一等奖", pos=(360, 500))
		self.Bind(wx.EVT_BUTTON, self.OnGetFirstButton, self.GetFirstButton)

		self.GetSpecialButton = wx.Button(self, label="抽取特等奖", pos=(480, 500))
		self.Bind(wx.EVT_BUTTON, self.OnGetSpecialButton, self.GetSpecialButton)

		self.showNumber = wx.StaticText(self, label="0000", pos=(240, 220))
		showNumberFont = wx.Font(128, wx.FONTFAMILY_DEFAULT, wx.ITALIC, wx.FONTWEIGHT_BOLD)
		self.showNumber.SetForegroundColour("Yellow")
	        self.showNumber.SetFont(showNumberFont)


		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

	def OnStartRollNumber(self, e):
		self.timer.Start(100)

	def OnGetThirdButton(self, e):
		self.timer.Stop()
		theNumber = self.getRandom()
		theNumberDisplay = str(theNumber).zfill(4)
		self.showNumber.SetLabel(theNumberDisplay)
		self.showResult("三等奖", theNumberDisplay)

	def OnGetSecondButton(self, e):
		dlg = wx.MessageDialog(self, "bb", "bbaaa", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnGetFirstButton(self, e):
		dlg = wx.MessageDialog(self, "cc", "cc", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnGetSpecialButton(self, e):
		dlg = wx.MessageDialog(self, "dd", "dd", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def showResult(self, title, msg):
		dlg = wx.MessageDialog(self, msg, title, wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def getRandom(self):
		theRandom = random.randint(1, 1000)
		return theRandom

	def showCurrentRollNumber(self):
		currentNumber = self.getRandom()
		willDisplay = str(currentNumber).zfill(4)
		self.showNumber.SetLabel(willDisplay)

	def OnTimer(self, e):
		self.showCurrentRollNumber();

#	def startRollNumber(self):
		#self.timer.Start(100)

app = wx.App(False)
frame = MainFrame(None)
app.MainLoop()

