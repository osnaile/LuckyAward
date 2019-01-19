import wx

class PanelMain (wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__ ( self, parent)

		self.showNumber = wx.StaticText(self, label="- - - -", size=(610, 118), style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE)
		showNumberFont = wx.Font(80, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="楷体")
		self.showNumber.SetForegroundColour(wx.Colour(255, 0, 0, 255))
		self.showNumber.SetBackgroundColour(wx.Colour(255, 207, 60, 255))
		self.showNumber.SetFont(showNumberFont)
		self.showNumber.SetPosition(wx.Point(120, 484))

