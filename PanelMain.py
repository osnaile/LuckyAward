import wx
import wx.grid

class PanelMain (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ ( self, parent)

        self.showNumber = wx.StaticText(self, label=u"祝大家中大奖", size=(610, 100), style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        showNumberFont = wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="楷体")
        self.showNumber.SetForegroundColour(wx.Colour(255, 0, 0, 255))
        self.showNumber.SetBackgroundColour(wx.Colour(255, 207, 60, 255))
        self.showNumber.SetFont(showNumberFont)
        self.showNumber.SetPosition(wx.Point(120, 500))

        self.txtTitle = wx.StaticText(self, label=u"", size=(610, 25), style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        self.txtTitle.Hide()
        txtTitleFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="黑体")
        self.txtTitle.SetForegroundColour(wx.Colour(255, 0, 0, 255))
        self.txtTitle.SetBackgroundColour(wx.Colour(255, 207, 60, 255))
        self.txtTitle.SetFont(txtTitleFont)
        self.txtTitle.SetPosition(wx.Point(120, 415))

        self.txtResult = wx.StaticText(self, label=u"", size=(920, 310), style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        self.txtResult.Hide()
        txtResultFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="楷体")
        self.txtResult.SetForegroundColour(wx.Colour(255, 0, 0, 255))
        self.txtResult.SetBackgroundColour(wx.Colour(255, 207, 60, 255))
        self.txtResult.SetFont(txtResultFont)
        self.txtResult.SetPosition(wx.Point(120, 455))

        self.gridResult = wx.grid.Grid(self, -1)
        self.gridResult.Hide()
        self.gridResult.CreateGrid(10, 5)
        self.gridResult.SetCellTextColour(wx.Colour(255, 0, 0, 255))
        self.gridResult.Size = (920, 310)
        self.gridResult.SetPosition(wx.Point(0, 445))
        self.gridResult.HideRowLabels()
        self.gridResult.HideColLabels()
        self.gridResult.EnableGridLines(False)
        self.gridResult.SetDefaultCellBackgroundColour(wx.Colour(255, 207, 60, 255))
        cellFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, faceName="楷体")
        self.gridResult.SetDefaultCellFont(cellFont)
        self.gridResult.SetDefaultRowSize(31)
        self.gridResult.SetDefaultColSize(180)
        self.gridResult.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

