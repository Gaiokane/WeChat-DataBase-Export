# coding=utf-8
import sqlite3
import re
import html
from pyhanlp import *
from collections import Counter
from operator import itemgetter

# 该行修改favorites.db文件所在路径，确保db文件已禁用加密
conn = sqlite3.connect('D:/share/WeChat DB/favorites.db')

"""
设置导出类型
TYPE = 1：打印不排序的dict（含数量）
TYPE = 2：打印降序的list（含数量）
TYPE = 4：打印降序前三名（不显示数量）
TYPE = 8：打印不排序dict，一行一个（含数量）
TYPE = 16：打印降序dict，一行一个（含数量）
TYPE = 3/5/7...可做与运算，打印多个
 """
TYPE = 16

c = conn.cursor()

# 默认按收藏时间降序，可自行调整
c.execute('SELECT xml FROM FavoritesItemTable ORDER by time DESC')

# sql查询结果存入元组
result = c.fetchall()

# 截取字符串
def xml_substring(start_str, end_str, str):
    rex = r'%s(.*?)%s' % (start_str, end_str)
    # 返回值list转string
    return ''.join(re.findall(rex, str))

# 存放取出来的所有关键字
all_Keywords = []

for xml in result:
    # list转string
    xml_str = ''.join(xml)
    # 取出pagetitle、link并进行反转义
    pagetitle = html.unescape(xml_substring('<pagetitle>', '</pagetitle>', xml_str))
    # 关键词提取，循环中的元组合并
    all_Keywords += HanLP.extractKeyword(pagetitle, 100)

# 统计元组中元素出现的次数并排序显示
def count_sort(strs, type):
    
    # 存放结果
    out = ''

    # 配合“打印不排序dict，一行一个（含数量）”使用
    dic = Counter(strs)
    
    count = 1
    l = len(strs) - 1
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

    # 1.打印不排序的dict（含数量）
    if type & 1 != 0:
        out += str(x) + '\n'
    
    if type != 1 and type & 1 != 0:
        out += '——————————————————————————————————————————' + '\n'

    # 2.打印降序的list（含数量）
    y = sorted(x.items(), key=lambda x: x[1], reverse=True)
    if type & 2 != 0:
        out += str(y) + '\n'
    
    if type != 2 and type & 2 != 0:
        out += '——————————————————————————————————————————' + '\n'
    
    # 3.打印降序前三名（不显示数量）
    if type & 4 != 0:
        three = (y[0], y[1], y[2])
        for t in three:
            out += t[0] + '\n'
    
    if type != 4 and type & 4 != 0:
        out += '——————————————————————————————————————————' + '\n'
    
    # 4.打印不排序dict，一行一个（含数量）
    if type & 8 != 0:
        for i in dic.items():
            out += str(i[0]) + ' ' + str(i[1]) + '\n'
    
    if type != 8 and type & 8 != 0:
        out += '——————————————————————————————————————————' + '\n'

    # 5.打印降序dict，一行一个（含数量）
    if type & 16 != 0:
        for k, v in y:
            out += k + ' ' + str(v) + '\n'

    return out

# 输出文件
with open('WeChat_Favorites_Automatic_Category.txt', 'w+', encoding = 'utf-8') as f:
    f.write(count_sort(all_Keywords, TYPE))

print('导出成功')