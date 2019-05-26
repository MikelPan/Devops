#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 开发团队：云飞国际
# 开发人员： 93792
# 开发时间： 2019/5/26 20:58
# 文件名称： Peewee.py
# 开发工具： PyCharm

from peewee import *

# 建立数据库引擎对象
db = SqlitDatabase("sampleDB.db")

# 定义ORM基类
class BeseModel(Model):
    class Meta:
        database = db

#定义course表，继承自BaseModel
class Course(BeseModel):
    id  = PrimaryKeyField()
    title = CharField(null = false)
    period = IntegerField()
    description = CharField()

    class Meta:
        order_by = ('title',)
        db_table = 'course'

Course.create_table()
