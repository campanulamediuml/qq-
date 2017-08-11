#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import time
import user_agents
import random
import sys
import os
from multiprocessing.dummy import Pool as ThreadPool 

def get_htmlsoup(site):
    randomarry = random.choice(user_agents.user_agent_list)
#随机挑选一个user_agent文件头
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6',
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent':randomarry
    }
#手动添加完整一套文件头，假装是不同的浏览器进行访问
    data = None
    requests = urllib2.Request(site,data,headers)
    try:
        response = urllib2.urlopen(requests,timeout=30)
        site_page = response.read()
        soup = BeautifulSoup(site_page, 'html.parser')
    except urllib2.HTTPError,e:
        if e.code == 404:
            soup = 0
    return soup


def get_name_url(html):
    name_list = html.find(class_="bookcont").find_all('a')
    url_list = []
    for name in name_list:
        url = name['href']
        url_list.append('http://so.gushiwen.org/'+url)
    return url_list


def get_content(url):
    html = get_htmlsoup(url)
    content = html.find(class_="contson")
    content = str(content)[21:-6].strip().split('<br/>')[2:]
    return content
        


page_html = get_htmlsoup('http://so.gushiwen.org/guwen/book_6.aspx')
url_list = get_name_url(page_html)




pool = ThreadPool(20)
result_list = pool.map(get_content,url_list)
result = []

for i in result_list:
    result.extend(i)
fh = open('name.txt','w')
for i in result:
    fh.write(str(i))
    fh.write('\n')  

    
