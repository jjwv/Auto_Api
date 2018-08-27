# -*- coding: utf-8 -*-
import pymysql
import os
import logging

class Operation_Interface(object):
    def __init__(self, host_db='192.168.169.159', user_db='root', passwd_db='123456', name_db='haha', prot_db=3306,
                 link_type=0):
        try:
            self.conn = pymysql.connect(host=host_db,user=user_db, passwd=passwd_db, db=name_db, port=prot_db, charset='utf8')
            if link_type==0:
                self.cur=self.conn.cursor(pymysql.cursors.DictCursor)
            else:
                self.cur=self.conn.cursor()
        except pymysql.Error as e:
            print("创建数据库连接失败|Mysql error %d %s" %(e.args[0],e.args[1]))
            logging.basicConfig(filename=os.path.join(os.getcwd(),'../Log/syserror.log'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s%(message)s')
            logger=logging.getLogger(__name__)
            logger.exception(e)

    def op_sql(self,condition):
        try:
            self.cur.execute(condition)
            self.conn.commit()
            result = {'code': '0000', 'message': u'执行通用操作成功', 'data': []}
        except pymysql.Error as e:
            result = {'code': '0000', 'message': u'执行通用操作成功', 'data': []}
            print("创建数据库连接失败|Mysql error %d %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=os.path.join(os.getcwd(), '../Log/syserror.log'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s%(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result

    def selectone(self,condition):
        try:
            self.cur.execute(condition)
            results=self.cur.fetchall()
            result = {'code':'0000','message':"kjshfkdsh",'data': results}
        except pymysql.Error as e:
            result = {'code': '9999', 'message': u'执行单条查询异常', 'data': []}
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=os.path.join(os.getcwd(), '../Log/syserror.log'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s%(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return result


 # 判断表是否存在
    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()



if __name__=="__main__":
    test = Operation_Interface()
    result = test.op_sql('update ')  # 操作条数据
    #result=test.selectone('select * from student where id=902')
    if result['code'] == '0000':
        print(result['data'],result['message'])
    else:
        print(result['message'])

