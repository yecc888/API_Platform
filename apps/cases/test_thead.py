__author__ = 'yecc'
__date__ = '2020/10/10 17:02'

from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
from threading import Thread,current_thread
import time,os,asyncio,requests
import datetime

def work():
    res = 1
    for i in range(1,100000):
        res *= i

async def hello():
    time.sleep(2)
    print("hello test")

async def job():
    print('start test')
    print('pause job')
    await hello()
    print('over job')

def get(url):
    print("%s GET %s" %(current_thread().name,url))
    time.sleep(3)
    reponse = requests.get(url)
    if reponse.status_code == 200:
        res = reponse.text
    else:
        res = "下载失败"
    return res

def parse_th(future):
    time.sleep(1)
    res = future.result()
    print("%s 解析结果为%s" %(current_thread().name,len(res)))

def parse_pro(future):
    time.sleep(1)
    res = future.result()
    # print(res)
    print("%s 解析结果为%s" % (os.getpid(), len(res)))



def parse1(res):
    time.sleep(1)
    # res = future.result()
    print("%s 解析结果为%s" % (os.getpid(), len(res)))

if __name__ == '__main__':
    urls = [
        'https://www.baidu.com',
        'https://www.sina.com.cn',
        'https://www.tmall.com',
        'https://www.jd.com',
        'https://www.python.org',
        'https://www.openstack.org',
        'https://www.baidu.com',
        'https://www.baidu.com',
        'https://www.baidu.com',
    ]

# ===============1.同步调用优点解耦合,缺点:速度慢
#     p = ProcessPoolExecutor(9)
#     l = []
#     start = time.time()
#     for url in urls:
#         future = p.submit(get, url)
#         l.append(future)
#     p.shutdown(wait=True)
#
#     for future in l:
#         parse1(future.result())
#     print('完成时间:', time.time() - start)
# ===================================================


# ==================2.异步调用方式：缺点存在耦合，优点速度快
#     start = time.time()
#     print(start)
#     p = ProcessPoolExecutor(os.cpu_count())
#     for i in urls:
#         p.submit(get,i)
#     p.shutdown(wait=True)
#     print('完成时间:',   time.time()- start)



# ===============3.进程池，异步调用+回调函数:解决耦合，速度慢,(异步调用＋回调)
#     start = time.time()
#     p = ProcessPoolExecutor(os.cpu_count())
#     for i in urls:
#         future = p.submit(get,i)
#         future.add_done_callback(parse_pro)
#     p.shutdown(wait=True)
#     print('完成时间:', time.time() - start)










# ------------------4.线程池:异步+回调 ----IO密集型主要使用方式,线程池:执行操作为谁有空谁执行
    p = ThreadPoolExecutor(4)
    start = time.time()
    for url in urls:
        future = p.submit(get,url)
        future.add_done_callback(parse_th)
    p.shutdown(wait=True)
    print("主",current_thread().name)
    print("完成时间",time.time()-start)
# if __name__=="__main__":
    # l=[]
    # print(os.cpu_count())  # 打印本机的核心数
    # start=time.time()
    # for i in range(3):
    #     # p=Process(target=work) #耗时5s多  # 显示多进程程序的执行时间
    #     p=Thread(target=work) #耗时18s多  # 显示多线程程序执行的时间
    #     l.append(p)
    #     p.start()
    #     print(p.is_alive())
    # for p in l:
    #     print(p.name)
    #     print(p.getName())
    #     print(p.is_alive())
    #     p.join()
    # stop=time.time()
    # print('run time is %s' %(stop-start))
    # d1 = {'aa3':555, "tyf":21,"byh":32323,"a":23423}
    # d1.update([('ll',229997772)])
    # print(sorted(d1.items(),key=lambda x:x[0]))
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(job())
