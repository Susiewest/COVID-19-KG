from bs4 import BeautifulSoup as bs
import pandas as pd
from queue import Queue
import datetime
import re
from get_wiki_geo.tools.html_paser import html_paser
from get_wiki_geo.tools.MyThreadPool import MyThreadPool

def getLocation (file_num):
    entities = pd.read_csv('data/entity_group/entity_'+str(file_num)+'.csv')
    entity_list = entities['entity']
    return entity_list

class Producer(object):
    @staticmethod
    def producer(q, data):
        q.put(data)

def insertDB(sql_value):
    global save_num
    fp.write(str(sql_value)+'\n')
    fp.flush()

# 构造生产者
def product_data(file_num):
    entity_queue = Queue()
    entity_list = getLocation(file_num)
    for item in entity_list:
        Producer.producer(entity_queue, item)
    return entity_queue

# 爬取每一个页面
def turn_page_thread(submission):
    url_pre = "https://baike.baidu.com/item/"
    url = url_pre+submission
    html = html_paser(url, 'utf-8')
    if html == 0:
        return
    pattern = re.compile('main-content')
    if re.search(pattern, str(html)) is None:
        return
    # pattern1 = re.compile(u'href="(/reference/[^"]+)">([^<]+)</a>')
    pattern1 = re.compile(u'<a\s*rel="nofollow" href="(/reference/[^"]+)"\s*target="_blank"\s*class="text">([^<]+)<')
    content = re.findall(pattern1, str(html))
    if len(content) == 0:
        return
    for link in content:
        triple = [submission, link[1], link[0]]
        Producer.producer(entity_queue, triple)

maxsize = 25
start = 1
end = 13
for i in range(start,end):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"entity_"+str(i))
    path = "data/triples/entity_externallink/entity_externallink_"+str(i)+".txt"
    f = open(path, "w+", encoding="utf-8")
    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    f.close()
    fp = open(path, "a+", encoding="utf-8")
    fp.truncate()
    q = product_data(i)
    entity_queue = Queue()
    pool = MyThreadPool()
    pool.addthread(queue=q, size=maxsize, func=turn_page_thread, timeout=15)
    pool.addthread(queue=entity_queue, size=3, func=insertDB, timeout=20)
    pool.startAll()
    pool.joinAll()
    fp.close()

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "结束")
