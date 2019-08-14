#### 1、curl get请求
```shell
curl -vv -s https://www.baidu.com
curl -vv -s https://www.baicu.com?ad=1\&dc=2\&cd=4
```
#### 2、curl post请求
```shell
# 定义格式化时间请求
cat > request_time.txt <<EOF
\n
    	      http: %{http_code}\n
               dns: %{time_namelookup}s\n
          redirect: %{time_redirect}s\n
      time_connect: %{time_connect}s\n
   time_appconnect: %{time_appconnect}s\n
  time_pretransfer: %{time_pretransfer}s\n
time_starttransfer: %{time_starttransfer}s\n
     size_download: %{size_download}bytes\n
    speed_download: %{speed_download}B/s\n
                  ----------\n
        time_total: %{time_total}s\n
\n
EOF
curl -vv -x POST -w "@request_time.txt" -H "Content-Type: application/json" -d @post.json -s https://www.baidu.com
# 指定json数据请求
cat > post.json <<EOF
{
    "username": "username",
    "password": "123456"
}
EOF
curl -vv -X POST -H "Content-Type: application/json" -d @post.json -s https://www.baidu.com
# 带数据请求
curl -vv -X POST -H "Content-Type: application/json" -d "{"username":"username","password":"123456"}" -s https://www.baidu.com
```
#### 3、curl soup请求
```shell
curl –d @request.xml –H "Content-Type:text/xml;charset=URF-8" http://localhost/servercenter/soap_all_srv.php?wsdl
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="urn:mytimeserv">
<soap:Body>
<now>
<format>H:i:s</format>
</now>
</soap:Body>
</soap:Envelope>
```
#### 4、curl 认证请求
```shell
curl -u user:pwd https://www.baidu.com
```

