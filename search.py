#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import time
import user_agents
import random
import sys
import os

place_dict = {u'\u660e\u6eaa': u'http://www.weather.com.cn/weather/101230807.shtml', u'\u6f33\u5dde': u'http://www.weather.com.cn/weather/101230601.shtml', u'\u9f13\u697c': u'http://www.weather.com.cn/weather/101230106.shtml', u'\u5b81\u5316': u'http://www.weather.com.cn/weather/101230802.shtml', u'\u5357\u9756': u'http://www.weather.com.cn/weather/101230603.shtml', u'\u601d\u660e': u'http://www.weather.com.cn/weather/101230203.shtml', u'\u6c38\u6cf0': u'http://www.weather.com.cn/weather/101230107.shtml', u'\u8386\u7530': u'http://www.weather.com.cn/weather/101230401.shtml', u'\u8bcf\u5b89': u'http://www.weather.com.cn/weather/101230607.shtml', u'\u6cc9\u6e2f': u'http://www.weather.com.cn/weather/101230514.shtml', u'\u65b0\u7f57': u'http://www.weather.com.cn/weather/101230708.shtml', u'\u8fde\u6c5f': u'http://www.weather.com.cn/weather/101230105.shtml', u'\u57ce\u53a2': u'http://www.weather.com.cn/weather/101230407.shtml', u'\u6e56\u91cc': u'http://www.weather.com.cn/weather/101230205.shtml', u'\u677e\u6eaa': u'http://www.weather.com.cn/weather/101230908.shtml', u'\u6885\u5217': u'http://www.weather.com.cn/weather/101230812.shtml', u'\u5efa\u9633': u'http://www.weather.com.cn/weather/101230907.shtml', u'\u5149\u6cfd': u'http://www.weather.com.cn/weather/101230903.shtml', u'\u4e30\u6cfd': u'http://www.weather.com.cn/weather/101230512.shtml', u'\u5fb7\u5316': u'http://www.weather.com.cn/weather/101230505.shtml', u'\u653f\u548c': u'http://www.weather.com.cn/weather/101230909.shtml', u'\u4e91\u9704': u'http://www.weather.com.cn/weather/101230609.shtml', u'\u9a6c\u5c3e': u'http://www.weather.com.cn/weather/101230113.shtml', u'\u5efa\u74ef': u'http://www.weather.com.cn/weather/101230910.shtml', u'\u6e05\u6d41': u'http://www.weather.com.cn/weather/101230803.shtml', u'\u6c38\u6625': u'http://www.weather.com.cn/weather/101230504.shtml', u'\u53a6\u95e8': u'http://www.weather.com.cn/weather/101230201.shtml', u'\u4ed9\u6e38': u'http://www.weather.com.cn/weather/101230402.shtml', u'\u664b\u5b89': u'http://www.weather.com.cn/weather/101230114.shtml', u'\u540c\u5b89': u'http://www.weather.com.cn/weather/101230202.shtml', u'\u95fd\u6e05': u'http://www.weather.com.cn/weather/101230102.shtml', u'\u5468\u5b81': u'http://www.weather.com.cn/weather/101230305.shtml', u'\u6f33\u6d66': u'http://www.weather.com.cn/weather/101230606.shtml', u'\u971e\u6d66': u'http://www.weather.com.cn/weather/101230303.shtml', u'\u5c06\u4e50': u'http://www.weather.com.cn/weather/101230805.shtml', u'\u9f99\u5ca9': u'http://www.weather.com.cn/weather/101230701.shtml', u'\u6b66\u5e73': u'http://www.weather.com.cn/weather/101230704.shtml', u'\u5357\u5b89': u'http://www.weather.com.cn/weather/101230506.shtml', u'\u4e09\u660e': u'http://www.weather.com.cn/weather/101230801.shtml', u'\u91d1\u95e8': u'http://www.weather.com.cn/weather/101230503.shtml', u'\u987a\u660c': u'http://www.weather.com.cn/weather/101230902.shtml', u'\u67d8\u8363': u'http://www.weather.com.cn/weather/101230307.shtml', u'\u798f\u6e05': u'http://www.weather.com.cn/weather/101230111.shtml', u'\u4e0a\u676d': u'http://www.weather.com.cn/weather/101230705.shtml', u'\u5b89\u6eaa': u'http://www.weather.com.cn/weather/101230502.shtml', u'\u5e73\u6f6d': u'http://www.weather.com.cn/weather/101230108.shtml', u'\u6d77\u6ca7': u'http://www.weather.com.cn/weather/101230204.shtml', u'\u9f99\u6587': u'http://www.weather.com.cn/weather/101230612.shtml', u'\u5ef6\u5e73': u'http://www.weather.com.cn/weather/101230911.shtml', u'\u5e73\u548c': u'http://www.weather.com.cn/weather/101230604.shtml', u'\u95fd\u4faf': u'http://www.weather.com.cn/weather/101230103.shtml', u'\u9ca4\u57ce': u'http://www.weather.com.cn/weather/101230511.shtml', u'\u8354\u57ce': u'http://www.weather.com.cn/weather/101230406.shtml', u'\u6c38\u5b89': u'http://www.weather.com.cn/weather/101230810.shtml', u'\u4e1c\u5c71': u'http://www.weather.com.cn/weather/101230608.shtml', u'\u60e0\u5b89': u'http://www.weather.com.cn/weather/101230508.shtml', u'\u6c38\u5b9a': u'http://www.weather.com.cn/weather/101230706.shtml', u'\u798f\u5dde': u'http://www.weather.com.cn/weather/101230101.shtml', u'\u5357\u5e73': u'http://www.weather.com.cn/weather/101230901.shtml', u'\u79c0\u5c7f': u'http://www.weather.com.cn/weather/101230405.shtml', u'\u6c99\u53bf': u'http://www.weather.com.cn/weather/101230808.shtml', u'\u798f\u9f0e': u'http://www.weather.com.cn/weather/101230308.shtml', u'\u957f\u6cf0': u'http://www.weather.com.cn/weather/101230602.shtml', u'\u6cf0\u5b81': u'http://www.weather.com.cn/weather/101230804.shtml', u'\u8549\u57ce': u'http://www.weather.com.cn/weather/101230310.shtml', u'\u96c6\u7f8e': u'http://www.weather.com.cn/weather/101230206.shtml', u'\u798f\u5b89': u'http://www.weather.com.cn/weather/101230306.shtml', u'\u5c4f\u5357': u'http://www.weather.com.cn/weather/101230309.shtml', u'\u664b\u6c5f': u'http://www.weather.com.cn/weather/101230509.shtml', u'\u6d66\u57ce': u'http://www.weather.com.cn/weather/101230906.shtml', u'\u6db5\u6c5f': u'http://www.weather.com.cn/weather/101230404.shtml', u'\u5927\u7530': u'http://www.weather.com.cn/weather/101230811.shtml', u'\u53f0\u6c5f': u'http://www.weather.com.cn/weather/101230109.shtml', u'\u4e09\u5143': u'http://www.weather.com.cn/weather/101230813.shtml', u'\u53e4\u7530': u'http://www.weather.com.cn/weather/101230302.shtml', u'\u6f33\u5e73': u'http://www.weather.com.cn/weather/101230707.shtml', u'\u90b5\u6b66': u'http://www.weather.com.cn/weather/101230904.shtml', u'\u6b66\u5937\u5c71': u'http://www.weather.com.cn/weather/101230905.shtml', u'\u5bff\u5b81': u'http://www.weather.com.cn/weather/101230304.shtml', u'\u5c24\u6eaa': u'http://www.weather.com.cn/weather/101230809.shtml', u'\u6cc9\u5dde': u'http://www.weather.com.cn/weather/101230501.shtml', u'\u8297\u57ce': u'http://www.weather.com.cn/weather/101230611.shtml', u'\u4ed3\u5c71': u'http://www.weather.com.cn/weather/101230112.shtml', u'\u6d1b\u6c5f': u'http://www.weather.com.cn/weather/101230513.shtml', u'\u8fde\u57ce': u'http://www.weather.com.cn/weather/101230703.shtml', u'\u7f57\u6e90': u'http://www.weather.com.cn/weather/101230104.shtml', u'\u534e\u5b89': u'http://www.weather.com.cn/weather/101230610.shtml', u'\u5efa\u5b81': u'http://www.weather.com.cn/weather/101230806.shtml', u'\u957f\u4e50': u'http://www.weather.com.cn/weather/101230110.shtml', u'\u77f3\u72ee': u'http://www.weather.com.cn/weather/101230510.shtml', u'\u5b81\u5fb7': u'http://www.weather.com.cn/weather/101230301.shtml', u'\u7fd4\u5b89': u'http://www.weather.com.cn/weather/101230207.shtml', u'\u9f99\u6d77': u'http://www.weather.com.cn/weather/101230605.shtml', u'\u957f\u6c40': u'http://www.weather.com.cn/weather/101230702.shtml'}

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

def get_weather(place):
    url = place_dict[place]
    
    page_html = get_htmlsoup(str(url))
    city_list = page_html.find(class_="t clearfix")
    city_list = city_list.find_all('li')
    city_weather = []
    for city in city_list:
        weather = (city.get_text()).strip().replace('\n',' ')
        city_weather.append(weather.replace('   ',''))
    result = '\n'.join(city_weather)
    #print result
    return result

#print get_weather('福州')
