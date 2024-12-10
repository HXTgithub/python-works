from tkinter import *
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='695273 ',
    autocommit=True
)

sort_stu = int(0)
sort_data = int(0)

cursor = conn.cursor()

cursor.execute("create database if not exists student1;")
conn.select_db("student1")

sql1="create table if not exists students(id varchar(10) not null,name varchar(10),class1 varchar(10),math int,english int,computer int,total int,primary key (id))"
cursor.execute(sql1)
sql2="create table if not exists admin(name varchar(10),pwd varchar(10))"
cursor.execute(sql2)

def check_login(uname,pwd):
    cursor.execute("select * from admin")
    results = cursor.fetchall()
    for na,pd in results:
        if na == uname and pd == pwd:
            return True,'登录成功'
        else:
            return False,'登录失败，用户名或密码错误'


def add_admin(uname,pwd):
    cursor.execute("insert into admin values('{0}','{1}');".format(uname,pwd))


def check_username(uname):
    cursor.execute("select count(*) from admin where name = '{0}';".format(uname))
    res = cursor.fetchall()
    if res[0][0]:
        return True
    return False


def all():
    if sort_stu==1:
        if sort_data == 0:
            cursor.execute("select * from students order by id;")
        elif sort_data == 1:
            cursor.execute("select * from students order by total;")
        elif sort_data == 2:
            cursor.execute("select * from students order by math;")
        elif sort_data == 3:
            cursor.execute("select * from students order by english;")
        elif sort_data == 4:
            cursor.execute("select * from students order by computer;")
    else:
        if sort_data == 0:
            cursor.execute("select * from students order by id desc;")
        elif sort_data == 1:
            cursor.execute("select * from students order by total desc;")
        elif sort_data == 2:
            cursor.execute("select * from students order by math desc;")
        elif sort_data == 3:
            cursor.execute("select * from students order by english desc;")
        elif sort_data == 4:
            cursor.execute("select * from students order by computer desc;")
    data = cursor.fetchall()
    key = ('id','name','class','math','english','computer','total')
    jsonList = []

    for i in data:
        jsonList.append(dict(zip(key,i)))
    return jsonList


def check_id(id):
    cursor.execute("select count(*) from students where id = '{0}';".format(id))
    res = cursor.fetchall()
    if res[0][0]:
        return False,"该学号已存在，请重新输入"
    return True,'录入成功'


def search_class(class_value):
    cursor.execute("select * from students where class1 = '{0}';".format(class_value))
    data = cursor.fetchall()
    key = ('id','name','class1','math','english','computer','total')
    jsonList = []

    for i in data:
        jsonList.append(dict(zip(key,i)))
    return jsonList


def insert(stu):
    cursor.execute("insert into students values('{0}','{1}','{2}','{3}','{4}','{5}','{6}');".
                   format(stu[0],stu[1],stu[2],stu[3],stu[4],stu[5],stu[6]))


def delete_id(user_id):
    cursor.execute("select * from students where id = '{0}';".format(user_id))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("delete from students where id = '{0}';".format(user_id))
        return True,'删除成功'
    else:
        return  False,'学号为'+ str(user_id) + '的学生不存在'


def delete_name(user_name):
    cursor.execute("select * from students where name = '{0}';".format(user_name))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("delete from students where name = '{0}';".format(user_name))
        return True,'删除成功'
    else:
        return False,'姓名为'+ str(user_name) + '的学生不存在'


def search_id(user_id):
    cursor.execute("select count(*) from students where id = '{0}';".format(user_id))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("select * from students where id = '{0}';".format(user_id))
        stu = cursor.fetchall()
        return True,stu
    else:
        return False,'学号为' + str(user_id) + '的学生不存在'


def search_name(user_name):
    cursor.execute("select count(*) from students where name = '{0}';".format(user_name))
    res = cursor.fetchall()
    if res[0][0]:
        cursor.execute("select * from students where name = '{0}';".format(user_name))
        stu = cursor.fetchall()
        return True,stu
    else:
        return False,'姓名为' + str(user_name) + '的学生不存在'


if not check_username("root"):
    add_admin('root','123456')