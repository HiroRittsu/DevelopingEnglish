import mysql.connector

conn = None
cur = None

def __init__(database):
    global conn, cur
    '''
    :param database:
    '''
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='linebot',
        password='',
        database=database,
    )

    connected = conn.is_connected()
    if (not connected):
        conn.ping(True)
    cur = conn.cursor(buffered=True)

def insert(sql, datas):
    global conn, cur
    '''
        -example-
        sql = 'insert into test values (%s, %s)'
        datas = [
            (2, 'foo'),
            (3, 'bar')
        ]
    :param sql:
    :param datas:
    :return:
    '''
    cur.execute(sql, datas)
    conn.commit()
