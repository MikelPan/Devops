#!/bin/bash
VIRTUAL_IP=172.18.28.100
INTERFACE=eth0
NETMASK_BIT=24
CHECK_PORT=8443
RID=10
VRID=160
MCAST_GROUP=224.0.0.18
docker container stop Keepalived-K8S
docker container rm Keepalived-K8S
docker run -d --restart=always --name=Keepalived-K8S \
        --net=host --cap-add=NET_ADMIN \
        -e VIRTUAL_IP=$VIRTUAL_IP \
        -e INTERFACE=$INTERFACE \
        -e CHECK_PORT=$CHECK_PORT \
        -e RID=$RID \
        -e VRID=$VRID \
        -e NETMASK_BIT=$NETMASK_BIT \
        -e MCAST_GROUP=$MCAST_GROUP \
        wise2c/keepalived-k8s