#coding=utf-8
import logging
import json
import time
import random
import search
import re

fh = open('Advts.txt','r')
sleeptime = 0.5
joke_list = fh.readlines()
fh.close()
logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
knowledge = {}
last1 = ''
administrator = []
root = []

def save():
    try:
        fh = open('database.save','w')
        fh.write(json.dumps(knowledge))
        fh.close()
    except Exception, e:
        logging.error("写存档出错："+str(e))

def load():
    global knowledge
    try:
        fh = open('database.save','r')
        saves = fh.read()
        knowledge = json.loads(saves)
        fh.close()
    except Exception, e:
        logging.info("读取存档出错:"+str(e))
        print "读取存档出错:"+str(e)


def main(send_uin, content, root_name, admini):
    global last1
    global knowledge
    global administrator
    global root
    administrator = admini
    root = root_name


    pattern = re.compile(r'^(?:./|./)(learn|delete) {(.+)}{(.+)}')
    match = pattern.match(content)
    if match:
        if match.group(1) == 'learn':
            if send_uin in administrator:
                result = learn(str(match.group(2)).decode('UTF-8'), str(match.group(3)).decode('UTF-8'))
                logging.debug(knowledge)
            else:
                result = random.choice(['人家才不学这些坏坏的知识呢！','宝宝只学主人和她的小伙伴教的知识！'])
        elif match.group(1) == 'delete':
            if send_uin in root:
                result = delete(str(match.group(2)).decode('UTF-8'), str(match.group(3)).decode('UTF-8'))
                logging.debug(knowledge)
            else:
                result = '只有主人能叫宝宝忘掉！╭(╯^╰)╮口亨'
        
    else:
        try:
            result = command(send_uin, content)
        except Exception,e:
            logging.critical(str(e))
    
    return result


def command(send_uin, content):
    global knowledge
    if './add_tip' in content:
        result = add_tip(send_uin,content)
                

    elif content == './weather':
        try:
            result = search.get_weather()
            result = '接下来七天，福州的天气是：\n'+result
        except:
            result = '获取天气信息失败……'
            logging.info(result)


    elif './tips' in content:
        try:
            joke_index = content.split()[1]
            logging.info('开始讲笑话了')
            result = joke_list[int(joke_index)]
        except:
            result = random.choice(joke_list)
                
        logging.info("AI REPLY:"+str(result))


    elif './search' in content:
        result = search_nlg(content)
        return result


    elif content == './about':
        try:
            logging.info("output about info")
            result = "人家呢~是一个采用麻省理工大学X11协议（MIT协议）的开源学习助手，开发语言是python，作者是菁菁同学（421248329）\n~快向宝宝下命令吧~~使用./explain进行名词解释，允许管理员账号使用./learn功能提交词条，使用./search功能搜索对应的百科词条并保存，如果您学习累了，可以选择./tips命令，宝宝会给您讲笑话哦~"
        except Exception, e:
            logging.error("ERROR"+str(e))


    elif content.split()[0] == './root':
        if send_uin in root:
            result = '宝宝为主人执行指令呢~'
        else:
            result = '你是谁！居然妄想操纵主人的电脑！biubiubiu~~'


    elif content == './list':
        result ='指令列表:\n./list\n./check\n./learn\n./delete\n./deleteall\n./tips\n./search\n./explain\n./about\n./shutdown'


    elif content == './checklist':
        if send_uin in root:
            load()
            kng_list = []
            for key in knowledge:
                kng_list.append(key)
            kng = ','.join(kng_list)
            result = '宝宝现在的知识库是：'+kng
        else:
            result = '权限不足呢~宝宝不告诉你'

 
    elif content == './deleteall':
        if send_uin in root:
            try:
                logging.info("Delete all learned data for group")
                result="宝宝经过努力，忘掉这些知识了呢！"
                knowledge = {}
                fh = open('database.save','w')
                fh.close()
                save()
            except Exception, e:
                logging.error("ERROR:"+str(e))
        else:
            result = '宝宝才不会删除这些信息呢！只有主人可以~'
     

    elif content == './check':
        if send_uin in administrator:
            count = 0
            for key in knowledge:
                count += 1
            result = '报告，宝宝学会了'+str(count)+'条知识，快夸我~'
        else:
            result ='只有主人和主人的小伙伴可以看宝宝学了多少知识呢~'


    elif content == './greeting':
        if send_uin in root:
            result = random.choice(['主人~您的宝宝回来惹~','主人~宝宝想你惹','宝宝会为主人尽心尽力服务哦~'])
        else:
            result = random.choice(['死变态你是谁啦，人家不认识你啦！','变态！人家还是宝宝呢！','主人说了，宝宝不能和陌生人说话！'])
        
    elif content == './cleanlog':
        if send_uin in root:
            fh = open('log.log','w')
            print '日志清理结束呀~'
            fh.close()
            result = '日志清理结束呀~'
        else:
            result = '权限不足呢，只有主人才能叫宝宝清理日志~'

    elif './roll' in content:
        result = roll(content) 


    else:
        content = content[2:]
        load()
        answer = '宝宝的知识库里没有这条知识呀'
        for key in knowledge:
            if content in key:
                answer = random.choice(knowledge[key])
                logging.info('Group Reply'+str(answer))
                break
            else:
                continue
        if answer == '宝宝的知识库里没有这条知识呀':
            answer = search_nlg('./search '+content)
        result = str(answer)


    return result


def search_nlg(content):
    global knowledge
    load()
    logging.info('SEARCH:'+content+'\n')
    url = 'http://baike.baidu.com/item/'+content.split()[1]
    key = content.split()[1]
    try:
        answer = (search.search_info(url)).strip()
        try:
            result = answer[:150]+'...'
        except:
            result = answer
        try:
            value = answer[:150]
        except:
            value = answer
    
        if key in knowledge:
            if value not in knowledge[key]:
                knowledge[key].append(value)
            else:
                pass
        else:
            knowledge[key] = [value]
        save()
    except:
        result = '宝宝找不到这个知识呀~'
    return result

def delete(key, value, needreply=True):
    global knowledge
    if key in knowledge and knowledge.count(value):
        knowledge[key].remove(value)
        if needreply:
            result = "人家忘掉 " + str(value) + " 了"
    else:
        if needreply:
            result = "咦~人家不知道你在说什么啦~"
    
    save()
    return result

def learn(key, value, needreply=True):
    global knowledge
    if key in knowledge:
        if value not in knowledge[key]:
            knowledge[key].append(value)
        else:
            pass
    else:
        knowledge[key] = [value]

    if needreply:
        result = ("宝宝学会“" + str(key) + "”了~")    
    save()
    return result

def add_tip(send_uin,content):
    global joke_list
    if './add_tip' in content:
        if send_uin in administrator:
            fh = open('Advts.txt','a')
            text_inside = (content.split())[1]
            joke_list.append(text_inside)
            fh.write(text_inside+'\n')
            fh.close()
            result = '成功写入内容'
        else:
            result = '权限不足，无法写入'
        logging.info(result)
    return result

def roll(content):
    try:
        diceface = int((content.split()[1])[1:])
    except:
        diceface = 20

    if diceface == 0:
        result = '你拿出一颗祖传的克莱因瓶骰子，结果它直接消失在了空气中。'
    elif diceface < 0:
        result = '你尝试丢%d个面的骰子的行为被未来局时空管理处制止了。' % int(diceface)
    elif diceface == 1:
        result = '你发现自己正盯着一个写着阿拉伯数字 1 的莫比乌斯环发呆。'
    elif diceface == 2:
        diceresult = random.randint(0,1)
        result = '你向空中抛出一枚硬币，结果是：%s' % ( u'正面(1)' if diceresult else u'反面(2)' )
    elif diceface <= 1024:
        diceresult = random.randint(1, diceface)
        result = '你丢了一个%d面骰，结果为：%d' % (diceface, diceresult )
        if diceresult <= diceface / 20 or diceresult == 1:
            result += "  …看来您的人品需要充值了呢。"
    else:
        result = '你丢出一个圆滚滚的%d面骰，等到天荒地老这货都没能停下来。' % diceface

    return result


load()      

