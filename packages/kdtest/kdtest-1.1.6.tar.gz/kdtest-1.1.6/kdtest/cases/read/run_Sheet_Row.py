'''# Third_party'''
from openpyxl.styles import *
'''# built_in'''
import traceback
'''custom'''
from action.key_Retrieval import SurveyKeyWord
from action.page_Action import KeyWordTest
from cases.read.cell_Value_Handle import CellValueHandle
from utils.decorator import case_retry
from utils.log.trusteeship import trusteeship


class RunSheetRow(CellValueHandle):

    def __repr__(self) -> str:
        return '单条步骤行操作处理'

    def __init__(self) -> None:
        super().__init__()
        self.survey = SurveyKeyWord()
        self.keyWord = KeyWordTest()

    @case_retry()
    def __call__(self, WS_Object, ws_rowsMax, elementExpression):
        """
         参数：
            @param WS_Object : 模块用例步骤文件单独sheet表对象
            @param ws_rowsMax : sheet表最大操作行数
            @param elementExpression : 模块用例caseStep.yaml文件内容
        """
        result_Step_Assert = True  # 步骤行执行结果“断言判断开关”
        result_Step_Abnormal = False  # 步骤行执行结果“异常判断开关”
        start_Row = 2  # sheet表，“行”起始位置
        end_Column = 0  # sheet表，“列”结束位置
        accept_Result = []  # 步骤行断言结果暂存数组
        for column in range(WS_Object.max_column, 1, -1):
            if WS_Object.cell(row=1, column=column).value: end_Column = column; break

        trusteeship.case_start()  # sheet表日志记录开始
        while start_Row <= ws_rowsMax:
            cellValueAggregation = super().__call__(WS_Object, start_Row, end_Column, elementExpression)
            step_Result = 'PASS'; step_Error = ''  # 步骤结果信息
            try:
                '''调用关键字检索函数, 完成相应操作'''
                result_Step_Assert = self.survey.keyRetrieval(self.keyWord, 
                    cellValueAggregation['tagging'],
                    cellValueAggregation['keywordName'],
                    cellValueAggregation['positionInformation'],
                    cellValueAggregation['manipulatedValue'])
            except Exception:
                '''异常抛出写入'''
                trusteeship.exceptinfo("\nAn exception problem was caught: ")
                result_Step_Abnormal = True  # 异常开关打开
                step_Error = traceback.format_exc()  # 异常信息
                step_Result = 'ABNORMAL'
            else:
                '''未出现异常，断言结果判断'''
                if (not result_Step_Assert) and result_Step_Assert != None:
                    step_Result = 'FAIL'; accept_Result.append(False)
                elif isinstance(result_Step_Assert, str) and ('isCycleSS_' in result_Step_Assert):
                    start_Row += int(result_Step_Assert[len('isCycleSS_'):])  # 步骤行值变化

            start_Row += 1  # 步骤行值变化
            cellValueAggregation['inColl']['R'] = [step_Result, f"{step_Result}-TEXT"]; cellValueAggregation['inColl']['E'] = [step_Error, "ERROR"]
            trusteeship.case_step(cellValueAggregation['inColl'])

        return {'abnormalJudgment': result_Step_Abnormal, 'caseError': step_Error, 'acceptResult': accept_Result}