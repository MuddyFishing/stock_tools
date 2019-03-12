# -*-coding=utf-8-*-
# 股市黑名单
from setting import get_mysql_conn,llogger,DATA_PATH
import os
import codecs

logger = llogger(__file__)

def create_tb(conn):
    cmd = '''CREATE TABLE IF NOT EXISTS `tb_blacklist` (DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,CODE VARCHAR(6) PRIMARY KEY,NAME VARCHAR(60),REASON TEXT);'''
    cur = conn.cursor()

    try:
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        logger.info(e)
        conn.rollback()


def update_data(filename,conn):
    cur = conn.cursor()

    with codecs.open(filename, 'r',encoding='utf8') as f:
        content = f.readlines()
    if not content:
        return

    for line in content:
        (code, name, reason) = line.strip().split(';')
        cmd = '''INSERT INTO `tb_blacklist` (CODE,NAME,REASON) VALUES (\"%s\",\"%s\",\"%s\")''' % (code, name, reason)

        try:
            cur.execute(cmd)

            conn.commit()

        except Exception as e:
            logger.info(e)
            logger.info('dup code {}'.format(code))
            conn.rollback()
            continue
        else:
            logger.info('insert successfully {}'.format(name))


# 调试
def get_name_number():
    filename = os.path.join(DATA_PATH, 'blacklist.csv')

    with codecs.open(filename, 'r', encoding='utf8') as f:
        content = f.readlines()
    if not content:
        return
    logger.info('len of content {}'.format(len(content)))
    code_list = []
    for i in content:
        code_list.append(i.split(';')[0])
    logger.info(code_list)
    logger.info(len(set(code_list)))

    # 找出重复

    seen = set()
    dup_list = []
    for i in code_list:
        if i in seen:
            dup_list.append(i)
        else:
            seen.add(i)
    logger.info('dup item {}'.format(dup_list))

def main():
    filename = os.path.join(DATA_PATH, 'blacklist.csv')
    # 本地更新
    logger.info('update local')
    db_name = 'db_stock'
    conn = get_mysql_conn(db_name, local='local')
    create_tb(conn)
    update_data(filename,conn)

    # 远程更新
    # db_name = 'db_stock'
    logger.info('update remote')
    remote_conn = get_mysql_conn('', local='ali')
    create_tb(remote_conn)
    update_data(filename,remote_conn)


if __name__ == '__main__':
    main()
    # get_name_number()