### nginx解决跨域问题
```shell
listen       80;
server_name  _;

#charset koi8-r;
#access_log  /var/log/nginx/log/host.access.log  main;
location / {
     if ($request_method = 'OPTIONS') {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET';
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
        add_header 'Access-Control-Expose-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
        return 204;
    }
    if ($request_method = 'GET') {
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Credentials' 'true';
        add_header 'Access-Control-Allow-Methods' 'GET';
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
        add_header 'Access-Control-Expose-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range';
    }
    root   /data/static;
    index  index.config;
}
```
### NGINX配置示例
```shell
#!nginx
: # 使用的用户和组
: user  www www;
: # 指定工作衍生进程数
: worker_processes  2;
: # 指定 pid 存放的路径
: pid /var/run/nginx.pid;

: # [ debug | info | notice | warn | error | crit ] 
: # 可以在下方直接使用 [ debug | info | notice | warn | error | crit ]  参数
: error_log  /var/log/nginx.error_log  info;

: events {
: # 允许的连接数
: connections   2000;
: # use [ kqueue | rtsig | epoll | /dev/poll | select | poll ] ;
: # 具体内容查看 http://wiki.codemongers.com/事件模型
: use kqueue;
: }

: http {
: include       conf/mime.types;
: default_type  application/octet-stream;

: log_format main      '$remote_addr - $remote_user [$time_local]  '
: '"$request" $status $bytes_sent '
: '"$http_referer" "$http_user_agent" '
: '"$gzip_ratio"';

: log_format download  '$remote_addr - $remote_user [$time_local]  '
: '"$request" $status $bytes_sent '
: '"$http_referer" "$http_user_agent" '
: '"$http_range" "$sent_http_content_range"';

: client_header_timeout  3m;
: client_body_timeout    3m;
: send_timeout           3m;

: client_header_buffer_size    1k;
: large_client_header_buffers  4 4k;

: gzip on;
: gzip_min_length  1100;
: gzip_buffers     4 8k;
: gzip_types       text/plain;

: output_buffers   1 32k;
: postpone_output  1460;

: sendfile         on;
: tcp_nopush       on;
: tcp_nodelay      on;
: send_lowat       12000;

: keepalive_timeout  75 20;

: #lingering_time     30;
: #lingering_timeout  10;
: #reset_timedout_connection  on;


: server {
: listen        one.example.com;
: server_name   one.example.com  www.one.example.com;

: access_log   /var/log/nginx.access_log  main;

: location / {
: proxy_pass         http://127.0.0.1/;
: proxy_redirect     off;

: proxy_set_header   Host             $host;
: proxy_set_header   X-Real-IP        $remote_addr;
: #proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;

: client_max_body_size       10m;
: client_body_buffer_size    128k;

: client_body_temp_path      /var/nginx/client_body_temp;

: proxy_connect_timeout      90;
: proxy_send_timeout         90;
: proxy_read_timeout         90;
: proxy_send_lowat           12000;

: proxy_buffer_size          4k;
: proxy_buffers              4 32k;
: proxy_busy_buffers_size    64k;
: proxy_temp_file_write_size 64k;

: proxy_temp_path            /var/nginx/proxy_temp;

: charset  koi8-r;
: }

: error_page  404  /404.html;

: location /404.html {
: root  /spool/www;

: charset         on;
: source_charset  koi8-r;
: }

: location /old_stuff/ {
: rewrite   ^/old_stuff/(.*)$  /new_stuff/$1  permanent;
: }

: location /download/ {

: valid_referers  none  blocked  server_names  *.example.com;

: if ($invalid_referer) {
: #rewrite   ^/   http://www.example.com/;
: return   403;
: }

: #rewrite_log  on;

: # rewrite /download/*/mp3/*.any_ext to /download/*/mp3/*.mp3
: rewrite ^/(download/.*)/mp3/(.*)\..*$
: /$1/mp3/$2.mp3                   break;

: root         /spool/www;
: #autoindex    on;
: access_log   /var/log/nginx-download.access_log  download;
: }

: location ~* ^.+\.(jpg|jpeg|gif)$ {
: root         /spool/www;
: access_log   off;
: expires      30d;
: }
: }
: }
```
### nginx两个虚拟主机
```shell
http {
: server {
: listen          80;
: server_name     www.domain1.com;
: access_log      logs/domain1.access.log main;
: location / {
: index index.html;
: root  /var/www/domain1.com/htdocs;
: }
: }
: server {
: listen          80;
: server_name     www.domain2.com;
: access_log      logs/domain2.access.log main;
: location / {
: index index.html;
: root  /var/www/domain2.com/htdocs;
: }
: }
}
```
### nginx一个虚拟主机
```shell
http {
: server {
: listen          80 default;
: server_name     _ *;
: access_log      logs/default.access.log main;
: location / {
: index index.html;
: root  /var/www/default/htdocs;
: }
: }
}
```
### nginx负载均衡
```shell
http {
: upstream myproject {
: server 127.0.0.1:8000 weight=3;
: server 127.0.0.1:8001;
: server 127.0.0.1:8002;
: server 127.0.0.1:8003;
: }

: server {
: listen 80;
: server_name www.domain.com;
: location / {
: proxy_pass http://myproject;
: }
: }
}
```
### nginx防盗链
```shell
location ~* \.(gif|jpg|png|swf|flv)$ {
root html
valid_referers none blocked *.nginxcn.com;
if ($invalid_referer) {
rewrite ^/ www.nginx.cn
#return 404;
}
}
```

