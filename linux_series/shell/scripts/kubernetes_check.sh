#!/bin/bash
pod_server_downing=$(echo |kubectl get pod | sed -n '2,$p'|grep -v Running|awk '{print $1}')
pod_server_restarts=`kubectl get pod | sed -n '2,$p' | awk '{if ($4>10)print $1 }'`
kube_apiserver_status=`ps aux | grep kube-apiserver | grep -v grep | wc -l`
etcd_status=`ps aux | grep etcd | grep -v grep | wc -l`
kube_scheduler_status=`ps aux | grep kube-scheduler | grep -v grep | wc -l`
kube_controlle_status=`ps aux | grep kube-controlle | grep -v grep | wc -l`
kubelet=`ps aux | grep kubelet | grep -v grep | wc -l`
if [ "$pod_server_downing" != ""  ];then
	printf "%s is downing.......\n" $pod_server_downing
elif [ "$pod_server_restarts" != "" ];then
	printf  "%s is Abnormaliang.......\n" $pod_server_restarts
elif [ $kube_apiserver_status -eq 0 ];then
        echo "kube-apiserver is downding"
	systemctl start kube-apiserver
elif [ $etcd_status -eq 0 ];then
	echo "etcd is downing"
	systemctl start etcd
elif [ $kube_controlle_status -eq 0 ];then 
	echo "kube-scheduler is downing"
	systemctl start kube-controlle
elif [ $kube_scheduler_status -eq 0 ];then
	echo "kube-scheduler is downding"
	systemctl start kube-scheduler
elif [ $kubelet -eq 0 ];then
	echo "kubelet is downding"
	systemctl start kubelet
else
       # echo "Public network test environment service is running......"
       exit 0
fi