'''# Third_party'''
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from kdtest import GSTORE, INFO, reset_implicitlyWait
'''# built_in'''
import re
import os
'''# .utils'''
from .utils.tool import isToolClass



class OA_webUI(object):

    def __repr__(self) -> str:
        return '公共UI操作方法库'


    def __init__(self) -> None:
        self.__CDCG = {}  # 全局数据缓存
        self.__logicFunction_Object = isToolClass()
        self.__elementNode_Data = self.__logicFunction_Object.raw_YamlTxt(f'{os.path.dirname(__file__)}\\elementData\\elementData.yaml')  # 读取WebUI公共套件的节点数据
        self.__ModularNode_Information = self.__logicFunction_Object.raw_YamlTxt(f'{os.path.dirname(__file__)}\\elementData\\modularInformation.json')  # 读取goto_Modular方法的各级模块节点信息
    

    '''# 用户登录'''
    def userLogin(self, userName=None, userPassword=None):
        '''
         参数：
            @param userName : 用户名
            @param userPassword : 密码
        '''
        KEYWORD = GSTORE['keyWord']  # 取出关键字对象

        if userName != None:
            KEYWORD.input_text(*self.__elementNode_Data['login']['userName'], content=userName)  # 用户名

        if userPassword != None:
            KEYWORD.input_text(*self.__elementNode_Data['login']['password'], content=userPassword)  # 密码

        # 点击登录按钮
        KEYWORD.click_btn(*self.__elementNode_Data['login']['submit'])


    '''# frame跳转封装'''
    def jumpFrame(self, Hierarchy):
        '''
        参数：
            @param Hierarchy : 代表要跳转的frame的层级以及，对应层级的节点 | List类型; Hierarchy = [3,['id', 'index', 'src']]
        
        注意：
            1、函数不做正确性判断，注意传入的层级节点的对应关系正确
            2、函数中的可以处理三种类型的“iframe标识”分别为 [标签ID、标签索引、标签src属性值]
        '''
        driver = GSTORE['driver']; KEYWORD = GSTORE['keyWord']

        driver.switch_to.default_content()  # 焦点切换回原页面
        operFrameList = Hierarchy[1]; operFrameIden = None
        for Item in operFrameList:
            try:
                operFrameIden = int(Item)  # 索引
            except Exception as error:
                if re.findall(r"[http\[s\]?://]?([/]|[\\]|[a-zA-Z0-9]\.[a-zA-Z])+", Item):
                    frame_Ele = KEYWORD.locators('tag_names', 'iframe')
                    for index in range(0, len(frame_Ele)):
                        if Item in frame_Ele[index].get_attribute('src'):
                            operFrameIden = index; break  # 路径索引
                else:
                    operFrameIden = Item  # ID

            '''iframe焦点跳转'''
            driver.switch_to.frame(operFrameIden)


    '''# 错误处理封装 【强制提示】'''
    @reset_implicitlyWait(1)
    def errorHandle(self, type=False, prompt_input=None):
        '''
         alert / 系统提示信息 / 右上角消息弹框
         参数：
            @param type : True代表点击alert弹框的【确定】按钮，False代表点击alert弹框的【取消】按钮
            @param alert_input : 代表在prompt弹框时要输入的文本内容

        注：
            1、提示处理优先级为 alert > 系统提示信息 > 右上角消息弹框
            2、由于系统中“tips 系统提示框”的操作按钮并不统一，故函数中采用“对照列表 [TIPS_BTN_ELE]”的方法进行操作
            3、函数中的元素判断采用EC[预期条件]模块方式
        '''
        driver = GSTORE['driver']; KEYWORD = GSTORE['keyWord']  # 暂存对象取出
        
        OPERATION = ['ALERT_ELE', 'TIPS_ELE', 'TIPS_SPRING_ELE']
        RETURN_Information = None; ALERT_ELE = None; TIPS_ELE = None; TIPS_SPRING_ELE = None # 过渡操作变量定义
        TIPS_BTN_ELE = self.__elementNode_Data['error']['TIPS_BTN_ELE']  # “系统提示信息处理” 操作按钮[返回、关闭..]元素节点暂存

        try:
            ALERT_ELE = WebDriverWait(driver, 2, 0.5).until(EC.alert_is_present())  # alert 提示框判断
        except Exception as error:
            TIPS_ELE = EC.presence_of_element_located((By.CSS_SELECTOR, self.__elementNode_Data['error']['TIPS']))(driver) # 系统提示信息 元素判断
            if not TIPS_ELE:
                TIPS_SPRING_ELE = EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.__elementNode_Data['error']['BOUNCED']))(driver)  # 系统右上角提示弹框

        '''INFO(f'ALERT_ELE is {ALERT_ELE}  TIPS_ELE is {TIPS_ELE}  TIPS_SPRING_ELE is {TIPS_SPRING_ELE}')'''
        for key in OPERATION:
            if eval(key):
                if key == 'ALERT_ELE':
                    '''alert提示框操作'''
                    RETURN_Information = ALERT_ELE.text
                    if prompt_input: ALERT_ELE.send_keys(prompt_input)  # prompt弹框输入判断
                    ALERT_ELE.accept() if type else ALERT_ELE.dismiss()  # 模拟alert点击
                    break
                elif key == 'TIPS_ELE':
                    '''系统提示信息处理'''
                    RETURN_Information = TIPS_ELE.text

                    for key in TIPS_BTN_ELE.keys():
                        BTN_ELE = KEYWORD.locators(*TIPS_BTN_ELE[key])  # 操作按钮查找
                        if BTN_ELE:
                            KEYWORD.click_btn(*TIPS_BTN_ELE[key]); break  # 操作按钮点击
                    break
                else:
                    '''右上角消息弹框处理'''
                    self.TipsSpringFrame('readAll')  # 调用公共库
                    break
            else:
                '''元素未加载；不做操作'''
                pass
        
        INFO(f'提示信息：{RETURN_Information}')
        if RETURN_Information: return RETURN_Information


    '''# 文本弱提示处理【弱提示】'''
    def WeakHint(self):
        '''用于处理文本输入框的弱提示'''
        driver = GSTORE['driver']  # 取出driver对象
        this_Weak_Text = None

        try:
            WeakElement = WebDriverWait(driver, 2, 1).until(
                EC.visibility_of_element_located((By.XPATH, self.__elementNode_Data['WeakHint']['Weak']))
            )
        except Exception as error:
            INFO('无弱提示！')
        else:
            if WeakElement.is_displayed():  # 提示框当前显示状态判断
                this_Weak_Text = "".join(re.findall(r'[0-9\u4e00-\u9fa5]', WeakElement.text))
        
        INFO(f'提示文本：{this_Weak_Text}')
        return this_Weak_Text


    '''# 人员选择逻辑封装'''
    def personnelChoice(self, type, dataList='', name='', department=''):
        '''
         参数：
            @param type : 以何种方式添加【'0'部门、'1'角色、'2'分组、'3'在线、'4'检索、'5'已选】
            @param dataList : 在使用【'0'部门、'1'角色、'2'分组】方式进行“人员选择”操作时传入
             按照部门选择输入参数为：dataList=[部门名称，人员姓名]
             按照角色选择输入参数为： dataList=[人员角色名称，人员姓名]
             按照分组选择输入参数为：dataList=[分组名称，人员姓名]
            @param name : 选填 | 在使用【'3'在线、'4'检索、'5'已选】方式进行“人员选择”操作时传入
             类型为字符串，用来存放目标人员的姓名，如果有两个同名人员默认取第一个
            @param department : 选填 | 类型为字符串，代表部门名称；当需要将整个部门的人员全部添加时给其传参即可

        注意：
            1、type参数不可省略，方法会以你传递的type参数为依据来处理其它的参数值
            2、在使用【'0'部门、'1'角色、'2'分组】方式进行[单级目录]“人员选择”操作时，dataList书写为： [目录名称，人员姓名] 
             例如: dataList=['市场营销部', '刘明才']
            3、在使用【'0'部门、'1'角色、'2'分组】方式进行[多级目录]“人员选择”操作时，dataList书写为： [[父级目录名称，子级目录名称n...]，人员姓名] 
             例如: dataList=[['市场营销部', '销售部', '北京销售部', '销售三组'],'温炳康']
            4、department使用时需要将type的值填充为'0'【部门方式添加】，才可以使用
        '''
        KEYWORD = GSTORE['keyWord']; driver = GSTORE['driver']  # 取出关键字对象

        KEYWORD.click_btn(*self.__elementNode_Data['personnel']['NAV_ITEM'][type])  # 导航按钮点击
        '''人员列表操作'''
        if type in ['3','4','5']:
            '''在线、检索方式添加'''
            if type == '4': KEYWORD.input_text(*self.__elementNode_Data['personnel']['search'], content=name)
            elementInformation = self.__elementNode_Data['personnel']['online' if type == '3' else 'resultOld' if type == '4' else 'selected']
            KEYWORD.click_btn(elementInformation[0], elementInformation[1].replace('INSERT', name))  # 点击目标人员
        else:
            TARGETING = self.__elementNode_Data['personnel']['TARGETING']
            if not department:
                DEPT_MENU = self.__elementNode_Data['personnel']['DEPT_MENU'][type]
                DEPT_ITEM = self.__elementNode_Data['personnel']['DEPT_ITEM'][type]
                if isinstance(dataList[0], list):
                    '''多级部门'''
                    for i in range(0, len(dataList[0])): KEYWORD.click_btn(TARGETING, DEPT_MENU.replace('INSERT', dataList[0][i]))
                else:
                    '''一级部门，角色，分组'''
                    KEYWORD.click_btn(TARGETING, DEPT_MENU.replace('INSERT', dataList[0]))
                KEYWORD.click_btn(TARGETING, DEPT_ITEM.replace('INSERT', dataList[-1]))  # 点击目标人员

            else:
                '''部门全部人员'''
                KEYWORD.click_btn(TARGETING, self.__elementNode_Data['personnel']['CHECKBOX'].replace('INSERT', department))  # 部门复选框点击
                KEYWORD.locator(TARGETING, self.__elementNode_Data['personnel']['MASK'].replace('INSERT', department))  # 加载遮罩层关闭判断
            
        '''组件关闭处理'''
        try:
            confirmBtn = WebDriverWait(driver, 1, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.__elementNode_Data['personnel']['confirm'])))
            confirmBtn.click()
        except Exception as error:
            pass
    

    '''# 人员选择逻辑封装 - 迭代后'''
    def personnelChoiceIteration(self, type, dataList='', name='', multiSelect='', globalSelect=''):
        '''兼容personnelChoice()方法，且支持“人员多选”和“人员全选全删”操作'''
        '''
        参数：
            @param type : 必填 | 以何种方式添加【'0'部门、'1'角色、'2'分组、'3'在线、'4'检索、'5'已选】

            @param dataList : 选填 | 在使用【'0'部门、'1'角色、'2'分组】方式进行“人员单选”操作时传入
             按照部门选择输入参数为：dataList=[部门名称，人员姓名]
             按照角色选择输入参数为： dataList=[人员角色名称，人员姓名]
             按照分组选择输入参数为：dataList=[分组名称，人员姓名]

            @param name : 选填 | 在使用【'3'在线、'4'检索、'5'已选】方式进行“人员单选”操作时传入
             类型为字符串，用来存放目标人员的姓名，如果有两个同名人员默认取第一个
             
            @param multiSelect : 选填 | 在进行 “人员多选” 操作时传入，支持全部的添加方式
             部门: [['部门名称', '值'], ...]  /   [[[路径], '值'], ...]
             角色: [['角色名称', '值'], ...]  /   [[[路径], '值'], ...]
             分组: [['分组名称', '值'], ...]  /   [[[路径], '值'], ...]
             检索: ['姓名','姓名'...]
             已选: ['姓名','姓名'...]
             在线: ['姓名','姓名'...]

            @param globalSelect : 选填 | 在进行 “人员全选、全删” 操作时传入，支持全部的添加方式；`all_add`全部添加、`all_remove`全部删除
             部门: ['部门名称', 'all_add / all_remove']  /  [['一级部门','二级部门',...], 'all_add / all_remove']
             角色: ['角色名称', 'all_add / all_remove']
             分组: ['分组名称', 'all_add / all_remove']
             检索: ['姓名','all_add / all_remove']
             已选: 'all_add / all_remove'
             在线: 'all_add / all_remove'

        注意：
            1、方法数据处理权重： 全局操作 > 多选操作 > 单选操作

            2、type参数不可省略，方法会以你传递的type参数为依据来处理其它的参数值
            
            3、在使用【'0'部门、'1'角色、'2'分组】方式进行[单级目录]“人员单选”操作时，dataList书写为： [目录名称，人员姓名] 
             例如: dataList=['市场营销部', '刘明才']

            4、在使用【'0'部门、'1'角色、'2'分组】方式进行[多级目录]“人员单选”操作时，dataList书写为： [[父级目录名称，子级目录名称n...]，人员姓名] 
             例如: dataList=[['市场营销部', '销售部', '北京销售部', '销售三组'],'温炳康']
            
            5、人员多选 multiSelect参数，在处理【'0'部门、'1'角色、'2'分组】方式时，参数需要区分“单级目录”和“多级目录”
             单级目录例如：multiSelect=[['综合管理部','王云'],['市场营销部','刘明才']]
             多级目录例如：multiSelect=[[['综合管理部','财务部'],'常白'],[['市场营销部','市场部','网络营销中心'],'刘永康']]
            
            6、人员多选 multiSelect参数，在处理【'0'部门、'1'角色、'2'分组】方式时，若要选择人员的所属目录一致，仍需要全部书写清楚
             单级目录例如：multiSelect=[['综合管理部','王云'],['综合管理部','系统管理员']]
             多级目录例如：multiSelect=[[['市场营销部','市场部','网络营销中心'],'刘为'],[['市场营销部','市场部','网络营销中心'],'刘永康']]
            
            7、人员多选 multiSelect参数，在处理【'3'在线、'4'检索、'5'已选】方式时，只需要传入人员的姓名即可
             例如：['王云','系统管理员']
            
            8、人员全选、全删 globalSelect参数，`all_add`代表全部添加、`all_remove`代表全部删除
            
            9、人员全选、全删 globalSelect参数，在处理【'0'部门、'1'角色、'2'分组】方式时，参数需要区分“单级目录”和“多级目录”
             单级目录例如：globalSelect=['综合管理部', 'all_add']
             多级目录例如：globalSelect=[['综合管理部','财务部'], 'all_remove']
            
            10、不论使用何种参数【'0'部门、'1'角色、'2'分组】方式在同一个参数中的所有涉及的“单级目录”和“多级目录”的书写格式均一致
        '''
        KEYWORD = GSTORE['keyWord']; driver = GSTORE['driver']  # 取出关键字对象

        KEYWORD.click_btn(*self.__elementNode_Data['personnel']['NAV_ITEM'][type])  # 导航按钮点击
        '''自由操作'''
        step = [globalSelect[:-1]] if isinstance(globalSelect, list) else [globalSelect] if globalSelect else multiSelect if multiSelect else [name] if type in ['3', '4', '5'] else [dataList]
        operIden = re.findall(r"all_add|all_remove", f"{globalSelect}")
        for item in step:
            if type in ['3','4','5']:
                '''在线、检索方式添加'''
                if type == '4': KEYWORD.input_text(*self.__elementNode_Data['personnel']['search'], content=f"['{''.join(item)}']")
                '''全局？自由？'''
                if globalSelect:
                    typeIden = self.__elementNode_Data['personnel']['TYPEIDEN_ITEM'][type]['title']
                    KEYWORD.click_btn(*eval(f"{self.__elementNode_Data['personnel'][operIden[0].upper()]}".replace('INSERT', typeIden)))
                else:
                    KEYWORD.click_btn(*eval(f"{self.__elementNode_Data['personnel']['TYPEIDEN_ITEM'][type]['location']}".replace('INSERT', item)))  # 点击目标人员
            else:
                contnetIden = item[0]
                TARGETING = self.__elementNode_Data['personnel']['TARGETING']
                DEPT_MENU = self.__elementNode_Data['personnel']['DEPT_MENU'][type]
                DEPT_ITEM = self.__elementNode_Data['personnel']['DEPT_ITEM'][type]
                if isinstance(item[0], list):
                    '''多级部门'''
                    for i in range(0, len(item[0])): KEYWORD.click_btn(TARGETING, DEPT_MENU.replace('INSERT', item[0][i]))
                    contnetIden = item[0][i]
                else:
                    '''一级部门，角色，分组'''
                    KEYWORD.click_btn(TARGETING, DEPT_MENU.replace('INSERT', item[0]))
                '''全局？自由？'''
                if globalSelect:
                    KEYWORD.click_btn(*eval(f"{self.__elementNode_Data['personnel'][operIden[0].upper()]}".replace('INSERT', contnetIden)))
                else:
                    KEYWORD.click_btn(TARGETING, DEPT_ITEM.replace('INSERT', item[-1]))  # 点击目标人员

        '''组件关闭处理'''
        try:
            confirmBtn = WebDriverWait(driver, 1, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.__elementNode_Data['personnel']['confirm'])))
            confirmBtn.click()
        except Exception as error:
            pass


    '''# 日期选择'''
    def setDate(self, expectDate):
        '''根据传入的日期形参，进行日期选择'''
        ''' 
         参数：
            @param expectDate: 要进行选择的日期；注意这里日期格式应为YYYY-MM-DD；如： 2021-09-24  ||  2021-9-24
        ''' 
        KEYWORD = GSTORE['keyWord']; driver = GSTORE['driver']  # 取出公共暂存对象
        self.jumpFrame([1,[self.__elementNode_Data['setDate']['frameSrc']]])  # 根据src属性，将焦点跳入日期选择对话框

        '''预期日期、实际日期 ‘数值列表化’处理'''
        currentData = KEYWORD.locator(*self.__elementNode_Data['setDate']['action_Day']).get_attribute("onclick")
        actualValue = list(map(int, re.compile(r'(\d+\.?\d*)').findall(currentData)))
        expectValue = list(map(int,expectDate.split('-')))

        INFO(f"操作选择日期：{expectDate}, 对话框当前日期：{actualValue[0]}-{actualValue[1]}-{actualValue[2]}")

        if expectValue == actualValue:
            '''日期相等'''
            KEYWORD.click_btn(*self.__elementNode_Data['setDate']['today'])
        else:
            '''目标年、月选择'''
            for i in range(0, len(actualValue[:-1])):
                arrow_Type = {'Left': self.__elementNode_Data['setDate']['YLeft'], 'Right': self.__elementNode_Data['setDate']['YRight']}\
                    if len(str(actualValue[i])) == 4 else {'Left': self.__elementNode_Data['setDate']['MLeft'], 'Right': self.__elementNode_Data['setDate']['MRight']}  # 年份，月份操作按钮处理 (单、双箭头)

                if not(actualValue[i] == expectValue[i]):
                    '''循环遍历点击'''
                    arrow_Button = arrow_Type['Left'] if actualValue[i] > expectValue[i] else arrow_Type['Right']  # 左、右箭头按钮处理
                            
                    for j in range(0, abs(expectValue[i] - actualValue[i])):
                        '''左、右侧方向箭头年份、月份'''
                        KEYWORD.click_btn(*arrow_Button)
                        '''处理年份多次点击，会激活年份选择下拉列表框的问题'''
                        if KEYWORD.locator(*self.__elementNode_Data['setDate']['Y_Select_Box']).is_displayed(): KEYWORD.click_btn(*arrow_Button)  # 重复二次点击
                else:
                    pass  # 值相等不做操作
        
            KEYWORD.click_btn('css_selector',f'[onclick="day_Click({expectValue[0]},{expectValue[1]},{expectValue[2]});"]')  # 目标日期选择
        
        '''组件关闭处理'''
        try:
            confirmBtn = WebDriverWait(driver, 1, 0.5).until(EC.presence_of_element_located((By.ID, self.__elementNode_Data['setDate']['confirm_Btn'])))
            confirmBtn.click()
        except Exception as error:
            pass


    '''# 系统左上角提示信息弹框处理'''
    def TipsSpringFrame(self, type):
        '''
         参数：
            @param type  必填项 ：代表要进行的操作 exit关闭对话框、 readAll已阅全部
        '''
        KEYWORD = GSTORE['keyWord']  # 取出关键字对象
        driver = GSTORE['driver']

        try:
            tipsBoxElements = WebDriverWait(driver, 1, 0.5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.__elementNode_Data['TSFrame']['tispElements']))
            )
        except Exception as error:
            INFO('界面无消息提示框，不做操作')
            return 0
        else:
            '''处理弹框'''
            for tipsBox_Item in tipsBoxElements:
                KEYWORD.actionBuilder_Move(*self.__elementNode_Data['TSFrame']['tispItem'], ParentObject=tipsBox_Item)  # 鼠标悬浮，调出操作按钮组
                if type == 'exit':
                    KEYWORD.click_btn(*self.__elementNode_Data['TSFrame']['exitButton'])  # 关闭
                else:
                    try:
                        KEYWORD.click_btn(*self.__elementNode_Data['TSFrame']['markAll'], ParentObject=tipsBox_Item)  # 已阅全部
                    except Exception as error:
                        KEYWORD.click_btn(*self.__elementNode_Data['TSFrame']['ignoreAll'], ParentObject=tipsBox_Item)  # 忽略全部
                    break
            return 1


    '''# 表单信息输入逻辑操作封装'''
    def FormInput(self, Parent, operationStep):
        '''
         参数:
            @param Parent: 父级表单的节点，css定位方式-元素表达式
            @param operationStep: dict类型，要操作的整体流程

         operationStep 传值格式：
         {
            'input': [xx, xx, xx, xx ..]   ||  [[Name, xx], [Name, xx], [] ..]    # 普通文本输入框，为 None则表示不输入

            'pass': [xx, xx, xx, xx ..]   ||  [[Name, xx], [Name, xx], [] ..]    # 密码文本输入框  为 None则表示不输入

            'textarea': [xx, xx, xx, xx ..]   ||  [[Name, xx], [Name, xx], [] ..]    # 多行文本输入框 如果为None则表示不输入
            
            'checkbox': [xx, xx, xx, xx ..]   ||  [[Name, xx], [Name, xx], [] ..]    # 复选框选择  

            'radio': [xx, xx, xx, xx ..]   ||  [[Name, xx], [Name, xx], [] ..]    # 单选框选择

            'select': [[Name, xx], [Name, xx], [] ..]    # 下拉列表框
         }

        operationStep传值格式说明：
         1、xx 为实际的操作值 (目前方法支持操作的表单组件)：
          在 [input输入框、pass密码输入框、textarea多行文本输入框]中该值应为文本类型；
          在 [checkbox复选按钮、radio单选按钮]中该值为布尔类型 (True代表选中该按钮，false代表不选中)；
          在 [select下拉列表框]中该值可以是其列表子项的 “index索引值”、“value属性值” 和 “text文本值” (方法自动识别传入的值类型，不需要特殊标明)；

         2、在 [input输入框、pass密码输入框、textarea多行文本输入框]中若传入'clear'则代表只对输入框做清空操作，不输入任何值。

         3、传值方法分为两种一种为 “[xx, xx, xx, xx ..] 按照组件先后顺序操作”，另一种为 “ [[Name, xx], [Name, xx], [] ..] 指定组件操作”。  
          “按照组件先后顺序操作”：是按照对应表单组件在界面中的先后顺序进行操作，在使用时需要注意值输入顺序；
          “指定组件操作”：是按照传入的组件Name属性值对指定组件进行定位并操作，该方法不需要考虑顺序问题；
         
         4、“组件先后顺序操作”方式，若传入的操作值个数大于实际的元素个数，则超出的操作值将被方法视为无效并其不对其进行操作。

         5、“指定组件操作”方式只支持对存在“Name属性”的表单组件进行操作，若表单组件不存在Name属性则此种方式将无法对其进行操作。

         6、“组件先后顺序操作方式”和“指定组件操作方式” 在不同表单组件元素之间可以混合使用，同种表单组件元素只可以二选一。
          例如：你可以在一次调用中使用“组件先后顺序操作方式”操作input输入框，同时使用“指定组件操作方式”操作radio单选按钮；

         7、select下拉列表框只支持通过“指定组件操作方式”进行操作，且“操作值个数大于实际的元素个数，超出的操作值将视为无效”特性不受用。

         8、除select下拉列表框外其它表单组件不论使用“组件先后顺序操作方式”还是“指定组件操作方式”，“操作值个数大于实际的元素个数，超出的操作值将视为无效”这个特性均受用。
        '''
        KEYWORD = GSTORE['keyWord']; driver = GSTORE['driver']  # 对象取出
        for StepKey in operationStep:
            parentNode = KEYWORD.locator('css_selector', Parent)  # 父级表单元素
            '''流程判断'''     
            if StepKey == 'select':  # 下拉列表框
                for index in range(0, len(operationStep[StepKey])):
                    selectObject = Select(KEYWORD.locator('name', operationStep[StepKey][index][0])); operattion = operationStep[StepKey][index][1]
                    if isinstance(operattion, int): 
                        selectObject.select_by_index(operattion)  # index
                    else:
                        if operattion in [item.text for item in selectObject.options]:
                            selectObject.select_by_visible_text(operattion)  # text
                        else:
                            selectObject.select_by_value(operattion)  # value
        
            else:  # input输入框，textarea多行文本输入框、checkbox复选按钮、radio单选按钮
                ''' StepKey == 'checkbox' or StepKey == 'radio' or StepKey == 'input' or StepKey == 'textarea' or StepKey == 'pass' '''
                operLength = len(operationStep[StepKey])  # 操作流程形参长度
                moduleAssemblys = KEYWORD.offLocator(parentNode, *self.__elementNode_Data['FormInput'][StepKey])  # 表单可操作组件元素获取

                for index in range(0, operLength if operLength <= len(moduleAssemblys) else len(moduleAssemblys)):
                    if operationStep[StepKey][index] != None:
                        type_boolean = isinstance(operationStep[StepKey][index], list)
                        operationElement = KEYWORD.offLocator(parentNode, 'name', operationStep[StepKey][index][0]) if type_boolean else moduleAssemblys[index]
                        operationContent = operationStep[StepKey][index][-1] if type_boolean else operationStep[StepKey][index]
                        
                        if StepKey == 'input' or StepKey == 'textarea' or StepKey == 'pass':  # 输入框操作
                            operationElement.clear()
                            if operationContent != 'clear': operationElement.send_keys(operationContent) # 输入/清除内容
                        else:  # 单、复选按钮选择操作
                            if operationElement.is_selected() != operationContent: driver.execute_script("arguments[0].click();", operationElement) # 选择操作
                    else:
                        pass  # 为None不做操作


    '''# 全局系统模块菜单跳转操作封装'''
    @reset_implicitlyWait(2)
    def goto_Modular(self, firstIden=None, secondIden=None, thirdIden=None, tagIden=None, localSwitch=False):
        '''
         参数：
            @param firstIden: OA系统一级模块标识【特殊字符标识】
            @param secondIden: OA系统二级模块标识【特殊字符标识】
            @param thirdIden: OA系统三级模块标识【特殊字符标识】
            @param tagIden: 对应模块tag标签标识【阿拉伯数字】
            @param localSwitch: 局部操作开关【布尔值】

         格式：(可以按照dict和list两种格式为函数传递形参值)
            dict(传入形参顺序与函数定义的形参位置不对应)/list(传入形参顺序与函数定义的形参位置对应)

            1、全局操作；目标模块不存在子模块和tag标签页(例如：个人事务-电子邮件)：
                {'firstIden':'personalAffairs','secondIden':'E_Mail'} || ['personalAffairs','E_Mail']

            2、全局操作；目标模块不存在子模块但存在tag标签页(例如：个人事务-消息管理-微讯)：
                {'firstIden':'personalAffairs','secondIden':'Message','tagIden':0} || 不支持list格式调用

            3、全局操作；目标模块存在子模块但不存在tag标签页(例如：行政办公-工作计划-工作计划类型设置)：
                {'firstIden':'administrativeOffice','secondIden':'Work_Plan','thirdIden':'Work_Plan_Type'} || ['administrativeOffice','Work_Plan','Work_Plan_Type']
            
            4、全局操作：目标模块存在子模块同时也存在tag标签页(例如：行政办公-工作计划-工作计划管理-新建工作计划)：
                {'firstIden':'administrativeOffice','secondIden':'Work_Plan','thirdIden':'Work_Plan_Query', 'tagIden':1} || ['administrativeOffice','Work_Plan','Work_Plan_Query',1]

            5、局部操作：目标模块不存在tag标签页(例如：个人事务-电子邮件、行政办公-工作计划-工作计划类型设置)：
                · 进行一次全局操作(全局路由跳转),将模块跳转至“个人事务-电子邮件”模块 → 用例步骤 → 用例步骤 →... → {'localSwitch':True} || 不支持list格式调用
                · 进行一次全局操作(全局路由跳转),将模块跳转至“行政办公-工作计划-工作计划类型设置”模块 → 用例步骤 → 用例步骤 →... → {'localSwitch':True} || 不支持list格式调用
            
            6、局部操作：目标模块存在tag标签页(例如：个人事务-消息管理-微讯 、行政办公-工作计划-工作计划管理-新建工作计划)：
                · 进行一次全局操作(全局路由跳转),将模块跳转至“个人事务-消息管理-微讯”模块 → 用例步骤 → 用例步骤 →... → {'tagIden':0,'localSwitch':True} || 不支持list格式调用
                · 进行一次全局操作(全局路由跳转),将模块跳转至“行政办公-工作计划-工作计划管理-新建工作计划”模块 → 用例步骤 → 用例步骤 →... → {'tagIden':1, 'localSwitch':True} || 不支持list格式调用

        注：
            1、方法适用于OA系统中的所有模块，包含所有“一级模块、二级模块、三级模块、tag页模块”；主要目的是为了简化“用例步骤文件”中的模块跳转步骤； 
            2、方法不会校验“各模块标识之间的层级关系是否有效以及其标识是否合法(是否存在)”，所以在使用时要注意检查你要操作的“模块标识”和“多级模块层级”是否正确；
            3、“全局操作”：不考虑当前正在处于活动状态的“模块”，直接将整个OA系统还原成初始状态(无任何菜单展开，无任何模块打开)，并根据传入的各级标识打开指定的目标模块；
            4、“局部操作”：不会对系统“展开菜单项”和“定位任务标签”进行清空操作，而是直接跳过一、二级模块直接以三级模块或者tag标签模块为起点进行操作； 
            5、“局部操作”不需要指定“各级模块标识”，但需要在调用方法进行“目标模块的局部操作”之前先调用方法完成一次“目标模块的全局操作”，目的则是为了获取“全局操作”所指定的各级模块标识信息；
            6、“局部操作”不支持用于模块之间的跳转，其本身目的只是为了用来刷新目标模块；
            7、在使用“局部操作”刷新目标模块时，不传入“tagIden对应模块tag标签标识(不论目标模块有无tag标签页)”则代表将该模块关闭(顶部选项卡)，并重新点击打开。
        '''
        KEYWORD = GSTORE['keyWord']  # 取出关键字对象
        targetTag = None  # 目标tag标签节点
        targetIframe = None  # 目标iframe标识
        modularIframeDict = eval(self.__ModularNode_Information.replace('null', 'None'))  # 系统各级模块节点信息
        if firstIden and (not localSwitch): self.__CDCG['firstIden'] = firstIden
        if secondIden and (not localSwitch): self.__CDCG['secondIden'] = secondIden
        if thirdIden and (not localSwitch): self.__CDCG['thirdIden'] = thirdIden
        try:
            '''//初始化重置刷新//'''
            KEYWORD.frame_default()
            if not localSwitch:
                KEYWORD.driver_refresh()
            else:
                try:
                    firstIden = self.__CDCG['firstIden']; secondIden = self.__CDCG['secondIden']; thirdIden = self.__CDCG['thirdIden']
                except Exception as error:
                    pass
                if not tagIden:  # 判断有无传入“tag标签标识”
                    KEYWORD.click_btn(*self.__elementNode_Data['gotoModular']['taskbar'])
        except Exception as error:
            raise Exception
        finally:
            if not localSwitch:
                '''//一级菜单展开//'''
                KEYWORD.click_btn(*modularIframeDict[firstIden]['selfLocatin'])
                '''//二级菜单点击//'''
                KEYWORD.click_btn(*modularIframeDict[firstIden]['subordinate'][secondIden]['locatingNodes'])
            try:
                if not modularIframeDict[firstIden]['subordinate'][secondIden]['submodule']:
                    '''//无子模块//'''
                    if localSwitch:
                        KEYWORD.click_btn(*modularIframeDict[firstIden]['subordinate'][secondIden]['locatingNodes'])
                    targetTag = modularIframeDict[firstIden]['subordinate'][secondIden]['tagPage']
                    targetIframe = modularIframeDict[firstIden]['subordinate'][secondIden]['iframe']
                else:
                    '''//存在子模块//'''
                    KEYWORD.click_btn(*modularIframeDict[firstIden]['subordinate'][secondIden]['submodule'][thirdIden]['locatinExpression'])
                    targetTag = modularIframeDict[firstIden]['subordinate'][secondIden]['submodule'][thirdIden]['thisTag']
                    targetIframe = modularIframeDict[firstIden]['subordinate'][secondIden]['submodule'][thirdIden]['thisIframe']
            except Exception as error:
                raise Exception
            finally:
                '''//判断有无tag标签页//'''
                if targetTag and tagIden:
                    KEYWORD.click_btn(*targetTag[int(tagIden)])
                '''//iframe焦点切入//'''
                KEYWORD.switch_frame(targetIframe)

        
    '''OA数据库操作'''
    def intervention_Mysql(self, information):
        '''
         参数：
            @param information: dist类型 存放数据库操作信息

            information = {localhost, port, user, password, charset, database, table, operation[, where, instructString]}
        '''

        '''
         {
            localhost  # mysql数据库地址
            port  # 端口号
            user  # 用户名
            password  # 密码
            charset  # 字符编码
            database  # 待操作数据库名称
            table  # 待操作数据表名称 
            operation  # 操作标识，可输入值：delete删除、update修改更新、insert插入
            where  # sql条件命令表达式，格式限定：字段名=字段值 AND ...
            instructString  # 字段名、字段值关系表达式，dist类型 {'字段名':'值', '字段名': '值'...}
         }

         实例一 
            删除 student表中所有的记录：information = {'table': 'studnet', 'operation': 'delete'}
            删除 student表中 name字段值为“王小明”的记录：information = {'table': 'studnet', 'operation': 'delete', 'where': "name='王小明'"}

         实例二
            将 student表中所有记录的 name字段值全部修改为 “王小明”：information = {'table': 'studnet', 'operation': 'update', 'instructString': {'name': '王小明'}}
            将 student表中 age字段值为0的记录的 name字段值修改为 “王小明”：information = {'table': 'studnet', 'operation': 'update', 'instructString': {'name': '王小明'}, 'where': "age='0'"}
        
         实例三
            向 student表中插入一条记录，其 name字段值为“王小明”、age字段值为12、class字段值为“六年级”、sex字段值为“男”：
            information = {'table': 'studnet', 'operation': 'insert', 'instructString': {'name':'王小明', 'age': '12', 'class':'六年级', 'xb':'男'}}
        
        注意：
            1、为了方便阅读和理解，在上文的实例中并没有书写 “localhost、 port” 等信息，但是在实际使用时除了 “where” 和 “instructString”两项外其它均是必填项。
            2、参数中 “operation” 代表操作动词，可选值有 ['delete 删除' / 'update 更新' / 'insert 插入']
            3、参数中 “where” 代表sql条件表达式语法和sql一致，“ 字段名=字段值 AND ... ”；需要注意其中的 “字段值” 若为中文或字符串在书写时需要用 ''、""引号包裹。
            4、参数中 “instructString” 代表字段名、字段值关系表达式，dist类型 {'字段名':'值', '字段名': '值'...}；需要注意其中的 “字段名” 和 “字段值” 在书写时不需要用 `` 符号包裹。
            5、 “where” 和 “instructString” 可选项说明：
                当“operation操作动词”为 delete删除时：
                    where可选填；有值且合法：则删除数据表中符合条件的记录，值为空或者无该项：则删除数据表中全部记录
                    instructString不参与处理，有无均可。
                
                当“operation操作动词”为 update更新时：
                    where可选填；有值且合法：则修改数据表中符合条件的记录，值为空或者无该项：则修改数据表中全部记录
                    instructString必填项；代表要修改的字段名和其对应的字段值(保证书写的字段名和值类型与表中实际对应)，{'name'='王小明', 'age': '12'}
                
                当“operation操作动词”为 insert插入时：
                    where不参与处理，有无均可。
                    instructString必填项；代表要插入记录的所有非空字段的字段名和其对应的字段值(保证书写的字段名和值类型与表中实际对应)，{'name'='王小明', 'age': '12', 'class':'六年级', 'xb':'男'}
        '''
        tran_information = information
        try:
            information = {
                'localhost': GSTORE['START']['selfDefinedParameter']['sql_host'],
                'port': GSTORE['START']['selfDefinedParameter']['sql_port'],
                'user': GSTORE['START']['selfDefinedParameter']['sql_user'],
                'password': GSTORE['START']['selfDefinedParameter']['sql_password'],
                'charset': GSTORE['START']['selfDefinedParameter']['sql_charset'],
                'database': GSTORE['START']['selfDefinedParameter']['sql_db']
            }
        except Exception as error:
            pass
        finally:
            for key in tran_information.keys(): information[key] = tran_information[key]

        commandStatement = ''  # sql命令语句
        if information['operation'].strip() == 'delete':
            commandStatement = f"DELETE FROM `{information['table']}`;" if not('where' in information.keys() and information['where'].strip())\
                else f"DELETE FROM `{information['table']}` WHERE {information['where']};"

        elif information['operation'].strip() == 'update':
            try:
                expression = ",".join([f"`{key}`=`{information['instructString'][key]}`" for key in information['instructString'].keys()])

                commandStatement = f"UPDATE `{information['table']}` SET {expression};" if not('where' in information.keys() and information['where'].strip())\
                    else f"UPDATE `{information['table']}` SET {expression} WHERE {information['where']};"
            except Exception as error:
                pass
                
        elif information['operation'].strip() == 'insert':
            try:
                fieldName = ",".join([f"`{key}`" for key in information['instructString'].keys()])
                fieldValue = ",".join([f"`{value}`" for value in information['instructString'].values()])
                commandStatement = f"INSERT INTO `{information['table']}` ({fieldName}) VALUES ({fieldValue});"
            except Exception as error:
                pass
        
        import pymysql
        sql_object = pymysql.connect(host=information['localhost'],port=int(information['port']),user=information['user'],password=information['password'],charset=information['charset'],db=information['database'])
        cursor = sql_object.cursor()  # 数据库连接
        try:
            cursor.execute(commandStatement); sql_object.commit()  # sql语句执行
        except Exception as error:
            raise Exception
        finally:
            cursor.close(); sql_object.close()  # 对象注销
            INFO("sql对象已注销")


    '''三元判断操作(暂未开发)'''
    def ternary_Judgement(self, ):
        '''
        参数：
            @param 
        '''
        return True