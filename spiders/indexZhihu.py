import collections
import traceback

import pymysql

from firstDemo.spiders.models import find_name, find_visit, find_author, get_driver_url_content, extract_urls, \
    modify_urls
# 打开各个问题所对应的URL，打开页面，读取信息
from firstDemo.spiders.mysql_connect import insert_tuple


def check_url(question_url, mid_urls) :
    website = get_driver_url_content(question_url)
    name = find_name(website)
    followers, visited = find_visit(website)
    uid, username = find_author(website)
    species = -1
    for i in range(0, len(mid_urls)) :
        if question_url in mid_urls[i] :
            species = i
    # 将问题信息打包成dict
    integrated_info = {'type' : species,
                       'ques_url' : question_url,
                       'ques_name' : name,
                       'followers' : followers,
                       'visited_times' : visited,
                       'answerer_id' : uid,
                       'answerer_name' : username
                       }
    return integrated_info


# 获取每个问题目录下问题的链接
def get_all_problem_urls(collect_urls) :
    print('Start searching url')
    all_problem_urls = []
    for url in collect_urls :
        bsObj = get_driver_url_content(url)
        urls = extract_urls(bsObj)
        modified_urls = modify_urls(urls)
        all_problem_urls.append(modified_urls)
        print("We have done one!")
    print('ALL urls searched')
    return all_problem_urls

"""
def collect_required_info(url_list) :
    try :
        all_info = []
        count = 0
        for url_set in url_list :
            part_info = []
            for url in url_set :
                start = time.time()
                info = check_url(url)
                all_info.append(info)
                end = time.time()
                print("No.", (count + 1), " page")
                count += 1
                print(end - start, "seconds")
            all_info.append(part_info)
        return all_info
    except Exception :
        traceback.print_exc()
"""


# 将所有的条目插入数据库
def insert_all_into_db(info_queue: collections.deque, db: pymysql.connections.Connection) :
    try :
        for i in range(0, len(info_queue)) :
            mid = info_queue.popleft()
            insert_tuple(mid, db)
            print('No.', (i+1))
    except Exception:
        traceback.print_exc()
