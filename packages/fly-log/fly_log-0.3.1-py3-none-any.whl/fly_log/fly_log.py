import sys
import os
import time
import traceback

"""    
最简单的日志实现模块，用于替换print函数，增加打印时间和代码位置信息    
"""

global_is_log_to_file = False
global_is_log_to_console = True 
global_is_log_to_redis = False
global_log_filepath = None

old_print = print
current_milli_time = lambda: int(round(time.time() * 1000))

def set_log_to_file(log_filepath,is_to_console=True):
    global global_is_log_to_file,global_log_filepath,global_is_log_to_console
    
    global_is_log_to_console = is_to_console
    global_log_filepath = log_filepath
    global_is_log_to_file = True

def debug_print(*p):
    """
    开发打印函数，打印时间和代码位置信息
    """
    current_frame = sys._getframe(1)

    milli_tim_str = "%03d " % (current_milli_time() % 1000)
    code_info = " %s(%s:%s)" % (current_frame.f_code.co_name, os.path.basename(current_frame.f_code.co_filename), current_frame.f_lineno)    

    if global_is_log_to_console:
        old_print(time.strftime("%Y-%m-%d %H:%M:%S.")  + milli_tim_str + code_info, *p)
    
    if global_is_log_to_file:
        with open(global_log_filepath,'a') as f:
            old_print(time.strftime("%Y-%m-%d %H:%M:%S.")  + milli_tim_str + code_info, *p, file=f) 

# 记录执行时间的装饰器
def log_time(func):    
    """
    记录执行时间的装饰器
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        dTime = time.time() - start 
        
        
        stack_infos = traceback.extract_stack()
        stack_info = stack_infos[-2] 
        # print(len(stack_info)) 
        # print(os.path.basename(stack_info.filename),stack_info.lineno) 
        # print(stack_info.line)
        
        # frames = sys._current_frames()
        # print(frames[0]) 
        # print(len(frames)) 
        
        # current_frame = sys._getframe(2)
        milli_tim_str = "%03d " % (current_milli_time() % 1000)
        code_info = " %s (%s:%s)" % (stack_info.line, os.path.basename(stack_info.filename), stack_info.lineno)
        
        old_print(time.strftime("%Y-%m-%d %H:%M:%S.") + milli_tim_str +"%s time cost %.3f sec" % (code_info, dTime))  
    return wrapper
    


