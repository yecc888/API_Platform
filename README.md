#API_PLATFORM是什么？
一款接口自动化测试管理平台，为了降低自动化测试的上手门槛、维护成本，提高测试效率、项目质量，帮助测试团队高效协作，基于以上目标开发接口测试平台；主要有基本信息管理、接口管理、用例管理、定时任务等功能模块组成。

**开源协议**：[GNU General Public License v2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)

**开源声明**：欢迎大家star或者fork我的开源项目，如果大家在自己的项目里面需要引用该项目代码，请在项目里面申明协议和版权信息。
## 开发语言与框架：
 * 编程语言：Python3.6 + HTML + JScripts
 * 前端Web框架：Vue
 * 后端Web框架：Django 2.2.17
 * 后端Task框架：Celery + Redis

## 环境要求
 * 编程语言：Python 3.6
 * 操作系统：CentOS 6+、Windows10
 * MySQL版本：5.1-5.6
## 体验地址：
http://39.106.176.210/#/login  ，登录密码可以加微信提供<br>

## 系统声明：
1.前端基于Vue Element-UI开发、为用户提供友好的操作界面，增强用户体验。<br>
2.后端基于Python Django 开发，其优势为快捷效率、简洁清晰.<br>

# 使用方法：
## 安装环境配置
一、安装Python
```
# yum install epel-release -y
# yum install zlib zlib-devel readline-devel sqlite-devel bzip2-devel openssl-devel gdbm-devel libdbi-devel ncurses-libs kernel-devel libxslt-devel libffi-devel python-devel zlib-devel openldap-devel sshpass gcc git rabbitmq-server supervisor -y
# yum localinstall http://dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm
# yum install mysql-community-server mysql-devel -y
# wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz  #CentOS 7不用安装python2.7
# tar -xzvf Python-3.6.6.tgz
# cd Python-3.6.6
# ./configure --prefix=/usr/local/python3
# make all
# make install
# make clean
# make distclean  
# ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

二、安装模块
```bash
# cd /opt/
# git clone -b v3 https://github.com/yecc888/API_PLATFORM
# cd /opt/API_PLATFORM/
# pip3 install -r requirements.txt  #CentOS 7使用pip3
```


三、安装Redis
```
# wget http://download.redis.io/releases/redis-3.2.8.tar.gz
# tar -xzvf redis-3.2.8.tar.gz
# cd redis-3.2.8
# make
# make install
# vim redis.conf
```
修改以下配置（不要配置认证）
```
daemonize yes
loglevel warning
logfile "/var/log/redis.log"
bind 你的服务器ip地址
例如： bind 127.0.0.1 192.168.88.201
```
```
# cd ../
# mv redis-3.2.8 /usr/local/redis
# /usr/local/redis/src/redis-server /usr/local/redis/redis.conf
```
四、安装MySQL
```
# vim /etc/my.cnf
[mysqld]
character_set_server = utf8
添加以上字段
# /etc/init.d/mysqld restart     	#centos 6
# systemctl start mysqld.service 	#centos 7
# mysql -uroot -p  				#初始密码为空，直接回车就行
mysql> create database opsmanage DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
mysql> grant all privileges on opsmanage.* to root@'%' identified by 'password';
mysql>\q
```

### 4.安装mysql数据库后，配置数据库连接，进入settings.py<br>

### 5.cmd到根目录下，让 Django 知道我们在我们的模型有一些变更<br>
```bash
python manage.py makemigrations
```
### 6.创造或修改表结构<br>
```bash
python manage.py migrate 
```
### 7.创建超级用户，用于登录后台管理<br>
```bash
python manage.py createsuperuser
```
### 11.运行启动django服务<br>
```bash
python manage.py runserver 0.0.0.0:8000
```
### 12.访问接口文档 http://127.0.0.1:8000/swagger/ ，http://127.0.0.1:8000/xadmin 为后台管理平台<br>
## 系统图解：

### 项目讲解：
1、登录页面，只提供了登录方法，并没有注册和忘记密码功能，账号由后台管理系统直接创建分配<br>
<br>
。。。
