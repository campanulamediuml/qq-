#coding=utf-8
import sqlite3
conn = sqlite3.connect("qq_bot_database.db")
cu = conn.cursor()

fh = open('Advts.txt','r')
joke_list = fh.readlines()

tmp = []
for i in joke_list:
    tmp.append(i.decode('utf-8'))

# cu.execute("DROP TABLE tips_data")

try:
    cu.execute("create table tips_data (id integer primary key,pid integer UNIQUE ,content text NULL)")
except:
    print 'table exists..'

for line in tmp:
    
    try:
        cu.execute("insert into tips_data (content) values(?)",(line,))
    except Exception,e:
        print line
        print e
        break

    
conn.commit()

