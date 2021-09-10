# -- coding: utf-8 --
import os

import requests  #请求模块 第三方模块 pip install requests
import parsel  # 数据解析模块
import time #时间模块
import concurrent.futures  #多线程模块
from fake_useragent import UserAgent  #反爬措施2 加入随机user-Agent pip install fake_useragent
location = os.getcwd() + '/fake_useragent_0.1.11.json'
ua = UserAgent(path=location)

def get_response(html_url):
    """
    发送请求
    :param html_url: 网址
    :return: response
    """
    headers = {
        'Cookie': '__yjs_duid=1_3ea3fe5ffef718b78da67ec3380415551628425408870; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1628425430; xygkqecookieinforecord=%2C12-23780%2C7-23778%2C19-23781%2C; Hm_lpvt_14b14198b6e26157b7eba06b390ab763=1628431315',
        'Host': 'www.netbian.com',
        # 'Referer': 'http://www.netbian.com/1920x1080/index_6.htm',
        'User-Agent': ua.random,
    }
    response = requests.get(url=html_url, headers=headers)
    # 获取源代码/获取网页文本数据 response.text
    # 出现乱码怎么办？  需要转码
    # html_data = response.content.decode('gbk')
    response.encoding = response.apparent_encoding  # 自动转码
    return response

def save(title, img_url):
    """
    保存数据
    :param title: 壁纸名字
    :param img_url: 壁纸图片
    :return:
    """
    # 下载所有图片
    img_content = requests.get(url=img_url).content
    if not os.path.exists('img'):
        os.makedirs('img')
    with open('img\\' + title + '.jpg', mode='wb') as f:
        f.write(img_content)
        print('正在保存: ', title)

def get_img_url(html_url):
    """
    获取图片url地址
    :param html_url: 壁纸详情页 url
    :return: 壁纸图片url
    """

    response_1 = get_response(html_url)
    print(f"啊啊啊啊啊{response_1}")
    selector_1 = parsel.Selector(response_1.text)
    # print(selector_1)
    img_url = selector_1.css('.pic img::attr(src)').get()
    return img_url

def main(html_url):
    """
    主函数
    :param html_url: 壁纸列表页的url
    :return:
    """
    response = get_response(html_url)
    # 获取源代码/获取网页文本数据 response.text
    # print(response.text)
    # 解析数据
    selector = parsel.Selector(response.text)
    # CSS选择器 就是根据网页标签内容提取数据
    # 第一次提取 提取所有的li标签内容
    lis = selector.css('.list li')
    # print(lis)
    for li in lis:
        # http://www.netbian.com
        title = li.css('b::text').get()

        if title:
            # 提取主页面所有图片的url
            href = 'http://www.netbian.com' + li.css('a::attr(href)').get()
            # 提取所有url下的图片src
            img_url = get_img_url(href)
            # print(f'哈哈哈哈哈{img_url}')
            save(title, img_url)

if __name__ == '__main__':
    # 开始时间
    time_1 =time.time()
    exe = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    for page in range(2, 12):
        print(f'=================正在爬取第{page}页的数据内容=================')
        url = f'http://www.netbian.com/1920x1080/index_{page}.htm'
        exe.submit(main, url)
    exe.shutdown()
    # 结束时间
    time_2 = time.time()
    use_time = int(time_2) - int(time_1)
    print(f'总计耗时{use_time}秒')