#__author__ = 'cuiwenhao'
#coding:utf-8
'''
定义对HTTP请求操作的封装
1.http_request是主方法，直接供外部调用
2.http_code，http_get，http_post是实际底层分类调用的方法
'''
import requests,os,logging,json
from Common.Operation_Interface import Operation_Interface

class request_interface(object):
    def __init__(self):
        global result

    # POST请求，参数在body中
    def __http_post(self,interface_url,headerdata,interface_param):
        '''
        :param interface_url: 接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :return:字典形式结果
        '''
        try:
            if interface_url!='':
                #aa=eval(interface_param)


                response = requests.post(url=interface_url, headers=headerdata,data=interface_param,verify=False,timeout=10)
                #response = requests.post(url=interface_url, headers=headerdata,data=interface_param)
                if response.status_code==200:
                    result={'code':'0000','message':u'成功','data':response.text}
                else:
                    result={'code':'2004','message':u'接口返回状态错误','data':[]}
            elif interface_url == '':
                result={'code':'2002','message':u'接口地址参数为空','data':[]}
            else:
                result = {'code': '2003', 'message': u'接口地址错误', 'data': []}
        except Exception as error:#记录日志到log.txt文件
            result={'code':'9999','message':u'系统异常','data':[]}
            logging.basicConfig(filename = os.path.join(os.getcwd(), '../Log/syserror.log'),level = logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result
    # GET请求，参数在接口地址后面
    def __http_get(self,interface_url,headerdata,interface_param):
        '''
        :param interface_url: 接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :return:字典形式结果
        '''
        try:
            if interface_url != '' :
                requrl = interface_url+interface_param

                response = requests.get(url=requrl, headers=headerdata,verify=False,timeout=10)
                #print response
                if response.status_code==200:
                    result={'code':'0000','message':u'成功','data':response.text}
                else:
                     result={'code':'3004','message':u'接口返回状态错误','data':[]}
            elif interface_url == '':
                result={'code':'3002','message':u'接口地址参数为空','data':[]}
            else:
                result={'code':'2003','message':u'接口地址错误','data':[]}
        except Exception as error:#记录日志到log.txt文件
            result={'code':'9999','message':u'系统异常','data':[]}
            logging.basicConfig(filename=os.path.join(os.getcwd(), '../Log/syserror.log'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result
    # 统一处理http请求
    def http_request(self,interface_url,headerdata,interface_param,request_type):
        '''
        :param interface_url: 接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :param request_type:请求类型
        :return:字典形式结果
        '''
        try:
            if request_type=='get' or request_type=='GET':
                result=self.__http_get(interface_url,headerdata,interface_param)
            elif request_type=='post' or request_type=='POST':
                result=self.__http_post(interface_url,headerdata,interface_param)
            else:
                result={'code':'1000','message':u'请求类型错误','data':request_type}
        except Exception as error:#记录日志到log.txt文件
            result={'code':'9999','message':u'系统异常','data':[]}
            logging.basicConfig(filename = os.path.join(os.getcwd(), './Log/syserror.log'),
                                level = logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result

if __name__ == "__main__":
    test_interface=request_interface()#实例化HTTP请求类
    #test_db=opmysql.operationdb_interface(host_db='192.168.1.103',user_db='root',passwd_db='root',name_db='test_interface',port_db=3306,link_type=0)#实例化mysql处理类
    test_db=Operation_Interface(host_db='192.168.13.128',user_db='root',passwd_db='123456',name_db='test',port_db=3306,link_type=0)#实例化mysql处理类
    sen_sql="select exe_mode,url_interface,header_interface,params_interface from case_interface where id=7"
    params_interface=test_db.selectone(sen_sql)
    if params_interface['code']=='0000':  #mysql查询成功返回0000进行判断
        url_interface=params_interface['data']['url_interface']
        headerdata=eval(params_interface['data']['header_interface'])#unicode转换成字典
        param_interface=params_interface['data']['params_interface']
        type_interface=params_interface['data']['exe_mode']
        result=test_interface.http_request(interface_url=url_interface,headerdata=headerdata,interface_param=param_interface,request_type=type_interface)
        if result['code']=='0000':
            pp=result['data']
            print(pp)
        else:
            print("发送http_request错误")
    else:
        print("Mysql操作失败")

