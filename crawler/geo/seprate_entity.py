import csv
import re
import pandas as pd

#得到所有实体
entity_set = set()
with open("data/geo_data/baidubaike_encoded/entity_category.nt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\r\n')
        pattern = re.compile(r'http://zhishi.me/baidubaike/resource/([^>]+)>')
        entity = re.findall(pattern, line)
        if len(entity) == 0:
            continue
        entity_set.add(entity[0])
print(len(entity_set))  # 374366,包含了所有实体

#将数据写入到本地，并存储为csv文件
# def data_write_csv(file_name, datas):
#     #file_name为写入CSV文件的路径，datas为要写入数据列表
#     with open(file_name, "w", newline='', encoding='utf-8') as file:
#         writer = csv.writer(file, delimiter=',')
#         writer.writerow(datas)

#file_name为写入CSV文件的路径，datas为要写入数据列表
def data_write_csv(file_name, datas):
    df = pd.DataFrame(datas,columns = ['entity'])
    df.to_csv(file_name,encoding='utf-8',index=None)

i=1
k=1
entity_list = []
prefix_path = 'data/entity_group/entity_'
for entity in entity_set:
    entity_list.append(entity)
    if i%30000==0:
        data_write_csv(prefix_path+str(k)+'.csv', entity_list)
        entity_list.clear()
        k+=1
    i+=1
