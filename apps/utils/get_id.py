__author__ = 'yecc'
__date__ = '2020/3/21 13:20'

from collections import OrderedDict
import os,requests,time

def getId_byName(model, name):
    """
    通过name，获取id
    :param model: model
    :param name: name
    :return:
    """
    model_id = model.objects.filter(name=name).values("id")
    if model_id:
        model_id = list(model_id)[0]["id"]
        return model_id
    else:
        return ""


class LRUCache:
    def __init__(self, capacity=128):
        self.orderDict = OrderedDict()
        self.capacity = capacity
def lru_cache():
    pass


def write_tofile(file, data):
    # files = open(file=file,mode="ab")
    if data:
        with open(file=file, mode="a+") as f:
            f.write(data)



def contrast_tradId(event, member_id, inancial_id):
    print("3.24-testdata")
    dirs = os.getcwd()
    files = os.path.join(dirs, "results.txt")
    if member_id == 0 or inancial_id == 0:
        print(0)
    if str(member_id) == str(inancial_id):
        data = "{0} type:{1}={2}".format(event, member_id, inancial_id)
        print(data)
        write_tofile(file=files, data=data)
    else:
        data = "{0} type:{1}！={2}".format(event, member_id, inancial_id)
        print(data)
        write_tofile(file=files, data=data)


def get_webhook_data(url):
    req = requests.get(url=url)
    resultes = req.text
    data = '{"bid":1234567,"event":"user","action":"add","content":{"uid":123,"uName":"haha"}}'
    rs = resultes.replace(data,"")
    mm = rs.count("function")

    print(mm)

if __name__ == "__main__":
    ts = time.time()
    print(int(ts))
    a = [1, 2, 3]
    b = [4, 5, 6, 7]
    print(list(zip(a, b)))
    c={'id':1,'name':'uuy'}
    print(list(zip(c, b)))
    l = [0,1,[2,4],'rrtf']
    l1 = l.copy()
    print(l)
    print(l1)

