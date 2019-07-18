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

###### 字典是一种可变容器，使用键值对的方式存储数据，每个key必须唯一，values可以不唯一，values可以是任何数据类型。
```python
In [5]: print(python["base"])                                                                     
1
In [6]: print(python)                                                                             
{'base': 1, 'shell': 'abc', 3: 1}
# 循环提取字典的值
In [7]: for k,v in python.items(): 
   ...:     print(k,v) 
base 1
shell abc
3 1
```
##### 1.3、条件语句和循环语句
###### 条件语句可以使得当满足条件的时候才执行某部分代码，条件为布尔值，只有True和False，当if条件成立时执行后面的语句，当条件不成立时，执行else后面的语句。
```python
In [10]: if book == "python": 
    ...:     print("my book is python") 
    ...: else: 
    ...:     print("my book is othe")                                                             
my book is python
# 如果需要判断多种条件就需要使用elif
In [12]: if book == "python": 
    ...:     print("my book is python") 
    ...: elif book == "java": 
    ...:     print("my book is java") 
    ...: else: 
    ...:     print("my book is others")                                                                         
my book is java
```
###### 循环语句能让执行一个代码的片段多次，循环分为for循环和while循环，for循环能在一个给定的顺序下重复执行。
```python
In [13]: for i in range(0,10): 
    ...:     print(i)                                                                                       
```
###### while能不断重复执行，只要满足一定的条件
```python
In [14]: count = 0                                                                                

In [15]: while count < 5: 
    ...:     print(count) 
    ...:     count += 1                                                                                        
0
1
2
3
4
```
##### 1.4、函数
###### 一个函数包含输入参数和输出参数，参数必须正确的写入到函数中，函数的参数也可以为多个。
```python
In [16]: def calulus(x): 
    ...:     y = x + 1 
    ...:     return y 
    ...: result = calulus(2)                                                                      
In [17]: print(result)                                                                            
3
# 定义多个参数函数
In [18]: def add(a,b): 
    ...:     c = a+b 
    ...:     return c 
    ...: c = add(1,2)                                                                             
In [19]: print(c)                                                                                 
3
```
##### 1.5、面向对象编程
###### 面对对象编程是把函数进行分类和封装后放入到对象中，使得开发更快，更强
```python
In [21]: class Persion: 
    ...:     def __init__(self, name, age): 
    ...:         self.name = name 
    ...:         self.age = age 
    ...:     def detail(self): 
    ...:         print(self.name) 
    ...:         print(self.age) 
    ...: pesion = Persion('abc', 18)                                                              
In [22]: pesion.detail()                                                                          
abc
18
```
**封装**
###### 封装分为两步，第一步为封装内容，第二步为调用被封装的内容
```python
# 封装内容
In [23]: class Persion: 
    ...:     def __init__(self, name, age): 
    ...:         self.name = name 
    ...:         self.age = age 
    ...: pesion = Persion('def', 18) # 将def和18分别封装到persion中以及self的name和age属性
# 调用被封装的内容
In [23]: class Persion: 
    ...:     def __init__(self, name, age): 
    ...:         self.name = name 
    ...:         self.age = age 
    ...: pesion = Persion('def', 18) # 将def和18分别封装到persion中以及self的name和age属性                    
In [24]: print(pesion.name)          # 直接调用pesion对象的name属性                                           
def
In [25]: print(pesion.age)           # 直接调用pesion对象的age属性                                            
18
# 通过self间接调用时，python会默认将pesion传给self参数，pesion.detail(pesion),此时方法内部的self=pesion，即self.name='def',self.age=18
In [26]: class Persion: 
    ...:     def __init__(self, name, age): 
    ...:         self.name = name 
    ...:         self.age = age 
    ...:     def detail(self): 
    ...:         print(self.name) 
    ...:         print(self.age) 
    ...: pesion = Persion('def', 18) 
In [28]: pesion.detail()    # python将pesion传给self参数，即pesion.detail(pesion),此时内部self=pesion                             
def
18  
```
**继承**
###### 继承是普通类为基础建立的专门的类对象，子继承父的某些特征
```python
In [31]: class Common(): 
    ...:     def eat(self): 
    ...:         print("%s eat" %self.name) 
    ...: class Cat(Common): 
    ...:     def __init__(self, name): 
    ...:         self.name = name 
    ...:     def cry(self): 
    ...:         print("wang wang jiao") 
    ...: class Dog(Common): 
    ...:     def __init__(self, name): 
    ...:         self.name = name 
    ...:     def cry(self): 
    ...:         print("gu gu jiao") 
    ...: cat1 = Cat('cat') 
    ...: cat1.cry() 
    ...: cat1.eat() 
    ...: dog1 = Dog('dog') 
    ...: dog1.cry() 
    ...: dog1.eat()                                                                                        
wang wang jiao
cat eat
gu gu jiao
dog eat
```
**多态**

