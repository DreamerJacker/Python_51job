#coding:gbk
#@Time : 2020/5/2 10:43
#@Author : Jacke
#@File : saveData.py
#@Software : PyCharm
import sqlite3

data = {'name': 'Python高级开发工程师', 'linkjob': 'https://jobs.51job.com/hangzhou-yhq/121784838.html?s=01&t=0', 'company': '杭州认识科技有限公司', 'linkcompany': 'https://jobs.51job.com/all/co5086712.html', 'jobplace': '杭州-余杭区', 'jobdate': '05/04', 'education': '本科', 'experience': '3-4年经验', 'information': '岗位职责，1、负责基于FeeSwitch的通讯平台功能开发2、负责呼叫系统的技术架构设计、方案实现；3、负责Feeswitch与客户端通讯过程中疑难问题的排查和解决岗位要求，1.统招本科及以上学历，至少三年以上Python开发经验2.熟悉TCP/IP协议，熟练掌握Linux下socket编程、多线程编程，有网络服务编程、feeswitch开发经验者优先3.熟悉Django/flask等，了解HTTP协议，有Web应用程序开发经验;4.了解数据库原理，至少熟悉MySQL数据库;5.熟悉Linux，对CentOS有深入了解，有丰富数据库使用经验者优先6.良好的编码风格和编程习惯，熟练掌握SVN，Git等代码版本管理工具'}


def saveData(data):
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql_key = ','.join(data.keys())
    sql_value = '\',\''.join(data.values())

    sql = '''
            insert into job (%s) values ('%s')'''%(sql_key,sql_value)

    print(sql_value)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    pass

saveData(data)