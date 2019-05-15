#!/bin/bash
# 传输参数
parms=$1
docker_install(){
yum install -y wget
wget https://download.docker.com/linux/static/stable/x86_64/docker-18.09.6.tgz -P /root/sofeware
tar zxvf /root/sofeware/docker-18.09.6.tgz -C /usr/local/src
mv /usr/local/src/docker/* /usr/bin
}
Auto_start(){
cat > /usr/lib/systemd/system/docker.service <<EOF
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
ExecStart=/usr/bin/dockerd $DOCKER_NETWORK_OPTIONS
ExecReload=/bin/kill -s HUP $MAINPID
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
# Uncomment TasksMax if your systemd version supports it.
# Only systemd 226 and above support this version.
#TasksMax=infinity
TimeoutStartSec=0
# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes
# kill only the docker process, not all processes in the cgroup
KillMode=process
# restart the docker process if it exits prematurely
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target
EOF
systemctl enable docker
systemctl start docker
}
config_docker(){
cat > /etc/docker/daemon.json <<EOF
{"data-root": "/data/docker","registry-mirrors": ["http://9b2cd203.m.daocloud.io"]}
EOF
systemctl restart docker
iptables -P FORWARD ACCEPT
}
main(){
case ${parms} in
   docker_install)
   docker_install
   ;;
   Auto_start)
   Auto_start
   ;;
   config_docker)
   config_docker
   ;;
   *)
   echo "Usge: please input dokcer-install (docker_install|Auto_start|config_start)"
   ;;
esac
}
main