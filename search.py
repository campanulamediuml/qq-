#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import time
import user_agents
import random
import sys
import os

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

def search_info(url):
    page_html = get_htmlsoup(url)
    if page_html == 0:
        result = '网络出错没有找到结果'
    else:
        content = page_html.find(class_="lemma-summary")
        result = content.get_text()
    return result

#print search_info('http://baike.baidu.com/item/福建农林大学')