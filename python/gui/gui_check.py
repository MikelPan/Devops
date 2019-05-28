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




cat >> roles/down/tasks/down_url.log <<EOF
https://storage.googleapis.com/kubernetes-release/release/v1.12.5/kubernetes-server-linux-amd64.tar.gz
https://github.com/coreos/etcd/releases/download/v3.3.13/etcd-v3.3.13-linux-amd64.tar.gz
https://download.docker.com/linux/static/stable/x86_64/docker-18.09.6.tgz
httpsttps://storage.googleapis.com/harbor-releases/release-1.8.0/harbor-offline-installer-v1.8.0-rc2.tgz
https://github.com/docker/compose/releases/download/1.24.0/docker-compose-Linux-x86_64
https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz
https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
> EOF

