'''# Third_party'''
from ruamel.yaml import YAML
'''# built_in'''
import re
'''# custom'''
from common import GSDSTORE
from utils.built_In_Function import Built_In_Function


class isLogicMethodClass:

    '../elementData/Login/elementData.yaml'
    def __init__(self):
        self.BI_function_Obj = Built_In_Function()  # 实例化Built_in_function模块对象
        self.yaml = YAML()  # 实例化yaml文件操作对象

        self.CONTRAST = {
            'FUNCTION': ['get_PrestoreData', 'System_date', 'get_thisWeek', 'get_thisMonth', 'get_thisYear', 'Increasing_date', 'Intercept_date', 'Mktime_date'],
            'PATH':['WORK_PATH-ROOT', 'WORK_PATH-PACKET', 'WORK_PATH-INTERFACE', 'WORK_PATH-ELEMENT'],
            'SDPI': GSDSTORE['START']['selfDefinedParameter'].keys() if 'selfDefinedParameter' in GSDSTORE['START'].keys() else []
        }  # "预处理数据" 筛查字典


    '''.yaml||.txt文件数据读写'''
    def raw_YamlTxt(self, fileSrc, oper='r', writeData=None):
        '''
         参数：
            @param oper: 操作方法[r读出、w写入、a追加]
            @param writeData: 需要写入的数据[string、list]

         注：除“r读”操作外，其它操作函数返还结果均为“None”
        '''
        file_Type = True if 'yaml' in "".join(fileSrc.split('\\')[-1:]) else False
        file_Object = open(fileSrc, mode=oper, encoding='utf-8') if file_Type else open(fileSrc, oper)  # 生成文件对象
        read_Data = None

        if oper in ['w', 'a']:
            '''写入操作'''
            if writeData:
                self.yaml.dump(writeData, file_Object) if file_Type else file_Object.write(str(writeData))
        else:
            '''读取操作'''
            read_Data = self.yaml.load(file_Object) if file_Type else "".join(file_Object.readlines())

        file_Object.close()
        return read_Data
    

    '''两值互相包含检查'''
    def mutual_in(self, former, latter):
        # 用于解决 python - in 方法单向包含的问题
        try:
            former = former.strip(); latter = latter.strip()  # 首尾空格清除
        except Exception:
            pass
        else:
            if former != "" and latter != "":
                return (former in latter) or (latter in former)
        return False


    '''正则表达式[日期、时间、整型、文本]数据提取'''
    def Regular_takeData(self, operation_text, Data_Type='date'):
        '''operation_text：操作字符串  ||  data_type：要获取数据类型 [(date默认)、time、dateTime、int、text]'''
        pattern = r'(\d{4}-\d{1,2}-\d{1,2})'\
            if Data_Type == 'date' else r'(\d{1,2}:\d{1,2}:\d{1,2})'\
            if Data_Type == 'time' else r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})'\
            if Data_Type =='dateTime' else r'(\d+\.?\d*)'\
            if Data_Type == 'int'  else r'[\u4e00-\u9fa5]+'
        pattern = re.compile(pattern)

        return pattern.findall(operation_text)  # 返还处理结果
    

    '''用例步骤 “函数操作值” 预处理'''
    def beforehand(self, data_text):
        '''
         res = re.findall(r'[(](.*?)[)]', '父串')
         entity_startindex = [i.start() for i in re.finditer('子串', '父串')]
         %Y-%m-%d %H:%M
        '''
        function_list = [function for function in self.CONTRAST['FUNCTION'] if function in data_text]  # 内置函数筛选
        workpath_list = [workpath for workpath in self.CONTRAST['PATH'] if workpath in data_text]  # 工作路径
        identity_list = [identity for identity in self.CONTRAST['SDPI'] if identity in data_text]  # 自定义参数标识筛选

        '''插值函数封装'''
        def interpolation(P_string, Emb, new):
            '''P_string：操作字符串  ||  Emb：内嵌函数  ||  new：新值'''
            tran_string = P_string[P_string.find(Emb):]; tran = tran_string[:tran_string.find(')') + 1]
            if Emb in tran:
                '''指定插值操作'''
                P_string = P_string.replace(tran, new)
            return P_string

        '''函数主逻辑'''
        if function_list or identity_list or workpath_list:
            '''内置函数相关'''
            for fun in function_list:
                tran = {}  # 函数参数值暂存字典
                function_Object = getattr(self.BI_function_Obj, fun)  # 内置函数对象

                for cum in range(0, data_text.count(fun)):  # 遍历预处理函数调用次数
                    tran_string = data_text[data_text.find(fun):]; par_text = tran_string[:tran_string.find(')') + 1]; res = re.findall(r'[(](.*?)[)]', par_text)
                    '''形参对应函数'''
                    tran[fun] = res[0] if fun == par_text[:par_text.find('(')] else ''

                    '''插值判断'''
                    if tran[fun]:  # 带参调用
                        data_text = interpolation(data_text, fun, function_Object(tran, fun))

                    else:  # 无参调用
                        if fun in ['get_PrestoreData']:
                            '''目前无参函数只支持 get_PrestoreData()函数，其他后续随功能需求补齐'''
                            data_text = interpolation(data_text, fun, function_Object())
            else:
                '''工作路径相关'''
                if workpath_list:
                    for path in workpath_list:
                        iden = "".join(path.split("-")[-1]);data_text = data_text.replace(path, GSDSTORE['WORKPATH'][iden]);data_text = data_text.replace('\\', '\\\\')
                
                '''自定义参数标识'''
                if identity_list:
                    for iden in identity_list: data_text = data_text.replace(iden, GSDSTORE['START']['selfDefinedParameter'][iden])

        '''函数结果返还'''
        return data_text  # 此处注意：经过预操作后的数据全部都会转换成 string类型