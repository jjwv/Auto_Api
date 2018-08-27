#__author__ = 'cuiwenhao'
#coding:utf-8
'''
1.发送http请求，得到结果
2.比较结果，写入数据库对应测试用例表
'''
import logging,os,json
from Common import Http_request,Analyse_data,Compare_param,Operation_Interface
from Poblic import Log
op_log=Log.Logger()#实例化日志
base_request=Http_request.request_interface()#实例化http请求
base_operationdb_interface=Operation_Interface.Operation_Interface()#实例化接口测试数据库操作类


try:

    print("开始接口自动化程序，请选择操作类型(0|执行用例；1|导出测试结果)")
    #value_input = int(input('请输出操作类型:'.decode('utf-8').encode('gbk')))
    value_input=int(input('请输入操作类型:'))
    if value_input not in (0,1):
        print ("请输入正确的操作类型(0|执行用例；1|导出测试结果)")
        #value_input = int(input('请输出操作类型:'.decode('utf-8').encode('gbk')))
        value_input = int(input('请输入操作类型:'))

        # base_operationdb_interface.op_sql('update case_interface set result_message=null;')  # 清空上次请求返回的错误信息
        # base_operationdb_interface.op_sql('update case_interface set result_code=null;')  # 清空上次请求返回的错误code

    else:
        if value_input==0:
            print(u"您输入的是：0|准备：执行用例")
            module_execute=base_operationdb_interface.selectAll("SELECT value_config from config_total where key_config='exe_setup' and status=0")#获取待执行接口数据

            base_operationdb_interface.op_sql('update case_interface set result_message=null;')  # 清空上次请求返回的错误信息
            base_operationdb_interface.op_sql('update case_interface set result_code=null;')  # 清空上次请求返回的错误code

            if len(module_execute['data'])!=0 and module_execute['code']=='0000':
                for module_execute_one in module_execute['data']:
                    temp_module_execute=eval(module_execute_one['value_config'])#每个接口的字典数据
                    #for temp_name_interface,condition in temp_module_execute.iteritems():  #python2.运用，python3用items
                    for temp_name_interface,condition in temp_module_execute.items():  # items() 方法以列表返回可遍历的(键, 值) 元组数组。
                        print(u'############开始执行接口：%s############\n' %(temp_name_interface))
                        temp_level_check=condition['level_check']#检查级别
                        temp_level_exe=tuple(condition['level_exe'])#执行级别
                        data_case_interface=base_operationdb_interface.selectAll("select * from case_interface where case_status=0 and name_interface='%s' and exe_level in %s"
                                                                                 %(temp_name_interface,temp_level_exe))#获取接口测试数据
                        if data_case_interface['code']=='0000' and len(data_case_interface['data'])!=0:
                            for temp_case_interface in data_case_interface['data']:
                                id_case=str(temp_case_interface['id'])#用例编号
                                url_interface=temp_case_interface['url_interface']#接口地址
                                headerdata=eval(temp_case_interface['header_interface'])#请求头文件
                                param_interface=temp_case_interface['params_interface']#接口请求参数
                                type_interface=temp_case_interface['exe_mode']#执行环境
                                result_http_response=base_request.http_request(interface_url=url_interface,headerdata=headerdata,interface_param=param_interface,request_type=type_interface,id_case=id_case)#发送http请求
                                print(u"接口地址:%s\n参数:%s\n返回包:%s\n" %(url_interface,param_interface,result_http_response))


                                base_operationdb_interface.op_sql("UPDATE case_interface set result_interface='%s' where id=%s" %(result_http_response['data'],id_case))#接口返回包写入用例表


                                if result_http_response['code']=='0000' and len(result_http_response['data'])!=0:
                                    for child_level_check in temp_level_check:#执行等级
                                        base_compare=Compare_param.Compare_param(temp_case_interface)
                                        if child_level_check in (0,u'0'):#执行返回码检查
                                            result_compare_code=base_compare.Compare_code(result_http_response['data'])
                                            print(u'编号：%s|级别：关键参数值|接口名称：%s|信息：%s' %(id_case,temp_name_interface,result_compare_code['message']))
                                            #op_log.info(u'检查级别：关键参数值|接口名称：%s|用例编号：%s|执行信息：%s' %(temp_name_interface,id_case,result_compare_code['message']))
                                        elif child_level_check in (1,u'1'):#执行参数完整性检查
                                            result_compare_params_complete=base_compare.Compare_params_complete(result_http_response['data'])
                                            print(u'编号：%s|级别：参数完整性|接口名称：%s|信息：%s' %(id_case,temp_name_interface,result_compare_params_complete['message']))
#.......................................................新增写入错误message和code
                                            result_message_code=base_compare.Write_to_messageandcode(result_http_response['data'])
#........................................................
                                        elif child_level_check in (2,u'2'):#执行功能测试,待开发
                                            pass
                                        else:
                                            print(u'编号：%s|接口名称：%s|检查级别错误：%s' %(id_case,temp_name_interface,child_level_check))
                                elif len(result_http_response['data'])==0:
                                    print(u'编号：%s|接口名称：%s|错误信息：接口返回数据为空' %(id_case,temp_name_interface))
                                else:
                                    print(u'编号：%s|接口名称：%s|错误信息：%s' %(id_case,temp_name_interface,result_http_response['message']))
                        elif len(data_case_interface['data'])==0:
                            print(u'接口名称：%s|错误信息：获取用例数据为空，请检查用例' %(temp_name_interface))
                        else:
                            print(u'接口名称：%s|错误信息：获取用例数据失败|错误信息：%s' %(temp_name_interface,data_case_interface['message']))
                        print(u'############结束执行接口：%s############\n' %(temp_name_interface))
            else:
                print(u'错误信息：待执行接口获取失败|错误信息：%s' %module_execute['message'])
        elif value_input==1:
            print("您输入的是：1|准备：导出测试结果，请注意在目录下查看")
            names_export=base_operationdb_interface.selectone("select value_config from config_total where key_config='name_export'")#获取导出的接口数据元祖
            if names_export['code']=='0000' and len(names_export['data']['value_config'])!=0:#判断查询结果
                temp_export=eval(names_export['data']['value_config'])#获取查询数据，并将其转换成字典
                test_analyse_data=Analyse_data.Analyes_data()
                result_export=test_analyse_data.Export2excel(temp_export)#导出结果
                print (result_export['message'])
                print (u"导出失败接口列表：%s" %result_export['data'])
            else:
                print(u"请检查配置表数据正确性，当前值为：%s" %names_export['data'])



except Exception as error:#记录日志到log.txt文件
    print(u"系统出现异常：%s" %error)
    logging.basicConfig(filename = os.path.join(os.getcwd(), './Log/syserror.log'),
                        level = logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.exception(error)
input('Press Enter to exit...')

