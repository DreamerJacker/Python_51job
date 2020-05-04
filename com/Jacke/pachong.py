#-*- codeing = utf-8 -*-
#@Time : 2020/5/2 10:42
#@Author : Jacke
#@File : pachong.py
#@Software : PyCharm

#-*- codeing = gbk -*-
#@Time : 2020/4/30 13:03
#@Author : Jacke
#@File : pachong.py
#@Software : PyCharm

import re
import requests
from urllib import parse
from bs4 import BeautifulSoup
import sqlite3

'''
url分析：
Python+杭州-第二页： https://search.51job.com/list/080200,000000,0000,00,9,99,Python,2,3.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=
Python+杭州-第二页： https://search.51job.com/list/080200,000000,0000,00,9,99,Python,2,2.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=
Python+杭州-第一页： https://search.51job.com/list/080200,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
Python开发+杭州：         https://search.51job.com/list/080200,000000,0000,00,9,99,Python%25E5%25BC%2580%25E5%258F%2591,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
Python开发工程师+杭州：    https://search.51job.com/list/080200,000000,0000,00,9,99,Python%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
Python开发工程师+温州：    https://search.51job.com/list/080400,000000,0000,00,9,99,Python%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=

'''
EDUCATION = ['本科','大专','硕士','博士','高中','初中及以下','中专','中技']
EXPERIENCE1 = r'在校生/应届生'

findPagenum = re.compile(r'<span class="td">共(\d*)页，到第</span>')
findName = re.compile(r'target="_blank" title="(.*?)"')
findLinkjob = re.compile(r'href="(.*?)"')
findCompany = re.compile(r'target="_blank" title="(.*?)"')
findLinkcompany = re.compile(r'href="(.*?)"')
findPlace = re.compile(r'<span class="t3">(.*?)</span>')
findSalary = re.compile(r'<span class="t4">(.*?)</span>')
findDate = re.compile(r'(\d*?)-(\d*?)发布')
findExperience = re.compile(r'(.*?)经验')
#findEducation = re.compile(r'')
findInformation = re.compile(r'<div class="bmsg job_msg inbox">(.*?)<div class="mt10">')
findMsg = re.compile(r'title="(.*?)"')
numTemp = re.compile(r'共(.*?)条职位')
pagepageTemp = re.compile(r'共(.*?)页')



def main():
    # str = '%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588'
    # str = parse.unquote(parse.unquote(str))
    # print(str)
    datalist = getData()
    print("爬取完毕！")
    saveDataDB(datalist)
    print("存储完毕")
    pass

#存储数据到excle表格
def saveDataDB(datalist):
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql_key = ""
    sql_value = ""
    try:
        for data in datalist:
            # print(data)
            sql_key = ','.join(data.keys())
            sql_value = '\',\''.join(data.values())
            # # print(key)
            sql = '''insert into job (%s) values ('%s')''' % (sql_key, sql_value)
            # print(data)
            # print(sql)
            # print("------------------------")

            # print(sql_value)
            # sql = '''
            #
            # '''
            cur.execute(sql)
            conn.commit()
            # print("执行了%s" %key)
    except  Exception as e:
        print(e)
        print(data)
    cur.close()
    conn.close()
    #except Exception as e:
        #print(e)
        #pass

#分析每条数据，将有用数据整理出来
def analysisData(link):
    data = {}
    html = ""
    name = ""       #0.工作名字
    linkjob = ""       #1.工作链接
    company = ""       #2.公司名字
    linkcompany = ""       #3.公司链接
    jobplace = ""       #4.工作地点
    salary = ""       #5.工作薪资
    jobdate = ""       #6.发布日期
    experience = ""       #7.工作经验
    education = ""       #8.学历
    information = ""       #9.工作信息

    #分析工作具体网页的信息
    html = askUrl(link)

    #判断访问的页面是否属于51job的
    if html != "":
        linkjob = link

        soup = BeautifulSoup(html,"html.parser")
        try:
            # 工作名字
            name = soup.select(".tHeader.tHjob > .in > .cn > h1")[0]
            name = name.get_text()
            data['name'] = name
            data['linkjob'] = linkjob

            # 工作公司和链接
            company = soup.select(".tHeader.tHjob > .in > .cn > .cname > .catn")[0]
            linkcompany = company["href"]
            company = company["title"]
            data['company'] = company
            data['linkcompany'] = linkcompany

            # 工作习惯信息
            jobmsg = soup.select(".tHeader.tHjob > .in > .cn > .msg")[0]
            jobmsg = jobmsg["title"]
            jobmsg = jobmsg.strip()
            jobmsg1 = re.sub(r'\xa0', '', jobmsg)
            jobmsg = jobmsg1.split("|")

            # 工作地点
            jobplace = jobmsg[0]
            data['jobplace'] = jobplace

            # 工作发布日期
            jobdate = re.findall(findDate, jobmsg1)[0]
            jobdate = str(jobdate[0]) + "/" + str(jobdate[1])
            data['jobdate'] = jobdate

            # 工作学历、经验要求
            for item in jobmsg:
                if item == EXPERIENCE1:
                    experience = EXPERIENCE1
                elif item in EDUCATION:
                    education = item
                else:
                    ex = re.findall(findExperience, item)
                    # print(ex)
                    if ex != []:
                        experience = ex[0] + "经验"
            if education == "":
                education = "无"
            if experience == "":
                experience = "无"
            data['education'] = education
            data['experience'] = experience

            # 工作详细信息
            msg2 = soup.find_all('div', class_='bmsg job_msg inbox')[0]
            m = str(msg2)
            # 筛选出工作基本信息
            m = re.sub(r'<p(.*?)>', '', m)
            m = re.sub(r'</p>', '', m)
            m = re.sub(r'<div>', '', m)
            m = re.sub(r'</div>', '', m)
            m = re.sub(r'<br>', '', m)
            m = re.sub(r'</br>', '', m)
            m = re.sub(r'<br/>', '', m)
            m = re.sub(r'</li>', '', m)
            m = re.sub(r'<li>', '', m)
            m = re.sub(r'<ul>', '', m)
            m = re.sub(r'</ul>', '', m)
            m = re.sub(r'<b(.*?)>', '', m)
            m = re.sub(r'</b>', '', m)
            m = re.sub(r'<i>', '', m)
            m = re.sub(r'</i>', '', m)
            m = re.sub(r'<u>', '', m)
            m = re.sub(r'</u>', '', m)
            m = re.sub(r'<sub>', '', m)
            m = re.sub(r'</sub>', '', m)
            m = re.sub(r'<sup>', '', m)
            m = re.sub(r'</sup>', '', m)
            m = re.sub(r'<b>', '', m)
            m = re.sub(r'</b>', '', m)
            m = re.sub(r'<strike>', '', m)
            m = re.sub(r'</strike>', '', m)
            m = re.sub(r'<ol>', '', m)
            m = re.sub(r'</ol>', '', m)
            m = re.sub(r'<\r>', '', m)
            m = re.sub(r'r', '', m)
            m = re.sub(r'/r', '', m)
            m = re.sub(r'<stong>', '', m)
            m = re.sub(r'</stong>', '', m)
            m = re.sub(r'<span(.*?)>', '', m)
            m = re.sub(r'</span>', '', m)
            m = re.sub(r'<t(.*?)>', '', m)
            m = re.sub(r'</t>', '', m)
            m = re.sub(r'<td>', '', m)
            m = re.sub(r'</td>', '', m)
            m = re.sub(r'\xa0', "", m)
            m = re.sub(r"\n", "", m)
            m = re.sub(r",","，",m)
            # m = re.sub('\(',"（",m)
            # m = re.sub('\)', "）", m)
            # m = re.sub('优先(.*?)6',"",m)
            # m = re.sub(r'<(.*?)>','',m)
            # m = re.sub(r'</(.*?)>','',m)
            m = re.findall(findInformation, m)[0]
            information = m.replace('\r', '')
            information = m.replace('：', '，')
            information = information.strip()
            data['information'] = information
            # print(information)
        except Exception as e:
            print(e)
            print(link)
    else:
        print("访问页面无法编码")
    # print(data)
    # print("---------------")
    return data

#获取51job的数据
def getData():
    datalist = []       #搜索的数据
    html = ''
    page = 1        #数据的页数
    num = 1
    allNum = 0      #数据的总条数
    allpageNum = 0      #数据的总页数
    initpage = "1"
    initurl = "https://search.51job.com/list/080200,000000,0000,00,9,99,Python,2," + initpage + ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
    #url = "https://search.51job.com/list/080200,000000,0000,00,9,99,Python,2," + str(page) + ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="

    #分析页面数据
    html = askUrl(initurl)
    soup = BeautifulSoup(html,"html.parser")

    #总条数
    allNum = soup.select(".dw_table > .dw_tlc > .rt")[0]
    allNum = allNum.get_text()
    allNum = allNum.strip()
    allNum = int(re.findall(numTemp,allNum)[0])
    #print(type(allNum))

    #若总条数不等于0，则开始分析相关数据
    if allNum != 0:
        #总页数
        allpageNum = soup.select(".p_box > .p_wp > .p_in > .td")[0]
        allpageNum = allpageNum.get_text()
        allpageNum = int(re.findall(pagepageTemp,allpageNum)[0])

        #遍历每一页的信息
        for i in range(1,allpageNum+1):
            url = "https://search.51job.com/list/080200,000000,0000,00,9,99,Python,2," + str(i) + ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
            html = askUrl(url)
            soup = BeautifulSoup(html, "html.parser")
            #工作的详细链接
            linkdiv = soup.select(".el > .t1 > span > a")      #返回值是一个包含link所在语句的列表
            page += 1
            #遍历每条信息
            for job in linkdiv:
                #print(link)
                num += 1
                link = job["href"]
                data = analysisData(link)
                #print(data)
                #工作详细界面无法解析
                if data == {}:
                    print("tttttt")
                    comdiv = soup.select(".el > .t2 > a")[0]
                    placediv = soup.select(".el > .t3")[0]
                    sadiv = soup.select(".el > .t4")[0]
                    datediv = soup.select(".el > .t5")[0]
                    data = {'name':job['title'],'linkjob':job['href'],'company':comdiv['title'],'linkcompany':comdiv['href'],'jobplace':placediv.get_text(),'jobdate':datediv.get_text(),'education':'无','experience':'无','information':'详情见官网'}
                datalist.append(data)
                print("爬取进度：%f\%"%(num/allNum))
                pass
            pass
        pass
    #print(datalist)
    return datalist

#访问51job的页面，并将页面返回
def askUrl(url):
    html = ""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    try:
        respones = requests.get(url,headers=headers)
        html = respones.content.decode('GBK')
        #print(html)
    except Exception as e:
        print(e)
        print(url)
    # print(html)
    return html


if __name__ == '__main__':
    main()
