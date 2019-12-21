import argparse

from firstDemo.spiders.indexZhihu import get_all_problem_urls, insert_all_into_db
from firstDemo.spiders.multithread import multi_check_info
from firstDemo.spiders.mysql_connect import connect_mysql, close_mysql
from firstDemo.spiders.toXlsx import read_mysql_to_xlsx


def main(config) :
    # 四个知乎目标网页的URL
    mianshi_url = 'https://www.zhihu.com/search?type=content&q=%E9%9D%A2%E8%AF%95'
    shixi_url = "https://www.zhihu.com/search?type=content&q=%E5%AE%9E%E4%B9%A0"
    zhaogongzuo_url = "https://www.zhihu.com/search?type=content&q=%E6%89%BE%E5%B7%A5%E4%BD%9C"
    jianli_url = "https://www.zhihu.com/search?type=content&q=%E7%AE%80%E5%8E%86"

    # 将四个搜索页面的URL组合起来，得到一个数组
    macro_urls = [mianshi_url, shixi_url, zhaogongzuo_url, jianli_url]
    # 获取这四个搜索页面下所得到的的问题的URL
    mid_urls = get_all_problem_urls(macro_urls)
    # 从收集到的各个问题URL中，获取最终信息
    collected_info = multi_check_info(mid_urls)
    # 将queue.Queue类型转换为deque
    mid_queue = collected_info.queue
    # 连接mysql数据库
    db = connect_mysql(db_addr=config.db_addr, db_user=config.db_user, db_passwd=config.db_passwd,
                       db_name=config.db_name)
    # 将所有数据插入
    insert_all_into_db(mid_queue, db)
    # 将数据导出到xlsx文件
    read_mysql_to_xlsx('latestResult.xlsx', db)
    # 关闭数据库连接
    close_mysql(db)


if __name__ == '__main__' :
    # 通过命令行传入启动参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_addr', type=str, default='localhost')
    parser.add_argument('--db_user', type=str, default='root')
    parser.add_argument('--db_passwd', type=str, default='990916')
    parser.add_argument('--db_name', type=str, default='zhihu')
    config = parser.parse_args()
    # 按照启动参数运行主函数
    main(config)
