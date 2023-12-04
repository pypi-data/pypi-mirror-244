'''built_in'''
import time
'''# custom'''
from common import GSDSTORE


'''用例出错二次执行装饰器'''
class case_retry:
    
    def __init__(self) -> None:
        self.__retry__ = True if ('retrySwitch' in GSDSTORE['START']['auxiliaryFunction'].keys()) and\
            GSDSTORE['START']['auxiliaryFunction']['retrySwitch'] == True else False
            
    def __call__(self, case_Function):
        '''限制使用，除“用例执行方法”外装饰其它函数或者方法无意义；'''
        def wrapper(*args, **kwargs):
            for case_Num in range(0, 2):
                self.__ds__ = case_Function(*args, **kwargs)  # 执行装饰函数
                if not (self.__ds__['abnormalJudgment'] or (False in self.__ds__['acceptResult'])): break
    
            return self.__ds__
    
        return wrapper if self.__retry__ else case_Function


'''driver对象隐式等待时间重置还原装饰器'''
class reset_implicitlyWait:
    
    def __init__(self, implicitly = 0) -> None:
        self.__implicitly__ = int(implicitly)

    def __call__(self, reset_Function):
        '''
         被装饰的函数或者方法，可以视情况自定义 “隐式等待时长implicitly”；(取值范围 0 - N)
         使用格式：@object()  或者  @object(10)
         装饰器形参解释：implicitly：代表要进行修改的“隐式等待时长”
        '''
        def wrapper(*args, **kwargs):
            GSDSTORE['driver'].implicitly_wait(self.__implicitly__)  # 重置
            var_functionReturnValue = reset_Function(*args, **kwargs)
            GSDSTORE['driver'].implicitly_wait(int(GSDSTORE['START']['implicitlyWait']))  # 还原

            return var_functionReturnValue

        return wrapper


'''全局定时器'''
class setInterval:
    
    def __init__(self, interval_Second = 1, total_Duration = 60) -> None:
        self.__interval_Second__ = interval_Second
        self.__total_Duration__ = total_Duration

    def __call__(self, oper_Function):
        '''
         被装饰的的函数或者方法，会根据设置的 “执行时间间隔interval_Second” 和 “执行时间上限total_Duration”进行循环执行；
         使用格式：@object()  或者  @object(2,10)

         装饰器形参解释：
           interval_Second：代表函数或者方法要循环执行的“执行时间间隔”；
           total_Duration： 代表函数或者方法要循环执行的“执行时间上限”；
        
         装饰器使用说明：
          1、若被装饰的函数或者方法存在return返回值，则当函数或者方法的返回值为True时装饰器会提前结束运行；
          2、若被装饰的函数或者方法不存在return返回值，则装饰器会一直执行到“执行时间上限total_Duration”时才会结束运行；
        '''
        def wrapper(*args, **kwargs):
            switch = None
            for second in range(0, self.__total_Duration__, self.__interval_Second__):
                time.sleep(1)
                switch = oper_Function(*args, **kwargs)
                if switch: break
            
            return switch

        return wrapper