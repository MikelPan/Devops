### 标签
#### head标签
```python
# 给标签加颜色修饰(内联)
<style type="text/css">
    span{
        color: read;
    }
    h3{
        color: orgre;
    }
</style>
# 给标签加颜色修饰(外联)
<link rel="stylesheet" type="text/css" href="outstyle.css">
```
#### body标签
##### 字体标签
```shell
h1~h6   -- 标题标签
u       --下划线
b       --加粗
strong  --加粗
em      --倾斜
i       --倾斜
sub     --上标
sup     --下标
hr      --单行横线
br      --换行
del     --定义删除
```
##### 排版标签
```shell
# 网页布局
div     --分割(大范围)
span    --局部分割(小范围)
```
##### 段落标签
```shell
p       --只能放文字，图片，表单元素，其他不能放，不能放容器标签
# a标签超链接
<a href="https://www.baidu.com" target="_self">百度一下</a>
<a href="#">百度一下</a>   -- 不做跳转
a       --超链接
<img src="http://myste.com/image.png" alt="网站制作者"/>
```