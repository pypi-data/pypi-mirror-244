'''# built_in'''
import os, json, traceback
'''# custom'''
from common import GSDSTORE, INTER, ELE, PARA
from reference import GSTORE


class InitializationParameter:

    def __init__(self) -> None:
        GSDSTORE['START'] = {}

    def __call__(self):
        '''自定义文件静态配置执行'''
        try:
            with open(f'./{PARA}.json', 'r', encoding="utf-8") as f:
                parameter = json.load(f)
        except Exception as error:
            print(f"No necessary documents：{PARA}.json ! \n{traceback.format_exc()}")
        else:
            notPath = [case['caseFilePath'] for case in parameter['testCaseFile'] if not os.path.exists(f"{GSDSTORE['WORKPATH']['ROOT']}\\{case['caseFilePath']}")]
            if notPath: print(f"所指定的用例步骤文件列表中，存在非法项：{notPath}"); raise Exception

            GSDSTORE['START']['testCaseFile'] = [
                dist for dist in parameter['testCaseFile'] if not dist.update({"caseFilePath": f"{GSDSTORE['WORKPATH']['ROOT']}\\{dist['caseFilePath']}"})
            ]
            GSDSTORE['START']['browser'] = parameter['testEnvironment']['browser']
            GSDSTORE['START']['url'] = parameter['testEnvironment']['url']
            GSDSTORE['START']['implicitlyWait'] = parameter['testEnvironment']['implicitlyWait']
            GSDSTORE['START']['auxiliaryFunction'] = parameter['auxiliaryFunction']
            if 'selfDefinedParameter' in parameter.keys(): GSDSTORE['START']['selfDefinedParameter'] = parameter['selfDefinedParameter']

        '''
            全局数据 - 工作目录路径信息 interfacePath elementPath
        '''
        for folder in os.listdir(f"{GSDSTORE['WORKPATH']['PACKET']}"):
            if folder[:len(INTER)] in INTER: GSDSTORE['WORKPATH']['INTERFACE'] = f"{GSDSTORE['WORKPATH']['PACKET']}\\{folder}"
            if folder[:len(ELE)] in ELE: GSDSTORE['WORKPATH']['ELEMENT'] = f"{GSDSTORE['WORKPATH']['PACKET']}\\{folder}"
        
        GSTORE['START'] = GSDSTORE['START']