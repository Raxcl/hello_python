# -- coding: utf-8 --
"""
思路：
一. 关于数据来源查找：
    1.确定目标需求：爬取高清壁纸图片（彼岸）
        通过开发者工具（F12） 查找图片的url地址来源
        请求 壁纸的详情页 获取它的网页源代码 就可以获取图片url地址了（一张）
        请求 列表页就可以获取 每个壁纸的详情页url 以及 标题

二. 代码实现：
1.发送请求
    壁纸的列表页url： http://www.netbian.com/1920x1080/index.htm
2.获取数据
    网页源代码/ response.text 网页文本数据
3.解析数据
    1.壁纸详情页url： /desk/23780.htm  2.壁纸标题
4.保存数据
    保存图片是二进制数据
"""
import os
from gooey import Gooey, GooeyParser
import requests  # 请求模块 第三方模块 pip install requests
import parsel  # 数据解析模块
import time  # 时间模块
from fake_useragent import UserAgent  # 反爬措施2 加入随机user-Agent pip install fake_useragent
location = os.getcwd() + '/fake_useragent_0.1.11.json'
ua = UserAgent(path=location)
# 开始时间
time_1 = time.time()

@Gooey
def main():
    """
        url = 'http://www.netbian.com/1920x1080/index.htm'
        # 请求头： 把python代码伪装成浏览器对服务器发送请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400'
        }
        response = requests.get(url=url, headers=headers)
        # 获取源代码/获取网页文本数据 response.text
        # 出现乱码怎么办？  需要转码
        # html_data = response.content.decode('gbk')
        response.encoding = response.apparent_encoding  # 自动转码
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
                #提取所有url下的图片src
                response_1 = requests.get(url=href, headers=headers)
                selector_1 = parsel.Selector(response_1.text)
                # print(selector_1)
                img_url = selector_1.css('.pic img::attr(src)').get()
                # print(href, title, img_url)
                # 下载所有图片
                img_content = requests.get(url=img_url, headers=headers).content
                with open('img\\' + title + '.jpg', mode='wb') as f:
                    f.write(img_content)
                    print('正在保存: ',title)
        """
    # 添加可视化界面
    parser = GooeyParser(description="欢迎使用龙宝制作的壁纸获取工具")
    parser.add_argument('start', help="请输入爬取信息的开始页")
    parser.add_argument('end', help="请输入爬取信息的结束页")
    args = parser.parse_args()
    # 第二页之后
    for page in range(int(args.start), int(args.end)):
        print(f'=================正在爬取第{page}页的数据内容=================')
        url = f'http://www.netbian.com/1920x1080/index_{page}.htm'
        # 请求头： 把python代码伪装成浏览器对服务器发送请求
        headers = {
            'User-Agent': ua.random,
        }
        response = requests.get(url=url, headers=headers)
        # 获取源代码/获取网页文本数据 response.text
        # 出现乱码怎么办？  需要转码
        # html_data = response.content.decode('gbk')
        response.encoding = response.apparent_encoding  # 自动转码
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
                response_1 = requests.get(url=href, headers=headers)
                selector_1 = parsel.Selector(response_1.text)
                # print(selector_1)
                img_url = selector_1.css('.pic img::attr(src)').get()
                # print(href, title, img_url)
                # 下载所有图片
                print('正在下载图片，请稍后...')
                img_content = requests.get(url=img_url, headers=headers).content
                if not os.path.exists('img'):
                    os.makedirs('img')
                with open('img\\' + title + '.jpg', mode='wb') as f:
                    print('正在保存: ', title)
                    f.write(img_content)
                    print('保存成功。。。')

    # 结束时间
    time_2 = time.time()
    use_time = int(time_2) - int(time_1)
    print(f'总计耗时{use_time}秒')

if __name__ == '__main__':
    main()
