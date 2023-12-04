'''# built_in'''
import re
'''# custom'''
from common import MODULEDATA


class SurveyKeyWord:

    '''构造函数'''
    def __init__(self) -> None:
        '''webUI --> 自定义插件'''
        return

    '''# ↓↓↓原Excel_Read.py模块检索逻辑↓↓↓'''
    def keyRetrieval(self, page_Object, tagging, keywordName, positionInformation=None, manipulatedValue=None):
        """
         参数：
            @param page_Object : page_Object关键字.py文件对象
            @param tagging : 步骤说明
            @param keywordName : 操作关键字
            @param positionInformation : 元素位置信息
            @param manipulatedValue : 操作值
        """
        self.acceptItch = None  # 存放断言结果

        if keywordName == 'time_sleep':  # 强制时间等待
            page_Object.time_sleep(manipulatedValue)

        elif keywordName == 'implicitly_time':  # 隐式时间等待
            page_Object.implicitly_time(manipulatedValue)
            
        elif keywordName == 'explain':  # 标注说明
            page_Object.explain(manipulatedValue)

        elif keywordName == 'driver_back':  # 浏览器窗口返回
            page_Object.driver_back()

        elif keywordName == 'driver_refresh':  # 浏览器窗口刷新
            page_Object.driver_refresh()

        elif keywordName == 'driver_close':  # 浏览器窗口关闭
            page_Object.driver_close()

        elif keywordName == 'frame_default':  # frame焦点初始化
            page_Object.frame_default()
        
        elif keywordName == 'parent_frame':  # frame焦点后退
            page_Object.parent_frame()
        
        elif keywordName == 'refresh_frame':  # frame页面刷新
            page_Object.refresh_frame()
            
        elif keywordName == 'switch_frame':  # iframe跳转
            page_Object.switch_frame(manipulatedValue)

        elif keywordName == 'Interface_Invoke':  # 公共接口类调用
            self.acceptItch = page_Object.Interface_Invoke(manipulatedValue)
        
        elif keywordName == 'ternary_Judgement':  # 三元判断
            self.acceptItch = page_Object.ternary_Judgement(*positionInformation, content = manipulatedValue)

        elif keywordName == 'input_text':  # 输入
            page_Object.input_text(*positionInformation, content = manipulatedValue)

        elif keywordName == 'click_btn':  # 点击
            page_Object.click_btn(*positionInformation)
        
        elif keywordName == 'js_control':  # js操作
            page_Object.js_control(*positionInformation, content = manipulatedValue)
        
        elif keywordName == 'alert_operation': # alert弹框操作
            page_Object.alert_operation(content = manipulatedValue)
        
        elif keywordName == 'selector_operation':  # <select>下拉列表框操作
            page_Object.selector_operation(*positionInformation, content = manipulatedValue)

        elif keywordName == 'radioCheck_operation':  # 单/复选按钮操作
            page_Object.radioCheck_operation(*positionInformation, content = manipulatedValue)
        
        elif keywordName == 'drag_scrollBar':  # 窗口滚动条拖动
            page_Object.drag_scrollBar(*positionInformation, content = manipulatedValue)

        elif keywordName == 'title_assert':  # 窗口title标签值断言
            self.acceptItch = page_Object.title_assert(manipulatedValue)
        
        elif keywordName == 'alert_assert':  # alert弹框文本断言
            self.acceptItch = page_Object.alert_assert(manipulatedValue)
        
        elif keywordName == 'selector_assert':  #  <select>标签子项存在与否断言
            self.acceptItch = page_Object.selector_assert(*positionInformation, content = manipulatedValue)

        elif keywordName == 'elementNumber_assert':  # 界面指定元素数量比较断言
            self.acceptItch = page_Object.elementNumber_assert(*positionInformation, content = manipulatedValue)

        elif keywordName == 'elementErgodic_assert':  # 元素值遍历比较断言 - 预期值存在
            self.acceptItch = page_Object.elementErgodic_assert(*positionInformation, content = manipulatedValue)
        
        elif keywordName == 'elementErgodicNot_assert':  # 元素值遍历比较断言 - 预期值不存在
            self.acceptItch = page_Object.elementErgodicNot_assert(*positionInformation, content = manipulatedValue)
        
        elif keywordName == 'elementExistence_assert':  # 指定元素存在与否断言
            self.acceptItch = page_Object.elementExistence_assert(*positionInformation, content = manipulatedValue)
        
        elif keywordName == 'elementComparison_assert':  # 元素大小值比较断言
            self.acceptItch = page_Object.elementComparison_assert(*positionInformation, content = manipulatedValue)
        
        elif keywordName == 'selfText_assert':  # 元素text文本值断言
            self.acceptItch = page_Object.selfText_assert(*positionInformation, content = manipulatedValue)

        elif keywordName == 'selfAttribute_assert':  # 元素属性值断言
            self.acceptItch = page_Object.selfAttribute_assert(*positionInformation, content = manipulatedValue)
        
        elif keywordName == 'functionReturn_assert':  # 插件方法返回值断言
            self.acceptItch = page_Object.functionReturn_assert(content = manipulatedValue)

        elif keywordName == 'downloadExport_assert':  # 下载导出检查断言
            self.acceptItch = page_Object.downloadExport_assert(content = manipulatedValue)

        elif keywordName == 'winUpload':  # 多文件批量上传
            page_Object.winUpload(content = manipulatedValue)

        elif keywordName == 'actionBuilder_Move':  # 鼠标悬停
            page_Object.actionBuilder_Move(*positionInformation)

        elif keywordName == 'actionBuilder_RightClick':  # 鼠标右键点击
            page_Object.actionBuilder_RightClick(*positionInformation)

        elif keywordName == 'actionBuilder_DoubleClick':  # 鼠标双击
            page_Object.actionBuilder_DoubleClick(*positionInformation)
        
        elif keywordName == 'actionBuilder_HoldClick':  # 鼠标按下
            page_Object.actionBuilder_HoldClick(*positionInformation)
        
        elif keywordName == 'actionBuilder_MoveTo':  # 鼠标拖动至元素
            page_Object.actionBuilder_MoveTo(*positionInformation)
        
        elif keywordName == 'actionBuilder_MoveOffset':  # 目标元素拖动至指定坐标位
            page_Object.actionBuilder_MoveOffset(*positionInformation, content = manipulatedValue)
    
        elif keywordName == 'keyBoard_Events':  # 键盘事件
            page_Object.keyBoard_Events(*positionInformation, content = manipulatedValue)
        
        elif keywordName == 'getElementText':  # 获取元素未知值
            page_Object.getElementText(*positionInformation, content = manipulatedValue)
            
        elif keywordName == 'takeElementText':  # 元素未知值遍历比较断言
            self.acceptItch = page_Object.takeElementText(*positionInformation, content = manipulatedValue)

        elif keywordName == 'gethandle':  # 获取当前窗口句柄
            page_Object.gethandle()

        elif keywordName == 'enterWindow':  # 窗口句柄跳入
            page_Object.enterWindow(content = manipulatedValue)

        elif keywordName == 'outWindow':  # 窗口句柄跳出
            page_Object.outWindow()
            
        else:
            '''# 未在关键字列表中查找到, 视为封装的插件操作逻辑'''
            '''[pluginName]functionName'''
            pluginName = "".join(re.findall(r'[[](.*?)[]]', keywordName)); functionName = keywordName[keywordName.find(']') + 1:]
            fun_Object = getattr(MODULEDATA[pluginName]['object'], functionName)  # 导入插件方法
            if manipulatedValue != None:  # 需要传值调用
                if isinstance(eval(manipulatedValue), dict):
                    self.acceptItch = fun_Object(**eval(manipulatedValue))  # 判断为指定形参传值操作
                else:
                    self.acceptItch = fun_Object(*eval(manipulatedValue))  # 判断为不指定形参值 
            else:
                self.acceptItch = fun_Object()  # 判断为不指定形参值
        
        if self.acceptItch != None: return self.acceptItch  # 函数返还值