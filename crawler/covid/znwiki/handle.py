total_entities = [line.strip() for line in open('template.txt', encoding='utf-8').readlines()]
dic = {}
for line in total_entities:
    if ';;;;||;;;;' in line:
        entity = line.split(';;;;||;;;;')[0]
        template = line.split(';;;;||;;;;')[1].strip()
        if template not in dic.keys():
            dic[template] = 1
        else:
            dic[template] += 1

for i in sorted(dic.items(), key=lambda kv: (kv[1], kv[0])):
    print(str(i).strip('()').split(',')[0] + ':' + str(i).strip('()').split(',')[1])
