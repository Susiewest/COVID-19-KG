from bs4 import BeautifulSoup
import requests
import random


def get_agent():
    agents = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
              'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) ',
              'Chrome/17.0.963.56 Safari/535.11',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)']
    fakeheader = {'User-agent': agents[random.randint(0, len(agents) - 1)]}
    return fakeheader


filename = 'babelnet taxonomy.txt'
fo = open(filename, 'w', encoding='utf-8')
base = 'http://live.babelnet.org/'
total = {"病毒": 'synset?word=bn:00080085n&details=1&lang=ZH',
         "细菌": 'synset?word=bn:00007854n&details=1&lang=ZH',
         "疾病": 'synset?word=bn:00027546n&details=1&lang=ZH',
         "药物": 'synset?word=bn:00061887n&details=1&lang=ZH',
         "症状": 'synset?word=bn:00075683n&details=1&lang=ZH'
         }

# wbdata = requests.get(base + 'synset?word=bn:00080085n&details=1&lang=ZH', timeout=30, headers=get_agent()).content
# soup = BeautifulSoup(wbdata, 'lxml')
# subclasses = soup.select('.tabbable.active .relation-row')
# fo.write('病毒的subclass:' + '\n')
#
# for subclass in subclasses:
#     if 'HAS KIND' in subclass.get_text():
#         types = subclass.select('small > a')
#         for concrete in types:
#             name = concrete.get_text()
#             url = concrete.get('href')
#             fo.write('\t' + name + '的subclass：' + '\n')
#             data = requests.get(base + url, timeout=30, headers=get_agent()).content
#             ssoup = BeautifulSoup(data, 'lxml')
#             ssubclasses = ssoup.select('.tabbable.active .relation-row')
#             for ssubclass in ssubclasses:
#                 if 'HAS KIND' in ssubclass.get_text():
#                     stypes = ssubclass.select('small > a')
#                     for sconcrete in stypes:
#                         sname = sconcrete.get_text()
#                         fo.write('\t\t' + sname + '\n')

for key in total:
    wbdata = requests.get(base + total[key], timeout=60, headers=get_agent()).content
    soup = BeautifulSoup(wbdata, 'lxml')
    subclasses = soup.select('.tabbable.active .relation-row')
    fo.write(key + '的subclass:' + '\n')
    for subclass in subclasses:
        if 'HAS KIND' in subclass.get_text():
            types = subclass.select('small > a')
            for concrete in types:
                name = concrete.get_text()
                url = concrete.get('href')
                fo.write('\t' + name + '的subclass：' + '\n')
                data = requests.get(base + url, timeout=60, headers=get_agent()).content
                ssoup = BeautifulSoup(data, 'lxml')
                ssubclasses = ssoup.select('.tabbable.active .relation-row')
                for ssubclass in ssubclasses:
                    if 'HAS KIND' in ssubclass.get_text():
                        stypes = ssubclass.select('small > a')
                        for sconcrete in stypes:
                            sname = sconcrete.get_text()
                            fo.write('\t\t' + sname + '\n')
                            print(sname)
    fo.write('\n')

fo.close()
