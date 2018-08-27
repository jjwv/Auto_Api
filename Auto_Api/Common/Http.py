#coding:utf-8
#Python发送HTTP请求
import http.client
import json
import logging
import os
import urllib
import urllib.request

from Common.Operation_Interface import Operation_Interface
from Poblic import Config


class Request_interface(object):
    #判断接口地址Http状态是否200
    def __http_code__(self,url):
        try:
            if url!="":
                code=urllib.request.urlopen(url).getcode()
            else:
                code='1000'#请求参数错误
        except Exception as error:  #记录日志到lig.txt文件
            code = '9999' #http请求异常
            logging.basicConfig(filename= os.path.join(os.getcwd(),'Log.txt'),
                    level = logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger=logging.getLogger(__name__)
            logger.exception(error)
        return code


    #POST请求，参数在body中
    def __http_post(self,interface_url,headerdata,param,environ):
        '''
        参数有：接口地址、头文件、接口 
        '''
        try:
            if interface_url!='' and environ==u'test':
                httpClient = http.client.HTTPConnection(Config.environ_test['ip'],
                                                        Config.environ_test['port'],
                                                        timeout=Config.environ_test['timeout'])
                httpClient.request('POST',interface_url,body=param,headers=headerdata)
                response=httpClient.getresponse()
                if response.status==200:
                    return response.read()
                else:
                    return '2004'#接口返回状态错误
            elif interface_url!=''and environ==u'product':
                httpClient=http.client.HTTPConnection(Config.environ_product['ip'],
                                                      Config.environ_product['port'],
                                                      timeout=Config.environ_product['timeout'])
                httpClient.request('POST',interface_url,body=param,headers=headerdata)
                response=httpClient.getresponse()
                if response.status==200:
                    return response.read()
                else:
                    return '2004' #接口返回状态错误
            elif interface_url=='':
                return '2002'#接口地址参数为空
            elif self.__http_code__(interface_url)!=200:
                return '2003'  #接口http访问错误
        except Exception as error: #记录日志到log.txt文件
            logging.basicConfig(filename=os.path.join(os.getcwd(), 'Log.txt'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s - %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
            return '9999'  #http请求异常


    #GET请求，参数在接口地址后面
    def __http_get(self,interface_url,headerdata,param,environ):
        '''
        参数有：接口地址、头文件、接口入参、执行环境（测试、生产）
        '''
        try:
            if interface_url!='' and environ==u'test':
                requrl = interface_url+param
                httpClient = http.client.HTTPConnection(Config.environ_test['ip'],
                                                        Config.environ_test['port'],
                                                        timeout=Config.environ_test['timeout'])
                httpClient.request('GET', interface_url, body=None, headers=headerdata)
                response = httpClient.getresponse()
                print(response)
                if response.status == 200:
                    return response.read()
                else:
                    return '3004'  #接口返回状态错误
            elif interface_url!='' and environ == u'product':
                requrl=interface_url+param
                httpClient = http.client.HTTPConnection(Config.environ_product['ip'],
                                                        Config.environ_product['port'],
                                                        timeout=Config.environ_product['timeout'])
                httpClient.request('GET', interface_url, body=None, headers=headerdata)
                response = httpClient.getresponse()
                if response.status == 200:
                    return response.read()
                else:
                    return '3004'  # 接口返回状态错误
            elif interface_url == '':
                return '3002'  # 接口地址参数为空
            elif self.__http_code__(interface_url) != 200:
                return '3003'  # 接口http访问错误
        except Exception as error:  # 记录日志到log.txt文件
            logging.basicConfig(filename=os.path.join(os.getcwd(), 'Log.txt'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] % (levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
            return '9999'  # http请求异常


    #统一处理http请求
    def http_request(self,interface_url,headerdata,param,type,environ=u'test',default_param=None):
        '''
        参数有：接口地址、头文件、接口入参、请求方式、执行环境（测试、生产，默认是测试），默认参数
        '''
        try:
            if type=='get' or type=='GET':
                result=self.__http_get(interface_url,headerdata,param,environ)
            elif type=='post' or type=='POST':
                result = self.__http_post(interface_url,headerdata,param,environ)
            else:
                result='1000' #请求参数烈性错误
        except Exception as error: #记录日志到log.txt文件
            result='9999'#系统异常返回码
            logging.basicConfig(filename=os.path.join(os.getcwd(), 'Log.txt'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] % (levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result




if __name__=="__main__":
    test_interface=Request_interface()  #实例化HTTP请求
    test_Opera=Operation_Interface()  #实例化MySQL处理
    sen_sql='select exe_mode,url_interface,header_interface,params_interface from case_interface where id=2;'
    #sen_sql = 'select exe_mode,url_interface,header_interface,params_interface from case_interface where id=1;'

    interface_params = test_Opera.selectone(sen_sql)
    interface_url = interface_params['url_interface']
    headerdata = json.loads(interface_params['header_interface'])
    param = interface_params['params_interface']
    type = interface_params['exe_mode']

    result = test_interface.http_request(interface_url=interface_url,headerdata=headerdata,
                                         param=param,type=type,
                                         environ=u'test',default_param=None)
    print(result)


