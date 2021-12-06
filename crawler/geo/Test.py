import re
import pandas as pd

host = "https://baike.baidu.com"
start = 1
end = 13
gap = ';;;;||;;;;'

def get_number(name,path):
    i = 0
    with open(path, "r", encoding="utf-8") as f:
        # list = f.readlines()
        for line in f:
            i+=1

    # 检查文件内容格式的正确性
    # for i, line in zip(range(1, 20), list):
    #     print(line)
    print(name, i)
    return i

def merge_triples(pre_path, out_path):
    out_file = open(out_path, "a+", encoding="utf-8")
    for i in range(start, end):
        path = pre_path + str(i) + ".txt"
        with open(path, "r", encoding="utf-8") as f:
            next(f)
            for line in f.readlines():
                pattern = re.compile(r"'([^']+)'")
                row = re.findall(pattern, line)
                if (len(row)) < 3:
                    continue
                triple = str(row[0]) +gap+ host+ str(row[1]) + gap+host+str(row[2]) + '\n'
                out_file.write(triple)
        out_file.flush()
    out_file.close()

def constrct_category(pre_path, out_path):
    pre_sub = '<http://zhishi.me/baidubaike/resource/'
    post_sub = '> <http://zhishi.me/ontology/category> <http://zhishi.me/baidubaike/category/'
    post_obj = '> . \n'
    out_file = open(out_path, "a+", encoding="utf-8")
    for i in range(1, 13):
        path = pre_path + str(i) + ".txt"
        with open(path, "r", encoding="utf-8") as f:
            next(f)
            for line in f.readlines():
                pattern = re.compile(r"'([^']+)'")
                row = re.findall(pattern, line)
                if (len(row)) < 3:
                    continue
                triple = pre_sub + row[0] + post_sub + row[2] + post_obj
                out_file.write(triple)
        out_file.flush()
    out_file.close()

def constrct_infobox(pre_path, out_path):
    pre_sub = '<http://zhishi.me/baidubaike/resource/'
    post_sub = '> <http://zhishi.me/ontology/property/'
    post_obj = '"@zh .	\n'
    out_file = open(out_path, "a+", encoding="utf-8")
    for i in range(1, 13):
        path = pre_path + str(i) + ".txt"
        with open(path, "r", encoding="utf-8") as f:
            next(f)
            for line in f.readlines():
                pattern = re.compile(r"'([^']+)'")
                row = re.findall(pattern, line)
                if (len(row)) < 3:
                    continue
                triple = pre_sub+row[0]+post_sub+row[1]+'>"' + row[2].replace('\\n','') + post_obj
                out_file.write(triple)
        out_file.flush()
    out_file.close()

def constrct_externallink(pre_path, out_path):
    pre_sub = '<http://zhishi.me/baidubaike/resource/'
    post_sub = '> <http://zhishi.me/ontology/externallink/'
    post_obj = '"@zh .	\n'
    out_file = open(out_path, "a+", encoding="utf-8")
    for i in range(1, 13):
        path = pre_path + str(i) + ".txt"
        with open(path, "r", encoding="utf-8") as f:
            next(f)
            for line in f.readlines():
                pattern = re.compile(r"'([^']+)'")
                row = re.findall(pattern, line)
                if (len(row)) < 3:
                    continue
                triple = pre_sub+row[0]+post_sub+row[1]+'>"' + host + row[2] + post_obj
                out_file.write(triple)
        out_file.flush()
    out_file.close()

def constrct_internallink(pre_path, out_path):
    pre_sub = '<http://zhishi.me/baidubaike/resource/'
    post_sub = '> <http://zhishi.me/ontology/internallink/'
    post_obj = '"@zh .	\n'
    out_file = open(out_path, "a+", encoding="utf-8")
    for i in range(1, 13):
        path = pre_path + str(i) + ".txt"
        with open(path, "r", encoding="utf-8") as f:
            next(f)
            for line in f.readlines():
                pattern = re.compile(r"'([^']+)'")
                row = re.findall(pattern, line)
                if (len(row)) < 3:
                    continue
                triple = pre_sub+row[0]+post_sub+row[1]+'>"' + host +row[2] + post_obj
                # print(triple)
                out_file.write(triple)
        out_file.flush()
    out_file.close()

def constrct_abstract(pre_path, out_path):
    pre_sub = '<http://zhishi.me/baidubaike/resource/'
    post_sub = '> <http://zhishi.me/ontology/abstract> <http://zhishi.me/baidubaike/abstract/'
    post_obj = '> . \n'
    out_file = open(out_path, "a+", encoding="utf-8")
    for i in range(1, 13):
        path = pre_path + str(i) + ".txt"
        with open(path, "r", encoding="utf-8") as f:
            next(f)
            for line in f.readlines():
                pattern = re.compile(r"'([^']+)'")
                row = re.findall(pattern, line)
                if (len(row)) < 3:
                    continue
                triple = pre_sub + row[0] + post_sub + row[2] + post_obj
                # print(triple)
                out_file.write(triple)
        out_file.flush()
    out_file.close()



# merge_triples('data/triples/entity_property/entity_property_','data/triples/entity_property.txt')
# merge_triples('data/triples/entity_externallink/entity_externallink_','data/triples/entity_externallink.txt')
# merge_triples('data/triples/entity_internallink/entity_internallink_','data/triples/entity_internallink.txt')
# merge_triples('data/triples/entity_abstract/entity_abstract_','data/triples/entity_abstract.txt')

#构造三元组，记得执行前确定要创建的文件已删除
# constrct_category('data/triples/entity_category/entity_category_','data/triples/entity_category.txt')
# constrct_infobox('data/triples/entity_property/entity_property_','data/triples/entity_property.txt')
# constrct_externallink('data/triples/entity_externallink/entity_externallink_','data/triples/entity_externallink.txt')
# constrct_internallink('data/triples/entity_internallink/entity_internallink_','data/triples/entity_internallink.txt')
# constrct_abstract('data/triples/entity_abstract/entity_abstract_','data/triples/entity_abstract.txt')

# get_number('entity_category数量：', 'data/triples/entity_category.txt')
get_number('entity_property数量：', 'data/triples/entity_property.txt')
get_number('entity_abstract数量：', 'data/triples/entity_abstract.txt')
get_number('entity_externallink数量：', 'data/triples/entity_externallink.txt')
get_number('entity_internallink数量：', 'data/triples/entity_internallink.txt')
