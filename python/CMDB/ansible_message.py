#！/usr/bin/env python
# _*_ coding: utf-8 _*_
# 开发团队：云飞国际
# 开发人员： 93792
# 开发时间： 2019/6/2 16:18
# 文件名称： ansible_message.py
# 开发工具： PyCharm

from subprocess import Popen, PIPE
import re

command = 'ansible 192.168.174.10 -m setup'

show_list = [('fqdn', u'主机名'),
             ('domain', u'域名'),
             ('uptime', u'运行时间'),
             ('kernelrelease', u'内核版本'),
             ('ip', u'IP'),
             ('mac', u'MAC'),
             ]

def get_hosts_message(command):
    content = Popen(command, stdout=PIPE, stderr=PIPE)
    content.wait()
    if content.returncode == 0:
        return content.stdout.read().decode('utf-8')
    else:
        return

def data(result):
    if result:
        for line in result.strip().split('\n'):
            print(line)
            if re.findall('=>', line):
                key, value = line.split('=>', 1)
                result_dict[key.strip()] = value.strip()
        for f_k, f_s in show_list:
            if f_k in result_dict:
                print(f_s, ":", result_dict[f_k])


if __name__ == '__main__':
    result_dict = {}
    result = get_hosts_message(command)
    data(result)
