import pymysql
import xlwt


# 初始化数据库连接
def get_conn():
    conn = pymysql.connect(host='localhost', port=3306, user='root',
                           passwd='990916', db='zhihu', charset='utf8mb4')
    return conn


# 获取表内所有内容
def query_all(cur, sql, args):
    cur.execute(sql, args)
    return cur.fetchall()


# 将数据库转换至xlsx表格
def read_mysql_to_xlsx(filename, db):
    list_table_head = []
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('data', cell_overwrite_ok=True)
    for i in range(len(list_table_head)):
        sheet.write(0, i, list_table_head[i])

    conn = db
    cur = conn.cursor()
    sql = f"SELECT * FROM zhihu.search_result;"
    results = query_all(cur, sql, None)
    conn.commit()
    cur.close()
    row = 1
    for result in results:
        col = 0
        print(type(result))
        print(result)
        for item in result:
            print(item)
            sheet.write(row, col, item)
            col += 1
        row += 1
    workbook.save(filename)
