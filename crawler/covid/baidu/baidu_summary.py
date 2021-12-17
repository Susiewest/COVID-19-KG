from bs4 import BeautifulSoup
import os
import re


def get_filename(path, filetype):
    name = []
    for root, dirs, files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1] == filetype:
                name.append(i)
    return name


fow = open('summary_baidu.txt', 'w', encoding='utf-8')
package = ['/bacteria', '/disease', '/drug', '/inspection', '/specialty', '/symptom', '/virus']
notes = ['[', ']', '(', ')', '{', '}']
count = 0
type_inference = {}

for data in package:
    pages = get_filename('../../HTML' + data, '.htm')
    for p in pages:
        fo = open('../../HTML' + data + '/' + p, 'r', encoding='utf-8')
        soup = BeautifulSoup(fo.read(), 'lxml')
        all_page = soup.select('html')
        for page in all_page:
            title = page.select('title')
            name = title[0].get_text()
            if '（' in name:
                real_name = name.split('（')[0]
            else:
                real_name = name.split('_')[0]
            # print(real_name)
            pattern = re.compile(real_name + '([a-zA-Z()]*?)是([^。]*?)(病毒|细菌|疾病|药物|医学专科|症状|检查科目)(，|。)')#模式？
            summaries = page.select('div.lemma-summary')  # 找summary 似乎是一个class
            for summary in summaries:#可能不止一个summary
                words = summary.get_text().strip()
                # print(words)
                # words = pseg.cut(summary.get_text())
                # outstr = ''
                # for x in words:
                #     outstr += "{}/{},".format(x.word, x.flag)
                result = pattern.findall(words)  # 正则表达式匹配
                if result:
                    count += 1
                    fow.write(real_name + '\t' + result[0][2] + '\n')#第三个括号的样子
                    type_inference[name] = result[0][2]#realname是为了不考虑别称的情况下提出的看来

print(type_inference)
