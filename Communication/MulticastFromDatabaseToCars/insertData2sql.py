#!/usr/bin/python3
# 首先安装PyMySQL库：pip install PyMySQL
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "", "swarmintelligence")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = """INSERT INTO `location` (`ID`, `X`, `Y`, `Z`, `speed`, `pitch`, `roll`, `azimuth`, `time`) VALUES ('100', '1', '1', '1', '1', '1', '1', '1', CURRENT_TIMESTAMP), ('101', '1', '2', '2', '2', '2', '2', '2', CURRENT_TIMESTAMP)"""
try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    db.rollback()

# 关闭数据库连接
db.close()


# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
#
# import mysql.connector
#
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="",
#     database="swarmintelligence"
# )
# mycursor = mydb.cursor()
#
# sql = "INSERT INTO sites (ID, X, Y, Z, speed, pitch, roll, azimuth, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
# val = [
#   ('100', '1', '1', '1', '1', '1', '1', '1', 'CURRENT_TIMESTAMP'),
#   ('101', '1', '2', '2', '2', '2', '2', '2','CURRENT_TIMESTAMP' )
# ]
#
# mycursor.execute(sql, val)
#
# mydb.commit()  # 数据表内容有更新，必须使用到该语句
#
# print(mycursor.rowcount, "记录插入成功。")

# import MySQLdb
#
# # 打开数据库连接
# db = MySQLdb.connect("localhost", "root", "", "swarmintelligence", charset='utf8' )
#
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()
#
# # SQL 插入语句
# sql = """INSERT INTO `location` (`ID`, `X`, `Y`, `Z`, `speed`, `pitch`, `roll`, `azimuth`, `time`) VALUES ('100', '1', '1', '1', '1', '1', '1', '1', CURRENT_TIMESTAMP), ('101', '1', '2', '2', '2', '2', '2', '2', CURRENT_TIMESTAMP)"""
# try:
#    # 执行sql语句
#    cursor.execute(sql)
#    # 提交到数据库执行
#    db.commit()
# except:
#    # Rollback in case there is any error
#    db.rollback()
#
# # 关闭数据库连接
# db.close()