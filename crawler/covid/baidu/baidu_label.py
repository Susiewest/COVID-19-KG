from bs4 import BeautifulSoup
import os
import re

f1 = open('infer_by_label.txt', 'w', encoding='utf-8')
dic_count = {'病毒': 0, '细菌': 0, '疾病': 0, '药物': 0,
             '症状': 0, '检查科目': 0, '医学专科': 0}


def get_filename(path, filetype):  # 获取指定路径下指定格式的文件
    name = []
    for root, dirs, files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1] == filetype:
                name.append(i)
    return name


package = ['/bacteria', '/disease', '/drug', '/inspection', '/specialty', '/symptom', '/virus']
notes = ['[', ']', '(', ')', '{', '}']
count = 0
type_inference = {}

for data in package:  # 在所有实体类型的页面中找信息
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
            tag = page.select('#open-tag > dd > span')  # 找标签
            if len(tag) > 0:
                count += 1
                for label in tag:
                    if label.text.strip() == '细菌':
                        dic_count['细菌'] += 1
                        f1.write(real_name + '\t细菌\n')
                    elif label.text.strip() == '病毒':
                        dic_count['病毒'] += 1
                        f1.write(real_name + '\t病毒\n')
                    elif label.text.strip() == ('药物' or '药品'):
                        dic_count['药物'] += 1
                        f1.write(real_name + '\t药物\n')
                    elif label.text.strip() == '疾病':
                        dic_count['疾病'] += 1
                        f1.write(real_name + '\t疾病\n')
                    elif label.text.strip() == '医学专科':
                        dic_count['医学专科'] += 1
                        f1.write(real_name + '\t医学专科\n')
                    elif label.text.strip() == '检查科目':
                        dic_count['检查科目'] += 1
                        f1.write(real_name + '\t检查科目\n')
                    elif label.text.strip() == '症状':
                        dic_count['症状'] += 1
                        f1.write(real_name + '\t症状\n')

print(dic_count)
print(count)
'''
似乎只在百度中进行使用
get_filename 获取所有文件的名字
files 目录下的文件名称
filetype 查找文件的种类吧
package 文件夹的名称的样子
notes ？？
type_inference ？？
pages
BeautifulSoup 似乎是处理解析xml和html
lxml 一个解析器 默认好像是html parser解析器 这个更快 用的是C
soup.select('html') 似乎可以用标签名来查找
all_page 全部页面的内容？ 可能不止一个页面的样子
real_name 名字？
tag 标签
fo 打开一个文件
#open-tag > dd > span 似乎是id名字到其子标签的内容 看起来有很多的span
strip 删除前后的空格
'''