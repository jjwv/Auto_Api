# -*- coding: utf-8 -*-
#__author__='cuiwenhao'
#python 操作mysql
'''
定义对mysql数据库基本操作的封装
1、包括基本的单挑语句操作，删除，修改，更新
2、独立的查询单条、多条数据
3、独立的a据
'''

import pymysql
import os
import logging

class Operation_Interface(object):
    def __init__(self,host_db='192.168.13.128',user_db='root',passwd_db='123456',name_db='test',port_db=3306,link_type=0):
        '''
        :param host_db: 数据库服务主机
        :param user_db: 数据库用户名
        :param passwd_db: 数据库密码
        :param name_db: 数据库名称
        :param port_db: 端口号，整型数字
        :param link_type: 链接类型，用于输出数据是元祖还是字典，默认是字典，link_type=0
        :return:游标
        '''
        try:
            self.conn = pymysql.connect(host=host_db,user=user_db, passwd=passwd_db, db=name_db, port=port_db, charset='utf8')
            if link_type==0:
                #self.cur = self.conn.cursor()   # 创建游标
                self.cur = self.conn.cursor(pymysql.cursors.DictCursor)  #创建游标返回字典格式
            else:
                self.cur=self.conn.cursor()  #返回元祖
        except pymysql.Error as e:
            print("创建数据库连接失败|Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=os.path.join(os.getcwd(), './Log/syserror.log'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s%(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)


    # 定义单条数据操作，增删改
    def op_sql(self, condition):
        '''
        :param condition: sql语句,该通用方法可用来替代insertone，updateone，deleteone
        :return:字典形式
        '''
        try:
            self.cur.execute(condition)  # 执行sql语句
            self.conn.commit()
            result = {'code': '0000', 'message': u'执行通用操作成功', 'data': []}
        except pymysql.Error as e:
            result = {'code': '9999', 'message': u'执行通用操作异常', 'data': []}
            print("Mysql Error %d: %s" % (e.args[0],e.args[1]))
            logging.basicConfig(filename= os.path.join(os.getcwd(),'./Log/syserror.log'),
                                level= logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s%(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return  result

    # 查询表中单条数据
    def selectone(self,condition):
        try:
            self.cur.execute(condition)
            results = self.cur.fetchone()  ##获得  'sql'语句 返回的结果集
            result = {'code': '0000', 'message': u'执行单条查询操作成功', 'data': results}#获取一条数据
        except pymysql.Error as e:
            result = {'code': '9999', 'message': u'执行单条查询异常', 'data': []}
            print("Mysql Error %d: %s" % (e.args[0],e.args[1]))
            logging.basicConfig(filename= os.path.join(os.getcwd(),'./Log/syserror.log'),
                                level= logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s%(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 查询表中多条数据
    def selectAll(self, condition):
        '''
        :param condition: sql语句
        :return:字典形式的批量查询结果
        '''
        try:
            rows_affect = self.cur.execute(condition)
            if rows_affect > 0:  # 查询结果返回数据数大于0
                self.cur.scroll(0, mode='absolute')  # 光标回到初始位置
                results = self.cur.fetchall()  # 返回游标中所有结果
                result = {'code': '0000', 'message': u'执行批量查询操作成功', 'data': results}
            else:
                result = {'code': '0000', 'message': u'执行批量查询操作成功', 'data': []}
        except pymysql.Error as e:
            result = {'code': '9999', 'message': u'执行批量查询异常', 'data': []}
            print("Mysql Error %d: %s" % (e.args[0],e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(),'./Log/syserror.log'),
                                level = logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    # 定义表中插入多条数据操作
    def insertMore(self, condition, params):
        '''
        :param condition: insert语句
        :param params: insert数据，列表形式[('3','Tom','1 year 1 class','6'),('3','Jack','2 year 1 class','7'),]
        :return:字典形式的批量插入数据结果
        '''
        try:
            results = self.cur.executemany(condition, params)  # 返回插入的数据条数
            self.conn.commit()
            result = {'code': '0000', 'message': u'执行批量查询操作成功', 'data': int(results)}
        except pymysql.Error as e:
            result={'code':'9999','message':u'执行批量查询异常','data':[]}
            print("Mysql Error %d: %s" % (e.args[0],e.args[1]))
            logging.basicConfig(filename = os.path.join(os.getcwd(),'./Log/syserror.log'),
                                level = logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result


    # 判断表是否存在
    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

if __name__ == '__main__':
    test =Operation_Interface()  # 实例化类
    #result=test.selectone('select exe_mode,url_interface,header_interface,params_interface from case_interface where id=2')
    result = test.selectone('select exe_mode,url_interface,header_interface,params_interface from case_interface where id=4')   #查询单挑数据
    #result=test.selectone("select value_config from config_total where key_config='name_export'")
    #result = test.selectAll('select * from student where id=901 OR id=902')
    #result = test.op_sql('alter table student add zxv int')   #操作条数据
    #result = test.Operate_more('update student set sex="女" where id=901，update student set sex="不男" where id=901')
    #print(result)
    if result['code'] == '0000':
        print(result['data'])
    else:
        print(result['message'])
