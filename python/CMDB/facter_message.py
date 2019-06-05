#/usr/bin/env python
# _*_ coding: utf-8 _*_
# 开发团队：云飞国际
# 开发人员： 93792
# 开发时间： 2019/6/2 6:30
# 文件名称： facter_message.py
# 开发工具： PyCharm

import subprocess
from subprocess import Popen,PIPE
import re

command = 'facter'

show_list = [('fqdn', u'主机名'),
             ('domain', u'域名'),
             ('uptime', u'运行时间'),
             ('kernelrelease', u'内核版本'),
             ('ip', u'IP'),
             ('mac', u'MAC'),
             ]

def handle_command_message(command):
    content = Popen(command, stdout=PIPE, stderr=PIPE)
    content.wait()
    if content.returncode == 0:
        return content.stdout.read().decode('utf-8')
    else:
        return

if __name__ == '__main__':
    result_dict = {}
    result = handle_command_message(command)
    if result:
        for line in result.strip().split('\n'):
            print(line)
            if re.findall('=>', line):
                key, value = line.split('=>', 1)
                result_dict[key.strip()] = value.strip()
        for f_k, f_s in show_list:
            if f_k in result_dict:
                print(f_s, ":", result_dict[f_k])