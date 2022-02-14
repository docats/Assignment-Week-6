import pymysql
import mysql.connector

#嘗試連接到資料庫
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="mydatabase"
)

#檢查資料庫是否存在
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
#使用迴圈遍歷
for x in mycursor:
    print(x)
