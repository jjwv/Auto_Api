#__author__='cuiwenhao'
#coding:utf-8
#domin用于替换接口地址中的测试环境下的ip

import time
domain='192.168.169.153:8080'
environ_test={'ip':'192.168.169.153','port':'8080','timeout':20}#测试环境ip、端口号
environ_product={'ip':'192.168.169.152','port':'8080','timeout':20}#生产环境环境ip、端口号

field_excel=[u'id',u'接口模块',u'接口名称',u'用例级别',u'请求类型',u'接口地址',u'接口头文件',
             u'接口请求参数',u'接口请求status_code',u'接口响应时间 单位ms',u'接口返回包',u'待比较参数',u'实际参数值',u'预期参数值',
             u'参数值比较结果',u'接口返回False时code值',u'接口返回False时message值',u'待比较参数集合',u'实际参数集合',u'参数完整性结果',
             u'用例状态',u'创建时间',u'更新时间']#导出的excel表格标题