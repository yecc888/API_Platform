import datetime
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
from threading import current_thread
import time, random, os,sys,shutil
import requests,zipfile
import subprocess
from hamcrest import *


class FastBuild:

    def __init__(self, target):
        self.target = target

        # build file
        self.pc_build_file_dir = '/opt/code/ai_stores/stores-web/taskmanager-web/src/main/resources/static'
        self.h5_build_file_dir = '/opt/code/ai_stores/stores-web/taskapp-web/src/main/resources/static'

    def remove_static_files(self):

        if self.target == 'pc':
            removedpath = self.pc_build_file_dir
        else:
            removedpath = self.h5_build_file_dir

        for roots, dirs, fiels in os.walk(removedpath):
            for dir_name in dirs:
                try:
                    shutil.rmtree(os.path.join(roots, dir_name))
                except Exception as ex:
                    print(ex)
            for file_name in fiels:
                if file_name != 'login.html':
                    os.remove(os.path.join(roots, file_name))

    def unzip_dist_files(self):
        p_path = os.getcwd()
        if self.target == 'pc':
            outdir = self.pc_build_file_dir
        else:
            outdir = self.h5_build_file_dir

        for _file in os.listdir(p_path):
            if os.path.isfile(_file):
                if zipfile.is_zipfile(_file):
                    try:
                        files = zipfile.ZipFile(_file)
                        files.extractall(outdir)
                        files.close()
                        os.remove(os.path.join(p_path, _file))
                        break
                    except Exception as ex:
                        pass



    @property
    def copy_files(self):
        """
        replace pc or h5 config files
        :return: none
        """
        cwd = os.getcwd()
        if self.target:
            target = str(self.target).lower()
        else:
            return None

        # cas config
        pc_soure_file = os.path.join(cwd, target, 'WebShiroCasConfiguration.java')
        pc_h5_soure_file = os.path.join(cwd, target, 'WebShiroConfiguration.java')
        ai_store_path = 'ai_stores/stores-common/stores-common-cas/src/main/java/cn/acewill/'
        pc_target_file = os.path.join(cwd, ai_store_path, 'cas/config/WebShiroCasConfiguration.java')
        h5_target_file = os.path.join(cwd, ai_store_path, 'shiro/config/WebShiroConfiguration.java')

        try:
            os.remove(pc_target_file)
            os.remove(h5_target_file)
        except FileNotFoundError as ex:
            pass
        finally:
            shutil.copyfile(pc_soure_file, pc_target_file)
            shutil.copyfile(pc_h5_soure_file, h5_target_file)
            self.remove_static_files()
            self.unzip_dist_files()



def copy_file(target):
    cwd = os.getcwd()
    if target:
        target = str(target).lower()
    else:
        return None
    pc_soure_file = os.path.join(cwd, target,'WebShiroCasConfiguration.java')
    pc_h5_soure_file = os.path.join(cwd, target,'WebShiroConfiguration.java')
    ai_store_path = 'ai_stores/stores-common/stores-common-cas/src/main/java/cn/acewill/'
    pc_target_file = os.path.join(cwd, ai_store_path,'cas/config/WebShiroCasConfiguration.java')
    h5_target_file = os.path.join(cwd, ai_store_path, 'shiro/config/WebShiroConfiguration.java')
    try:
        os.remove(pc_target_file)
        os.remove(h5_target_file)
    except FileNotFoundError as ex:
        pass
    finally:
        shutil.copyfile(pc_soure_file, pc_target_file)
        shutil.copyfile(pc_h5_soure_file, h5_target_file)

zip_file = 'E:\\framwork\API_PLATFORM\\apps\cases\models.py'
zip_t= 'E:\\framwork\API_PLATFORM\\apps\cases\\t'

print(zipfile.is_zipfile(zip_file))


def remove_static_fiels(removedpath):
    """
    del statci files
    :param removedpath: static files path
    :return: None
    """
    for roots, dirs, fiels in os.walk(removedpath):
        for dir_name in dirs:
            try:
                shutil.rmtree(os.path.join(roots, dir_name))
            except Exception as ex:
                print(ex)
        for file_name in fiels:
            if file_name != 'login.html':
                os.remove(os.path.join(roots, file_name))







def unzip_dist_files(outdir):
    p_path = os.getcwd()
    for _file in os.listdir(p_path):
        if os.path.isfile(_file):
            if zipfile.is_zipfile(_file):
                try:
                    files = zipfile.ZipFile(_file)
                    files.extractall(outdir)
                    unzip_files_path  = os.path.join(outdir,'dist')
                    for root, unzpied_dirs, unzpied_files in os.walk(unzip_files_path):
                        for moved_file in unzpied_files:
                            shutil.move(os.path.join(unzip_files_path,moved_file),outdir)
                        for moved_dir in unzpied_dirs:
                            shutil.move(os.path.join(unzip_files_path,moved_dir),outdir)
                    os.rmdir(unzip_files_path)
                    # os.remove(unzip_files_path)
                    files.close()
                    os.remove(os.path.join(p_path,_file))
                    break
                except Exception as ex:
                    print(ex)



def build():
    cmd = 'mvn clean install'
    # os.chdir('/opt/code/ai_stores')
    out_data, out_err = subprocess.Popen(args='ls', shell=True,stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           cwd='/opt/code/ai_stores').communicate()

    if "BUILD SUCCESS" in out_data:
        return True
    else:
        return False



if __name__=="__main__":

    m = 18>>1

    print(m)
    print(9/2)
    # s = "汉族"
    # b = bytes(s,encoding='utf-8')
    # print(b)
    # m = b'\xe6\xb1\x89\xe6\x97\x8f'
    # p = str(m,encoding='utf8')
    # print(p)
    #
    #
    # from jsonpath import jsonpath
    #
    #  # 如果取不到将返回False # 返回列表，如果取不到将返回False
    #
    # js = "{'Date': 'Sat, 07 Nov 2020 03:00:41 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'X-Powered-By': 'PHP/7.1.24', '_requestid': '39325fa60dd927e51', 'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding'}"
    # import json,requests
    # from jsonpath import jsonpath
    #
    # dictStr = {"city": "北京", "name": "大猫"}
    # print(json.dumps(dictStr, ensure_ascii=False))
    # book_dict = {
    #     "store": {
    #         "book": [
    #             {"category": "reference",
    #              "author": "Nigel Rees",
    #              "title": "Sayings of the Century",
    #              "price": 8.95
    #              },
    #             {"category": "fiction",
    #              "author": "Evelyn Waugh",
    #              "title": "Sword of Honour",
    #              "price": 12.99
    #              },
    #             {"category": "fiction",
    #              "author": "Herman Melville",
    #              "title": "Moby Dick",
    #              "isbn": "0-553-21311-3",
    #              "price": 8.99
    #              },
    #             {"category": "fiction",
    #              "author": "J. R. R. Tolkien",
    #              "title": "The Lord of the Rings",
    #              "isbn": "0-395-19395-8",
    #              "price": 22.99
    #              }
    #         ],
    #         "bicycle": {
    #             "color": "red",
    #             "price": 19.95
    #         }
    #     }
    # }
    # print(jsonpath(book_dict,'$.store.book[0].price'))


# def task(name):
#     print('%s %s is running'%(name,os.getpid()))
#     return random.randint(1,8)
#     #print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%Sif __name__ == '__main__':
#     zip_file = 'E:\\framwork\API_PLATFORM\\apps\cases\dist_1604282550.zip'
    zip_t = 'E:\\framwork\API_PLATFORM\\apps\cases\\t'
#     # os.remove(zip_file)
#     print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
#     s2= datetime.datetime.now().timestamp()
#     s1 = datetime.datetime.fromtimestamp(1604366393).strftime('%Y-%m-%d %H:%M:%S')
#     print(s2)
#     print(s1)

#     copy_file('t')
    # p=ProcessPoolExecutor(4) #设置进程池内进程数
    # for i in range(10):
    #     #同步调用方式，调用和等值
    #     obj = p.submit(task,"进程pid：")#传参方式(任务名，参数),参数使用位置或者关键字参数
    #     # res =obj.result()
    #     # print(res)
    # p.shutdown(wait=True) #关闭进程池的入口，等待池内任务运行结束
    # print("主")
    # import socket
    #
    # print(socket.gethostname())

