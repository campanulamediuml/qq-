#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import time
import user_agents
import random

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


soup = get_htmlsoup('http://fj.weather.com.cn/')
place_list = soup.find(class_="navbox")
place_list = place_list.find('span')
place_list = place_list.find_all('a')

city_dict = {}

for i in place_list:
    try:
        url = 'http://fj.weather.com.cn'+i['href']
        soup = get_htmlsoup(url)
        places = soup.find(id="forecastID")
        city_list = places.find_all('dt')
        for city in city_list:
            city_url = city.find('a')['href']
            city_name = city.get_text()
            city_dict[city_name.strip()] = city_url
    except:
        continue

print city_dict

