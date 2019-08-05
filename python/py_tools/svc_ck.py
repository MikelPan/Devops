#!/usr/bin/env python

import os
import sys


'''定位问题工具
'''

http_code = {
    '服务器内部错误': 500,
    '权限不足': 403,
    '请求方式错误': 405,
    '资源未找到': 404,
    '网关超时': 504,
    '服务不可用': 503,
    '请求不可达': 502
}

request_time = {
    '总时间': 'time_total',
    'DNS解析时间': 'time_namelookup',
    '重定向时间': 'time_redirect',
    '开始传输时间': 'time_starttransfer'
}

class CkTools(object):
    def __init__(self, svc_name):
        self.http_code = http_code
        self.request_time = request_time
        self.svc_name = svc_name

    def get_svc(self):
        svc = os.popen("kubectl get pods | awk '{print $1}' | cut -f1,2,3 -d '-' | grep \"%s\" " %self.svc_name).read()
        return svc

    def get_ip(self, svcname):
        svc = CkTools.get_svc()
        ip = os.popen("kubectl get pods -o wide | grep \"%s\" |awk '{print $6}'| sed -n '1p'" %svc).read()
        return ip

    def get_port(self, svcname):
        svc = CkTools.get_svc()
        port = os.popen("kubectl get services | grep \"%s\" | awk '{print $5}'| cut -f1 -d '/' " %svc).read()
        return port

    def check_registered(self, svcname):
        pass

    def main(self):
        pass

if __name__ == "__main__":
    pass













