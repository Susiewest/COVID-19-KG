import re

pattern = re.compile('热微菌门([a-zA-Z()]*?)是([^。]*?)(病毒|细菌|疾病|药物|医学专科|症状|检查科目)(，|。)')

result = pattern.findall('热微菌门(Thermomicrobia)是一类绿非硫细菌。')

print(result)