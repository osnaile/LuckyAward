import wx
from wx import FontEnumerator

app = wx.App(False)
theFontEnumerator = wx.FontEnumerator()
fontList = theFontEnumerator.GetFacenames()
for font in fontList:
    print(font)