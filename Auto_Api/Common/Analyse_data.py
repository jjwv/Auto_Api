import datetime
import logging
import os

from xlrd import open_workbook
from xlutils.copy import copy

from Common.Operation_Interface import Operation_Interface
from Poblic import Config

Operation_db=Operation_Interface(link_type=1)#实例化自动化测试数据库操作类  link_type=1返回元祖

class Analyes_data(object):
    '''
    定义对接口测试数据分析的类，包含的方法有：
    1.到处测试数据到excel
    '''
    def __init__(self):
        self.field= Config.field_excel


    #定义导入置顶数据到Excel表中
    def Export2excel(self,names_export):
        '''
        :param names_export: 待导出的接口名称，列表形式数据
        :return: 
        '''
        counts_export=len(names_export)#导出总数
        print(counts_export)
        fail_export=[]#导出接口失败接口名列表
        try:
            #src = open_workbook('../Report/report_module.xls','r',formatting_info=True)
            src = open_workbook('/Users/cuiwenhao/Auto_Api/Report/report_module.xls', 'r', formatting_info=True)
            destination = copy(src)
            dt=datetime.datetime.now().strftime('%Y%m%d%H%M%S')#当前时间戳
            #filepath='../Report/'+str(dt)+'.xls'
            filepath = '/Users/cuiwenhao/Auto_Api/Report/' + str(dt) + '.xls'
            destination.save(filepath) #复制模板表格
            for names_interface in names_export:
                cases_interface=Operation_db.selectAll("select * from case_interface where case_status=0 and name_interface='%s'"
                                                       %(names_interface))#获取指定接口的测试用例数据
                if len(cases_interface['data'])!=0 and cases_interface['code']=='0000':
                    src = open_workbook(filepath, formatting_info=True)
                    destination = copy(src)
                    sheet = destination.add_sheet(names_interface,cell_overwrite_ok=True)
                    for name in range(0,len(self.field)):
                        sheet.write(0,name,self.field[name]) #获取并写入数据段信息到sheet中  0行，name列
                    for row in range(1,len(cases_interface['data'])+1):
                        for col in range(0,len(self.field)):
                            sheet.write(row,col,u'%s'%cases_interface['data'][row-1][col])#写数据
                        destination.save(filepath)
                elif len(cases_interface['data'])==0 and cases_interface['code']=='0000':
                    fail_export.append(names_interface)
                else:
                    fail_export.append(names_interface)
            result={'code':'0000','message':u'导出总数：%s   失败数：%s'
                        %(counts_export,len(fail_export,)),'data':fail_export}
        except Exception as error: #记录日志到log.txt文件
            result={'code':'9999','message':u'导出过程异常|导出总数：%s,失败数：%s'
                    %(counts_export,len(fail_export)),'data':fail_export}

            logging.basicConfig(filename=os.path.join(os.getcwd(), './Log/syserror.log'),
                                level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result

if __name__ == "__main__":
    names_export=Operation_db.selectone("select value_config from config_total where key_config='name_export'")#获取导出的接口数据元祖
    if names_export['code']=='0000':  #判断查询结果
        temp_export = eval(names_export['data'][0]) #获取查询数据，并将其转换成字
        test_analyse_data=Analyes_data()
        result_export=test_analyse_data.Export2excel(temp_export)#导出结果
        print(result_export)
