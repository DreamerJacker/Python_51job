#coding:gbk
#@Time : 2020/5/2 10:43
#@Author : Jacke
#@File : saveData.py
#@Software : PyCharm
import sqlite3

data = {'name': 'Python�߼���������ʦ', 'linkjob': 'https://jobs.51job.com/hangzhou-yhq/121784838.html?s=01&t=0', 'company': '������ʶ�Ƽ����޹�˾', 'linkcompany': 'https://jobs.51job.com/all/co5086712.html', 'jobplace': '����-�ຼ��', 'jobdate': '05/04', 'education': '����', 'experience': '3-4�꾭��', 'information': '��λְ��1���������FeeSwitch��ͨѶƽ̨���ܿ���2���������ϵͳ�ļ����ܹ���ơ�����ʵ�֣�3������Feeswitch��ͻ���ͨѶ����������������Ų�ͽ����λҪ��1.ͳ�б��Ƽ�����ѧ����������������Python��������2.��ϤTCP/IPЭ�飬��������Linux��socket��̡����̱߳�̣�����������̡�feeswitch��������������3.��ϤDjango/flask�ȣ��˽�HTTPЭ�飬��WebӦ�ó��򿪷�����;4.�˽����ݿ�ԭ��������ϤMySQL���ݿ�;5.��ϤLinux����CentOS�������˽⣬�зḻ���ݿ�ʹ�þ���������6.���õı�����ͱ��ϰ�ߣ���������SVN��Git�ȴ���汾������'}


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