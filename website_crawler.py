from urllib import request
import re
import os

target_url = 'http://www.heiyange.com'
book_url = '/read/2/'    # 修改此处可确定爬取哪一本小说
book_title = ''
book_dict = {}

data = request.urlopen(target_url + book_url).read().decode('gbk')

book_title = re.search('<h3>(.+?)</h3>', data).group(1)
chapter = re.findall('<li><a href="(.+?)<span></span></a></li>', data)
print("正在爬取小说："+book_title)
for str in chapter:
    book_dict.update({re.search('^(.+?)">(.+?)$', str).group(2): target_url + re.search('(.+?)">(.+?)$', str).group(1)})

# 创建存储目录
save_dir = "./" + book_title
if not os.path.isdir(save_dir):
    # 创建存储目录
    print("存储目录不存在，正在创建...")
    os.mkdir(save_dir)
    print("创建完成！")
    print("-----------------------------------------------")

# 创建txt
for key in book_dict.keys():
    if not os.path.isfile(save_dir + '/' + key + '.txt'):
        print("-----------------------------------------------")
        print("开始爬取：" + key)
        text = request.urlopen(book_dict.get(key)).read().decode('gbk')
        content = re.findall('&nbsp;&nbsp;&nbsp;&nbsp;(.+?)<br />', text)
        print("正在爬取......")
        file = open(save_dir + '/' + key + '.txt', 'a')
        for str in content:
            file.write(str + '\n')
            file.write('\n')
        file.write(re.search('&nbsp;&nbsp;&nbsp;&nbsp;(.+?)\t', text).group(1))
        file.close()
        print("爬取成功")
    else:
        print("-----------------------------------------------")
        print("已经爬取：" + key)
print("-----------------------------------------------")
print("小说爬取成功！")
