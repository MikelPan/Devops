### haproxy配置文件
```shell
global
    maxconn 51200
    pidfile /usr/local/haproxy/logs/haproxy.pid
    ssl-default-bind-ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4:!DH:!DHE:!3DES
defaults
    option tcplog
    mode http
    timeout connect  5000ms
    timeout server 30000ms
    timeout client 30000ms
    balance roundrobin
frontend  main
    bind *:80
    bind *:443  ssl crt /etc/haproxy/haproxy.crt
    bind *:8001  ssl crt /etc/haproxy/haproxy.crt
    log global
    
    # acl 规则
    acl zipkin-dashboard hdr_beg(host) -i zipkin-dashboard-xiajin-dezhou-sd.ssiid.com
    use_backend dashboard if k8s-dashboard || spring-dashboard || eureka-dashboard || hystrix-dashboard || zipkin-dashboard
```