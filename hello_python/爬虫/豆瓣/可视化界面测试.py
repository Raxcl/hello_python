# -- coding: utf-8 --
from gooey import Gooey, GooeyParser

@Gooey
def main():
    # 添加可视化界面
    parser = GooeyParser(description="欢迎使用龙宝制作的top250网站信息获取工具")
    parser.add_argument('path', help="下载路径", widget="DirChooser")
    args = parser.parse_args()


if __name__ == '__main__':
    main()