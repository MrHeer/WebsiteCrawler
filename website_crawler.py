import socket
from urllib import request
import re
import os

import time

target_url = 'http://www.heiyange.com'
book_url = '/read/4394/'  # 修改此处可确定爬取哪一本小说
book_title = ''
book_href = {}  # 序号-链接
book_chapter = {}  # 序号-章节
socket.setdefaulttimeout(10)

while True:
    try:
        data = request.urlopen(target_url + book_url).read().decode('gbk')
        break
    except:
        time.sleep(5)
        print("正在尝试重连......")
        pass

book_title = re.search('<h3>(.+?)</h3>', data).group(1)
target_string = re.findall('<li><a href="(.+?)<span></span></a></li>', data)
print("正在爬取小说：" + book_title)
i = 1
for string in target_string:
    chapter = re.search('^(.+?)">(.+?)$', string).group(2)
    href = target_url + re.search('(.+?)">(.+?)$', string).group(1)
    book_href.update({str(i): href})
    book_chapter.update({str(i): chapter})
    i = i + 1

# 创建存储目录
save_dir = "./" + book_title
if not os.path.isdir(save_dir):
    # 创建存储目录
    print("-----------------------------------------------")
    print("存储目录不存在，正在创建...")
    os.mkdir(save_dir)
    print("创建完成！")

# 创建章节txt
finish_count = 0
for key in book_href.keys():
    if not os.path.isfile(save_dir + '/' + key + '.txt'):
        print("-----------------------------------------------")
        print("开始爬取：" + book_chapter.get(key) + "（" + key + ".txt）")
        while True:
            try:
                text = request.urlopen(book_href.get(key)).read().decode('gbk')
                break
            except:
                time.sleep(5)
                print("正在尝试重连......")
                pass
        content = re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.+?)<br />', text)
        print("正在爬取......")
        file = open(save_dir + '/' + key + '.txt', 'a')
        file.write(book_chapter.get(key) + '\n')
        file.write('\n')
        for string in content:
            file.write(string + '\n')
            file.write('\n')
        file.write(re.search('&nbsp;&nbsp;&nbsp;&nbsp;(.+?)\t', text).group(1))
        file.close()
        print("爬取成功")
        finish_count = finish_count + 1
        print("已完成：" + str(int(finish_count / len(book_href) * 100)) + "%")
    else:
        print("-----------------------------------------------")
        print("已经爬取：" + book_chapter.get(key) + "（" + key + ".txt）")
        finish_count = finish_count + 1
        print("已完成：" + str(int(finish_count / len(book_href) * 100)) + "%")

# 创建小说txt
if not os.path.isfile(save_dir + '/' + book_title + '.txt'):
    print("-----------------------------------------------")
    print("正在生成：" + book_title + '......')
    file = open(save_dir + '/' + book_title + '.txt', 'a')
    file_count = 0
    i = 1
    while file_count < len(book_href):
        if os.path.isfile(save_dir + '/' + str(i) + '.txt'):
            read_file = open(save_dir + '/' + str(i) + '.txt')
            file.write(read_file.read())
            file.write('\n')
            file.write('\n')
            file.write('\n')
            read_file.close()
            file_count = file_count + 1
        i = i + 1
    file.close()
    print('生成成功！')
else:
    print("-----------------------------------------------")
    print("已经生成：" + book_title)

print("-----------------------------------------------")
print("小说爬取成功！")