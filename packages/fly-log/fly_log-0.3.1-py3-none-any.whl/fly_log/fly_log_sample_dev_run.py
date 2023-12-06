# from .fly_log import debug_print
from fly_log import debug_print as print, log_time,set_log_to_file
import time

"""   
    1. 本文件用于开发测试
"""

def test1():
    print("my fly log ") 

@log_time 
def test2():
    time.sleep(0.5) 

def test3():
    set_log_to_file("logs/a.log")
    print("aaa")     

def dev_run():
    # test1()
    # test2()  
    test3()





if __name__ == '__main__':
    dev_run()
