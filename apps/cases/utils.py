__author__ = 'yecc'
__date__ = '2020/5/11 18:16'

from urllib.parse import urlencode, quote
import hashlib,re,random,uuid,time,string

def ordered_data(data):
    """
    对数据进行排序，返回排序好的数据
    :param data:
    :return:
    """
    if data is not {}:
        da = sorted([(k, v) for k, v in data.items()])
        ll = []
        ls = []
        for k, v in enumerate(da):
            if isinstance(v[1], list):
                if len(v[1]) == 0:
                    ll.append(v)
                elif len(v[1]) == 1:
                    if v[1][0] == "":
                        pass
        for j, k in enumerate(ll):
            if k in da:
                da.remove(k)
        for i, m in enumerate(da):
            if isinstance(m[1], list):
                if len(m[1]) >= 1:
                    for li in m[1]:
                        if isinstance(li, dict):
                            sd = ordered_data(li)
                            ls.append(sd)
                            key = da[i][0]
                            da.pop(i)
                            da.insert(i, (key, ls))
            elif isinstance(m[1], dict):
                in_da = sorted(m[1].items(), key=lambda x:x[0])
                s = dict(in_da)
                da.pop(i)
                da.insert(i,(m[0],s))


    else:
        da = data
    return da


class doDatas(object):
    """
    处理数据，生成sign
    """
    # 单列模式
    # _instance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super(doDatas, cls).__new__(cls)
    #     return cls._instance

    def __init__(self, data, appid, appkey, v, ts):
        self.data = data
        self.ts = ts
        self.v = v
        self.appid = appid
        self.appkey = appkey

    def join_data(self):
        """
        对数据进行排序，返回排序好的数据
        :param data:
        :return:
        """
        joining_data = ordered_data(self.data)
        sa = ''
        if joining_data is not {}:
            for index, item in enumerate(joining_data):
                if isinstance(item[1], list):
                    for i, v in enumerate(item[1]):
                        key = item[0]
                        if isinstance(v, list):
                            if isinstance(v[0], tuple):
                                for j, k in enumerate(v):
                                    if isinstance(k[1], list):
                                        for x, y in enumerate(k[1]):
                                            sa += "{0}[{1}][{2}][{3}]={4}&".format(key, i, k[0], x, y)
                                    else:
                                        sa += "{0}[{1}][{2}]={3}&".format(key, i, k[0], k[1])
                        else:
                            # for m, n in enumerate(item[1]):
                            sa += "{0}[{1}]={2}&".format(key, i, v)
                elif isinstance(item[1], dict):
                    keys = item[0]
                    for key,vs in item[1].items():
                        sa += "{0}[{1}]={2}&".format(keys, key, vs)
                else:
                    sa += "{0}={1}&".format(item[0], item[1])
            return sa.rstrip('&')
        else:
            return joining_data

    def qute_data(self):
        """
        urlencode,= | &,不进行操作
        :param data:
        :return:
        """
        q_data = self.join_data()
        if q_data:
            q_data = q_data.replace('False', '0').replace('True', '1')
            q_data = q_data.replace('false', '0').replace('true', '1')
            return quote(q_data, safe="= | &")
        else:
            return q_data

    @property
    def sign_data(self):
        """
        生成sign
        :return:
        """
        data = self.qute_data()
        if data:
            URL_TMP = '{}&appid={}&appkey={}&v={}&ts={}'
            md5_data = URL_TMP.format(data,self.appid,
                                      self.appkey,self.v,self.ts)
        else:
            URL_TMP = 'appid={}&appkey={}&v={}&ts={}'
            md5_data = URL_TMP.format(self.appid,
                                      self.appkey,self.v,self.ts)
        md5_object = hashlib.md5()
        md5_object.update(md5_data.encode('utf-8'))
        return str(md5_object.hexdigest()).lower()


def generate_randint(min,max):
    """
    产生随机数
    :param min: 最小值
    :param max: 最大值
    :return:
    """
    if min and max:
        return random.randint(min,max)
    else:
        return random.randint(0,999999)


def generate_timestamp():
    """
    返回当前时间戳
    :return:
    """
    return int(time.time())


def generate_uuid(uuidFormt=None):
    """
    返回指定类型的uuid
    :param uuidFormt:
    :return:
    """
    if uuidFormt:
        return str(uuid.uuid4()).replace('-', str(uuidFormt))
    else:
        return str(uuid.uuid4())


def generate_data(dataFormt=None):
    """
    返回指定类型的日期格式
    :param dataFormt:
    :return:
    """
    if dataFormt:
        return time.strftime(str(dataFormt),time.localtime())
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def generate_strings(str_type=None,lenth=None):
    """
    返回指定类型的字符串
    :param str_type:
    :param lenth:
    :return:
    """
    lowcase = string.ascii_lowercase  # 所有大写字母
    uppcase = string.ascii_uppercase  # 所有小写字符
    digits = string.digits  # 数字 0-9
    # 小写字符串
    if str_type == 1:
        if lenth:
            return ''.join(random.sample(lowcase,lenth))
        else:
            return ''.join(random.sample(lowcase,8))
    # 大写字符串
    elif str_type == 2:
        if lenth:
            return ''.join(random.sample(uppcase,lenth))
        else:
            return ''.join(random.sample(uppcase,8))
    # 大小写字符
    elif str_type == 3:
        if lenth:
            return ''.join(random.sample(string.ascii_letters,lenth))
        else:
            return ''.join(random.sample(string.ascii_letters,8))
    # 字母和数字
    else:
        if lenth:
            return ''.join(random.sample(string.ascii_letters + string.digits,lenth))
        else:
            return ''.join(random.sample(string.ascii_letters + string.digits,8))


def get_customParas(args):
    """
    获取arg参数
    :param args:
    :return:
    """
    return args.replace('${__','').replace('}','')



if __name__ == "__main__":
    ss = {"cno": "1353210023779896", "shop_id": 1905736354, "cashier_id": "1180940478", "consume_amount": 10000,
          "sub_balance": 0, "sub_credit": 2, "deno_coupon_ids": [], "gift_coupons_ids": [], "payment_amount": 0,
          "credit_amount": 0, "payment_mode": 1, "count_num": 1, "biz_id": 8036, "table_id": "A023", "tags": ["tt","eeeed"],
          "products": [{"name": "酸菜鱼", "no": 219830, "num": "1", "price": "2000", "is_activity": 1, "coupons_ids": [],
                        "tags": ["测试cl"]}]}
    s0 = {"cno":1113212, "cashier_id":"-1", "shop_id":1706625831, "type":1, "credit":1, "biz_id":9851308882,"remark":"heihei"}
    d1= {"name":"礼品券测试55555","type":2,"deno_type":1,"coupon_bg":{"logo":"https://welifepublicmedias.oss-cn-beijing.aliyuncs.com/welife-marketing/e1289cdb-97b6-429c-9625-dbaf3d691cfa.jpg", "background":"https://welifepublicmedias.oss-cn-beijing.aliyuncs.com/welife-marketing/0ce5dfc0-5d3b-43ec-8f52-2f1dfd9e9cb5.jpg"},"valid_data":"relative,20,1","creator":1111741635,"enable_amount":50000,"max_use":2,"products":[1342,3243],"mix_use":2,"limit_coupon":[{"couponId":"8890731","name":"10元代金券ymm","aaaar":1121}]}
    nm = {
    "coupon_code":"3056952818649102",
    "cashier_id": -1,
    "is_verification": "false",
      "repeal":"false",
        "from":1
}
    s1 = doDatas({},'dp0Rm4wNl6A7q6w1QzcZQstr','b16058ee2fcdfec8f033c1ec0aff200e','2.0','1589160854')
    s2 = doDatas(nm,'dp0Rm4wNl6A7q6w1QzcZQstr','b16058ee2fcdfec8f033c1ec0aff200e','2.0','1603100246')
    s3 = doDatas(ss,'dp0Rm4wNl6A7r','b16058ee2fcdfec8f033c1ec0aff200e','2.0','1589160854')
    s5 = doDatas(d1,'dp0Rm4wNl6A7r','b16058ee2fcdfec8f033c1ec0aff200e','2.0','1589160854')
    print(s2.sign_data)

    m = {
    "name": "转增测试",
    "type": 1,
    "summary": "测试试试",
    "deno_type": 0,
    "deno": 18800,
    "coupon_bg": {
        "logo": "https://welifepublicmedias.oss-cn-beijing.aliyuncs.com/welife-marketing/e1289cdb-97b6-429c-9625-dbaf3d691cfa.jpg"
    },
    "valid_data": "absolute,2020-10-11,2020-12-01",
    "creator": 1891059688,
    "shop_list": "ALL",
    "limit_type": 0,
    "enable_amount": 5000,
    "use_week_day": [],
    "max_use": 2,
    "products": [111],
    "use_scope": 1,
    "give_friend": 0,
    "mix_use": 1,
    "limit_coupon": [
        {
            "couponId": "8890731",
            "name": "10元代金券ymm"
        }
    ]
}
    # print(ordered_data(ss))
    # s5.join_data()
    # import string
    # print(s2.join_data())
    # print(id(s1),id(2),id(s3))
    # print(s1.sign_data)
