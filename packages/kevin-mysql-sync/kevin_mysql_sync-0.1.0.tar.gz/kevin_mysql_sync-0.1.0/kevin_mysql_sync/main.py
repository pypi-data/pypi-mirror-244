import json
import os

import pymysql.cursors
import dotenv

# 从.env文件中加载所有的配置
dotenv.load_dotenv()

MASTER_HOST = os.environ.get('master_host')
MASTER_PORT = os.environ.get('master_port')
if MASTER_PORT:
    MASTER_PORT = int(MASTER_PORT)
MASTER_USER = os.environ.get('master_user')
MASTER_PASSWORD = os.environ.get('master_password')
MASTER_DB = os.environ.get('master_db')

SLAVE_HOST = os.environ.get('slave_host')
# 转为int类型
SLAVE_PORT = os.environ.get('slave_port')
if SLAVE_PORT:
    SLAVE_PORT = int(SLAVE_PORT)
SLAVE_USER = os.environ.get('slave_user')
SLAVE_PASSWORD = os.environ.get('slave_password')
SLAVE_DB = os.environ.get('slave_db')

CHECK_RESULT_FILE = "check_info.json"

LOG_FILE = "log.txt"

PER_PROCESS_ROWS = 100


# 打印日志信息，并将日志写到文件中
def pl(msg):
    """
    打印日志信息
    :param msg: 日志信息
    """
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")


# 打印程序启动，开始检查
pl("程序启动，开始检查")


def print_connection_info(connection):
    """
    打印数据库连接信息
    :param connection: 数据库连接对象
    """
    pl("===数据库连接信息========================")
    pl("数据库主机地址：%s" % connection.host)
    pl("数据库端口号：%s" % connection.port)
    pl("数据库用户名：%s" % connection.user)
    pl("数据库密码：%s" % connection.password)
    pl("数据库名：%s" % connection.db)
    pl("===========================")


def get_connection(host, port: int, user, password, db):
    """
    获取数据库连接
    :param host: 数据库主机地址
    :param port: 数据库端口号
    :param user: 数据库用户名
    :param password: 数据库密码
    :param db: 数据库名
    :return: 数据库连接对象
    """
    connection = pymysql.connect(host=host,
                                 port=port,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    # 打印数据库连接信息
    print_connection_info(connection)
    return connection


# 获取所有表名
def get_tables(connection) -> list[str]:
    """
    获取所有表名
    :param connection: 数据库连接对象
    :return: 所有表名列表
    """
    with connection.cursor() as cursor:
        sql = "show tables"
        cursor.execute(sql)
        result = cursor.fetchall()
        tables = [row['Tables_in_' + MASTER_DB] for row in result]
        return tables


# 获取指定表的记录数量
def get_table_row_count(connection, table):
    """
    获取指定表的记录数量
    :param connection: 数据库连接对象
    :param table: 表名
    :return: 记录数量
    """
    with connection.cursor() as cursor:
        sql = "select count(*) from %s" % table
        cursor.execute(sql)
        result = cursor.fetchone()
        count = result['count(*)']
        return count


# 获取指定表中从指定行开始的指定数量的记录
def get_records(connection, table, begin, count):
    """
    获取指定表中从指定行开始的指定数量的记录
    :param begin:
    :param connection: 数据库连接对象
    :param table: 表名
    :param count: 记录数量
    :return: 记录列表
    """
    result = []
    with connection.cursor() as cursor:
        sql = "select * from %s limit %s, %s" % (table, begin, count)
        pl(sql)
        count = cursor.execute(sql)
        if count > 0:
            result = cursor.fetchall()
    return result


# 在目标数据库，指定的表中，检查指定主键值的记录是否存在，并返回是否存在
def check_record(connection, table, primary_key, value):
    """
    在目标数据库，指定的表中，检查指定主键值的记录是否存在，并返回是否存在
    :param primary_key:
    :param connection: 数据库连接对象
    :param table: 表名
    :param value: 主键值
    :return: 是否存在
    """
    count = 0
    with connection.cursor() as cursor:
        sql = "select %s from %s where %s = %s" % (primary_key, table, primary_key, value)
        count = cursor.execute(sql)
    # result中是否有记录
    if count > 0:
        return True
    else:
        return False


# 获取指定表的主键
def get_primary_key(connection, table):
    """
    获取指定表的主键
    :param connection: 数据库连接对象
    :param table: 表名
    :return: 主键
    """
    with connection.cursor() as cursor:
        sql = "show create table %s" % table
        cursor.execute(sql)
        result = cursor.fetchone()
        # 打印表结构
        # pl(result['Create Table'])
        # 正则匹配主键
        for line in result['Create Table'].split('\n'):
            if 'PRIMARY KEY' in line:
                # 正则匹配主键
                primary_key = line.split('`')[1]
                return primary_key


# 主程序入口

def main():
    # 源数据库连接
    source_connection = get_connection(MASTER_HOST, MASTER_PORT, MASTER_USER, MASTER_PASSWORD, MASTER_DB)

    # 目标数据库连接
    target_connection = get_connection(SLAVE_HOST, SLAVE_PORT, SLAVE_USER, SLAVE_PASSWORD, SLAVE_DB)

    # 从源数据库中读取所有的表名，存入一个list中
    tables = get_tables(source_connection)

    # 打印当前共有多少个表
    pl("共有%s个表需要检查" % len(tables))

    # 从本地加载检查结果文件，如果文件不存在，则以表名为key, 值为0的字典形式创建文件；如果存在，则加载到一个对象中
    check_result = {}
    if not os.path.exists(CHECK_RESULT_FILE):
        for table in tables:
            check_result[table] = 0
        with open(CHECK_RESULT_FILE, 'w') as f:
            json.dump(check_result, f)
    else:
        with open(CHECK_RESULT_FILE, 'r') as f:
            check_result = json.load(f)

    for table in tables:
        # 如果table的名称以clt_eb_store_order开始，跳过
        # if table.startswith('clt_eb_store_order'):
        #     continue

        pl("数据表：%s 开始检查" % table)

        # 从检查结果中加载进度，并打印
        pl("数据表：%s 已检查%s条" % (table, check_result[table]))

        # 检查目标数据库中是否有指定的表，如果没有则创建表
        # if not target_connection.cursor().execute("select * from %s" % table):
        #     with target_connection.cursor() as cursor:
        #         sql = "create table %s like %s" % (table, table)
        #         cursor.execute(sql)
        #         # 打印，创建的数据表名称
        #         pl("创建数据表：%s" % table)
        #         target_connection.commit()
        # 获取源数据库表中的记录总数
        total_count = get_table_row_count(source_connection, table)

        # 换行打印：当前表名开始检查
        pl("记录总量：%s" % total_count)
        start = 0

        # 如果表为空，退出
        if total_count == 0:
            continue

        # 从检查结果中取当前表的检查进度
        if check_result[table] > 0:
            checks = check_result[table]
            start = checks
            if checks >= total_count:
                pl("数据表：%s 已检查%s条，检查完成" % (table, checks))
                continue
            pl("当前表[%s]已检查%s条记录" % (table, checks))
        else:
            checks = 0

        # 检查目标表和源表记录数是致一致
        total_count_target = get_table_row_count(target_connection, table)
        if total_count == total_count_target:
            # 目标表和源表记录数一致，跳过
            pl("目标表%s记录数[%s]和源表记录数[%s]一致，跳过" % (table, total_count, total_count_target))
            # 在检查结果文件中记录当前检查的进度
            check_result[table] = total_count
            # 并回写到文件中
            with open(CHECK_RESULT_FILE, 'w') as f:
                json.dump(check_result, f)
            continue

        # 获取当前表的主键
        primary_key = get_primary_key(source_connection, table)

        first_records = get_records(source_connection, table, 0, 1)

        fields_list = []
        # 将当前表的所有字段加上引号保存到fields_list中
        # 如：['`id`', '`name`', '`age`']
        # 注意：字段名中不能有引号
        for field in first_records[0].keys():
            fields_list.append('`%s`' % field)

        # 将fields_list中的字段用逗号连接成一个字符串，如：'`id`,`name`,`age`'
        fields = ','.join(fields_list)
        pl("主键：%s，当前共有%s个字段" % (primary_key, len(fields_list)))
        # 拼接sql语句
        sql = "insert into %s (%s) values (%s)" % (
            table, fields, ','.join(['%s'] * len(fields_list)))

        # 如源数据库指定表中从0取记录，每次取指定条数，直到取完
        for begin in range(start, total_count, PER_PROCESS_ROWS):
            # 获取指定表中从指定行开始的指定数量的记录
            records = get_records(source_connection, table, begin, PER_PROCESS_ROWS)

            # 从目标表中查询当前已查出来的记录的第一条和最后最后一条记录是否一致，一致则跳过逐条对比
            records_target = get_records(target_connection, table, begin, PER_PROCESS_ROWS)

            # 对比records中的第一条和records_target中的第一条记录的主键是否一致
            # 对比最后一条记录是否一致
            if records and records_target and len(records) == len(records_target) and (
                    records[0][primary_key] != records_target[0][primary_key] or records[-1][primary_key] !=
                    records_target[-1][primary_key]):
                # 一个列表用来存放未被复制的记录
                not_copy_records = []

                # 遍历记录列表
                for record in records:
                    # 按主键查询指定的记录是否存在
                    is_has = check_record(target_connection, table, primary_key, record[primary_key])
                    # 如果没有记录，则将记录存放到not_copy_records列表中
                    if not is_has:
                        not_copy_records.append(record)

                # 将not_copy_records列表中的记录插入到目标数据库的目标表中
                if len(not_copy_records) > 0:
                    with target_connection.cursor() as cursor:
                        # 将list[dict{}]转为list[tuple()]
                        datas = [tuple(record.values()) for record in not_copy_records]
                        cursor.executemany(sql, datas)
                        # 打印sql语句
                        # for data_row in datas:
                        #     formatted_sql = cursor.mogrify(sql, data_row)
                        #     pl(formatted_sql)

                        # 提交数据
                        pl("本次提交%s条记录" % len(datas))
                        target_connection.commit()
                        # 打印当前成功的条数
                        pl("成功插入%s条记录" % len(datas))
                        # 仅测试时使用
                        # exit(0)
            else:
                # 打印 最后一条记录的id的值
                if records:
                    pl("最后一条记录的id：%s, %s, 一致，跳过对比" % (
                        records[-1][primary_key], records_target[-1][primary_key]))

            checks = begin + len(records)
            # 打印当前的检查位置
            pl("数据表：%s 已检查%s条" % (table, checks))
            # 在检查结果文件中记录当前检查的进度
            check_result[table] = checks
            # 并回写到文件中
            with open(CHECK_RESULT_FILE, 'w') as f:
                json.dump(check_result, f)
    # 关闭所有的数据库连接
    source_connection.close()
    target_connection.close()
    exit(0)


if __name__ == '__main__':
    main()
