import wx
from wx.lib import flatnotebook as fnb

from menu import *


class ProtoFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title='ProtoFrame')
        self.mb = MenuBar(self)
        self.mb.register_menu_entry(MenuEntry('File', 'Event', self.OnEvent,
                                              shortcut='Alt-e'))
        self.mb.register_to_frame(self)
        self.CreateStatusBar()
        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(50)
        self.nb = fnb.FlatNotebook(splitter)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.nb.AddPage(ProtoPanel(self, self.nb), 'F1')
        self.nb.AddPage(ProtoPanel(self, self.nb), 'F2')
        self.nb.AddPage(ProtoPanel(self, self.nb, entry='Bar'), 'F3')
        self.nb.AddPage(ProtoPanel(self, self.nb, menu='X', entry='Bar'), 'F4')
        self.nb.AddPage(ProtoPanel(self, self.nb, entry='D', scut='Del'), 'D1')
        self.nb.AddPage(ProtoPanel(self, self.nb, entry='D', scut='Del',
                                   container=False), 'D2')
        splitter.SplitVertically(Tree(splitter), self.nb, 100)

    def OnPageChanging(self, event):
        newindex = event.GetSelection()
        if newindex <= self.nb.GetPageCount() - 1:
            self.nb.GetPage(newindex).SetFocus()

    def register_menu_entry(self, menu, name, action, container=None,
                            shortcut=None, doc=''):
        self.mb.register_menu_entry(MenuEntry(menu, name, action, container,
                                              shortcut, doc))

    def OnEvent(self):
        wx.MessageBox('Main frame')


class Tree(wx.TreeCtrl):

    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent)
        root = self.AddRoot('root')
        self.AppendItem(root, 'Foo')


class ProtoPanel(wx.Panel):
    counter = 0

    def __init__(self, frame, parent, menu='Edit', entry='Foo', scut='Ctrl-F',
                 container=True):
        ProtoPanel.counter += 1
        name = 'Panel %d' % ProtoPanel.counter
        wx.Panel.__init__(self, parent, name=name)
        container = container and self or None
        frame.register_menu_entry(menu, entry,
                                  lambda: wx.MessageBox(name), 
                                  container, scut, 'Doc for '+name)
        frame.register_menu_entry(menu, entry+' (2)', 
                                  lambda: wx.MessageBox(name+' (2)'), 
                                  container, None, 'Doc 2 for '+name)
        wx.TextCtrl(self, value=name)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    ProtoFrame().Show()
    app.MainLoop()
