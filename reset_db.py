#coding=utf-8
import sqlite3
import jieba

conn = sqlite3.connect("qq_bot_database.db")
cu = conn.cursor()
cu.execute('SELECT * FROM learn_data')
results = cu.fetchall()

print len(results)

dict_main = []
for i in results:
    tmp = []
    for j in i:
        tmp.append(j)
    dict_main.append(tmp)

db_key = []
for i in results:
    db_key.append(i[2:])

db_key = list(set(db_key))

final_result = []
for i in dict_main:
    tmp = []
    item_list = jieba.cut(i[2])
    item_list = ','.join(item_list).split(',')
    for item in item_list:
        tmp.append((item,i[-1]))


    final_result.extend(tmp)

final_result = list(set(final_result))

for line in final_result:
    if line not in db_key:
        cu.execute('INSERT INTO learn_data(name,content) VALUES(?,?)',line)
conn.commit()

cu.execute('SELECT * FROM learn_data')
results = cu.fetchall()

print len(results)






