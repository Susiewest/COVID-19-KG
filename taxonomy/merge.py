import os
import re


def get_filename(path, filetype):
    name = []
    for root, dirs, files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1] == filetype:
                name.append(i)
    return name


files = ['baidu_entity.txt', 'hudong_entity.txt', 'yixue_entity.txt']
fo = open('total_entity.txt', 'w', encoding='utf-8')
total = []

for wikifile in get_filename('../entity/wiki', '.txt'):
    wiki = [line.strip() for line in open('../entity/wiki/' + wikifile, encoding='utf-8').readlines()]
    for item in wiki:
        result11 = re.sub(u'\（.*?\）', '', item)
        result1 = re.sub(u'\(.*?\)', '', result11)
        if result1 in total:
            print(result1 + "已经出现了")
        else:
            total.append(result1)
            fo.write(result1 + '\n')
            print(wikifile + result1)

for file in files:
    entity = [line.strip() for line in open('../entity/' + file, encoding='utf-8').readlines()]
    for item in entity:
        result22 = re.sub(u'\（.*?\）', '', item)
        result2 = re.sub(u'\(.*?\)', '', result22)
        if result2 in total:
            print(result2 + "已经出现了")
        else:
            total.append(result2)
            fo.write(result2 + '\n')
            print(file + result2)

znwiki = [line.strip() for line in open('../entity/znwiki_entity.txt', encoding='ansi').readlines()]
for item in znwiki:
    result33 = re.sub(u'\（.*?\）', '', item)
    result = re.sub(u'\(.*?\)', '', result33)
    if result in total:
        print(result + "已经出现了")
    else:
        total.append(result)
        fo.write(result + '\n')
        print('znwiki.txt' + result)
fo.close()
