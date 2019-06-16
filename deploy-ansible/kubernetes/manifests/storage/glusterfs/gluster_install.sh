#!/bin/bash
# 安装glusterfs
yum install centos-release-gluster -y
yum install -y glusterfs glusterfs-server glusterfs-fuse glusterfs-rdma glusterfs-geo-replication glusterfs-devel
mkdir /opt/glusterd
sed -i 's/var\/lib/opt/g' /etc/glusterfs/glusterd.vol
systemctl enable glusterd.service
systemctl start glusterd

# 创建分区卷
mdkir - p /opt/ops_data/01 # 三台节点都创建对应的分区
gluster volume create pv1 replica 3 transport tcp node1:/opt/ops_data/01 node2:/opt/ops_data/01 node3:/opt/ops_data/01 force
gluster volume start pv1


