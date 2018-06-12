#coding=utf-8
#__author__ = GaoY
# python err_logging.py

import logging, time, functools

def log(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            #print('Function %s() runs' % func.__name__)
            logger.info('Function %s() runs' % func.__name__)
            start = time.time()

            try:
                temp = func(*args, **kw)
                end = time.time()
                #print('Function %s() Completed in %ds' % (func.__name__, (end - start)))
                logger.info('Function %s() Completed in %ds' % (func.__name__, (end - start)))
                return temp
            except Exception as e:
                logger.exception(e)

        return wrapper
    return decorator



class Config():  
    # 创建一个logger  
    logger = logging.getLogger('Recommend System')  
    logger.setLevel(logging.DEBUG)  
  
    # 创建一个handler，用于写入日志文件  
    fh = logging.FileHandler('test.log')  
    fh.setLevel(logging.DEBUG)  
  
    # 再创建一个handler，用于输出到控制台  
    ch = logging.StreamHandler()  
    ch.setLevel(logging.DEBUG)  
  
    # 定义handler的输出格式  
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)  
    ch.setFormatter(formatter)  
  
    # 给logger添加handler  
    logger.addHandler(fh)  
    logger.addHandler(ch)  
    def getLog(self):  
        return self.logger  




if __name__ == '__main__':  
    conf=Config()  
    logger=conf.getLog()  
    logger.info('START')  
    @log(logger)
    def test():
        return 10 / 0
    print(test())
    logger.info('Completely Done\n')
