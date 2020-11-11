__author__ = 'yecc'
__date__ = '2020/4/26 10:34'

import requests
import xlsxwriter, xlwt, xlrd,openpyxl
from ruamel import yaml
import os
from multiprocessing import Pool

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
            else:
                self.openedSheet = self.openedExcel.active
        except Exception:
            raise

    # 保存
    def save(self):
        self.openedExcel.save(self.excel)

    def colse(self):
        self.openedExcel.close()

    def write_to_excle_cell(self,row,col,value):
        """
        :param row:
        :param col:
        :param value:
        :return:
        """
        self.openedSheet.cell(row=row, column=col, value=value)
        self.save()

    def write_to_excel_rows(self,data):
        """
        按行写入
        :param data: list,dict,tuple
        :return:
        """
        self.openedSheet.append(data)
        self.save()

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




if __name__ == "__main__":
    files = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), 'data.yaml')
    # da = get_yaml(dirs=None,filename=files)
    TaskAssItemfile = 'C:/Users/Administrator/Downloads/test4.xlsx'
    import time
    time1 = int(time.time())
    ex = doExcel(TaskAssItemfile,'')
    ex.open()
    pool = Pool(6)
    # 多进程并发写入excel
    for i in range(1,1002):
        pool.apply_async(getTaskAssItem,(i,), callback=ex.write_to_excel_rows)
    pool.close()
    pool.join()
    # for i in range(1,1002):
    #     ex.write_to_excel_rows(getTaskAssItem(i))
    time2 = int(time.time()) - time1
    # ex.colse()
    print(time2)
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







