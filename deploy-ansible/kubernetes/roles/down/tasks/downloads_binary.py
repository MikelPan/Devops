#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 开发团队：云飞国际
# 开发人员： 93792
# 开发时间： 2019/5/26 14:10
# 文件名称： downloads_binary.py
# 开发工具： PyCharm

import os
import time
import yaml
import sys
import urllib.request

# 获取需要下载的url地址
def get_url(f):
    url = yaml.load(f)['kubernetes'][:]
    url_list = []
    for data in url:
        url_list.append(data['url'])
    return url_list

# 获取需要下载的软件包名
def get_tagname(f):
    tag = yaml.load(f)['kubernetes'][:]
    tagname_list = []
    for data in tag:
        url_list.append(data['tag_name'])
    return tagname_list

# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)
'''
urllib.request.urlretrieve 的回调函数：
def callbackfunc(blocknum, blocksize, totalsize):
    @blocknum:  已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
'''
def Schedule(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    f.write('\r')

def down_file(url,desc_dir):
    local = os.path.join(desc_dir,file_name)
    urllib.request.urlretrieve(url,local,Schedule)

def main():
    down_file(url,desc_dir)

if __name__ == "__main__":
    # 定义下载文件路径
    url = '/root/Devops/deploy-ansible/kubernetes/roles/down/tasks/down_binary.yml'
    desc_dir = '/root/Devops/deploy-ansible/kubernetes/down'
    f = open(url)
    start_time = time.time()
    file_name = get_tagname(f)
    url = get_url(f)
    desc_dir = desc_dir
    main()

