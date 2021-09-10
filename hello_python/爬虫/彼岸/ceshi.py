# -- coding: utf-8 --
import os
import random
import requests  #请求模块 第三方模块 pip install requests
import parsel  # 数据解析模块
import time #时间模块
from fake_useragent import UserAgent  #反爬措施2 加入随机user-Agent pip install fake_useragent
location = os.getcwd() + '/fake_useragent_0.1.11.json'
ua = UserAgent(path=location)
# 开始时间
print("程序开始运行...")
url = 'http://www.netbian.com/1920x1080/index.htm'
# 请求头： 把python代码伪装成浏览器对服务器发送请求
headers = {
        # 'Cookie': '__yjs_duid=1_3ea3fe5ffef718b78da67ec3380415551628425408870; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1628425430; xygkqecookieinforecord=%2C12-23780%2C7-23778%2C19-23781%2C; Hm_lpvt_14b14198b6e26157b7eba06b390ab763=1628431315',
        # 'Host': 'www.netbian.com',
        # 'Referer': 'http://www.netbian.com/1920x1080/index_6.htm',
        'User-Agent': ua.random,
    }
print('正在获取网站返回数据...')
response = requests.get(url=url, headers=headers)
print(f'返回值:{response}...')
# 获取源代码/获取网页文本数据 response.text
# 出现乱码怎么办？  需要转码
# html_data = response.content.decode('gbk')
response.encoding = response.apparent_encoding  # 自动转码
# 获取源代码/获取网页文本数据 response.text
# print(response.text)
# 解析数据
print('正在解析网页数据...')
selector = parsel.Selector(response.text)
print(f'网页数据解析完成：{selector}')

# CSS选择器 就是根据网页标签内容提取数据
# 第一次提取 提取所有的li标签内容
lis = selector.css('.list li')
# print(f'所有lis标签下内容:{lis}')
print(f'所有lis标签下内容获取成功')
for li in lis:
    print('正在获取标题信息')
    # http://www.netbian.com
    title = li.css('b::text').get()
    print(f'标题信息:{title}')

    if title:
        # 提取主页面所有图片的url
        print('正在获取图片地址...')

        href = 'http://www.netbian.com' + li.css('a::attr(href)').get()
        print(f'图片地址:{href}')

        #提取所有url下的图片src
        response_1 = requests.get(url=href, headers=headers)
        selector_1 = parsel.Selector(response_1.text)
        # print(selector_1)
        img_url = selector_1.css('.pic img::attr(src)').get()
        # print(href, title, img_url)
        # 下载所有图片
        # 反爬措施1  加入随机等待时间
        print('正在下载图片...')
        # time.sleep(random.randint(0,3)) #随机等待时间
        img_content = requests.get(url=img_url, headers=headers).content
        print('图片下载成功...')
        if not os.path.exists('img'):
            os.makedirs('img')
        with open('img\\' + title + '.jpg', mode='wb') as f:
            print('正在保存: ',title)
            f.write(img_content)

