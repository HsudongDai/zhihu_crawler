import queue  # 队列模块
import random
import threading  # 多线程模块
import time

from firstDemo.spiders.indexZhihu import check_url

concurrent = 8  # 采集线程数


class Crawl(threading.Thread) :  # 采集线程类
    # 初始化
    def __init__(self, number, req_list, data_list, mid_urls) :
        # 调用Thread 父类方法
        super(Crawl, self).__init__()
        # 初始化子类属性
        self.number = number
        self.req_list = req_list
        self.data_list = data_list
        self.mid_urls = mid_urls
        # 线程启动的时候调用

    def run(self) :
        # 输出启动线程信息
        print('启动采集线程%d号' % self.number)
        # 如果请求队列不为空，则无限循环，从请求队列里拿请求url
        while self.req_list.qsize() > 0 :
            # 从请求队列里提取url
            url = self.req_list.get()
            print('%d号线程采集：%s' % (self.number, url))
            # 防止请求频率过快，随机设置阻塞时间
            time.sleep(random.randint(1, 3))
            # 发起http请求，获取响应内容，追加到数据队列里，等待解析
            info = check_url(url, self.mid_urls)
            self.data_list.put(info)  # 向数据队列里追加


def multi_check_info(mid_urls):
    # 生成请求队列
    req_list = queue.Queue()
    # 生成数据队列 ，请求以后，响应内容放到数据队列里
    data_list = queue.Queue()
    for i in range(0, len(mid_urls)) :
        for j in range(0, len(mid_urls[i])):
            base_url = mid_urls[i][j]
            # 加入请求队列
            req_list.put(base_url)
    # 生成N个采集线程
    req_thread = []
    for i in range(concurrent) :
        t = Crawl(i + 1, req_list, data_list, mid_urls)  # 创造线程
        t.start()
        req_thread.append(t)
    for t in req_thread :
        t.join()
    return data_list
