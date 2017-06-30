#coding=utf-8
import logging
import json
import time
import random
import search

file_handle = open('Advts.r','r')
joke_list = file_handle.readlines()
file_handle.close()
logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
knowledge = {}
last1 = ''

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


def main(send_uin, content, root, administrator):
    global last1
    if last1 == str(content) and content != '' and content != ' ':
        return content
    else:
        last1 = content


        if './add_tip' in content:
            global joke_list
            if send_uin in administrator:
                fh = open('Advts.r','a')
                text_inside = (content.split())[1]
                joke_list.append(text_inside)
                fh.write(text_inside)
                fh.close()
                result = '成功写入内容'
            else:
                result = '权限不足，无法写入'
            return result


        elif content == './weather':
            try:
                result = search.get_weather()
                return_info = '接下来七天，福州的天气是：\n'+result
            except:
                return_info = '获取天气信息失败……'
                logging.info(return_info)
            return return_info


        elif './tips' in content:
            try:
                joke_index = content.split()[1]
                logging.info('开始讲笑话了')
                joke = joke_list[joke_index]
            except:
                joke = random.choice(joke_list)
                    
            logging.info("AI REPLY:"+str(joke))
            return joke


        elif content == './shutdown' :
            if send_uin in root:
                result ='主人晚安哦~么么哒~'
                save()
            else:
                result ='不是主人叫我去睡觉！宝宝不去！'
            return result


        elif './explain' in content:
            load()
            answer = '宝宝的知识库里没有这条知识呀'
            for key in knowledge:
                if key in content.split()[1]:
                    answer = random.choice(knowledge[key])
                    logging.info('Group Reply'+str(answer))
                    break
                else:
                    continue
            result = str(answer)
            return result


        elif './search' in content:
            global knowledge
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



        if content == './about':
            try:
                logging.info("output about info")
                info="人家呢~是一个采用麻省理工大学X11协议（MIT协议）的开源学习助手，开发语言是python，作者是菁菁同学（421248329）\n~快向宝宝下命令吧~~使用./explain进行名词解释，允许管理员账号使用./learn功能提交词条，使用./search功能搜索对应的百科词条并保存，如果您学习累了，可以选择./tips命令，宝宝会给您讲笑话哦~"
            except Exception, e:
                logging.error("ERROR"+str(e))
            return info





load()      

