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

all_Keywords = []

for xml in result:
    # list转string
    xml_str = ''.join(xml)
    # 取出pagetitle、link并进行反转义
    pagetitle = html.unescape(xml_substring('<pagetitle>', '</pagetitle>', xml_str))
    #关键词提取，循环中的元组合并
    all_Keywords += HanLP.extractKeyword(pagetitle, 100)

#打印合并后的元组
#print(all_Keywords)

#打印元组中出现最多次数的元素
#print(max(all_Keywords, key=all_Keywords.count))

# 存放结果
out = ''

#统计元组中元素出现的次数并排序显示
def count_sort(strs,type):
    
    out = ''

    #1.统计各元素出现的次数，一行显示一个
    """ dic = Counter(strs)
    for i in dic.items():
        print(i[0], i[1]) """
    
    #2.字典形式统计各元素出现的次数，不排序/降序
    count = 1
    l = len(strs)-1
    x = {}
    t = 0
    
    while t <= l:
        th = strs[t]
        i = t + 1
        while i <= l:
            if th == strs[i]:
                count += 1
                del strs[i]
                i -= 1
                l -= 1
            i += 1
        x[th] = count
        count = 1
        t += 1
    #不排序
    #print(x)
    if type & 1 != 0:
        #global out
        out += str(x) + '\n'
    
    if type == 3 or type == 5 or type == 7:
        out += '——————————————————————————————————————————' + '\n'

    #降序
    y = sorted(x.items(), key=lambda x: x[1], reverse=True)
    #print(y)
    
    #显示出现次数最多的前三名
    """ three = (y[0], y[1], y[2])
    for t in three:
        print(t[0]) """
    if type & 2 != 0:
        three = (y[0], y[1], y[2])
        for t in three:
            #global out
            out += t[0] + '\n'
    
    if type == 7:
        out += '——————————————————————————————————————————' + '\n'
    
    #降序一行一个 输出
    """ for k,v in y:
        #print(k,v)
        global out
        out += k + ' ' + str(v) + '\n' """
    if type & 4 != 0:
        for k,v in y:
            #global out
            out += k + ' ' + str(v) + '\n'

    return out

#count_sort(all_Keywords,7)
#print(count_sort(all_Keywords,3))

# 输出文件
with open('WeChat_Favorites_Automatic_Category.txt', 'w+', encoding='utf-8') as f:
    f.write(count_sort(all_Keywords,7))

print('导出成功')