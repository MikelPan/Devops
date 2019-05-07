#### 一、基本命令
##### 1.1、基本命令
```python
In [1]: print("hello world!")                                                                     
hello world!
In [3]: x=1                                                                                       
In [4]: if x ==1: 
   ...:     print("hello world")                                                                                  
hello world
```
##### 1.2、数据类型
**字符串**

###### 字符串是最常见的数据类型，一般用来存储类似的“句子”，并放在单引号(')或双引号(")中。
```python
In [5]: string1 = 'Python'                                                                        
In [6]: string2 = "is"                                                                            
In [7]: string3 = string1 + "" + string2                                                          
In [8]: print(string3)                                                                            
Pythonis
```
**数字**

###### 数字用来存储数值，包含两种数值类型：整数(int)和浮点型(float),其中浮点数由整数和小数部分组成。两种类型相互转换，如果要将整数转换为浮点数，就在变量前面加上float；如果要将浮点数转换为整数，就在前面加上int。
```python
In [9]: int1 = 1                                                                                  
In [10]: float1 = 1.1                                                                             
In [11]: int2 = float(int1)                                                                       
In [12]: float2 = int(float1)                                                                     
In [13]: print(int2,float2)                                                                       
1.0 1
```
**列表**

###### 列表包含任意种类的数据类型和任意数量。创建列表只需要把不同的变量放到[]中，中间用逗号分隔。
```python
In [14]: list1 = [1,2,3,4,5]                                                                      
In [15]: list2 = ["a","b","c","d","e"]                                                            
In [16]: list3 = ['abc','def']                                                                    
In [17]: list4 = list1 + list2 + list3                                                            
In [18]: print(list4)                                                                             
[1, 2, 3, 4, 5, 'a', 'b', 'c', 'd', 'e', 'abc', 'def']
```
###### 列表中索引从0开始，-1为最后一位，:表示列表所有元素，m：n表示从索引m开始到索引n结束
```python
In [19]: list5 = list1[0]                                                                         
In [20]: print(list5)                                                                             
1
In [21]: list6 = list4[:]                                                                         
In [22]: print(list6)                                                                             
[1, 2, 3, 4, 5, 'a', 'b', 'c', 'd', 'e', 'abc', 'def']
In [23]: list7 = list4[-1]                                                                        
In [24]: print(list7)                                                                             
def
```
**字典**

###### 字典是一种可变容器

