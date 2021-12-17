from bs4 import BeautifulSoup
import bs4
import os
import re


def get_filename(path, filetype):
    name = []
    for root, dirs, files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1] == filetype:
                name.append(i)
    return name


def is_child(child, father):
    # print(type(father))
    # print(type(child))
    if child in father:
        return True
    seek_list = father.contents
    for i in seek_list:
        if isinstance(i, bs4.element.NavigableString):
            pass
        elif child in i:
            return True
        else:
            flag = is_child(child, i)
            if flag == True:
                return True
    return False


def get_content_between_tables(pre, nxt):
    # 如果第二个table在第一个里面
    txt = ""
    if is_child(nxt, pre):
        cur = pre.next_element
        while cur != nxt and cur is not None:
            if isinstance(cur, bs4.element.NavigableString):
                txt += cur
            cur = cur.next_element
    # 类似并列关系
    else:
        # 先找到pre结束的下一个元素
        cur = pre.next_element
        while is_child(cur, pre):
            cur = cur.next_element
        # 获取内容
        while cur != nxt and cur is not None:
            if isinstance(cur, bs4.element.NavigableString):
                txt += cur
            cur = cur.next_element
    return txt


fow = open('summary_yixue.txt', 'w', encoding='utf-8')
notes = ['[', ']', '(', ')', '{', '}']
count = 0
type_inference = {}
pages = get_filename('../../yixue', '.xml')

for p in pages:
    fo = open('../../yixue/' + p, 'r', encoding='utf-8')
    soup = BeautifulSoup(fo.read(), 'lxml')
    title = soup.find('table', class_='nav')
    table = soup.find('table', class_='toc')
    entity_name = soup.select('div#content > h1.firstHeading')
    # print(title[0].get_text() + p)
    name = entity_name[0].get_text()
    try:
        summary = get_content_between_tables(title, table)
    except TypeError:
        print('出现问题的实体：' + name)
    else:
        flag = 0
        for note in notes:
            if note in name:
                flag = 1
        if flag == 0:
            pattern = re.compile(name + '([a-zA-Z()]*?)是([^。]*?)(病毒|细菌|疾病|药物|医学专科|症状|检查科目)(，|。)')
            if summary is not None:
                summary_paras = summary.replace('\n', '').strip()
                summary_final = ''.join(summary_paras)
                result = pattern.findall(summary_final)
                if result:
                    count += 1
                    fow.write(name + '\t' + result[0][2] + '\n')
                    type_inference[name] = result[0][2]

print(type_inference)
