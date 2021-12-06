from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import threading
from queue import Queue
import datetime
import time
import random
import re
import pymysql
from get_wiki_geo.tools.html_paser import html_paser
from get_wiki_geo.tools.MyThreadPool import MyThreadPool

# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# url = "https://baike.hk.xileso.top/wiki/上海中心大厦"
url_pre = "https://baike.hk.xileso.top/wiki/"

# 设置临界区（资源锁）
mylock = threading.RLock()
mylock2 = threading.RLock()

# 打开数据库连接
db_zhwiki = pymysql.connect("localhost", "root", "123456", "zhwiki", charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor_zhwiki = db_zhwiki.cursor()

# 清空数据表
# cursor_urllist.execute('SET foreign_key_checks = 0')
# cursor_urllist.execute('truncate table companies')
# cursor_urllist.execute('SET foreign_key_checks = 1')
# cursor_zhwiki.execute('truncate table entity_category')
# db_zhwiki.commit()

# 测试速度用
return_num = 0
num = 0
save_num = 0

def getLocation (file_num):
    entities = pd.read_csv('data/entity_group/entity_'+str(file_num)+'.csv')
    entity_list = entities['entity']
    return entity_list

class Producer(object):
    @staticmethod
    def producer(q, data):
        q.put(data)

def insertDB(sql_value):
    fp.write(str(sql_value)+'\n')
    fp.flush()
# 构造生产者
def product_data(file_num):
    entity_queue = Queue()
    entity_list = getLocation(file_num)
    for item in entity_list:
        Producer.producer(entity_queue, item)
    return entity_queue

j=0
# 爬取每一个页面
def turn_page_thread(submission):
    url = url_pre+submission
    html = html_paser(url, 'utf-8')
    if html == 0:
        return
    # print(html)
    soup = bs(html, 'html.parser')
    category_box = soup.find(attrs={'id': 'mw-normal-catlinks'})
    if category_box is None:
        return
    categories = category_box.ul.findAll('li')
    if categories is None:
        return
    for item in categories:
        pattern = re.compile('title="Category:(.+)">')
        category = re.findall(pattern, str(item))
        triple = [submission, 'category', category[0]]
        # print(triple)
        Producer.producer(entity_queue, triple)


k = 0
maxsize = 25
for i in range(26,28):
    save_num = 0
    path = "data/entitylist_"+str(i)+".txt"
    f = open(path, "w+", encoding="utf-8")
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    f.close()
    fp = open(path, "a+", encoding="utf-8")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"entity_"+str(i))
    q = product_data(i)
    entity_queue = Queue()
    pool = MyThreadPool()
    pool.addthread(queue=q, size=maxsize, func=turn_page_thread, timeout=15)
    pool.addthread(queue=entity_queue, size=3, func=insertDB, timeout=20)
    pool.startAll()
    pool.joinAll()
    db_zhwiki.commit()
    fp.close()

db_zhwiki.commit()
db_zhwiki.close()
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),save_num, "结束")
