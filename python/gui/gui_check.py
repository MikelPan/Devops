#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 开发团队：云飞国际
# 开发人员： 93792
# 开发时间： 2019/5/26 21:26
# 文件名称： gui_check.py
# 开发工具： PyCharm

import wx
class App(wx.App):
    # 初始化方法
    def OnInit(self):
        frame = wx.Frame(parent=None, title='Hello wxPython', size=(400, 300))
        panel = wx.Panel(frame)
        label = wx.StaticText(panel, label="Hello World", pos=(200, 10))
        frame.Show()
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()



