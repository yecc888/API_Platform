__author__ = 'yecc'
__date__ = '2020/4/26 10:34'

import requests,time
import xlsxwriter, xlwt, xlrd,openpyxl
from ruamel import yaml
import os,threading
from copy import deepcopy
from faker import Faker
import random,threading,re
from multiprocessing import Pool
from concurrent.futures.thread import ThreadPoolExecutor

host = "http://yxd.acewill.cn:8095"


def get_yaml(dirs=None, filename=''):

    with open(filename, mode='r', encoding='utf-8') as f:
        contents = f.read()
    data = yaml.safe_load(contents)
    return data


class doExcel(object):

    def __init__(self,excelName,sheetName):
        self.excel = excelName
        self.sheet = sheetName
    # 打开excel，并选择sheet页

    def open(self):
        try:
            self.openedExcel = openpyxl.load_workbook(self.excel)
            if self.sheet:
                self.openedSheet = self.openedExcel[self.sheet]
                return self
            else:
                self.openedSheet = self.openedExcel.active
                return self
        except Exception:
            raise

    # 保存
    def save(self):
        self.openedExcel.save(self.excel)
        return self

    def colse(self):
        self.openedExcel.close()
        return self

    def write_to_excle_cell(self,row,col,value):
        """
        :param row:
        :param col:
        :param value:
        :return:
        """
        self.openedSheet.cell(row=row, column=col, value=value)
        # self.save()
        return self


    def write_to_excel_rows(self,data):
        """
        按行写入
        :param data: list,dict,tuple
        :return:
        """
        self.openedSheet.append(data)
        # self.save()
        return self

    def read_from_excel(self, flag='rows'):
        """
        读入文件
        :param flag: rows,按行读；col，按列读
        :return:list
        """
        self.open()
        rows = list(self.openedSheet.rows)
        cols = list(self.openedSheet.columns)
        if flag == 'rows':
            area = []
            title = []
            for i in rows[0]:
                    title.append(i.value)
            for row in rows[1:]:
                rdata = []  # 单行数据
                for r in row:
                    rdata.append(r.value)
                area.append(rdata)
            self.colse()
            return title, area
        else:
            area = []
            title = []
            for col in cols:
                ldata = []  # 单列的所有数据
                for l in col:
                    ldata.append(l.value)
                area.append(ldata)
            self.colse()
            return area

    def read_yeild_excel(self, flag='rows'):
        """
        读入文件
        :param flag: rows,按行读；col，按列读
        :return:list
        """
        self.open()
        rows = list(self.openedSheet.rows)
        cols = list(self.openedSheet.columns)
        if flag == 'rows':
            area = []
            title = []
            for i in rows[0]:
                    title.append(i.value)
            for row in rows[1:]:
                rdata = []  # 单行数据
                for r in row:
                     yield r.value
            #     area.append(rdata)
            # self.colse()
            # return title, area
        else:
            area = []
            title = []
            for col in cols:
                ldata = []  # 单列的所有数据
                for l in col:
                    yield l.value
                    # ldata.append(l.value)

                # area.append(ldata)
            # self.colse()
            # return area


def send(area):
    headers = {}
    headers['Cookie'] = "JSESSIONID=9b19f872-99eb-4f9f-9da9-e5068afc7fc1"
    url = "http://123.57.63.39:9077/wsg/api/addArea"
    datas = {"title":"新增","brandId":"1297046340215312399","parentId":"1308941062345134078","name":area,"areaLevel":"2"}
    req = requests.post(headers=headers,url=url,json=datas)
    return req.status_code


def login(phone):
    url = "http://123.57.63.39:9079/app/api/login"
    data = {"tenant":"test","account":str(phone),"password":"123456"}
    urlq = "http://123.57.63.39:9079/app/api/findCurrentUserStores"
    time.sleep(1)
    req = requests.post(url=url,json=data)
    if req.status_code == 200:
        s = dict(req.headers)['Set-Cookie']
        cookie = s.split(";")[0]
        headers = {'Cookie':cookie}
        req1 = requests.get(url=urlq,headers=headers)
        storeid = req1[0]['id']

    else:
        cookie = None
        print('error')
    return cookie


def updateShops():
    headers = {}
    headers['Cookie'] = "JSESSIONID=6cfec19a-d232-4591-b159-e310b15bdf55"
    url = "http://123.57.63.39:8077/wsg/api/getStoreArchives"
    par = {"pageNum":1,"name":'', "pageSize": 10}
    req = requests.get(url=url,params=par,headers=headers)
    data = req.json()
    url2 = "http://123.57.63.39:8077/wsg/api/updateStoreArchives"
    records1 = data['data']['records']
    if records1:
        for item in records1:
            item['circleIds']=['1']
            datas  = item
            reqq = requests.post(url=url2,json=datas,headers=headers)
            print(reqq)



    print(req)







def getTaskAssItem(ids):
    TaskAssItemfile = 'C:/Users/Administrator/Downloads/test.xlsx'
    cookie = ".AspNetCore.Antiforgery.cNBjir4wSBg=CfDJ8G9CDFDoJ_FElllKKpcnQohpP2Og13HacVm2s64RiqfEe6bttJfVEjXmiEcfvkj4KW_fl_ZHMoxHTtAqh31tssTS1M4EKRHtP1iMJ-K-lBjKSqgB60_YfduOL8CjPj-IGzMNsWHaY72AzTk0HMsGljs; .AspNet.Consent=yes; .AspNetCore.Session=CfDJ8G9CDFDoJ%2FFElllKKpcnQohf99O5ipr2chsh5NxGf13lGbhFOIhBgmoeXZwxnPPXDag%2FuxVQHH7imrOxPT6MTmY1wya%2ByytdBcvjVb41SI7%2BrWEtcmTcCe%2Fn%2BsvV9vTUj9OWQHgALDr%2F2HUBPwVE7kUxiQTsc92C4gkGUWTBluFi"
    RequestVerificationToken= "CfDJ8G9CDFDoJ_FElllKKpcnQogq7JzCu69ewzkhJzD1hdH_1MCZiLFHjeiaHpzam3aY6D4YhquqVI6-4BjQCl9vTY6QkkxbrcC1J02j3tfkZkr-PRgjZvIYKtCgZA5Wp1po0yqA4gUyC6jE3_riOf3Cpuk"
    Users = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    url = 'http://yxd.acewill.cn:8095/Main/Task/AssItem?handler=LoadItems'
    headers = {"User-Agent": Users, "RequestVerificationToken": RequestVerificationToken, "Content-Type": "application/json"
               ,"Cookie":cookie
               }

    datalist = []
    url1 = "http://yxd.acewill.cn:8095/Main/Task/AssItem?handler=LoadItem&id={0}".format(ids)
    try:
        req2 = requests.get(url=url1,headers=headers)
        if req2.status_code == 200:
            assItemData = req2.json()['data']['assItem']
            # print(assItemData)
            for i,k in assItemData.items():
                # if k!='' and k != None :
                datalist.append(k)
            assItemData1 = req2.json()['data']['options']
            if assItemData1:
                for j ,v in enumerate(assItemData1):
                    datalist.append(v['text'])
                    datalist.append(v['score'])
        return datalist
    except Exception as ex:
        print(ex)


def get_shopps():

    cookie = ".AspNet.Consent=yes; .AspNetCore.Antiforgery.cNBjir4wSBg=CfDJ8FvBCGWrj_lCqV4FOxsy46m4W0ymUXXsay62VNo4XkOWv40BemVG6mGJ1v3HXnh31T2BEImOVDj9r2Hi83cIFJRQmWOTlf6l3_CEIrlLDDS8aLiQBugxSacuWfYU17QjzNEqLXGZPAw_rPdyPisjKmU; .AspNetCore.Session=CfDJ8FvBCGWrj%2FlCqV4FOxsy46ks6Re52mND41okg%2BH6BDFY5fxbGZrdi3J31sy%2FD%2F%2FmReg1Ugewakj5NX1iK8UpX%2BPwxzkzj4OVUKZwFuPSX%2F7Ou8VwUlwrvAg1Tc2ETXpPnm4SR%2FvYC6LzQH%2F8KHw7zEWPKFOWkvnKWGRcl1KyceT8"
    RequestVerificationToken= "CfDJ8FvBCGWrj_lCqV4FOxsy46lIg8qApmaLaulGNGAiX4Gt4VgqrqYEvaULWc1uMuUiDAIUuIxFg33yaC9_XeQGztVuDmMAZXCkgoFXYdgxq6pXuFlrlmVaCcOqvqRMoSJgPUlq-WEKVd2XlWu4-jVxXEM"
    Users = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    headers = {"User-Agent": Users, "RequestVerificationToken": RequestVerificationToken, "Content-Type": "application/json"
               ,"Cookie":cookie
               }

    url = host + '/Main/Maintain/Store?handler=LoadStores'
    shops = 'C:/Users/Administrator/Downloads/shops.xlsx'
    datalist = []
    ex = doExcel(shops,'')
    ex.open()
    try:
        req2 = requests.post(url=url,headers=headers)
        if req2.status_code == 200:
            assItemData = req2.json()['data']
            # print(assItemData)
            for k in assItemData:
                datalist = []
                datalist.append(k['number'])
                datalist.append(k['name'])
                datalist.append(k['bName'])
                datalist.append(k['areaName'])
                datalist.append(k['cityName'])
                datalist.append(k['addr'])
                ex.write_to_excel_rows(datalist)
    except Exception as ex:
        print(ex)


def shops(file):
    ext = doExcel(file,'')
    alldata = ext.read_from_excel()
    data = alldata[1]
    return data
        # reList.append(_data)
    # return reList

def users(file,areaname):
    ext = doExcel(file,'').open()
    area = deepcopy(areaname)
    for i in range(1,2001):
        ext.write_to_excle_cell(i,7,area.pop())
        if not area:
            area = deepcopy(areaname)
    ext.colse()


def users1(file,areaname):
    ext = doExcel(file,'').open()
    fake = Faker('zh_cn')
    num = []
    for i in range(0,5001):
        name = fake.name()
        phone = fake.phone_number()
        shop = random.choice(areaname)
        if phone not in num:
            ext.write_to_excel_rows([name,phone,shop])
            num.append(phone)
    ext.save()
    ext.colse()



def all_users(file,areaname):
    ext = doExcel(file,'').open()
    try:
        for user in areaname:
            ext.write_to_excel_rows(user)
    except Exception as ex:
        print(ex)
    finally:
        ext.save()
        ext.colse()



def single(cls):
    _instance = {}
    def warpper(*args,**kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args,**kwargs)
        return _instance[cls]
    return warpper


class Single(object):
    _lock = threading.Lock()

    def __int__(self,*args,**kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            # 反射，看下是否有_instance属性
            with Single._lock:
                if not hasattr(cls, '_instance'):
                    Single._instance = super().__new__(cls)
            return Single._instance

n=8

def excepts(fn):
    start =time.time()
    i = 0
    def wapper():
        try:
            fn()
        except Exception as ex:
            nonlocal i
            # i = 0
            i += 1
            print(f'{ex.args},{i}')
            if i== n:
                print(f'total time:{round(time.time() -start,2)}')
    return wapper


def excepter(n):
    # 装饰器，指定出现的次数给出提示
    def wappers(fn):
        start=time.time()
        i = 0
        def inner():
            try:
                fn()
            except Exception as ex:
                nonlocal i
                i+=1
                print(f'{ex.args[0]},{i}')
                if i == n:
                    print(f'total time:{round(time.time() - start, 2)}')
        return inner
    return wappers


# @excepts
@excepter(8)
def divide_zero_except():
    time.sleep(0.1)
    j = 1/(40-20*2)

# test zero divived except




class MyThead(threading.Thread):

    def __int__(self,id):

        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        time.sleep(8)
        print(self.id)


if __name__ == "__main__":
    files = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), 'data.yaml')
    # da = get_yaml(dirs=None,filename=files)

    TaskAssItemfile = 'E:\loadtest\\aishop\sforCookie.xlsx'
    shopfile = 'E:\loadtest\\aishop\\forCookie.xlsx'
    import time
#   shops(shopfile)
#     login(18618880014)
    phone = doExcel(shopfile,'').open().read_from_excel(flag='col')[0]
    ext = doExcel(shopfile,'').open()


    for i in phone:
        co = login(i)
        if not co:
            break
        ext.write_to_excel_rows([i,co])
    ext.save()
    ext.colse()


    # for i in area:
    #     print(i)
    # exct = ThreadPoolExecutor(max_workers=40)
    # for data in exct.map(login,phone):
    #     print(data)
    # 多进程并发写入excel
    # for i in range(1,1002):
    #     pool.apply_async(getTaskAssItem,(i,), callback=ex.write_to_excel_rows)
    # pool.close()
    # pool.join()
    # for i in range(1,1002):
    #     ex.write_to_excel_rows(getTaskAssItem(i))
    # time2 = int(time.time()) - time1
    # # ex.colse()
    # print(time2)
    # get_shopps()
    # dt = {}
    # dl = []
    # for i,v in enumerate(ll) :
    #     if '省' in v:
    #         ss = v.split('省')
    #         s1 = ss[0] + '省'
    #         dt[i] = s1
    #         dl.append(s1)
    #     elif '市' in v and '省' not in v:
    #         s = v.split('市')
    #         s2 = s[0] + '市'
    #         dt[i] = s2
    #         dl.append(s2)
    #     else:
    #         dt[i] = v
    #         dl.append(v)
    #
    # for i ,k in enumerate(dl):
    #     i+=3
    #     ex.write_to_excle_cell(i,8,k)
    #     ex.write_to_excle_cell(i,9,k)
    # ex.colse()







