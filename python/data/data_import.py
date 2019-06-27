#!/usr/bin/env python

import pymysql
import xlwt

src_table_name ='TXJBXX_RS_190527'
dest_table_name ='TXJBXX_RS_190527_delete01'


def quary(sql, *parms):
    '''查询数据
    '''
    coon = pymysql.connect(host="192.168.99.3", user="mikel", password="Password1@mikel", database="data_import",
                           charset="utf8")  # 连接数据库
    cursor = coon.cursor()  # 定义游标
    cursor.execute(sql)  # 执行sql
    data = cursor.fetchall()  # 获取查询结果
    cursor.close()  # 关闭游标
    coon.close()  # 关闭连接
    return data

def data_Processing():
    # 增加字段
    quary("alter table %s add id_number_enc varchar(128) comment '身份证加密字段'" % src_table_name)
    # 身份证加密
    quary("update %s set id_number_enc = HEX(AES_ENCRYPT(SHBZHM, 'N8HblK2%0$5ihB)C'))" % src_table_name)
    # 创建新表存储数据
    quary("CREATE TABLE %s select * from %s" % (src_table_name, dest_table_name))
    # 删除身份证不为18的数据
    quary("delete from %s where `SHBZHM` not REGEXP '[0-9]{18}|[0-9]{17}X|[0-9]{15}'" % src_table_name)

def data_to

def data_to_excel(data, file):
    data = quary("select * from %s where SHBZHM not REGEXP '^[1-9]{1}[0-9]{17}|[0-9]{16}X$' and SHBZHM not REGEXP '^[0-9]{15}$'" % src_table_name)

def set_style_excel(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold  # 是否加粗，默认不加粗
    font.color_index = 4
    font.height = height  # 定义字体大小
    style.font = font

    alignment = xlwt.Alignment()  # 创建居中
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 可取值: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 可取值: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    style.alignment = alignment  # 文字居中

def msyql_to_excel():
    data = quary("")
def wite_to_excel(name):
    filename = name + '.xls'  #定义Excel名字
    wbk = xlwt.Workbook()     #实例化一个Excel
    sheet1 = wbk.add_sheet('sheet1',cell_overwrite_ok=True) #添加该Excel的第一个sheet，如有需要可依次添加sheet2等
    fileds = [u'ID编号',u'名字'] #直接定义结果集的各字段名
    execude_sql(1024)  #调用函数执行SQL，获取结果集
    # 写入字段信息
    for filed in range(0, len(fileds)):
        sheet1.write(0,filed,fileds[i])
    # 写入SQL查询数据
    for row in range(1,len(result)+1):
        for col in range(0,len(fileds))
　　　　　　sheet1.write(row,col,result[row-1][col])
　　 wbk.save(filename)　　#保存Excel



