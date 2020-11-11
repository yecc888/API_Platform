__author__ = 'yecc'
__date__ = '2019/12/5 11:22'

import psycopg2
import random
import datetime,time
import multiprocessing
import re
from API_PLATFORM.settings import REGEX_MOBILE
from db_tools.wsgData import doExcel

def pase():
    conn = psycopg2.connect(database='yxd-test', user='postgres',
                            password='wsg@pg#', host='123.57.63.39', port='5432')
    cur = conn.cursor()
    return conn,cur


def connect_pg(ids):
    conn = psycopg2.connect(database='yxd-test', user='postgres',
                            password='wsg@pg#', host='123.57.63.39', port='5432')
    cur = conn.cursor()
    ids = 3296958114107730000 + ids
    task_statuss = 2

    # 店长已完成
    dianzhang = "INSERT INTO task_record(id, assess_id, assess_name, start_time, end_time, role_id, role_name, store_id, store_name, task_status, task_template_id, score, state, create_time, createby, create_user, modify_time, modifyby, modify_user, delete_time, deleteby, delete_user)" \
         "VALUES ({0}, 1196732036093202433, '19日测试任务', '18:23', '18:28', 1196728507580436482, '收银员', 1196728832504778753, '奥森旗舰店', {1}, 1196733491843846145, NULL, 1, '2019-12-06', 1196734110730178561, '刘收银员', '2019-12-06', 1196734110730178561, '刘收银员', NULL, NULL, NULL)".format(ids,task_statuss)

    # 店长进行中
    dianzhang_3 = "INSERT INTO task_record(id, assess_id, assess_name, start_time, end_time, role_id, role_name, store_id, store_name, task_status, task_template_id, score, state, create_time, createby, create_user, modify_time, modifyby, modify_user, delete_time, deleteby, delete_user)" \
                  "VALUES (1196958114107772908, 1196732036093202433, '19日测试任务', '18:23', '18:28', 1196728507580436482, '收银员', 1196728832504778753, '奥森旗舰店', 3, 1196733491843846145, NULL, 1, '2019-12-05', 1196734110730178561, '刘收银员', '2019-11-20', 1196734110730178561, '刘收银员', NULL, NULL, NULL)"

    cur.execute(dianzhang)
    # rows = cur.fetchall()

    conn.commit()
    conn.close()

def connect_pg1(ids):
    conn = psycopg2.connect(database='yxd-test', user='postgres',
                            password='wsg@pg#', host='123.57.63.39', port='5432')
    cur = conn.cursor()
   # 收银员
    ids = 2496958114107790000 + ids
    task_statuss = 2
    shouyin = "INSERT INTO task_record(id, assess_id, assess_name, start_time, end_time, role_id, role_name, store_id, store_name, task_status, task_template_id, score, state, create_time, createby, create_user, modify_time, modifyby, modify_user, delete_time, deleteby, delete_user) " \
              "VALUES ({0}, 1197705065058594817, '22日周任务', '11:06', '11:12', 1196728467294146561, '店长', 1196729132984717314, '天安门店', {1}, 1197705557641850882, NULL, 1, '2019-12-06', 1196733888683724802, '李店长', '2019-12-06', 1196733888683724802, '李店长', NULL, NULL, NULL)".format(ids,task_statuss)

    cur.execute(shouyin)
    # rows = cur.fetchall()

    conn.commit()
    conn.close()

def run_pg1():
    pool = multiprocessing.Pool(processes=4)
    pool.map(connect_pg, range(1000,1050))
    # pool.map(connect_pg1, range(1000,1050))



def updata():
    conn = psycopg2.connect(database='yxd-test', user='postgres',
                            password='wsg@pg#', host='123.57.63.39', port='5432')
    cur = conn.cursor()
    deldata = "delete from task_record"
    cur.execute(deldata)
    # rows = cur.fetchall()

    conn.commit()
    conn.close()


def generate_rule(fiels,sheet):
    conn = psycopg2.connect(database='aoqiwei', user='postgres',
                            password='wsg@pg#', host='47.93.99.61', port='5432')
    cur = conn.cursor()
    e = doExcel(fiels,sheet)
    datas = e.read_from_excel()[1]
    for da in datas:
        ids = int(da[0])
        target_rule_id = int(da[1])
        predict_value = str(da[2])
        reach_value = str(da[3])
        reach_rate = da[4]
        store_id = int(da[5])
        times = da[6]
        times = times.date()
        modify_time = datetime.datetime.utcnow()
        create_time = datetime.datetime.utcnow()
        s = datetime.datetime.now().date()
        times = times.strftime('%Y-%m-%d')
        # times = datetime.datetime.strptime(times,'%Y-%m-%d')
        # data1 = "INSERT INTO target_reach(id, target_rule_id, predict_value, reach_value, reach_rate, reason, brand_id, " \
        #     "area_id, store_id, market_separation_id, state, create_time, createby, modify_time, modifyby, delete_time, " \
        #     "deleteby, create_user, modify_user, delete_user) VALUES ({}, {}, {}, {}, {:.2f}, NULL, 1280451715635679234, 1270621473534447618, {}, NULL, 1, {}, 1270647914993094657,'2020-01-01' , 1270647914993094657, NULL, NULL, '奥森店店长', '奥森店店长', NULL)".format(ids,target_rule_id,predict_value,reach_value,reach_rate,
        #                                                  store_id,times)

        data2 = "INSERT INTO target_reach(id, target_rule_id, predict_value, reach_value, reach_rate, reason, brand_id, " \
            "area_id, store_id, market_separation_id, state, create_time, createby, modify_time, modifyby, delete_time, " \
            "deleteby, create_user, modify_user, delete_user) VALUES (%(ids)s, %(target_rule_id)s, %(predict_value)s, %(reach_value)s, %(reach_rate)s, NULL, 1280451715635679234, 1270621473534447618, %(store_id)s, NULL, 1, %(create_time)s, 1270647914993094657, %(modify_time)s, 1270647914993094657, NULL, NULL, '奥森店店长', '奥森店店长', NULL)"

        cur.execute(data2,{'ids': ids, 'target_rule_id':target_rule_id,
                           'predict_value': predict_value,
                           'reach_value': reach_value,
                           'reach_rate': reach_rate,
                           'store_id': store_id,
                           'create_time': times,
                           'modify_time': times})
        conn.commit()
    cur.close()
    conn.close()


def pgdb(dbname):
    '''
    连接pg数据库
    :param dbname: 数据库名称
    :return:
    '''
    return psycopg2.connect(database=dbname, user='postgres',
                            password='wsg@pg#', host='47.93.99.61', port='5432')


def upper_level(username,shopname):

    try:
        conn = pgdb('wsg')
        cur = conn.cursor()
        shopperid_sql = "SELECT id from users WHERE name= %(username)s and role_id = '1311198606765658114'"
        storeid_sql = "SELECT id FROM store WHERE name = %(shopname)s"
        cur.execute(shopperid_sql,{'username':username})
        shopperid = cur.fetchone()
        if shopperid:
            shopperid = cur.fetchone()[0]
            cur.execute(storeid_sql,{'shopname':shopname})
            storeid = cur.fetchone()[0]
            u1 = "SELECT id from users where id in ( SELECT user_id from user_store WHERE store_id= %(storeid)s and user_id<> %(shopperid)s) and role_id<>'1311198606765658114'"
            cur.execute(u1,{'storeid':storeid,'shopperid':shopperid})
            usersid =  cur.fetchall()
            updated_sql = "UPDATE users set parent_id = %(shopperid)s WHERE id = %(id)s"

            for user in usersid:
                sql_id = user[0]
                cur.execute(updated_sql,{'shopperid':shopperid,'id':sql_id})
                conn.commit()
    except psycopg2.DatabaseError as ex:
        pass
    finally:
        cur.close()
        conn.close()


def com_shop(shopname):
    conn = pgdb('wsg')
    cur = conn.cursor()
    storeid_sql = "SELECT id FROM store WHERE name = %(shopname)s"
    cur.execute(storeid_sql, {'shopname': shopname})
    shopperid = cur.fetchone()
    count  = 0
    if shopperid:
        count += 1
    return count











def job(v,num,lock):
    # 进程锁，共享数据不会发生争抢
    lock.acquire()
    for i in range(6):
        time.sleep(0.1)
        v.value+=num
        print(v.value)
    lock.release()

def job1(v,num):
    for i in range(6):
        time.sleep(0.1)
        v.value+=num
        print(v.value)


def run_job1():
    val = multiprocessing.Value('i', 0)
    t1 = multiprocessing.Process(target=job1, args=(val, 1))
    t2 = multiprocessing.Process(target=job1, args=(val, 3))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def run_job():
    # 进程锁，共享数据不会发生争抢
    lock = multiprocessing.Lock()
    val = multiprocessing.Value('i', 0)
    t1 = multiprocessing.Process(target=job, args=(val, 1, lock))
    t2 = multiprocessing.Process(target=job, args=(val, 3, lock))
    t1.start()
    t2.start()
    t1.join()
    t2.join()



if __name__ == "__main__":
    # print(re.match(REGEX_MOBILE,'13584444664'))
    # print(re.match(r"^1[35789]\d{9}$", '135875594955'))
    import logging
    # updata()
    statrt_time = datetime.datetime.now()
    # for i in range(1000,5000):
    #     ids = 1196958114107770000 + i
    #     ids1 = 1196958114107970000 + i
    #     connect_pg(ids,random.randint(1,3))
    #     connect_pg1(ids1,random.randint(1,3))
    fiels = 'C:\\Users\Administrator\Desktop\data5.xlsx'
    # e = doExcel(fiels,'Sheet1')
    # s = e.read_from_excel()

    # generate_rule(fiels,'tangshi')
    # generate_rule(fiels,'waimai')
    # generate_rule(fiels,'huiyuan')
    # delt = (datetime.datetime.now()-statrt_time).seconds
    # print(delt)
    upper_level('符史豪', '奥体东门')

