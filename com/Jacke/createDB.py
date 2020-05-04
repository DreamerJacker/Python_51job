#-*- codeing = utf-8 -*-
#@Time : 2020/5/2 18:58
#@Author : Jacke
#@File : createDB.py
#@Software : PyCharm

import sqlite3

def createDB():
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql = '''
        create table job(
           id integer primary key ,
           name varchar,
           linkjob message_text ,
           company varchar ,
           linkcompany message_text ,
           jobplace varchar ,
           jobdate varchar ,
           education varchar ,
           experience varchar ,
           information message_text 
           );
    '''

    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    pass


if __name__ == '__main__':
    createDB()