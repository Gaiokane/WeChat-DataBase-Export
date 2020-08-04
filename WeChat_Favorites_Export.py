# coding=utf-8

import sqlite3
import re

#该行修改favorites.db文件所在路径，确保db文件已禁用加密
conn = sqlite3.connect('D:/share/favorites.db')

c = conn.cursor()

#默认按收藏时间降序，可自行调整
c.execute('SELECT xml FROM FavoritesItemTable ORDER by time DESC')

# sql查询结果存入元组
result = c.fetchall()

# 截取字符串
def xml_substring(start_str, end_str, str):
    rex = r'%s(.*?)%s' % (start_str, end_str)
    return re.findall(rex, str)

out = ''

#序号自增
i = 1

for xml in result:
    xml_str = xml.__str__()
    #&转义（&amp;）
    pagetitle = ''.join(xml_substring(
        '<pagetitle>', '</pagetitle>', xml_str)).replace('&amp;', '&')
    link = ''.join(xml_substring('<link>', '</link>', xml_str)
                   ).replace('&amp;', '&')
    out += str(i) + '）' + pagetitle + '\n' + link + '\n\n'
    i += 1

with open('WeChat_Favorites_Export.txt', 'w+', encoding='utf-8') as f:
    f.write(out)

c.close()

conn.close()