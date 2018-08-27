#__author__='cuiwenhao'
#-*-coding:utf-8-*-
import importlib,sys,os,json,logging
importlib.reload(sys)

from Common.Operation_Interface import Operation_Interface
Operation_db = Operation_Interface()


class Compare_param(object):
    '''
    定义比较类，包含code比较，参数完成性比较，功能测试比较三种方法
    '''
    #初始化数据
    def __init__(self,params_interface):
        global result
        self.params_interface = params_interface#接口入参
        self.id_case=params_interface['id']#测试用id
        self.result_list_response=[]#定义用来储存参数集的空列表
        self.params_to_compare=params_interface['params_to_compare']


    #定义关键参数值（code）比较
    def Compare_code(self,result_interface):
        '''
        :param result_interface:HTTP返回 包数据
        :return: 返回码code，返回信息Message,数据data
        '''
        try:
            if json.loads(result_interface):
                temp_result_interface=json.loads(result_interface)#将字符类型转换成字典类型
                temp_code_to_compare=self.params_interface['code_to_compare']#获取待比较code名称
                if temp_code_to_compare in temp_result_interface:
                    if str(temp_result_interface[temp_code_to_compare])==str(self.params_interface['code_expect']):
                        result={'code':'0000','message':u'关键字参数相同','data':[]}
                        Operation_db.op_sql("UPDATE case_interface set code_actual='%s',result_code_compare=%s,result_interface='%s' where id='%s'"
                                            %(temp_result_interface[temp_code_to_compare],0,result_interface,self.id_case))
                    elif str(temp_result_interface[temp_code_to_compare])!=str(self.params_interface['code_expect']):
                        result = {'code':'1003','message':u'关键字参数不相同','data':[]}
                        Operation_db.op_sql("UPDATE case_interface set code_actual='%s',result_code_compare=%s,result_interface='%s' where id='%s'"
                                             %(temp_result_interface[temp_code_to_compare],1,result_interface,self.id_case))

                    else:
                        result={'code':'1002','message':u'关键字参数比较出错','data':[]}
                        Operation_db.op_sql("UPDATE case_interface set code_actual='%s',result_code_compare=%s,result_interface='%s' where id='%s'"
                            % (temp_result_interface[temp_code_to_compare], 3, result_interface,self.id_case))


                else:
                    result={'code':'1001','message':u'返回包数据无关键字参数','data':[]}
                    Operation_db.op_sql("UPDATE case_interface set result_code_compare=%s,result_interface='%s' where id='%s'"
                                        %(2,result_interface,self.id_case))

            else:
                result = {'code': '1000', 'message': u'返回包格式不合法', 'data': []}
                Operation_db.op_sql("UPDATE case_interface set result_code_compare=%s,result_interface='%s' where id='%s'"
                                    %(4,result_interface,self.id_case))

        except Exception as error:#记录到log.txt文件
            result= {'code': '9999', 'message': u'关键字参数比较异常', 'data': []}
            Operation_db.op_sql("UPDATE case_interface set result_code_compare=%s,result_interface='%s' where id='%s'"
                                %(9,result_interface,self.id_case))

            logging.basicConfig(filename=os.path.join(os.getcwd(), '../Log/syserror.log'),
                           level=logging.DEBUG,
                           format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result

    #定义接口返回数据中参数名写入列表中
    def Get_compare_params(self,result_interface):
        '''
        :param result_interface:HTTP返回 包数据
        :return: 返回码code，返回信息Message,数据data
        '''
        try:
            if json.loads(result_interface):
                temp_result_interface=json.loads(result_interface)#将字符类型转换成字典类型
                self.result_list_response=  list(temp_result_interface.keys())

                result= {'code': '0000', 'message': u'成功', 'data':self.result_list_response}
            else:
                result= {'code': '1000', 'message': u'返回包格式不合法', 'data':[]}
        except Exception as error:  # 记录到log.txt文件
            result = {'code': '9999', 'message': u'处理数据异常', 'data': []}

            logging.basicConfig(filename=os.path.join(os.getcwd(), './syserror.Log'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result

    #参数完整性比较方法，传参值与get_compare_params方法返回结果比较
    def Compare_params_complete(self,result_interface):
        '''
        :param result_interface:HTTP返回 包数据
        :return: 返回码code，返回信息Message,数据data
        '''
        try:
            temp_compare_params=self.Get_compare_params(result_interface)#获取返回包参数集
            if temp_compare_params['code']=='0000':
                temp_result_list_response=temp_compare_params['data']#获取接口返回参数去重列表


                if self.params_to_compare==u'' or isinstance(self.params_to_compare,(tuple,dict)):#判断用例中数据为空或者类型不符合
                    result = {'code': '4001', 'message': u'用例中待比较参数集错误', 'data': self.params_to_compare}
                else:
                    list_params_to_compare=eval(self.params_to_compare)#数据库表unicode编码数据转换成员列
                    if set(list_params_to_compare).issubset(set(temp_result_list_response)):#集合的包含关系  后边包括前边

                        result = {'code': '0000', 'message': u'参数完成性比较一致', 'data': []}
                        Operation_db.op_sql('UPDATE case_interface set params_actual="%s",result_params_compare=%s where id="%s"'
                                            % (temp_result_list_response, 0, self.id_case))
                    else:
                        result = {'code': '3001', 'message': u'实际结果中元素不都在预期结果中', 'data': []}
                        Operation_db.op_sql('UPDATE case_interface set params_actual="%s",result_params_compare=%s where id="%s"'
                                            % (temp_result_list_response, 1, self.id_case))
            else:
                result = {'code': '2001', 'message': u'调用get_compare_params方法返回错误', 'data':[]}
                Operation_db.op_sql('UPDATE case_interface set result_params_compare=%s where and id="%s"'%(2,self.id_case))

        except Exception as error:  # 记录到log.txt文件
            result = {'code': '9999', 'message': u'参数完整性异常', 'data': []}
            Operation_db.op_sql('UPDATE case_interface set result_params_compare=%s where id="%s"'%(9,self.id_case))


            logging.basicConfig(filename=os.path.join(os.getcwd(), './syserror.Log'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result

    # 定义递归方法
    def recur_params(self, result_interface):
        # 定义递归操作，将接口返回数据中参数名写入列表中(去重)
        try:
            if isinstance(result_interface, (str)) and json.loads(result_interface):  # 入参是字符串类型且能被转换成字典
                temp_result_interface = json.loads(result_interface)
                self.recur_params(temp_result_interface)
            elif isinstance(result_interface, dict):  # 入参是字典
                for param, value in result_interface.items():
                    self.result_list_response.append(param)
                    if isinstance(value, list):
                        for param in value:
                            self.recur_params(param)
                    elif isinstance(value, dict):
                        self.recur_params(value)
                    else:
                        continue
            else:
                pass
        except Exception as error:  # 记录日志到log.txt文件
            logging.basicConfig(filename=os.path.join(os.getcwd(), '../log/syserror.log'), level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
            return {'code': '9999', 'message': u'处理数据异常', 'data': []}
        return {'code': '0000', 'message': u'成功', 'data': list(set(self.result_list_response))}





#新增将response请求错误的message和code写入sql
    def Write_to_messageandcode(self,result_interface):
        '''
        :param result_interface: HTTP返回 包数据
        :return:返回码code，返回信息Message,数据data
        '''
        try:
            if json.loads(result_interface):
                temp_result_interface = json.loads(result_interface)  # 将字符类型转换成字典类型

                if temp_result_interface.__contains__('state'):
                    temp_result_state=str(temp_result_interface['state']) #获取response state的值

                    # dict.__contains__(key）如果键在字典dict里返回true，否则返回false。
                    if temp_result_state!='1':
                        if temp_result_state!='True':
                            if temp_result_interface.__contains__('message') and temp_result_interface.__contains__('code'):
                                temp_result_message=temp_result_interface['message'] #获取reponse message的值
                                temp_result_code=temp_result_interface['code']

                                result = {'code': '0000', 'message': u'response包含message，code准备写入sql', 'data': []}

                                Operation_db.op_sql('UPDATE case_interface set result_message="%s",result_code="%s" where id="%s"'
                                        % (temp_result_message,temp_result_code , self.id_case))
                            else:
                                result = {'code': '1001', 'message': u'response不包含messagez,code', 'data': []}

                        else:
                            result = {'code': '1002', 'message': u'state=True,请求错误', 'data': []}
                    else:
                        result = {'code': '1003', 'message': u'state=1,请求错误', 'data': []}

                else:
                    result = {'code': '1004', 'message': u'response不包含state', 'data': []}
            else:
                result = {'code': '1005', 'message': u'返回包格式不合法', 'data': []}

        except Exception as error:  # 记录到log.txt文件
            result = {'code': '9999', 'message': u'关键字参数比较异常', 'data': []}

            logging.basicConfig(filename=os.path.join(os.getcwd(), './syserror.Log'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result







if __name__=="__main__":
    #测试
    # result_interface = '{"message": "获取附近服务商成功", "nextPage": 1, "pageNo": 0, ' \
    #                    '"merchantInfos": "测试环境店铺", "resultCode": "000", "totalPage": 66746}'

    result_interface='{"code": 42204012, "message": "您不是管理员,无权操作", "state": 0}'

    params_interface={'table_name': 'test', 'update_time': '2017-8-21 00:52:44', 'result_interface': '',
                      'result_code_compare': 0, 'exe_mode': 'post', 'code_to_compare': 'resultCode',
                      'params_actual': None, 'case_status': 0,
                      'params_interface': '{"latitude": "NULL", "pageNo": 0, "longitude": "123.154212"}',
                      'result_params_compare': None, 'code_expect': '000', 'code_actual': '',
                      'create_time': None, 'exe_level': 0,
                      'url_interface': 'http://192.168.1.88:8080/personalOrder/getNearbyServiceMerchantList',
                      'header_interface': '{"Content-Length": " 0", "UUID": " 862096032360278", '
                                          '"POSTFIX": " 9BCE6A51E0DDE0D759A55D199E691919CF3E492C9B77EA3985D6C2291B71A6274ABD93FA91EF65AC9660EC51C4D97DA1", '
                                          '"SYSTEM": " 5.1", "Host": " 192.168.1.88", "VERSION": " 2.6.1.161221", '
                                          '"User-Agent": " Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1", '
                                          '"PHONE": " ", "Connection": " Keep-Alive", '
                                          '"CLIENT_TYPE": " 1", "APIVERSION": " 1.0", "TIME": " 1483597250589", '
                                          '"MODEL": " iPhone 5S", "CLIENT_FLAG": " 1", "CHANNEL": " Default", '
                                          '"Accept-Encoding": " gzip, deflate"}', 'id': 1,
                      'params_to_compare': "['state','message','data']"}
    test_compare_param=Compare_param(params_interface)
    # result_compare_code=test_compare_param.Compare_code(result_interface)#关键参数值比较
    # print(result_compare_code)
    #result_get_compare_params=test_compare_param.Get_compare_params(result_interface)#获取参数集
    #print(result_get_compare_params)
    # result_compare_params_complete=test_compare_param.Compare_params_complete(result_interface)#参数完整性比较
    # print(result_compare_params_complete)
    result_get_compare_params = test_compare_param.Write_to_messageandcode(result_interface)  # 错误信息写入sql
    print(result_get_compare_params)








