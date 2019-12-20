import re
import time

import bs4
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


'''
test_mid_urls = [
    ['https://www.zhihu.com/question/35953016', 'https://www.zhihu.com/question/20602526',
     'https://www.zhihu.com/question/290543744', 'https://www.zhihu.com/question/295572212',
     'https://www.zhihu.com/question/267849861', 'https://www.zhihu.com/question/49088785',
     'https://www.zhihu.com/question/20390946', 'https://www.zhihu.com/question/282880854',
     'https://www.zhihu.com/question/29708629', 'https://www.zhihu.com/question/295453435',
     'https://www.zhihu.com/question/19920401', 'https://www.zhihu.com/question/28058827',
     'https://www.zhihu.com/question/302600406', 'https://www.zhihu.com/question/294078513'],

    ['https://www.zhihu.com/question/28434997', 'https://www.zhihu.com/question/34276390',
     'https://www.zhihu.com/question/22787536', 'https://www.zhihu.com/question/19628805',
     'https://www.zhihu.com/question/62744637', 'https://www.zhihu.com/question/327988343',
     'https://www.zhihu.com/question/341518514', 'https://www.zhihu.com/question/338274193',
     'https://www.zhihu.com/question/30090464', 'https://www.zhihu.com/question/22787536',
     'https://www.zhihu.com/question/20862281', 'https://www.zhihu.com/question/26878695',
     'https://www.zhihu.com/question/30878846', 'https://www.zhihu.com/question/22365131',
     'https://www.zhihu.com/question/30767121', 'https://www.zhihu.com/question/320785005',
     'https://www.zhihu.com/question/20263889', 'https://www.zhihu.com/question/304136206',
     'https://www.zhihu.com/question/21310219', 'https://www.zhihu.com/question/290543744'],

    ['https://www.zhihu.com/question/28476231', 'https://www.zhihu.com/question/29477111',
     'https://www.zhihu.com/question/324367397', 'https://www.zhihu.com/question/295239735',
     'https://www.zhihu.com/question/320784313', 'https://www.zhihu.com/question/54209414',
     'https://www.zhihu.com/question/352205559', 'https://www.zhihu.com/question/21957078',
     'https://www.zhihu.com/question/22873570', 'https://www.zhihu.com/question/319380868',
     'https://www.zhihu.com/question/19963860', 'https://www.zhihu.com/question/34949538',
     'https://www.zhihu.com/question/334053330', 'https://www.zhihu.com/question/20221715',
     'https://www.zhihu.com/question/52398927', 'https://www.zhihu.com/question/63305198',
     'https://www.zhihu.com/question/22679775', 'https://www.zhihu.com/question/292842337',
     'https://www.zhihu.com/question/324367397', 'https://www.zhihu.com/question/21641405',
     'https://www.zhihu.com/question/35953016'],

    ['https://www.zhihu.com/question/19766230', 'https://www.zhihu.com/question/270327306',
     'https://www.zhihu.com/question/23734172', 'https://www.zhihu.com/question/28592283',
     'https://www.zhihu.com/question/19727053', 'https://www.zhihu.com/question/20368865',
     'https://www.zhihu.com/question/296480350', 'https://www.zhihu.com/question/36383870',
     'https://www.zhihu.com/question/307936450', 'https://www.zhihu.com/question/19883567',
     'https://www.zhihu.com/question/347850675', 'https://www.zhihu.com/question/25097618',
     'https://www.zhihu.com/question/19616431', 'https://www.zhihu.com/question/300576878',
     'https://www.zhihu.com/question/26265144', 'https://www.zhihu.com/question/28381582',
     'https://www.zhihu.com/question/20182310']
]
'''


def get_driver_url_content(url, timeout=3) :
    """
    使用浏览器获取动态内容
    :param url:         网页url
    :param timeout:     设置超时
    :return:
    """
    try :
        # 设置启动的Chrome为无桌面、不使用显卡模式
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)
        # 获取网页
        driver.get(url)
        time.sleep(timeout)
        # 使用python自带的html.parser来分割HTML网页
        bsObj = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        # 关闭网页
        driver.close()
        return bsObj
    except selenium.common.exceptions.TimeoutException:
        print('Failed, try again')
        get_driver_url_content(url, timeout=3)
    except AttributeError:
        print('Failed, try again')
        get_driver_url_content(url, timeout=3)


# 提取页面中包含的URL
def extract_urls(bsObj: bs4.BeautifulSoup) :
    # 得到网页HTML的字符串形式
    text = str(bsObj.prettify())
    # 文本中包含很多意外“\n”换行符
    text = re.sub('\n', '', text)
    # 文本中有很多“\\002F”， 其实是“/”，影响识别
    pas = re.sub(r"\\u002F", '/', text)
    mids = re.findall(r"https://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", pas)
    urls = []
    for url in mids :
        if "question" in url \
                and "answer" not in url \
                and "link" not in url :
            urls.append(url)
    return urls


def modify_urls(urls) :
    mids = []
    new_url = ''
    for url in urls :
        if url.find("api") != -1 :
            new_url = url.replace('api', 'www')
            new_url = new_url.replace('questions', 'question')
            if new_url not in mids :
                mids.append(new_url)
            else :
                pass
        else :
            mids.append(url)
    return mids


def find_name(website: bs4.BeautifulSoup) :
    name = website.find(class_='QuestionHeader-title')
    return name.string


def find_visit(website: bs4.BeautifulSoup) :
    visit = website.find_all(class_='NumberBoard-itemValue')
    # 0 是关注者数目， 1是被浏览数目
    return visit[0].string, visit[1].string


def find_author(website: bs4.BeautifulSoup) :
    author_info = website.find(class_="UserLink-link")
    avatar: str = author_info['href']
    avatar = avatar.split('/')[-1]
    alias = author_info.find(class_="Avatar AuthorInfo-avatar")
    alias = alias['alt']
    # avatar是用户ID， alias是用户名
    return avatar, alias
