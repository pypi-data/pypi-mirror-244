import os
# 项目根目录
PROJECTROOT = os.path.dirname(os.path.realpath(__file__))

# 通用名称
CASES = "casesAggregate"  # 用例数据包
INTER = "interface_"  # 接口数据文件夹名称开头格式限定
ELE = "element_"  # 元素节点数据文件夹名称开头格式限定
RE = "result\\report"  # excel测试结果目录结构
RL = "result\\log"  # 运行日志测试结果目录结构
DOWN = "download"  # 指定下载文件夹名称
PIUG = "plugins"  # 自定义插件默认包文件夹名称
P = "CJ_1"  # 自定义插件默认文件夹名称
P_E = "elementData"  # 自定义插件默认数据文件夹名称
P_U = "utils"  # 自定义插件默认工具文件夹名称
P_INI = "my"  # 自定义插件默认配置文件名称
P_M = "module"  # 自定义插件默认文件名称
P_EY = "elementData"  # 自定义插件默认数据文件名称
CHANGE = "change"  # 框架自定义配置文件名称
PARA = "parameters"  # 框架静态启动参数配置文件名称
ST = "__st__"  # 框架初始化清除脚本文件名称

# 全局 共享数据 存储
GSDSTORE = {}

# 模块 插件数据 存储
MODULEDATA = {}

# 私有 共享数据 存储
PRIVATEDATA = {}

# 测试用例数据 存储
CASESDATA = {}

# ‘框架插件包声明文件’预写入内容
INI_CONTENT = f'''[Information]\nNAME = "插件名，注意：此处插件名不应由引号包裹 NAME = {P_M}"\nDETAILE = "插件详细描述；可省略不写"\nSTATE = "插件状态[finish, update, disabled]"'''
MODULE_CONTENT = f'''# 注意class类名要与{P_INI}.ini文件中的模块名和插件文件.py文件名一致\nclass {P_M}(object):\n    def __init__(self) -> None:\n        return\n\n    def __call__(self) -> None:\n        return'''

# ‘框架自定义配置文件’预写入内容
CHANGE_CONTENT = """# 该版本暂不支持，会在后续发布的版本中完善该功能"""

# ‘静态启动参数文件’预写入内容
PARAMETERS_CONTENT = """{\n    "//": "待执行用例文件路径信息; 路径从""" + CASES + """用例数据包开始; 例如："""+ f"{CASES}\\test\\test1.xlsx" +"""",\n    "testCaseFile": [\n        {\n            "//": "用例步骤文件路径(必填不可省略)",\n            "caseFilePath": " """ + f"{CASES}\\test\\test1.xlsx" + """ ",\n            "//": "待执行用例编号(用例对应的sheet表名)；为空或者不书写(且未设置 caseStart 和 caseEnd 两项)则代表按文件中的顺序执行全部",\n            "caseItem": ["xxxx", "xxxx"],\n            "//": "待执行用例区间-起始用例编号(包含在执行区间内)(用例对应的sheet表名)；为空或者不书写则代表从文件中第一条用例开始，若设置了caseItem参数则该项无效",\n            "caseStart": "xxxx",\n            "//": "待执行用例区间-截止用例编号(包含在执行区间内)(用例对应的sheet表名)；为空或者不书写则代表到文件中最后一条用例结束，若设置了caseItem参数则该项无效",\n            "caseEnd": "xxxx",\n            "//": "接口脚本执行开关 [True || False]",\n            "interfaceSwitch": true\n        },\n        {\n            "caseFilePath": " """ + f"{CASES}\\test1.xlsx" + """ ",\n            "caseItem": ["xxxx", "xxxx"],\n            "caseStart": "xxxx",\n            "caseEnd": "xxxx",\n            "interfaceSwitch": true\n        }\n    ],\n    "//": "测试环境配置信息  @browser: 浏览器平台 [Chrome, Edge, Firefox, IE]  @url: 被测系统地址 [http:// || https://]  @implicitlyWait: 隐式等待时长 [0 - n]",\n    "testEnvironment": {"browser": "Chrome","url": "http://localhost","implicitlyWait": 10},\n    "//": "辅助功能配置  @retrySwitch: 用例出错二次重试开关 [True || False]",\n    "auxiliaryFunction": {"retrySwitch": false},\n    "//": "自定义参数，若不需要则删除或者置空{}此项即可",\n    "selfDefinedParameter":{"参数名 key": "参数值 value",...}\n}"""

# ‘框架初始化清除脚本’预写入内容
ST_CONTENT = """'''\n本文件中可使用对象(注意：中括号'[]'内的对象名为固定不可变)：\n    GSTORE['driver']  # 对应driver驱动对象\n    GSTORE['keyWord']  # 对应keyWord关键字对象\n    INFO('日志信息')  # 将一些自定义的信息内容打印在框架的运行日志中\n\n# driver对象应用实例(你可以用它做任何selenium库支持的操作)：\n    test_driver = GSTORE['driver']\n    test_driver.find_element_by_id['定位表达式'].send_key('要输入的内容')\n    test_driver.fin_elements_by_id['定位表达式'].click()\n    test_driver.quit()\n\n# keyWord 关键字对象应用实例(详细的关键字解释见框架说明文档)\n    test_keyWord = GSTORE['keyWord']\n    test_keyWord.input_text('xpath', '定位表达式', '要输入的内容')  # 输入\n    test_keyWord.click_btn('xpaths', '定位表达式', '索引值')  # 点击\n'''\n# from kdtest import GSTORE, INFO\n\n\ndef suite_setup():\n    '''初始化'''\n\ndef suite_teardown():\n    '''清除'''"""