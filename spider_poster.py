"""导入包"""
import os
import requests
from lxml import etree
from selenium import webdriver

"""编写下载单张海报的函数"""


def downloadposter(src, id):
    """
        src -- 图片的地址
        id -- 图片的标题
    """
    downloadpath = './webspider/posters/'
    if not os.path.exists(downloadpath):
        os.mkdir(downloadpath)

    dir = downloadpath + str(id) +'66'+ '.webp'

    try:
        pic = requests.get(src, timeout=30)  # 获取图片
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print("图片无法下载")


"""下载海报函数"""


def posterwebspider(postersnums=10, query='王祖贤'):
    """
        postersnums -- 海报数
        query -- 人
    """

    # 这个循环为了循环翻页时用
    for i in range(0, 150, 15):
        # 创建url
        url = 'https://search.douban.com/movie/subject_search?search_text= %s &cat=1002&start=%s' % (query, str(i))

        # 通过WebDriver创建一个谷歌浏览器的drive, 并且通过drive获取访问页面的完整HTML
        driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
        driver.get(url)
        html = etree.HTML(driver.page_source)

        # 获取海报和电影标题的XPath
        # 使用xpath helper, ctrl+shit+x 选中元素，如果要匹配全部，则需要修改query 表达式
        src_xpath = "//div[@class='item-root']/a[@class='cover-link']/img[@class='cover']/@src"
        title_xpath = "//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']"

        # 从获取的HTML页面中解析出XPath
        srcs = html.xpath(src_xpath)
        titles = html.xpath(title_xpath)

        # 开始下载海报
        for src, title in zip(srcs, titles):
            print('\t'.join([str(src), str(title.text)]))
            downloadposter(src, title.text)
            postersnums -= 1
            if postersnums == 0:
                return


"""测试爬虫"""
if __name__ == '__main__':
    name=input("请输入要爬取的人物")
    posterwebspider(20, name)  # # 第一个参数代表多少张， 第二个参数代表人物名
