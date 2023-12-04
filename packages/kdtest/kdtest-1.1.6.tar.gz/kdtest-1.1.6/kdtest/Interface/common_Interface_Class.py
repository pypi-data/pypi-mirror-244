'''# Third_party'''
import requests
from ruamel.yaml import YAML
from tqdm import tqdm
'''# built_in'''
import re
import os
import json
'''# custom'''
from common import GSDSTORE, PROJECTROOT
from utils.public_Script import isLogicMethodClass
from utils.log.trusteeship import trusteeship


class CommonInterfaceClass:

    def __repr__(self) -> str:
        '''
        公共接口类 方法组成：
            __file_Tool(): 文件操作工具函数；
            __mapping(): “接口数据”映射文件操作函数；
            __cache_Data: 接口缓存数据“提取”操作封装；
            __callback_Data(): “接口回调数据”处理函数；
            __call_Interface(): 接口调用函数；
            __read_InterfaceData(): “接口数据”读取函数；
            __result_Comparison(): “接口响应结果”值比对函数；
        '''

        '''
        模块单独接口数据文件[InterfaceData.yaml]书写说明及示例：
            
            特殊：“登录接口”名称中包含“Login_Interface”代表为【主角色/初始角色】；__Configure() 函数会进行相应的处理。


            X[int]_接口名称: [注意：此处的“接口名称”前需要按照顺序填写阿拉伯数字；例如 “1_Login_Interface”]
                _PARAMETERS: [接口参数集合]
                _RESULT: [“接口响应结果”预期比对值]
                _RS: None [接口“执行状态”，固定写入None]

            _PARAMETERS接口参数集合 可选参数解释：
                METHOD：请求类型 【string类型；不做解释】 

                URL：接口地址 【string类型；不做解释】 

                DATA：接口请求参数
                    书写规则说明：参数为dict类型；根据不同的接口请求参数随之改变；
                    书写示例P[--yaml文件写法--]：
                        DATA：
                            KEY1: "1"  # 普通字符串
                            KEY2:  # [12, 10] 列表
                                - 12
                                - 10 
                            KEY3:  # {'NAME': "123", 'AGE': 12}  字典
                                NAME: "123"
                                AGE: 12

                PARAMS: 接口请求参数(URL地址解析写法) [写法与DATA同理]

                HEADER：请求头
                    书写规则说明：参数为dict类型；其子项均为固定项，需要根据接口进行填写
                    书写示例P[--yaml文件写法--]：
                        HEADER:
                            Content-Type: application/x-www-form-urlencoded

                FILE：文件参数
                    书写规则说明：参数为dict类型；固定子项KEY书写为：FFILE_KEY, NAME，SRC，TYPE；功能迭代优化后支持多文件上传。
                    书写示例P[--yaml文件写法--]：
                        #  单文件
                        FILE:
                            FILE_KEY: 'file'  # 参数key键[视实际接口为准]
                            NAME: 'test1.jpeg'  # 文件名
                            SRC: 'D:\\Program_code\\python\\Python_requests\\test1.jpeg'  # 文件路径
                            TYPE: 'image/jpeg'  # 文件类别
                        
                        # 多文件,采用“列表list”嵌套“字典dict”形式
                        FILE:
                            - FILE_KEY: 'file1'  # 参数key键[视实际接口为准]
                            NAME: 'test1.jpeg'  # 文件名
                            SRC: 'D:\\Program_code\\python\\Python_requests\\test1.jpeg'  # 文件路径
                            TYPE: 'image/jpeg'  # 文件类别

                            - FILE_KEY: 'file2'  # 参数key键[视实际接口为准]
                            NAME: 'test2.jpeg'  # 文件名
                            SRC: 'D:\\Program_code\\python\\Python_requests\\test2.jpeg'  # 文件路径
                            TYPE: 'image/jpeg'  # 文件类别
                
                I_CODE：接口请求参数编码
                    书写规则说明：该参数用于为 DATA数据中的“中文参数”设置编码，以避免在传入接口后出现乱码的问题。
                    [该参数值默认为'GB2312'，如果需要设置其它编码需要在yaml数据中标明；注意：输入的编码名必须为有效编码名且能够正确被'requests库'解析]

                    书写示例P[--yaml文件写法--]：
                        I_CODE: 'GB2312' || 'utf-8'

                COOKIE：登录态
                    书写规则说明：该参数用于接收“系统登录态Cookie”值；如果想要使用“Cookie缓存文件[Cookie.txt]中的Cookie值[这里大多数为“登录接口”回调缓存]”
                    则只需要传入固定参数[CACHE]即可；如果想要使用自定义的Cookie值则根据Cookie参数传入dict字典即可。

                    书写示例P[--yaml文件写法--]：
                        使用“缓存文件[Cookie.txt]中的Cookie” :
                        COOKIE: CACHE  【string类型】
                        使用“自定义Cookie值” :
                        COOKIE:  【dict类型】
                            KEY1: xxxx
                            KEY2: xxxx

                CALLBACK：接口回调数据缓存信息列表；即将需要缓存的数据标注在[CALLBACK]列表中。
                    书写规则说明：该参数为list类型；用于存放需要进行缓存的数据标识。规定参数为三种[Cookie，A_Cookie，“接口响应结果”]

                    其中“Cookie”和“A_Cookie”为固定写法；Cookie 和 A_Cookie 二者都是对Cookies登录态进行缓存；不同的区别为：
                    “Cookie”会将[Cookie.txt]文件中的数据先清空，在将获取到的新数据写入文件中。
                    “A_Cookie” 不会清空[Cookie.txt]文件，它是将[Cookie.txt]文件中的数据进行一一判别，如果数据key存在则将其value值更新，如果数据key不存在则在文件中追加该键值对。

                    
                    “接口响应结果”写法分为两种[“json数据类型”，“非Json数据类型”]，以下对“接口响应结果”的书写规则进行解释：
                    “当响应结果为json数据类型时”：
                        写法不做限制，可以理解为 “缓存数据在缓存文件[Response_result.txt]”中的key键ID。在后续数据访问时通过此“key键”进行访问。
                        示例: CALLBACK = ['Cookie', '自定义ID']

                    “当响应结果为非json数据类型时”：
                        书写格式：[{'ID':'xxxx', 'REGULAR': 'xxxx'},{.....}]
                        格式说明：此种写法是为了更好的对响应结果进行数据筛选；它可以将一个“接口响应接口”进行指定次数的“正则表达式筛选”和“缓存”
                        子项key解释：ID[缓存数据在缓存文件[Response_result.txt]”中的key键ID]，REGULAR[要进行数据筛选的“正则表达式”]

                        举例说明：
                            “接口响应结果”：'<input type="hidden" name="csrf_token" value="eiYDGzpZgQM6a9ImXEFr">'[非json类型]

                            需要缓存的数据为：csrf_token，eiYDGzpZgQM6a9ImXEFr

                            原逻辑下：需要进行两次接口调用，一次缓存一个数据

                            现逻辑下：CALLBACK = [[{'ID': 'name', 'REGULAR': '.+?name="(.+?)"'},{'ID': 'value', 'REGULAR': '.+?value="(.+?)"'}]]
                            即一次接口调用缓存多个需求数据

                        示例：CALLBACK = ['Cookie', [{'ID': XXX, 'REGULAR': 'XXXX'}, {'ID': XXX, 'REGULAR': 'XXXX'}]] 
                    

                    注：不管“接口响应数据”类型是否为json；如果需要对“接口响应结果”进行数据缓存则在 CALLBACK 参数中必须要指明“接口响应结果数据指定ID”；否则会对数据读取产生影响。

                    书写示例[--yaml文件写法--]：
                        “json类型”
                        CALLBACK: 
                            - Cookie
                            - 自定义ID
                    
                    书写示例[--yaml文件写法--]：
                        “非json类型”
                        CALLBACK:
                            - Cookie
                            -
                                - ID: XXX
                                REGULAR: XXX
                                - ID: XXX
                                REGULAR: XXX
                        
                    举例说明：
                        1、假设“A接口”请求需要保存其回调数据中的Cookie值，则在接口数据文件[InterfaceData.yaml]中“A接口的CALLBACK”参数书写为：
                            CALLBACK:
                                - Cookie
                        
                        2、假设“B接口”的请求需要保存其回调数据中的“接口响应结果”，则在接口数据文件[InterfaceData.yaml]中“B接口的CALLBACK”参数书写为：
                            CALLBACK:
                                - B_KEYID  # 此处为举例，名称随意不重复即可
                        
                        此时“响应结果缓存文件[Response_result.txt]”中的数据为：{'B_KEYID': “B接口响应结果”}
                            {'B_KEYID': {'name':"wangming", 'age':18}[此处为举例，用于“假设3”]}

                        3、假设“C接口”请求需要使用“B接口”响应结果中的某个值来作为“C接口的请求参数”，则在接口数据文件[InterfaceData.yaml]中“C接口的DATA”参数书写为：
                            DATA:
                                NAME[举例，需要参照接口书写]: CACHE['B_KEYID']['name']
                                AGE[举例，需要参照接口书写]: CACHE['B_KEYID']['age']
                            
                            解释：
                                “CACHE” 固定写法代表要使用“响应结果缓存文件[Response_result.txt]”中的缓存数据
                                “B_KEYID” 在“B接口”的“CALLBACK参数”中指定
                                “name” 响应结果中的key需要参照实际响应结果书写
                
                REGULAR：需要对“接口响应结果”进行筛选的“正则表达式”；如果该项为空[None]则代表不对“接口响应结果”进行筛选原样返还。
                    书写规则说明：该项为string类型不做规定格式限制，但要确保传入的值是有效的“正则表达式”否则会出现异常问题

                    书写示例[--yaml文件写法--]：
                        REGULAR：'[\u4e00-\u9fa5]+'  # 筛选所有汉字文本

                    注意：
                        1、此处正则表达式为举例，需要参照实际情况的需要书写。
                        2、该参数项只有在“接口响应结果”为非json数据时才会生效。


            _RESULT：参数填写规则解释：
                目前web系统中的接口响应结果为两种：“JSON类型”、“HTML”

                如果“接口响应结果”为JSON类型，则在进行“_RESULT”参数填写时为：
                    [--yaml文件写法--]
                    _RESULT:
                        status: SUCCESS [举例，需要参照实际“接口响应结果数据”填写]
                        msg: 上传成功！[举例，需要参照实际“接口响应结果数据”填写]
                        .....
                    
                    注：在“接口响应结果”为JSON类型时，脚本可支持“响应结果多参数判断”
                    
                如果““接口响应结果”为HTML类型”,则在进行“_RESULT”参数填写时为：
                    [--yaml文件写法--]
                        _RESULT: 系统登录正在进入系统请稍候 
                    
                    注：在“接口响应结果”为HTML类型时，脚本会对结果进行“正则表达式筛选”将所有汉字内容筛选出来
                    例如：“<div class=big1>正在进入OA系统，请稍候...</div>” 筛选完成后： “正在进入系统请稍候”


            _RS: 固定输入None，不做解释
        '''

        '''
        响应结果数据缓存文件[Response_result.txt]，数据结构及使用说明：
            {
                'CacheID[“缓存数据ID” yaml文件中指出]': CacheDATA'[“缓存数据” 数据类型不限，目前常用 string、dict]'
                ...
                例如：
                'login_One': '登录成功！！' [string]
                'File_Upload_One': {"id": "882@2202_383612189,","name": "test1.jpeg*"} [json]
            }

            注：
                1、整个文件的数据操作，全部根据其“唯一标识”[CacheID 缓存ID]进行操作。

                2、为了避免冗余数据的产生，在对应的“模块接口”全部调用结束之后[即：模块对应的 InterfaceData.yaml文件读取完毕,且全部为“运行成功”状态]，
                会对响应结果数据缓存文件[Response_result.txt]进行清空操作。

                3、如果需要使用缓存数据作为“接口请求参数”则在相应的“接口yaml数据”中声明即可。
                例如：
                    [--dict格式写法--]
                    DATA: {"ATTACHMENT_ID"："CACHE['login_One']"} [取出数据为 string]
                    DATA: {"ATTACHMENT_ID"："CACHE['File_Upload_One']['name']"} [取出数据为 json]

                    [--yaml文件写法--]
                    DATA:
                        ATTACHMENT_ID: CACHE['File_Upload_One']['name']

                说明：
                    ATTACHMENT_ID [接口请求参数key，此处为举例；实际使用需要根据相应接口进行调整]

                    CACHE [固定写法，代表需要使用缓存数据]；如果不需要使用“缓存数据”则直接写入对应的value值即可。例如：DATA: {"ATTACHMENT_ID": 1}

                    如果你需要将两个缓存数据进行“拼接操作” 如：文件批量上传时经常出现的 “test1.jpeg,test2.jpeg”情况，可以用“+”号连接。如下书写：
                    FILE_NAME: CACHE['File_Upload_One']['name']+CACHE['File_Upload_Two']['name']  # 注意不要出现空格符
        '''
        '''
        接口请求参数使用“缓存数据”、“预设数据”时的书写说明：

            1、缓存数据：这里的解释为“在接口数据文件执行过程中通过‘CALLBACK’参数项暂时存储在‘接口响应结果缓存文件 Response_result.txt’中的数据”

                书写示例：DATA(PARAMS参数同样适用):
                            KEY1: CACHE['数据存放时指定的key键']  # CACHE[XXX]固定写法
                
                注：此类型的数据会在“接口数据执行完毕”之后被清空
            
            2、预设数据：这里的解释为“在接口请求之前”提前存储好的关键数据，例如“主角色信息”、“OA用户数据”

                2.1 “主角色信息”使用书写示例:
                    DATA(PARAMS参数同样适用):
                        KEY1: MAIN_ROLE-Uid  # 对应主角色“权重编号”

                    MAIN_ROLE-ID  # 主角色ID
                    MAIN_ROLE-Name  # 主角色实际姓名
                    MAIN_ROLE-priv_id  # 主角色 职务ID
                    MAIN_ROLE-priv_name  # 主角色 职务
                    MAIN_ROLE-DLN  # 主角色所属部门
                    MAIN_ROLE-AS  # 主角色在线，离线状态
                
                2.2 “OA用户数据”使用书写示例：
                    DATA(PARAMS参数同样适用):
                        KEY1: USER_REPLACE_ID['XXXX']  # 对应某个(XXXX)用户的“ID”

                    USER_REPLACE_Name['XXXX']  # 对应某个(XXXX)用户的“实际姓名”
                    USER_REPLACE_UserName['XXXX']  # 对应某个(XXXX)用户的“登录用户名”

                    注：XXXX为要提取人员信息的姓名全拼；例如: “刘明才 USER_REPLACE_ID['liumingcai']”
                
                注：此类型的数据是永久保存的，每次对任意“接口数据文件”操作时都会更新文件中的数据
        '''
        return


    '''构造函数'''
    def __init__(self) -> None:
        self.COOLIE_FILE = f"{PROJECTROOT}\\data\\cache\\cookie.txt"  # Cookie
        self.RESULT_FILE = f"{PROJECTROOT}\\data\\cache\\response_result.txt"  # 响应结果
        self.yaml = YAML()
        self.logicFunction_Object = isLogicMethodClass()
        self.CODE = 'utf-8'  # 测试系统接口编码格式


    '''入口函数'''
    def __call__(self, File_Src) -> None:
        '''
         @param File_Src：需要进行数据读取的[InterfaceData.yaml]文件路径
        '''
        __MappingSrc = self.__mapping(File_Src)
        __Execute =  self.__read_InterfaceData(__MappingSrc)

        if __Execute:
            '''流程正常结束'''
            self.__file_Tool(self.RESULT_FILE, "w")  # 清空 “响应结果数据缓存文件”
            os.remove(__MappingSrc)  # 删除“接口数据”映射文件
            return True

        else:
            '''接口回调数据验证失败'''
            return False
    

    '''文件操作工具函数'''
    def __file_Tool(self, SRC, OPER='r', W_DATA=None):
        '''
         @param SRC：需要进行操作的文件路径
         @param oper：需要进行何种操作 [w写入, r读取]；默认值为 'r读取'
         @param w_data：需要进行写入文件的数据; OPER为“w写入操作”时生效
        '''
        file_Type = True if 'yaml' in "".join(SRC.split('\\')[-1:]) else False  # 文件类型获取[True: yaml文件 || False: txt文件]
        file_Object = open(SRC, mode=OPER, encoding='utf-8') if file_Type else open(SRC, OPER)  # 生成文件对象
        read_Data = None  # 数据读取结果暂存

        if OPER.lower() == 'w':
            '''写入操作'''
            if W_DATA:
                self.yaml.dump(W_DATA, file_Object) if file_Type else file_Object.write(str(W_DATA))
        else:
            '''读取操作'''
            read_Data = self.yaml.load(file_Object) if file_Type else "".join(file_Object.readlines())
        file_Object.close()  # 关闭文件对象

        return read_Data  # 返还读取数据；“写入操作”时返还为None


    '''接口数据映射文件[_InterfaceData.yaml]处理操作封装'''
    def __mapping(self, File_Src):
        '''
         @param File_Src：需要进行数据读取的[InterfaceData.yaml]文件路径
        '''
        mapping_src = "\\".join(File_Src.split("\\")[:-1]) + "\\_InterfaceData.yaml"
        if os.path.exists(mapping_src):
            '''映射文件已存在，数据操作'''
            source_data = self.__file_Tool(File_Src)
            mapping_data = self.__file_Tool(mapping_src)
            pop_key = [key for key in mapping_data.keys() if mapping_data[key]['_RS'] == True]  # 记录已执行数据

            for key in pop_key: mapping_data.pop(key)
            for i_key in source_data.keys():  # 源文件是否出现数据改动判别
                if i_key in mapping_data:
                    for p_key in [key for key in source_data[i_key].keys()][:-1]:
                        if source_data[i_key][p_key] != mapping_data[i_key][p_key]:
                            mapping_data[i_key][p_key] = source_data[i_key][p_key]  # 数据不一致, 以“源数据”为准进行数据替换
                else:
                    pass
            
            self.__file_Tool(mapping_src, 'w', mapping_data)  # 处理数据写入

        else:
            os.system(f'copy {File_Src} {mapping_src}')
        
        return mapping_src  # 返还“映射文件”路径


    '''接口缓存数据“提取”操作封装'''
    def __cache_Data(self, O_DATA=None, CD='RESULT'):
        '''
         @param O_DATA：选填项；代表要进行处理的“接口请求数据[DATA][PARAMS]”
         @param CD：选填项；代表要“提取”缓存数据的类型 [COOKIE cookie, RESULT 响应结果, ROLE 角色]
        '''
        # STR_DATA = self.__file_Tool(self.RESULT_FILE if CD == 'RESULT' else self.COOLIE_FILE if CD == 'COOKIE' else self.ROLE_FILE)  # 缓存数据取出
        STR_DATA = self.__file_Tool(self.RESULT_FILE if CD == 'RESULT' else self.COOLIE_FILE)  # 缓存数据取出
        CONTENT = eval(STR_DATA) if STR_DATA else STR_DATA
        if not O_DATA:
            '''原样返还[Cookie、数据响应结果]'''
            return CONTENT
        else:
            '''处理返还[主要针对“取出缓存的响应结果数据”]'''
            Rewrite = {}; Tran_value = None  # 过渡数据暂存
            O_DATA = eval(self.logicFunction_Object.beforehand(f'''{O_DATA}'''))
            for key in O_DATA.keys():
                try:
                    if 'CACHE' in O_DATA[key]:
                        '''缓存数据提取'''
                        String = O_DATA[key].replace('CACHE', 'CONTENT')
                        if '+' in String:  # 参数拼接判断
                            for EXPRESSION in String.split('+'): Tran_value += eval(EXPRESSION)  # 处理数据写入
                        else:
                            Tran_value = eval(String)  # 处理数据写入
                    else:
                        '''response.apparent_encoding'''
                        Tran_value = O_DATA[key].encode(self.CODE)
                except:
                    Tran_value = O_DATA[key]  # 原样写入
                finally:
                    Rewrite[key] = Tran_value  # 数据写入

            return Rewrite  # 重写结果返还


    '''接口回调数据处理封装'''
    def __callback_Data(self, DATAGRID, RESPONSE, RE):
        '''
         @param DATAGRID: 必填项；代表需要进行缓存操作的数据列表 [由__call_Interface() 方法传入, 对应CALLBACK参数]
         @param RESPONSE: 必填项；接口请求对象 [由__call_Interface() 方法传入]
         @param RE: 必填项；代表要进行请求结果筛选的“正则表达式” [由__call_Interface() 方法传入, 对应REGULAR参数]
        '''
        __DICT_COOKIE = {}  # Cookie 字典化处理结果暂存
        __RESPONSE_RESULTS = None  # 接口响应结果暂存
        __TRAN_DATA = {}  # 过渡数据暂存

        '''接口响应结果处理'''
        try:
            __RESPONSE_RESULTS = json.loads(RESPONSE.text)  # json数据解析
        except Exception as error:
            __RESPONSE_RESULTS = "".join(re.findall(f"{RE}", RESPONSE.text)) if RE else RESPONSE.text  # [响应结果返还]正则表达式筛选

        '''接口回调数据缓存处理'''
        for ITME_KEY in DATAGRID:
            if 'Cookie' in ITME_KEY:
                '''Cookie缓存Json化处理'''
                Source_Cookies = re.findall(r"[[](.*?)[]]", str(RESPONSE.cookies))
                for Cookie in "".join(Source_Cookies).split(','):
                    Cookie_Text = "".join(re.findall(r"[<](.*?)[>]", Cookie))
                    C_KEY = Cookie_Text.split(' ')[1].split('=')[0]; C_VALUE = Cookie_Text.split(' ')[1].split('=')[1]

                    __DICT_COOKIE[C_KEY] = C_VALUE

                if ITME_KEY == 'A_Cookie':  # 文件数据保存判断
                    COOKIE_CACHE_DATA = self.__cache_Data(CD='COOKIE')
                    for key in COOKIE_CACHE_DATA.keys():
                        if key in __DICT_COOKIE:
                            '''数据一致性判断'''
                            __DICT_COOKIE[key] = COOKIE_CACHE_DATA[key] if COOKIE_CACHE_DATA[key] != __DICT_COOKIE[key]\
                                else __DICT_COOKIE[key]
                        else:
                            '''追加键值对'''
                            __DICT_COOKIE[key] = COOKIE_CACHE_DATA[key]

                self.__file_Tool(self.COOLIE_FILE, "w", W_DATA=str(__DICT_COOKIE))  # 将处理后的Cookie存入
            else:
                '''响应结果数据处理'''
                if isinstance(__RESPONSE_RESULTS, str):
                    for Num in range(0, len(ITME_KEY)):
                        __TRAN_DATA[ITME_KEY[Num]['ID']] =\
                            "".join(re.findall(f"{ITME_KEY[Num]['REGULAR']}", RESPONSE.text.replace('\n', '')))  # [响应结果缓存]正则表达式筛选
                else:
                    __TRAN_DATA[ITME_KEY] = __RESPONSE_RESULTS

                for key in __TRAN_DATA.keys():
                    RESULT_CACHE_DATA = self.__cache_Data(CD='RESULT')
                    if RESULT_CACHE_DATA:
                        '''追加'''
                        RESULT_CACHE_DATA[key] = __TRAN_DATA[key]
                    else:
                        '''新建'''
                        RESULT_CACHE_DATA = {}; RESULT_CACHE_DATA[key] = __TRAN_DATA[key]

                    self.__file_Tool(self.RESULT_FILE, "w", W_DATA=RESULT_CACHE_DATA)  # 将“接口响应结果”存入

        return __RESPONSE_RESULTS

    
    '''接口[Requests] 调用封装'''
    def __call_Interface(self, URL, HEADER=None, DATA=None, PARAMS=None, FILE=None, I_CODE=None, COOKIE=None, CALLBACK=[], REGULAR=None, METHOD='GET'):
        '''
         @param METHOD：必填项；请求类型 [默认值：GET]
         @param URL：必填项；接口地址
         @param HEADER：选填项 dict类型；请求头
         @param DATA：选填项 dict类型；接口请求参数[不需要请求参数URL解码时使用]
         @param PARAMS：选填项 dict类型；接口请求参数[需要请求参数URL解码时使用]
         @param FILE：dict类型；文件参数 [书写示例：{'FILE_KEY':'file', 'NAME':'test1.jpeg', 'SRC':'XXX\\test1.jpeg', 'TYPE':'image/jpeg'}]
         @param I_CODE：选填项 string类型；接口请求参数编码
         @param COOKIE：选填项 dict类型；登录态
         @param CALLBACK：选填项 list类型；是否需要缓存接口回调数据中的信息。[目前支持缓存“Cookie”，“接口响应结果”]
         @param REGULAR: 选填项；需要对“非json数据类型的接口响应结果”进行筛选的“正则表达式”，为空则代表不进行筛选“响应结果原样返还”
        '''

        '''预请求数据处理'''
        if COOKIE == 'CACHE': COOKIE = self.__cache_Data(CD='COOKIE')  # 缓存Cookie提取
        
        if I_CODE: self.CODE = I_CODE  # 请求接口编码I_CODE“预处理”

        if DATA: DATA = self.__cache_Data(DATA)  # 请求参数DATA“预处理”
        
        if PARAMS: PARAMS = self.__cache_Data(PARAMS)  # 请求参数PARAMS“预处理”
        
        if FILE:  # “文件”参数预处理
            FILE = eval(self.logicFunction_Object.beforehand(f"{FILE}")); TRAN_FILE = {}
            if isinstance(FILE, list):
                for ITEM_DICT in FILE: TRAN_FILE[ITEM_DICT['FILE_KEY']] = (ITEM_DICT['NAME'], open(ITEM_DICT['SRC'], 'rb'), ITEM_DICT['TYPE'])
            else:
                TRAN_FILE[FILE['FILE_KEY']] = (FILE['NAME'], open(FILE['SRC'], 'rb'), FILE['TYPE'])
            FILE = TRAN_FILE  # 处理数据写入

        '''调用请求'''
        response = requests.request(METHOD.upper(),  f"{GSDSTORE['START']['url']}/{URL}", data=DATA, params=PARAMS, headers=HEADER, files=FILE, cookies=COOKIE)

        ''''接口回调数据，处理返还'''
        return self.__callback_Data(CALLBACK, response, REGULAR)


    '''接口数据[InterfaceData.yaml]读取、调用操作封装'''
    def __read_InterfaceData(self, Mapping_Src):
        '''
         @param Mapping_Src：需要进行数据读取的[_InterfaceData.yaml]映射文件路径
        '''
        __RESULT = None  # 接口响应结果
        __OPER_DATA = self.__file_Tool(Mapping_Src)  # 接口数据取出
        
        '''执行调用流程'''
        pbar = tqdm([key for key in __OPER_DATA.keys()])
        for _key in pbar:
            pbar.set_description("\r “测试数据”生成中： %s" % _key)

            '''请求参数处理'''
            _PAR = 'DATA' if 'DATA' in __OPER_DATA[_key]['_PARAMETERS'] else 'PARAMS' if 'PARAMS' in __OPER_DATA[_key]['_PARAMETERS'] else False  # 请求参数有无判别
            if _PAR and isinstance(__OPER_DATA[_key]['_PARAMETERS'][_PAR], list):
                '''循环接口调用'''
                PARAMETERS = {}
                for index in range(0, len(__OPER_DATA[_key]['_PARAMETERS'][_PAR])):
                    '''请求参数字典数据重写'''
                    for key in __OPER_DATA[_key]['_PARAMETERS'].keys():
                        PARAMETERS[key] = __OPER_DATA[_key]['_PARAMETERS'][key] if key != _PAR else __OPER_DATA[_key]['_PARAMETERS'][key][index]

                    __RESULT = self.__call_Interface(**PARAMETERS)
            else:
                '''单接口调用'''
                __RESULT = self.__call_Interface(**__OPER_DATA[_key]['_PARAMETERS'])

            '''响应结果比对处理'''
            if not self.__result_Comparison(_key, __OPER_DATA, __RESULT): return False
            self.__file_Tool(Mapping_Src, 'w', __OPER_DATA)  # 流程执行结果写入

        '''流程执行结果返还'''
        return True
    

    '''接口响应结果比对处理封装'''
    def __result_Comparison(self, _key, __OPER_DATA, __RESULT):
        '''
         @param _key: 由 __read_InterfaceData()方法传入，代表当前正在执行的“接口key键”
         @param __OPER_DATA: 由 __read_InterfaceData()方法传入，当前正在操作的“接口映射文件”数据
         @param __RESULT: 由 __read_InterfaceData()方法传入，接口回调结果
        '''
        __outcome = None  # 比对结果

        if '_RESULT' in __OPER_DATA[_key]: 
            ACTUAL_RESULT = __RESULT; EXPECT_RESULT = __OPER_DATA[_key]['_RESULT']

            if isinstance(ACTUAL_RESULT, dict):
                for key in __OPER_DATA[_key]['_RESULT'].keys(): __outcome = False if EXPECT_RESULT[key] != ACTUAL_RESULT[key] else True
            else:
                __outcome = True if self.logicFunction_Object.mutual_in(str(ACTUAL_RESULT), str(EXPECT_RESULT)) else False
            
            __OPER_DATA[_key]['_RS'] = __outcome  # 接口“运行状态”值修改
            if not __outcome: 
                trusteeship.debug(f'common_Interface_Class --- 执行终止 --- [{_key}]接口响应结果出错: ')
                trusteeship.debug(f"实际响应结果：{ACTUAL_RESULT}    预期响应结果：{EXPECT_RESULT}")
                return __outcome
        else:
            '''不需要进行预期结果值比对'''
            __outcome = True
            __OPER_DATA[_key]['_RS'] = __outcome  # 接口“运行状态”值修改

        '''比对结果返还'''
        return __outcome