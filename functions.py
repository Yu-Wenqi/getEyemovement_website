#该py文件保存系统中所用到的python函数
import pymysql
import datetime
import random
import json
import numpy as np

#数据库参数
host = '127.0.0.1'
port = 3306
user = 'root'
password = '1234567'
database = 'eyeweb'

#登录页面
# 获取密码
def get_password_by_id(id):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    sql = "select * from users where Uid = '%s'" %(id)
    #执行sql语句
    cursor.execute(sql)
    result = cursor.fetchone()
    return result


def get_task_list(username, datatype):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    #默认显示所有数据
    if datatype == 'all':
        sql = '''
        select a.Aid, a.Atitle, a.Alength, t.readtime
        from artical as a, task as t
        where A.Aid = t.Aid AND t.Uid = '%s'
        order by t.readtime ASC
        ''' % (username)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    # 显示已经标注的数据
    elif datatype == 'true':
        sql = '''
        SELECT a.Aid, a.Atitle, a.Alength, t.readtime
        FROM artical AS a, task AS t
        WHERE a.Aid = t.Aid AND t.Uid = '%s' AND t.readtime is not null
        ORDER BY t.readtime ASC
        ''' % (username)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    # 显示未标注的数据
    elif datatype == 'false':
        sql = '''
        SELECT a.Aid, a.Atitle, a.Alength, t.readtime
        FROM artical AS a, task AS t
        WHERE a.Aid = t.Aid AND t.Uid = '%s' AND t.readtime is null
        ORDER BY t.readtime ASC
        ''' % (username)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def get_task_list_admin(datatype):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    #默认显示所有数据
    if datatype == 'all':
        sql = '''
        select a.Aid,t.Uid,a.Atitle,t.readtime,t.duringtime
        from artical as a, task as t
        where A.Aid = t.Aid
        ORDER BY t.readtime ASC
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    # 显示已经标注的数据
    elif datatype == 'true':
        sql = '''
        select a.Aid,t.Uid,a.Atitle,t.readtime,t.duringtime
        from artical as a, task as t
        WHERE a.Aid = t.Aid AND t.readtime is not null
        ORDER BY t.readtime ASC
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    # 显示未标注的数据
    elif datatype == 'false':
        sql = '''
        select a.Aid,t.Uid,a.Atitle,t.readtime,t.duringtime
        from artical as a, task as t
        WHERE a.Aid = t.Aid AND t.readtime is null
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        return result



#根据aid和uid获取某一任务的完成情况（0为未完成，1为已完成）
def check_state(uid,aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    sql = '''
    SELECT t.state
    FROM task as t
    WHERE t.Uid = '%s' AND t.Aid = '%s'  
    '''% (uid,aid)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

#通过aid获取相关句子的信息('1', '我是第一篇文章的第一个句子。')
def get_sentence(aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    sql = '''
        SELECT Sid,Sentence
        FROM sentence 
        WHERE Aid = '%s'  
        ''' % (aid)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = list(result)
    #排列好句子的顺序
    result = bubble_sort(result)
    sentence = []
    for i in range(0,len(result)):
        sentence.append(result[i][1])
    return sentence

#获取文章句子所对应的sid列表
def get_sentence_id(aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    sql = '''
        SELECT Sid,Sentence
        FROM sentence 
        WHERE Aid = '%s'  
        ''' % (aid)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = list(result)
    #排列好句子的顺序
    result = bubble_sort(result)
    sentence_id = []
    for i in range(0,len(result)):
        sentence_id.append(result[i][0])
    return sentence_id


#对句子编号进行冒泡排序来确定句子顺序
def bubble_sort(sentence):
    for j in range(0,len(sentence) - 1):#整个数列排序循环
        for i in range(0,len(sentence) - 1 - j):
            # 元素从头走到尾，走完一次，排好一个数
            temple = 0
            if sentence[i][0] > sentence[i + 1][0]:
                #因为要和下一个数相比，所以i只需要走到len(alist) - 1 - j
                # sentence[i],sentence[i + 1] = sentence[i + 1],sentence[i]
                temple= sentence[i]
                sentence[i] = sentence[i + 1]
                sentence[i + 1] = temple
    return sentence

#从artical中获取文章的标题
def get_title(aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    sql = '''
            SELECT Atitle
            FROM artical 
            WHERE Aid = '%s'  
            ''' % (aid)
    cursor.execute(sql)
    result = cursor.fetchone()
    result = result[0]
    return result



#更改task中的信息
def change_state(uid,aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    time = datetime.datetime.now()
    print(time)
    try:
        sql_up = '''
            UPDATE task
            SET state ='1',readtime = '%s'
            WHERE  Uid = '%s' And Aid = '%s'
            '''% (time,uid,aid)
        cursor.execute(sql_up)
        db.commit()
    except:
        print("数据修改失败,请返回登陆页面")

#计算duringtime并保存到数据库中
#1.获取当前的时间
#2.获取数据库中的readtime
#3.计算两者之间的时间差
#4，将结果插入
def get_duringtime(uid,aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    #1.
    time = datetime.datetime.now()
    #2.
    sql = '''
        SELECT readtime
        FROM task 
        WHERE Uid = '%s' AND Aid = '%s'  
        ''' % (uid,aid)
    cursor.execute(sql)
    readtime = cursor.fetchone()
    readtime = readtime[0]
    # print(time)
    # print(readtime)
    #3.计算时间差(单位为秒）
    duringtime = time-readtime
    duringtime = duringtime.seconds
    #修改表中的数据
    try:
        sql_up = '''
            UPDATE task
            SET duringtime = '%s'
            WHERE  Uid = '%s' And Aid = '%s'
            '''% (duringtime,uid,aid)
        cursor.execute(sql_up)
        db.commit()
    except:
        print("数据修改失败,请返回登陆页面")






#重置相关任务的信息
def reset_task_info(a_id,u_id):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    state = 0
    #打印修改前的task表
    sql = '''
            SELECT *
            FROM task 
            WHERE Uid = '%s' AND Aid = '%s'  
            ''' % (u_id, a_id)
    cursor.execute(sql)
    result_be= cursor.fetchone()
    print(result_be)
    try:
        # 更改task中的信息(更改成功）
        sql_reset = '''
            UPDATE task
            SET state ='0',readtime = NUll,duringtime = NULL
            WHERE  Uid = '%s' And Aid = '%s'
            '''% (u_id,a_id)
        cursor.execute(sql_reset)
        db.commit()
        # 删除eyedata表中的相关数据
        sql_delete = '''
            DELETE a
            FROM eyedata AS a, sentence AS b
            WHERE  a.Sid = b.Sid And b.Aid = '%s' And a.Uid = '%s'
            '''% (a_id,u_id)
        cursor.execute(sql_delete)
        db.commit()
        state = 1
        sql = '''
                SELECT *
                FROM task 
                WHERE Uid = '%s' AND Aid = '%s'  
                ''' % (u_id, a_id)
        cursor.execute(sql)
        result_af = cursor.fetchone()
        print(result_af)
        return state
    except:
        print("数据修改失败,请返回登陆页面")


def save_eyedata_info(sid,uid,wordid,x,y,time):
    #连接数据库
    state = 0
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    # print(sid)
    sid = sid[1:-1]
    print(sid)
    #将数据存入数据库
    try:
        sql_in = '''
            INSERT  INTO  eyedata
            VALUES  ('%s','%s','%s','%s','%s','%s')
            '''% (sid,uid,wordid,time,x,y)
        cursor.execute(sql_in)
        db.commit()
        state = 1
        return state
    except:
        print("眼动数据保存失败！")
        return state


#获取artical表中的文章选项
def get_options(aid):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    sql = '''
            SELECT options
            FROM artical 
            WHERE Aid = '%s'  
            ''' % (aid)
    cursor.execute(sql)
    result = cursor.fetchone()
    result = result[0]
    #结果为”信息熵；主题标引；服务；“，要对其进行分割成数组
    return result


def exchange_options(options):
    #在0-2中间获取一个随机数字
    a = random.randint(0, 2)
    b = random.randint(0, 2)
    temp = options[a]
    options[a] = options[b]
    options[b] = temp
    return options


#保存用户的验证问题答案
def save_u_answer(aid,uid,option):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306)
    cursor = db.cursor()
    state = 0
    #打印修改前的task表
    sql = '''
            SELECT *
            FROM task 
            WHERE Uid = '%s' AND Aid = '%s'  
            ''' % (uid, aid)
    cursor.execute(sql)
    result_be= cursor.fetchone()
    print(result_be)
    if result_be[6] != None:
        return state
    else:
        try:
            time = datetime.datetime.now()
            # 更改task中的信息(更改成功）
            sql_answer = '''
                UPDATE task
                SET u_answer = '%s',a_time = '%s'
                WHERE  Uid = '%s' And Aid = '%s' 
                '''% (option,time,uid,aid)
            cursor.execute(sql_answer)
            db.commit()
            state = 1
            sql = '''
                SELECT *
                FROM task 
                WHERE Uid = '%s' AND Aid = '%s'  
                ''' % (uid, aid)
            cursor.execute(sql)
            result_af = cursor.fetchone()
            print(result_af)
            return state
        except:
            print("数据修改失败,请返回登陆页面")
            return state

#测试函数功能
if __name__ == '__main__':
    # a = '2'
    # b = '2'
    # get_duringtime(a,b)
    # test = (('4', '我是第二篇文章的第二个句子，我是第二篇文章的第二个句子。'),('3', '我是第二篇文章的第一个句子。'), ('5', '我是第二篇文章的第三个句子呐！'))
    # test = list(test)
    # bubble_sort(test)
    # time = datetime.datetime.now()
        # strftime("%Y-%m-%d %H:%M:%S.%L")
    #测试string可以用下标获取
    aid = "001"
    uid = "202201"
    option = "test"

    state = save_u_answer(aid, uid, option)
    print(state)
    # options = ["第一个","第二个","第三个"]
    # exchange_options(options)




