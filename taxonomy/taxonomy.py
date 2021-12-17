file1 = 'subclasses.txt'
fo = open(file1, 'w', encoding='utf-8')
pairs = []
virus = []
bacteria = []
medicine = []
disease = []
speciaty = []
symptom = []
total = {'病毒': virus, '细菌': bacteria, '药物': medicine, '疾病': disease, '医学专科': speciaty, '症状': symptom}

for line in open('yagoTaxonomy.ttl', encoding='utf-8').readlines():
    if 'rdfs:subClassOf' in line:
        content = line.split('rdfs:subClassOf')
        pair = [content[0].strip(), content[1].strip().strip('.')]
        pairs.append(pair)

for duizi in pairs:
    if '<wordnet_virus_101328702>' in duizi[1] and 'wordnet' in duizi[0]:
        virus.append(duizi[0])
    if '<wordnet_bacteria_101348530>' in duizi[1] and 'wordnet' in duizi[0]:
        bacteria.append(duizi[0])
    if '<wordnet_medicine_103740161>' in duizi[1] and 'wordnet' in duizi[0]:
        medicine.append(duizi[0])
    if '<wordnet_disease_114070360>' in duizi[1] and 'wordnet' in duizi[0]:
        disease.append(duizi[0])
    if '<wordnet_medicine_106043075>' in duizi[1] and 'wordnet' in duizi[0]:
        speciaty.append(duizi[0])
    if '<wordnet_symptom_114299637>' in duizi[1] and 'wordnet' in duizi[0]:
        symptom.append(duizi[0])
# fo.close()

for key in total:
    fo.write(key+'的subclass:' + '\n')
    for item in total[key]:
        fo.write('\t' + item + '的subclass：' + '\n')
        for duizi in pairs:
            if item in duizi[1] and 'wordnet' in duizi[0]:
                fo.write('\t\t' + duizi[0] + '\n')

fo.close()
