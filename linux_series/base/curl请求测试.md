#### 1、curl get请求
```shell
curl -vv -s https://www.baidu.com
curl -vv -s https://www.baicu.com?ad=1\&dc=2\&cd=4
```
#### 2、curl post请求
```shell
curl -vv -X POST -H "Content-Type: application/json" -d @post.json -s https://www.baidu.com
curl -vv -X POST -H Content-Type: application/json" -d "{"username":"username","password":"123456"}" -s https://www.baidu.com
```
#### 3、curl soup请求
```shell
curl –d @request.xml –H “Content-Type:text/xml;charset=URF-8” http://localhost/servercenter/soap_all_srv.php?wsdl
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

