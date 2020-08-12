# coding=utf-8
import sqlite3
import re
import html
from pyhanlp import *
from collections import Counter
from operator import itemgetter

# 该行修改favorites.db文件所在路径，确保db文件已禁用加密
conn = sqlite3.connect('D:/share/WeChat DB/favorites.db')

c = conn.cursor()

# 默认按收藏时间降序，可自行调整
c.execute('SELECT xml FROM FavoritesItemTable ORDER by time DESC')

# sql查询结果存入元组
result = c.fetchall()

# 截取字符串
def xml_substring(start_str, end_str, str):
    rex = r'%s(.*?)%s' % (start_str, end_str)
    #返回值list转string
    return ''.join(re.findall(rex, str))

""" # 存放结果
out = ''

# 序号自增
i = 1

for xml in result:
    # list转string
    xml_str = ''.join(xml)
    # 取出pagetitle、link并进行反转义
    pagetitle = html.unescape(xml_substring('<pagetitle>', '</pagetitle>', xml_str))
    link = html.unescape(xml_substring('<link>', '</link>', xml_str))
    # 拼接输出内容
    out += str(i) + '）' + pagetitle + '\n' + link + '\n\n'
    # 序号+1
    i += 1

# 输出文件
with open('WeChat_Favorites_Export.txt', 'w+', encoding='utf-8') as f:
    f.write(out)

c.close()

conn.close()

print('导出成功') """

all_Keywords = []

for xml in result:
    # list转string
    xml_str = ''.join(xml)
    # 取出pagetitle、link并进行反转义
    pagetitle = html.unescape(xml_substring('<pagetitle>', '</pagetitle>', xml_str))
    #关键词提取
    #print(HanLP.extractKeyword(pagetitle, 100))
    #循环中的元组合并
    all_Keywords += HanLP.extractKeyword(pagetitle, 100)

#打印合并后的元组
#print(all_Keywords)

#打印元组中出现最多次数的元素
#print(max(all_Keywords, key=all_Keywords.count))

#统计元组中元素出现的次数并降序显示
def count_sort(str):
    #from collections import Counter
    
    #str = ['Tom', 'Sim', 'Jack', 'Tom', 'Sleep', 'We', 'Tom', 'Tom', 'Sim', 'We', 'Tom']
    dic = Counter(str)
    
    #1.统计各元素出现的次数，一行显示一个
    """ for i in dic.items():
        print(i[0], i[1]) """
    
    #2.字典形式统计各元素出现的次数，不排序/降序
    count = 1
    l = len(str)-1
    x = {}
    t = 0
    
    while t <= l:
        th = str[t]
        i = t + 1
        while i <= l:
            if th == str[i]:
                count += 1
                del str[i]
                i -= 1
                l -= 1
            i += 1
        x[th] = count
        count = 1
        t += 1
    #不排序
    #print(x)
    #降序
    y = sorted(x.items(), key=lambda x: x[1], reverse=True)
    print(y)
    
    #显示出现次数最多的前三名
    """ three = (y[0], y[1], y[2])
    for t in three:
        print(t[0]) """
    
    #
    """ item = x.items()
    #item.sort()
    #sorted(item,key=itemgetter(1))
    sorted(item,key=lambda x: x[1], reverse=True)
    for k,v in item:
        print(k,v) """

    """ item = x.items()
    print(item)
    #item.sort()
    #sorted(item,key=itemgetter(1))
    sorted(item,key=lambda x: x[1])
    print(item)
    for k,v in item:
        print(k,v) """

count_sort(all_Keywords)