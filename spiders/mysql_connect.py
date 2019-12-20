import datetime
import re
import traceback

import pymysql as pms


def connect_mysql(*, db_addr='localhost', db_user='root', db_passwd='990916', db_name='zhihu'):
    db = pms.connect(db_addr, db_user, db_passwd, db_name)
    return db


def insert_tuple(info: dict, db) :
    species = ['面试', '实习', '找工作', '简历']
    today = datetime.date.today().isoformat()
    cursor = db.cursor()
    sql = f"INSERT INTO zhihu.search_result" \
          f"(search_rank,search_terms, question_url, question_title, question_follow_num, " \
          f"question_view_num, question_top_answer_username, question_top_answer_id, create_time) " \
          f" VALUE (null, \"{species[info['type']]}\", \"{info['ques_url']}\", \"{info['ques_name']}\", " \
          f"{int(re.sub(',', '', info['followers']))}, {int(re.sub(',', '', info['visited_times']))}, " \
          f"\"{info['answerer_name']}\", \"{info['answerer_id']}\", \"{today}\");"
    try :
        cursor.execute(sql)
        db.commit()
        print('插入成功')
    except Exception:
        db.rollback()
        print(sql)
        print(traceback.print_exc())


def close_mysql(db):
    db.close()
