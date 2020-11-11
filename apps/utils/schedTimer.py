__author__ = 'yecc'
__date__ = '2020/3/23 10:01'

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os


def job():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def time_ago(value):
    if not isinstance(value,datetime):
        return value
    now = datetime.now()
    timestamp = now - value


if __name__ == "__main__":
    import re
    scheduler = BlockingScheduler()
    # scheduler.add_job(job, 'interval', seconds=5)
    # scheduler.start()
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # print(datetime.now().second)
    # print(os.path.join(os.path.curdir, 'all.log'))
    data = {"pr":{'id':88,'name':'uuyuu'},'name':"yyyy","owe":[{'name':'iii','id':88},{'name':'ii0i','id':777}],'m_time':'ddfas'}
    # data.update({'pr':data['pr']['id']})
    ss = "adfad213132"
    print(re.match(r'[^A-Za-z0-9]$',ss))
    s1 = '200'
    print(s1.startswith('2'))