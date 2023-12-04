'''# custom'''
from utils.public_Script import isLogicMethodClass


class CellValueHandle:

    def __repr__(self) -> str:
        return '用例步骤文件，各步骤行单元格值获取并处理'

    def __init__(self) -> None:
        self.logicFunction_Object = isLogicMethodClass()  # 实例化公共脚本对象

    def __call__(self, WS_Object, startRow, endColumn, elementExpression) -> None:
        self.WS_Object = WS_Object
        self.startRow = startRow
        self.endColumn = endColumn
        self.elementExpression = elementExpression

        '''读出步骤行单元格值'''
        self.__get_Value()

        '''处理步骤行单元格值'''
        self.__handle_Value()

        self.inColl = {'T':[self.tagging, "TAGGING"], 'K':[self.keywordName, "KEYWORD"], 'P':[self.incoll_positionInformation, "PASITION"], 'M':[self.incoll_manipulatedValue, "MANIPULATED"]}
        '''返还步骤行单元格值'''
        return {
            'inColl': self.inColl,
            'tagging': self.tagging,
            'keywordName': self.keywordName,
            'positionInformation': self.positionInformation,
            'manipulatedValue': self.manipulatedValue
        }

    def __get_Value(self) -> None:
        value_list = [self.WS_Object.cell(row=self.startRow, column=column).value for column in range(3, self.endColumn + 1)]
        self.tagging = value_list[0]  # 步骤说明
        self.keywordName = value_list[1]  # 关键字
        self.positionInformation = [item for item in value_list[2:-1] if (item != None)]  # 元素定位
        self.manipulatedValue = value_list[-1]  # 操作值
        self.incoll_positionInformation =  ", ".join(map(str, self.positionInformation))
        self.incoll_manipulatedValue = self.manipulatedValue

    def __handle_Value(self) -> None:
        # positionInformation 值处理
        if self.positionInformation and ('/' in self.positionInformation[0]):
            try: 
                node_Key = self.positionInformation[0].split('/')
                self.positionInformation = self.elementExpression[node_Key[0]][node_Key[1]] + self.positionInformation[1:]
            except Exception as error:
                self.incoll_positionInformation += " 该行元素操作关键字书写错误！"

        # manipulatedValue 值处理
        try:
            self.manipulatedValue.strip()[5]  # string类型且不为空字符
        except Exception as error:
            pass
        else:
            '''操作内容预处理'''
            self.manipulatedValue = self.logicFunction_Object.beforehand(self.manipulatedValue)