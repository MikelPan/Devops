### 1、编写第一个爬虫
#### 1.1、第一步，获取页面
```python
#!/usr/bin/python

import requests
import urllib3

urllib3.disable_warnings()
url  = "https://www.plyx.site"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}

r = requests.get(url, headers=headers, verify=False)
print(r.text)
# 结果输出
<li><a href='https://www.plyx.site/2018/12/'>2018年十二月</a></li>
		</ul>
		</div><div id="categories-2" class="widget widget_categories"><h5>分类目录</h5>		<ul>
	<li class="cat-item cat-item-1"><a href="https://www.plyx.site/category/linux-tutorial-series/" >linux系列</a>
</li>
	<li class="cat-item cat-item-5"><a href="https://www.plyx.site/category/mongodb/" >mongo进阶之路</a>
</li>
	<li class="cat-item cat-item-3"><a href="https://www.plyx.site/category/mysql-analysis/" >Mysql浅析</a>
</li>
	<li class="cat-item cat-item-4"><a href="https://www.plyx.site/category/redis/" >redis学习指南</a>
</li>
	<li class="cat-item cat-item-7"><a href="https://www.plyx.site/category/%e5%b7%a5%e5%85%b7%e7%b1%bb/" >工具类</a>
</li>
	<li class="cat-item cat-item-6"><a href="https://www.plyx.site/category/%e6%80%a7%e8%83%bd%e6%b5%8b%e8%af%95/" >性能测试</a>
</li>
	<li class="cat-item cat-item-10"><a href="https://www.plyx.site/category/%e9%a3%8e%e6%99%af%e9%89%b4%e8%b5%8f/" >风景鉴赏</a>
</li>
```
##### 首先 import requests，使用requests.get(url,headers=headers,verify=False)获取网页内容

- 使用requests的headers伪装成浏览器访问
- r是requests的response对象，可以通过r.text获取返回的网页代码

#### 1.2、提取需要的数据
```python
#!/usr/bin/python
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()
url  = "https://www.plyx.site"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}

r = requests.get(url, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "lxml")
title = soup.find("h1", class_="hestia-title").text.strip()
print(title)
# 输出结果
Until the end of the sky
```
##### 在获取整个网页后，提取整个网页的博客标题头，使用BeautifulSoup进行解析，将html页面转换为soup对象，接下来使用soup.find("h1", class_="hestia-title").text.strip()得到标题图，并且打印出来。

#### 1.3、存储数据
```python
#!/usr/bin/python
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()
url  = "https://www.plyx.site"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}

r = requests.get(url, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "lxml")
title = soup.find("h1", class_="hestia-title").text.strip()
print(title)

with open('title.txt', "a+") as f:
    f.write(title)
    f.close()
```
##### 将变量存储到本地的同目录下txt文件下