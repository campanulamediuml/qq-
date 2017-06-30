#coding=utf-8
import logging

logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')

def method_list(send_uin,content,root,administrator,replyList):
    if aboutme(content):
        return
    if deleteall(send_uin,content):
        return
    if callout(content):
        return
    if tucao(content):
        return
    if repeat(content):
        return
    if search(content):
        return
    if shutdown(send_uin, content):
        return
    if checklength(send_uin,content):
        return
    if greet(send_uin, content):
        return
    if what_can_do(content):
        return
    if cleanlog(send_uin, content):
        return
    if pos(send_uin, content):
        return
    if run_script(send_uin, content):
        return
    if checkknowledge(send_uin, content,):
        return
    if selfcheck(send_uin, content):
        return
    if weather(content):
        return 
    if add_admin(send_uin, content):
        return
    if add_root(send_uin, content):
        return
    if check_admins(send_uin, content):  
        return 
    if add_tips(send_uin, content):   
        return

def run_script(send_uin, content):
    pattern = re.compile(r'^(?:./)(root)(.+)')
    match = pattern.match(content)
    if match:
        if send_uin in root:
            reply('宝宝为主人执行指令呢~')
            
        else:
            reply('你是谁！居然妄想操纵主人的电脑！biubiubiu~~')

    return False

def pos(send_uin, content):
    if content == './宝宝真聪明~':
        if send_uin in root:
            reply('谢谢主人夸奖，宝宝会更努力的！')
        else:
            reply('无事献殷勤，非奸即盗！哼！你是不是对宝宝有什么企图呀！╭(╯^╰)╮')
    return False
def what_can_do(content):
    if content == './list':
        reply('指令列表:\n./list\n./check\n./learn\n./delete\n./deleteall\n./tips\n./search\n./explain\n./about\n./shutdown')
    return False

def shutdown(send_uin, content):

    if content == './shutdown' :
        if send_uin in root:
            reply('主人晚安哦~么么哒~')
            save()
            exit()
        else:
            reply('不是主人叫我去睡觉！宝宝不去！')
    return False

def tucao(content):
    pattern = re.compile(r'^(?:./)(explain)(.+)')
    match = pattern.match(content)
    if match:
        load()
        answer = '宝宝的知识库里没有这条知识呀'
        for key in replyList:
            if key in match.group(2):
                answer = random.choice(replyList[key])
                logging.info('Group Reply'+str(answer))
                break
            else:
                continue
        reply(str(answer))

    return False

def repeat(content):
    if last1 == str(content) and content != '' and content != ' ':
        reply(content)
        return True
    last1 = content

    return False

def save():
    try:
        with open("database.save", "w+") as savefile:
            savefile.write(json.dumps(replyList))
            savefile.close()
    except Exception, e:
        logging.error("写存档出错："+str(e))

def load():
    try:
        with open("database.save", "r") as savefile:
            saves = savefile.read()
            if saves:
                replyList = json.loads(saves)
            savefile.close()
    except Exception, e:
        logging.info("读取存档出错:"+str(e))
        print "读取存档出错:"+str(e)

def checkknowledge(send_uin, content,):
    if content == './checklist':
        if send_uin in root:
            load()
            kng_list = []
            for key in replyList:
                kng_list.append(key)
            kng = ','.join(kng_list)
            reply('宝宝现在的知识库是：'+kng)
        else:
            reply('权限不足呢~宝宝不告诉你')

    return False


def callout(content):
    global joke_list
    if './tips' in content:
        try:
            joke_index = content.split()[1]
            logging.info('开始讲笑话了')
            joke = joke_list[int(joke_index)]
        except:
            joke = random.choice(joke_list)
                
        logging.info("AI REPLY:"+str(joke))
        print "AI REPLY:"+str(joke)
        reply(joke)

    return False

def search(content):
    pattern = re.compile(r'^(?:./)(search) (.+)')
    match = pattern.match(content)
    if match:
        logging.info('SEARCH:'+content+'\n')
        url = 'http://baike.baidu.com/item/'+match.group(2)
        key = match.group(2)
        try:
            answer = (search.search_info(url)).strip()
            try:
                reply(answer[:150]+'...')
            except:
                reply(answer)
            try:
                value = answer[:150]
            except:
                value = answer
            
            if key in replyList:
                if value not in replyList[key]:
                    replyList[key].append(value)
                else:
                    pass
            else:
                replyList[key] = [value]
            save()
        except:
            reply('宝宝找不到这个知识呀~')
    return False


def aboutme(content):
    pattern = re.compile(r'^(?:./|./)(about)')
    match = pattern.match(content)
    try:
        if match:
            logging.info("output about info")
            info="人家呢~是一个采用麻省理工大学X11协议（MIT协议）的开源学习助手，开发语言是python，作者是菁菁同学（421248329）\n~快向宝宝下命令吧~~使用./explain进行名词解释，允许管理员账号使用./learn功能提交词条，使用./search功能搜索对应的百科词条并保存，如果您学习累了，可以选择./tips命令，宝宝会给您讲笑话哦~"
            reply(info)
            return True
    except Exception, e:
        logging.error("ERROR"+str(e))
    return False


def deleteall(send_uin, content):

    pattern = re.compile(r'^(?:./|./)(deleteall)')
    match = pattern.match(content)
    
    if match:

        if send_uin in root:
            try:
                logging.info("Delete all learned data for group:"+str(gid))
                info="宝宝经过努力，忘掉这些知识了呢！"
                replyList.clear()
                save()
                reply(info)
                return True
            except Exception, e:
                logging.error("ERROR:"+str(e))
        else:
            reply('宝宝才不会删除这些信息呢！只有主人可以~')
    
    
    return False

def checklength(send_uin, content):

    if content == './check':
        if send_uin in administrator:
            count = 0
            for key in replyList:
                count += 1
            reply('报告，宝宝学会了'+str(count)+'条知识，快夸我~')
        else:
            reply('只有主人和主人的小伙伴可以看宝宝学了多少知识呢~')
    return False

def greet(send_uin, content):
    if content == './greeting':
        if send_uin in root:
            reply(random.choice(['主人~您的宝宝回来惹~','主人~宝宝想你惹','宝宝会为主人尽心尽力服务哦~']))
        else:
            reply(random.choice(['死变态你是谁啦，人家不认识你啦！','变态！人家还是宝宝呢！','主人说了，宝宝不能和陌生人说话！']))
    return False

def cleanlog(send_uin, content):
    if content == './cleanlog':
        if send_uin in root:
            fh = open('log.log','w')
            print '日志清理结束呀~'
            fh.close()
            reply('日志清理结束呀~')
        else:
            reply('权限不足呢，只有主人才能叫宝宝清理日志~')
    return False

def selfcheck(send_uin, content):
    if content == './selfcheck':
        if send_uin in administrator:
            time_now = time.time()
            run_time = str(int(time_now - start))
            mem = psutil.virtual_memory()
            mem_per = str((float(mem.free)/float(mem.total))*100)+' %'
            cpu = str(psutil.cpu_percent())+' %'
            py_info = platform.python_version()
            plat_info = platform.platform()
            cpu_plt = (platform.uname())[-2]
            answer = '运行报告概览：\n运行时间:\n'+run_time+'秒\ncpu负载:\n'+cpu+'\n内存负载:\n'+str(mem_per)+'\npython版本:\n'+str(py_info)+'\n运行环境:\n'+str(plat_info)+'\nCPU架构:\n'+str(cpu_plt)
            reply(answer)
        else:
            reply('权限不足')
    return False


def weather(content):
    if content == './weather':
        try:
            result = search.get_weather()
            reply('接下来七天，福州的天气是：\n'+result)
        except:
            logging.info('获取天气信息失败……')
    return False

def add_admin(send_uin, content):
    if './add_admin' in content:
        if send_uin in root:
            try:
                administrator.append(int(content.split()[1]))
                reply('添加'+str((content.split())[1])+'管理员成功！')
            except:
                logging.info('添加'+str((content.split())[1])+'失败')
                reply('添加失败，详情请查看日志')
        else:
            reply('权限不足')

    return False

def add_root(send_uin, content):
    if './add_root' in content:
        if send_uin in root:
            try:
                root.append(int(content.split()[1]))
                administrator.append(int(content.split()[1]))
                reply('添加'+str((content.split())[1])+'root权限成功！')
            except:
                logging.info('添加'+str((content.split())[1])+'失败')
                reply('添加失败，详情请查看日志')
        else:
            reply('权限不足')

    return False

def check_admins(send_uin, content):
    global administrator
    if content == './check_admins':
        if send_uin in administrator:
            administrator = list(set(administrator))
            answer = str(administrator)
            reply('现在管理员账号列表为：'+answer)
        else:
            reply('权限不足')

    return False

def add_tips(send_uin, content):
    global joke_list
    global administrator
    if './add_tip' in content:
        if send_uin in administrator:
            fh = open('Advts.r','a')
            text_inside = (content.split())[1]
            joke_list.append(text_inside)
            fh.write(text_inside)
            fh.close()
            reply('成功写入内容')
        else:
            reply('权限不足，无法写入')

    return False
