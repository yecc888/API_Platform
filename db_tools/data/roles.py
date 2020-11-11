__author__ = 'yecc'
__date__ = '2020/9/30 10:35'


import requests
from requests.exceptions import ConnectionError
from db_tools.wsgData import doExcel

def do_roles(name,type):
    url = 'http://60.205.231.173:8077/wsg/api/addRole'
    cok = 'SESSION=MGY0MTNhM2ItMzllZS00NGQ4LWFhZTAtODAxNDFhYTRjODRh; JSESSIONID=0a29b95a-4325-4c8c-b631-ef15b89d5b46'
    da = {'title':'新增', 'name': name, 'type':type}
    headers = {'Cookie': cok}
    try:
        req = requests.post(url=url, data=da, headers=headers)
        if req.status_code == 200:
            return True
    except ConnectionError:
        return False



def change_type(title):
    pass


if __name__ == '__main__':
    do = doExcel('C:\\Users\Administrator\Desktop\\roles.xlsx','test1')
    text = do.read_from_excel()
    role = text[1]
    for index, roles in enumerate(role):
        if not do_roles(roles[0],roles[1]):
            print('go')
            break

