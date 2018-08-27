#__author__ = 'cuiwenhao'
#coding:utf-8
import logging.handlers

class Logger(logging.Logger):
    def __init__(self, filename=None):
        super(Logger, self).__init__(self)
        # 日志文件名
        if filename is None:
            filename = './Log/autotest_interface.Log'
        self.filename = filename

        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30)
        fh.suffix = "%Y%m%d-%H%M.Log"
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s]|%(filename)s [Line:%(lineno)d]|[%(levelname)s]| %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.addHandler(fh)
        self.addHandler(ch)
if __name__ == '__main__':
    pass


'''

    #写日志
    def write_log(self,logType,content):
        if logType == 1:
            logging.info(content)
        elif logType == 2:
            logging.error(content)
        elif logType == 3:
            logging.debug(content)
        else:
            logging.info(content)

class Log(object):
    def __init__(self):
        #self.logPath = CO.TestedLogDir
        #asctime = GP.gRunTime
        self.logName = './main_exe/Log/autotest_interface1.Log'

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=self.logName,
                            filemode='w')

        #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    #写日志
    def write_log(self,logType,content):
        if logType == 1:
            logging.info(content)
        elif logType == 2:
            logging.error(content)
        elif logType == 3:
            logging.debug(content)
        else:
            logging.info(content)

'''

