#!/usr/bin/env python

import docker
import sys


def auth_push_image():
    # 判断镜像是否存在
    image = client.images.get(src_image_repository + '/' + image_name + ':' + tag_version)
    if image:
        print(image_name + "is exits!")
    else:
        client.images.pull(image_repository + '/' + image_name + ':' + tag_version)

    # tag镜像
    client.api.tag(src_image_repository + '/' + image_name + ':' + tag_version, dest_image_repository + '/' + image_name,  tag_version, force=True)
    # 推送镜像
    client.images.push(dest_image_repository + '/' + image_name, tag=tag_version, stream=True, decode=True)

def main(*args, **kargs):
    auth_push_image()

if __name__ == "__main__":
    # 定义全局变量
    global src_image_repository
    global dest_image_repository
    global image_name
    global tag_version
    global client
    src_image_repository = sys.argv[1]
    dest_image_repository = sys.argv[2]
    image_name = sys.argv[3]
    tag_version = sys.argv[4]
    client = docker.from_env()
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])



