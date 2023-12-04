'''# Third_party'''
from ruamel.yaml import YAML



class isToolClass:

    def __init__(self):
        self.yaml = YAML()  # 实例化yaml文件操作对象


    '''.yaml||.txt文件数据读写'''
    def raw_YamlTxt(self, fileSrc, oper='r', writeData=None):
        '''
         # oper: 操作方法[r读出、w写入、a追加]

         # writeData: 需要写入的数据[string、list]

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
        # 用于解决in关键字单向包含的问题
        self.former = former.replace(' ',''); self.latter = latter.replace(' ','')  # 多余空格清除
        return (self.former in self.latter) or (self.latter in self.former)