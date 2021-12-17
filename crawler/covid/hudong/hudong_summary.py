from bs4 import BeautifulSoup
import os
import jieba.posseg as pseg
import re


def get_filename(path, filetype):
    name = []
    for root, dirs, files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1] == filetype:
                name.append(i)
    return name


fow = open('summary_hudong.txt', 'w', encoding='utf-8')
notes = ['[', ']', '(', ')', '{', '}']
count = 0
type_inference = {}
pages = get_filename('../../hudong', '.xml')

for p in pages:
    fo = open('../../hudong/' + p, 'r', encoding='utf-8')
    soup = BeautifulSoup(fo.read(), 'lxml')
    all_page = soup.select('page')
    for page in all_page:
        title = page.select('title')
        # print(title[0].get_text() + p)
        name = title[0].get_text()
        flag = 0
        for note in notes:
            if note in name:
                flag = 1
        if flag == 0:
            pattern = re.compile(name + '([a-zA-Z()]*?)(为|是|属于)([^。]*?)(病毒|细菌|病|药品|药物|医学专科|症状|检查科目|检查项目)(，|。)')
            summaries = page.select('div.summary')
            for summary in summaries:
                # words = pseg.cut(summary.get_text())
                # outstr = ''
                # for x in words:
                #     outstr += "{}/{},".format(x.word, x.flag)
                result = pattern.findall(summary.get_text().strip())
                if result:
                    count += 1
                    if result[0][3] == '病毒':
                        print(name + ':' + '病毒' + str(count))
                        type_inference[name] = '病毒'
                        fow.write(name+'\t'+'病毒'+'\n')
                    elif result[0][3] == '细菌':
                        print(name + ':' + '细菌' + str(count))
                        type_inference[name] = '细菌'
                        fow.write(name + '\t' + '细菌' + '\n')
                    elif result[0][3] == '病':
                        print(name + ':' + '疾病' + str(count))
                        type_inference[name] = '疾病'
                        fow.write(name + '\t' + '疾病' + '\n')
                    elif result[0][3] == ('药物' or '药品'):
                        print(name + ':' + '药物' + str(count))
                        type_inference[name] = '药物'
                        fow.write(name + '\t' + '药物' + '\n')
                    elif result[0][3] == '医学专科':
                        print(name + ':' + '医学专科' + str(count))
                        type_inference[name] = '医学专科'
                        fow.write(name + '\t' + '医学专科' + '\n')
                    elif result[0][3] == '症状':
                        print(name + ':' + '症状' + str(count))
                        type_inference[name] = '症状'
                        fow.write(name + '\t' + '症状' + '\n')
                    elif result[0][3] == ('检查科目' or '检查项目'):
                        print(name + ':' + '检查科目' + str(count))
                        type_inference[name] = '检查科目'
                        fow.write(name + '\t' + '检查科目' + '\n')

print(type_inference)
fow.close()
