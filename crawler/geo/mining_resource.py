from bs4 import BeautifulSoup as bs
import requests
import re
import csv
import random
import pandas as pd
import threading

#得到所有实体
entities = pd.read_csv('data/entity_group/entity_1.csv')
entity_list = entities['entity']

#file_name为写入CSV文件的路径，datas为要写入数据列表,columns为列表名
def data_write_csv(file_name, datas,columns):
    df = pd.DataFrame(datas,columns = columns)
    df.to_csv(file_name,encoding='utf-8',index=None)

# 浏览器代理池
def user_agent():
    #浏览器列表,每次访问可以用不同的浏览器访问
    user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    ]
    #随机选取一个浏览器访问
    user_agent = random.choice(user_agent_list)
    return user_agent

# 解析网页
def html_paser(url):
    try:
        header = {'User-Agent': user_agent()}
        response = requests.get( url=url, headers=header)
    except BaseException:
        return 0
    else:
        response.encoding = 'utf-8'
        html_text = response.text
        html = bs(html_text, 'html.parser')
        # print(html)
        return html

error_url = []

#查找abstract
entity_abstract = []
def get_abstract(html,entity):
    str = ""
    prefix = "<http://zhishi.me/zhwiki/resource/"
    subfix = "> "
    predicate = "<http://zhishi.me/ontology/abstract"
    abstract = html.find(attrs={'class': 'lemma-summary'})
    if abstract is None:
        return
    paras = abstract.findAll(attrs={'class': 'para'})
    for para in paras:
        str = str + para.text
    triple = prefix+entity+subfix+predicate+subfix+predicate+'/'+str+subfix
    entity_abstract.append(triple)
    # print(triple)

#查找infobox
entity_property_infobox = []
def get_infobox(html,entity):
    # prefix = "<http://zhishi.me/zhwiki/resource/"
    # subfix = "> "
    # predicate = "<http://zhishi.me/ontology/property/"
    infobox = html.find(attrs={'class': 'infobox vcard'})
    if infobox is None:
        infobox = html.find(attrs={'class': 'infobox geography vcard'})
        if infobox is None:
            return
    trs = infobox.findAll('tr')
    if trs is None:
        print("trs is None")
        return
    for tr in trs:
        # print(tr)
        th = tr.find('th',scope="row")
        if th is None:
            continue
        # triple = prefix + entity + subfix + predicate + tr.th.text + subfix + '"'+ tr.td.text + '"'
        triple=[entity,tr.th.text,tr.td.text]
        # print(triple)
        entity_property_infobox.append(triple)

#查找internallink
def get_internallink(html,entity):
    prefix = "<http://zhishi.me/zhwiki/resource/"
    subfix = "> "
    predicate = "<http://zhishi.me/ontology/internallink/"
    links = html.find('a')
    links.get("href")
    if links is None:
        return
    key_list_div = links.findAll(attrs={'class': 'basicInfo-item name'})
    value_list_div = links.findAll(attrs={'class': 'basicInfo-item value'})
    for key, value in zip(key_list_div, value_list_div):
        triple = prefix + entity + subfix + predicate + key.text + subfix + '"' + value.text + '"'
        entity_property_infobox.append(triple)

#查找externallink(参考文献)
def get_externallink(html,entity):
    prefix = "<http://zhishi.me/zhwiki/resource/"
    subfix = "> "
    predicate = "<http://zhishi.me/ontology/externallink/"
    infobox = html.find(attrs={'class': 'basic-info cmn-clearfix'})
    if infobox is None:
        return
    key_list_div = infobox.findAll(attrs={'class': 'basicInfo-item name'})
    value_list_div = infobox.findAll(attrs={'class': 'basicInfo-item value'})
    for key,value in zip(key_list_div,value_list_div):
        triple = prefix + entity + subfix + predicate + key.text + subfix + '"'+ value.text + '"'
        entity_property_infobox.append(triple)

#访问每个实体的百科
i=1
for entity in entity_list:
    # print(i,entity)
    prefix_path = "https://baike.hk.xileso.top/wiki/"
    path = prefix_path + entity
    # path = "https://baike.hk.xileso.top/wiki/弗内罗尔"
    html = html_paser(path)
    if i % 10 == 0:
        print(i,entity)
    # if i==10:
    #     break
    i = i + 1
    if html==0:
        error_url.append(entity)
    else:
        #进入主页找到三元组；
        # get_abstract(html,entity)
        get_infobox(html,entity)
    # print(entity_property_infobox)


data_write_csv('data/error_url.csv',error_url,['error_url'])
# data_write_csv("data/entity_abstract.csv",entity_abstract)
data_write_csv("data/triples/entity_property_infobox.csv",entity_property_infobox,['subject','predicate','object'])











