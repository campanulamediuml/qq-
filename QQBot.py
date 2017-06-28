# -*- coding: utf-8 -*-
import re
import random
import json
import os
import sys
import datetime
import time
import threading
import logging
import urllib
from HttpClient import HttpClient
import search
import config

reload(sys)
sys.setdefaultencoding("utf-8")

HttpClient_Ist = HttpClient()

ClientID = 53999199
PTWebQQ = ''
APPID = 0
msgId = 0
ThreadList = []
GroupThreadList = []
GroupWatchList = []
GroupNameList = {}
GroupCodeList = {}
PSessionID = ''
Referer = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
httpsReferer = 'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1'
SmartQQUrl = 'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001'
VFWebQQ = ''
AdminQQ = '0'
MyUIN = ''


initTime = time.time()

logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

# -----------------
# 方法声明
# -----------------


def pass_time():
    global initTime
    rs = (time.time() - initTime)
    initTime = time.time()
    return str(round(rs, 3))

def get_ts():
    ts = time.time()
    while ts < 1000000000000:
        ts = ts * 10
    ts = int(ts)
    return ts

def CProcess(content):
    return str(content.replace("\\", r"\\").replace("\n", r"\n").replace("\r", r"\r").replace("\t", r"\t").replace('"', r'\"'))

def getQRtoken(qrsig):
    e = 0
    for i in qrsig:
        e += (e << 5) + ord(i)
    return 2147483647 & e;

#Encryption Algorithm Used By QQ
def gethash(selfuin, ptwebqq):
    selfuin += ""
    N=[0,0,0,0]
    for T in range(len(ptwebqq)):
        N[T%4]=N[T%4]^ord(ptwebqq[T])
    U=["EC","OK"]
    V=[0, 0, 0, 0]
    V[0]=int(selfuin) >> 24 & 255 ^ ord(U[0][0])
    V[1]=int(selfuin) >> 16 & 255 ^ ord(U[0][1])
    V[2]=int(selfuin) >>  8 & 255 ^ ord(U[1][0])
    V[3]=int(selfuin)       & 255 ^ ord(U[1][1])
    U=[0,0,0,0,0,0,0,0]
    U[0]=N[0]
    U[1]=V[0]
    U[2]=N[1]
    U[3]=V[1]
    U[4]=N[2]
    U[5]=V[2]
    U[6]=N[3]
    U[7]=V[3]
    N=["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    V=""
    for T in range(len(U)):
        V+= N[ U[T]>>4 & 15]
        V+= N[ U[T]    & 15]
    return V

def getReValue(html, rex, er, ex):
    v = re.search(rex, html)

    if v is None:
        logging.error(er)

        if ex:
            raise Exception, er
        return ''

    return v.group(1)


def date_to_millis(d):
    return int(time.mktime(d.timetuple())) * 1000


def msg_handler(msgObj):
    for msg in msgObj:
        msgType = msg['poll_type']

        # QQ私聊消息
        if msgType == 'message' or msgType == 'sess_message':  # 私聊 or 临时对话
            txt = combine_msg(msg['value']['content'])
            tuin = msg['value']['from_uin']
            msg_id = msg['value']['msg_id']

            # print "{0}:{1}".format(from_account, txt)
            targetThread = thread_exist(tuin)
            if targetThread:
                targetThread.push(txt, msg_id)
            else:
                try:
                    service_type = 0
                    isSess = 0
                    group_sig = ''
                    if msgType == 'sess_message':
                        isSess = 1
                        service_type = msg['value']['service_type']
                        myid = msg['value']['id']
                        info = json.loads(HttpClient_Ist.Get('http://d1.web2.qq.com/channel/get_c2cmsg_sig2?id={0}&to_uin={1}&clientid={2}&psessionid={3}&service_type={4}&t={5}'.format(myid, tuin, ClientID, PSessionID, service_type, get_ts()), Referer))
                        logging.info("Get group sig:" + str(info))
                        if info['retcode'] != 0:
                            raise ValueError, info
                        info = info['result']
                        group_sig = info['value']
                    tmpThread = pmchat_thread(tuin,isSess,group_sig,service_type)
                    tmpThread.start()
                    ThreadList.append(tmpThread)
                    tmpThread.push(txt,msg_id)
                except Exception, e:
                    logging.info("error"+str(e))

            # print "{0}:{1}".format(self.FriendList.get(tuin, 0), txt)

            # if FriendList.get(tuin, 0) == AdminQQ:#如果消息的发送者与AdminQQ不相同, 则忽略本条消息不往下继续执行
            #     if txt[0] == '#':
            #         thread.start_new_thread(self.runCommand, (tuin, txt[1:].strip(), msgId))
            #         msgId += 1

            # if txt[0:4] == 'exit':
            #     logging.info(self.Get('http://d1.web2.qq.com/channel/logout2?ids=&clientid={0}&psessionid={1}'.format(self.ClientID, self.PSessionID), Referer))
            #     exit(0)

        # 群消息
        if msgType == 'group_message':
            global GroupWatchList
            txt = combine_msg(msg['value']['content'])
            guin = msg['value']['from_uin']
            gid = GroupCodeList[int(guin)]
            tuin = msg['value']['send_uin']
            seq = msg['value']['msg_id']
            if str(guin) in GroupWatchList:
                g_exist = group_thread_exist(gid)
                if g_exist:
                    g_exist.handle(tuin, txt, seq)
                else:
                    tmpThread = group_thread(guin, gid)
                    tmpThread.start()
                    GroupThreadList.append(tmpThread)
                    tmpThread.handle(tuin, txt, seq)
                    logging.info("群线程已生成")
            else:
                logging.info(str(gid) + "群有动态，但是没有被监控")

        # QQ号在另一个地方登陆, 被挤下线
        if msgType == 'kick_message':
            logging.error(msg['value']['reason'])
            raise Exception, msg['value']['reason']  # 抛出异常, 重新启动WebQQ, 需重新扫描QRCode来完成登陆


def combine_msg(content):
    msgTXT = ""
    for part in content:
        # print type(part)
        if type(part) == type(u'\u0000'):
            msgTXT += part
        elif len(part) > 1:
            # 如果是图片
            if str(part[0]) == "offpic" or str(part[0]) == "cface":
                msgTXT += "[图片]"

    return msgTXT


def send_msg(tuin, content, isSess, group_sig, service_type):
    if isSess == 0:
        reqURL = "https://d1.web2.qq.com/channel/send_buddy_msg2"
        data = (
            ('r', '{{"to":{0}, "face":594, "content":"[\\"{4}\\", [\\"font\\", {{\\"name\\":\\"Arial\\", \\"size\\":\\"10\\", \\"style\\":[0, 0, 0], \\"color\\":\\"000000\\"}}]]", "clientid":{1}, "msg_id":{2}, "psessionid":"{3}"}}'.format(tuin, ClientID, msgId, PSessionID, CProcess(content))),
            ('clientid', ClientID),
            ('psessionid', PSessionID)
        )
        rsp = HttpClient_Ist.Post(reqURL, data, httpsReferer)
        rspp = json.loads(rsp)
        if rspp['errCode']!= 0:
            logging.error("reply pmchat error"+str(rspp['errCode']))
    else:
        reqURL = "https://d1.web2.qq.com/channel/send_sess_msg2"
        data = (
            ('r', '{{"to":{0}, "face":594, "content":"[\\"{4}\\", [\\"font\\", {{\\"name\\":\\"Arial\\", \\"size\\":\\"10\\", \\"style\\":[0, 0, 0], \\"color\\":\\"000000\\"}}]]", "clientid":{1}, "msg_id":{2}, "psessionid":"{3}", "group_sig":"{5}", "service_type":{6}}}'.format(tuin, ClientID, msgId, PSessionID, CProcess(content), group_sig, service_type)),
            ('clientid', ClientID),
            ('psessionid', PSessionID),
            ('group_sig', group_sig),
            ('service_type',service_type)
        )
        rsp = HttpClient_Ist.Post(reqURL, data, httpsReferer)
        rspp = json.loads(rsp)
        if rspp['errCode']!= 0:
            logging.error("reply temp pmchat error"+str(rspp['errCode']))

    return rsp


def thread_exist(tuin):
    for t in ThreadList:
        if t.isAlive():
            if t.tuin == tuin:
                t.check()
                return t
        else:
            ThreadList.remove(t)
    return False


def group_thread_exist(gid):
    for t in GroupThreadList:
        if str(t.gid) == str(gid):
            return t
    return False

# -----------------
# 类声明
# -----------------


class Login(HttpClient):
    MaxTryTime = 5

    def __init__(self, vpath, qq=0):
        global APPID, AdminQQ, PTWebQQ, VFWebQQ, PSessionID, msgId, MyUIN, GroupNameList, tmpUserName, GroupCodeList
        self.VPath = vpath  # QRCode保存路径
        AdminQQ = int(qq)
        logging.critical("正在获取登陆页面")
        self.Get('http://w.qq.com/')
        html = self.Get(SmartQQUrl,'http://w.qq.com/')
        logging.critical("正在获取appid")
        APPID = getReValue(html, r'<input type="hidden" name="aid" value="(\d+)" />', 'Get AppId Error', 1)
        logging.critical("正在获取login_sig")
        sign = getReValue(html, r'g_login_sig\s*=\s*encodeURIComponent\s*\("(.*?)"\)', 'Get Login Sign Error', 0)
        logging.info('get sign : %s', sign)
        logging.critical("正在获取pt_version")
        JsVer = getReValue(html, r'g_pt_version\s*=\s*encodeURIComponent\s*\("(\d+)"\)', 'Get g_pt_version Error', 1)
        logging.info('get g_pt_version : %s', JsVer)
        logging.critical("正在获取mibao_css")
        MiBaoCss = getReValue(html, r'g_mibao_css\s*=\s*encodeURIComponent\s*\("(.*?)"\)', 'Get g_mibao_css Error', 1)
        logging.info('get g_mibao_css : %s', sign)
        StarTime = date_to_millis(datetime.datetime.utcnow())
        T = 0
        while True:
            T = T + 1
            self.Download('https://ssl.ptlogin2.qq.com/ptqrshow?appid={0}&e=0&l=M&s=5&d=72&v=4&t=0.0836106{1}4250{2}6653'.format(APPID,random.randint(0,9),random.randint(0,9)), self.VPath)

            logging.info('[{0}] Get QRCode Picture Success.'.format(T))

            QRSig = self.getCookie('qrsig')
            while True:
                html = self.Get('https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken={0}&webqq_type=10&remember_uin=1&login2qq=1&aid={1}&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-{2}&mibao_css={3}&t=1&g=1&js_type=0&js_ver={4}&login_sig={5}&pt_randsalt=2'.format(getQRtoken(QRSig),APPID, date_to_millis(datetime.datetime.utcnow()) - StarTime, MiBaoCss, JsVer, sign),
                        SmartQQUrl)
                # logging.info(html)
                ret = html.split("'")
                if ret[1] == '65' or ret[1] == '0':  # 65: QRCode 失效, 0: 验证成功, 66: 未失效, 67: 验证中
                    break
                time.sleep(2)
            if ret[1] == '0' or T > self.MaxTryTime:
                break

        logging.info(ret)
        if ret[1] != '0':
            raise ValueError, "RetCode = "+ret['retcode']
            return
        logging.critical("二维码已扫描，正在登陆")
        pass_time()
        # 删除QRCode文件
        if os.path.exists(self.VPath):
            os.remove(self.VPath)

        # 记录登陆账号的昵称
        tmpUserName = ret[11]

        html = self.Get(ret[5])
        url = getReValue(html, r' src="(.+?)"', 'Get mibao_res Url Error.', 0)
        if url != '':
            html = self.Get(url.replace('&amp;', '&'))
            url = getReValue(html, r'location\.href="(.+?)"', 'Get Redirect Url Error', 1)
            html = self.Get(url)

        PTWebQQ = self.getCookie('ptwebqq')

        logging.info('PTWebQQ: {0}'.format(PTWebQQ))

        LoginError = 3
        while LoginError > 0:
            try:
                html = self.Post('http://d1.web2.qq.com/channel/login2', {
                    'r': '{{"ptwebqq":"{0}","clientid":{1},"psessionid":"{2}","status":"online"}}'.format(PTWebQQ, ClientID, PSessionID)
                }, 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2')
                ret = json.loads(html)
                html2 = self.Get("http://s.web2.qq.com/api/getvfwebqq?ptwebqq={0}&clientid={1}&psessionid={2}&t={3}".format(PTWebQQ, ClientID, PSessionID, get_ts()), Referer)
                logging.info("getvfwebqq html:  " + str(html2))
                ret2 = json.loads(html2)
                LoginError = 0
            except:
                LoginError -= 1
                logging.critical("登录失败，正在重试")

        if ret['retcode'] != 0 or ret2['retcode'] != 0:
            raise ValueError, "Login Retcode="+str(ret['retcode'])
            return

        VFWebQQ = ret2['result']['vfwebqq']
        PSessionID = ret['result']['psessionid']
        MyUIN = ret['result']['uin']
        logging.critical("QQ号：{0} 登陆成功, 用户名：{1}".format(ret['result']['uin'], tmpUserName))
        logging.info('Login success')
        logging.critical("登陆二维码用时" + pass_time() + "秒")

        msgId = int(random.uniform(20000, 50000))
        html = self.Post('http://s.web2.qq.com/api/get_group_name_list_mask2', {
                'r': '{{"vfwebqq":"{0}","hash":"{1}"}}'.format(str(VFWebQQ),gethash(str(MyUIN),str(PTWebQQ)))
            }, Referer)
        ret = json.loads(html)
        if ret['retcode']!= 0:
            raise ValueError, "retcode error when getting group list: retcode="+str(ret['retcode'])
        for t in ret['result']['gnamelist']:
            GroupNameList[str(t["name"])]=t["gid"]
            GroupCodeList[int(t["gid"])]=int(t["code"])
        self.Get('http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq={0}&clientid={1}&psessionid={2}&t={3}'.format(VFWebQQ,ClientID,PSessionID,get_ts()),Referer)

class check_msg(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global PTWebQQ
        E = 0
        # 心跳包轮询
        while 1:
            if E > 5:
                break
            try:
                ret = self.check()
            except:
                E += 1
                continue
            # logging.info(ret)

            # 返回数据有误
            if ret == "":
                E += 1
                continue

            # POST数据有误
            if ret['retcode'] == 100006:
                break

            # 无消息
            if ret['retcode'] == 102:
                E = 0
                continue

            # 更新PTWebQQ值
            if ret['retcode'] == 116:
                PTWebQQ = ret['p']
                E = 0
                continue

            if ret['retcode'] == 0:
                # 信息分发
                if 'result' in ret:
                    msg_handler(ret['result'])
                E = 0
                continue

            # Other retcode e.g.: 103
            E += 1
            HttpClient_Ist.Get('http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq={0}&clientid={1}&psessionid={2}&t={3}'.format(VFWebQQ,ClientID,PSessionID,get_ts()),Referer)

        logging.critical("轮询错误超过五次")

    # 向服务器查询新消息
    def check(self):

        html = HttpClient_Ist.Post('https://d1.web2.qq.com/channel/poll2', {
            'r': '{{"ptwebqq":"{1}","clientid":{2},"psessionid":"{0}","key":""}}'.format(PSessionID, PTWebQQ, ClientID)
        }, httpsReferer)
        logging.info("Check html: " + str(html))
        print str(html)

        try:
            ret = json.loads(html)
        except Exception as e:
            logging.error(str(e))
            logging.critical("Check error occured, retrying.")
            return self.check()

        return ret
class group_thread(threading.Thread):
    last1 = ''
    lastseq = 0
    replyList = {}
    followList = []
    NickList = {}

    # 属性
    repeatPicture = True

    def __init__(self, guin, gcode):
        threading.Thread.__init__(self)
        self.guin = guin
        self.gid = gcode
        self.load()
        self.lastreplytime=0
        ret = HttpClient_Ist.Get('http://s.web2.qq.com/api/get_group_info_ext2?gcode={0}&vfwebqq={1}&t={2}'.format(gcode,VFWebQQ,get_ts()),Referer)
        ret = json.loads(ret)
        for t in ret['result']['minfo']:
            self.NickList[str(t["nick"])]=int(t["uin"])

    def learn(self, key, value, needreply=True):
            if key in self.replyList:
                self.replyList[key].append(value)
            else:
                self.replyList[key] = [value]

            if needreply:
                self.reply("学习内容：“" + str(key) + "”成功")
                self.save()

    def delete(self, key, value, needreply=True):
        if key in self.replyList and self.replyList[key].count(value):
            self.replyList[key].remove(value)
            if needreply:
                self.reply("我已经不会说" + str(value) + "了")
                self.save()

        else:
            if needreply:
                self.reply("没找到你说的那句话哦")

    def reply(self, content):
        if time.time() - self.lastreplytime < 3.0:
            logging.info("REPLY TOO FAST, ABANDON："+content)
            return False
        self.lastreplytime = time.time()
        reqURL = "https://d1.web2.qq.com/channel/send_qun_msg2"
        data = (
            ('r', '{{"group_uin":{0}, "face":564,"content":"[\\"{4}\\",[\\"font\\",{{\\"name\\":\\"Arial\\",\\"size\\":\\"10\\",\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}}]]","clientid":{1},"msg_id":{2},"psessionid":"{3}"}}'.format(self.guin, ClientID, msgId, PSessionID, CProcess(content))),
            ('clientid', ClientID),
            ('psessionid', PSessionID)
        )
        logging.info("Reply package: " + str(data))
        rsp = HttpClient_Ist.Post(reqURL, data, httpsReferer)
        try:
            rspp = json.loads(rsp)
            if rspp['errCode'] == 0:
                logging.info("[Reply to group " + str(self.gid) + "]:" + str(content))
                print "[Reply to group " + str(self.gid) + "]:" + str(content)
                return True
        except:
            pass
        logging.error("[Fail to reply group " + str(self.gid)+ "]:" + str(rsp))
        return rsp

    def handle(self, send_uin, content, seq):
        # 避免重复处理相同信息
        if seq != self.lastseq:
            pattern = re.compile(r'^(?:./|./)(learn|delete) {(.+)}{(.+)}')
            match = pattern.match(content)
            if match:
                if match.group(1) == 'learn':
                    if send_uin in config.administrator:
                        self.learn(str(match.group(2)).decode('UTF-8'), str(match.group(3)).decode('UTF-8'))
                        logging.debug(self.replyList)
                    else:
                        self.reply('只有管理员和超级管管理员可以添加内容')
                if match.group(1) == 'delete':
                    if send_uin in config.root:
                        self.delete(str(match.group(2)).decode('UTF-8'), str(match.group(3)).decode('UTF-8'))
                        logging.debug(self.replyList)
                    else:
                        self.reply('权限不足哦，只有root账号可以删除内容')

            else:
                if self.aboutme(content):
                    return
                if self.deleteall(send_uin,content):
                    return
                if self.callout(content):
                    return
                if self.tucao(content):
                    return
                if self.repeat(content):
                    return
                if self.search(content):
                    return
                if self.shutdown(send_uin, content):
                    return
                if self.checklength(send_uin,content):
                    return
                if self.greet(send_uin, content):
                    return
                if self.what_can_do(content):
                    return
                if self.cleanlog(send_uin, content):
                    return
                

        else:
            logging.warning("message seq repeat detected.")
        self.lastseq = seq
    def what_can_do(self, content):
        if content == './list':
            self.reply('指令列表：./list  ./check  ./learn  ./delete  ./deleteall  ./tips  ./search  ./explain  ./about  ./shutdown')
        return False

    def shutdown(self, send_uin, content):

        if content == './shutdown' :
            if send_uin in root:
                self.reply('日志已保存，关机中...')
                time.sleep(1)
                self.reply('进程结束，退出成功')
                exit()
            else:
                self.reply('权限不足，只有root账号可以关闭该机器人')

        return False


    def tucao(self, content):
        pattern = re.compile(r'^(?:./)(explain)(.+)')
        match = pattern.match(content)
        if match:
            for key in self.replyList:
                if str(key) in match.group(2) and self.replyList[key]:
                    rd = random.randint(0, len(self.replyList[key]) - 1)
                    self.reply(self.replyList[key][rd])
                    logging.info('Group Reply'+str(self.replyList[key][rd]))
                    return True
            return False

    def repeat(self, content):
        if self.last1 == str(content) and content != '' and content != ' ':
            self.reply(content)
            return True
        self.last1 = content

        return False

    def save(self):

        try:
            with open("database.save", "w+") as savefile:
                savefile.write(json.dumps(self.replyList))
                savefile.close()
        except Exception, e:
            logging.error("写存档出错："+str(e))
    def load(self):
        try:
            with open("database.save", "r") as savefile:
                saves = savefile.read()
                if saves:
                    self.replyList = json.loads(saves)
                savefile.close()
        except Exception, e:
            logging.info("读取存档出错:"+str(e))
            print "读取存档出错:"+str(e)

    def callout(self, content):
        if './tips' in content:
            fh = open('Advts.r','r')
            joke_list = fh.readlines()
            joke = random.choice(joke_list)
            try:
                joke_index = content.split()[1]
                logging.info('开始讲笑话了')
                joke = joke_list[joke_index]
            except:
                joke = random.choice(joke_list)
                    
            logging.info("AI REPLY:"+str(joke))
            print "AI REPLY:"+str(joke)
            self.reply(joke)
            fh.close()

        return False

    def search(self, content):
        pattern = re.compile(r'^(?:./)(search) (.+)')
        match = pattern.match(content)
        if match:
            logging.info('SEARCH:'+content+'\n')
            url = 'http://baike.baidu.com/item/'+match.group(2)
            key = match.group(2)
            try:
                answer = (search.search_info(url)).strip()
                try:
                    self.reply(answer[:150]+'...')
                except:
                    self.reply(answer)
                try:
                    value = answer[:150]
                except:
                    value = answer
                
                if key in self.replyList:
                    self.replyList[key].append(value)
                else:
                    self.replyList[key] = [value]


                self.save()
            except:
                self.reply('妈呀我被打入未知领域了……')
        return False


    def aboutme(self, content):
        pattern = re.compile(r'^(?:./|./)(about)')
        match = pattern.match(content)
        try:
            if match:
                logging.info("output about info")
                info="这是一个开源的python学习助手,使用./explain进行名词解释，允许管理员账号使用./learn功能提交词条，使用./search功能搜索对应的百科词条并保存，如果你学习累了，可以选择./tips命令，让它讲个段子"
                self.reply(info)
                return True
        except Exception, e:
            logging.error("ERROR"+str(e))
        return False


    def deleteall(self, send_uin, content):
    
        pattern = re.compile(r'^(?:./|./)(deleteall)')
        match = pattern.match(content)
        
        if match:

            if send_uin in config.root:
                try:
                    logging.info("Delete all learned data for group:"+str(self.gid))
                    info="已删除所有学习内容"
                    self.replyList.clear()
                    self.save()
                    self.reply(info)
                    return True
                except Exception, e:
                    logging.error("ERROR:"+str(e))
            else:
                self.reply('权限不足，只有root可以删除信息')
        
        
        return False

    def checklength(self, send_uin, content):

        if content == './check':
            if send_uin in config.administrator:
                count = 0
                for key in self.replyList:
                    count += 1
                self.reply('报告，目前总计学习了'+str(count)+'条知识')
            else:
                self.reply('权限不足，只有管理员以上权限可以查看学习情况')
        return False

    def greet(self, send_uin, content):
        if content == './greeting':
            if send_uin in config.root:
                self.reply('主人~您的宝宝回来惹~')
            else:
                self.reply('死变态你是谁啦快滚开！')
        return False

    def cleanlog(self, send_uin, content):
        if content == './cleanlog':
            if send_uin in config.root:
                fh = open('log.log','w')
                print '日志清理结束'
                fh.close()
                self.reply('日志清理完毕')
            else:
                self.reply('权限不足，该操作仅限root用户')
        return False

if __name__ == "__main__":
    vpath = './v.png'
    qq = 0
    if len(sys.argv) > 1:
        vpath = sys.argv[1]
    if len(sys.argv) > 2:
        qq = sys.argv[2]

    try:
        pass_time()
        qqLogin = Login(vpath, qq)
    except Exception, e:
        logging.critical(str(e))
        os._exit(1)
    t_check = check_msg()
    t_check.setDaemon(True)
    t_check.start()
    try:
        with open('groupfollow.txt','r') as f:
            for line in f:
                tmp = line.strip('\n').strip('\r')
                if str(tmp) in GroupNameList:
                    GroupWatchList.append(str(GroupNameList[str(tmp)]))
                    logging.info("关注:"+str(tmp))
                else:
                    logging.error("无法找到群："+str(tmp))
    except Exception, e:
        logging.error("读取组存档出错:"+str(e))


    t_check.join()
