from utils.log.trusteeship import trusteeship

# 框架共享数据
GSTORE = {}

def INFO(message):
    """
     在框架运行日志中打印信息

     参数：
        @param message:  描述
    """
    trusteeship.info(f'{message}')