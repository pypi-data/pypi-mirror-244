'''# built_in'''
import re
import time
import datetime
from datetime import timedelta
'''# custom'''
from common import PRIVATEDATA


'''@tool class'''
class Tool:

    def __init__(self) -> None:
        return
    
    def get_dateTimeFormat(self, date):
        '''
         // ***Format string acquisition of date and time*** //

         特殊数据使用说明：[除一下三种情况外，其它情况你可以任意书写在数据中出现的分隔符号]
            1、如果你想要对最大单位为天(%d %H:%M:%S)的数据做操作则“日期数据和时间数据”之间的分隔符必须为[' '空格]，其它分隔符号任意;例如：02 15:14_05, 处理为“02日 15时14分05秒 %d %H:%M_%S”
            2、如果你想要单独对时间数据(%H:%M:%S)做操作则“小时与分钟”之间的分隔符必须为[:冒号]，其它分隔符号任意;例如：15:14-05, 处理为“15时14分05秒 %H:%M-%S”
            3、函数不支持最大单位为“分钟”或者“秒”(%M:%S || %S)的数据操作
        '''
        dateSte = re.findall(r'\d+|\s+', date)
        '''0, 1, 2, 3, 4, 5'''
        contrast = ['%Y', '%m', '%d', '%H', '%M', '%S']; format_String = [item for item in re.findall(r'(\D)+', date)]

        start_Index = 0 if len(dateSte[0]) == 4 else 1 if (int(dateSte[0]) <= 12 and date[len(dateSte[0]):][0] != ' ') else 3 if (int(dateSte[0]) <= 23 and date[len(dateSte[0]):][0] == ':') else 2
        for num, index in enumerate(range(0, len(format_String)+len(re.findall(r'\d+', date)), 2)):
            format_String.insert(index, contrast[num + start_Index])
        
        return "".join(format_String)


'''@functionList Class'''
class Built_In_Function(Tool):

    def __init__(cls) -> None:
        return
    
    def System_date(self, tran, fun) -> None:
        '''
            // ***Get the current system date*** //
        '''
        try:
            date = time.strftime(tran[fun], time.localtime(time.time()))
            return date
        except Exception as error:
            return ""

    def Increasing_date(self, tran, fun) -> None:
        '''
            // ***Addition and subtraction of date and time data*** // Day/Hour/Min/Second
        '''
        try:
            par_date = tran[fun].split(','); date_Format = self.get_dateTimeFormat(par_date[0]); Pending_date = datetime.datetime.strptime(par_date[0], date_Format)
            try:
                Addend = int(par_date[1]); key = 'days'
            except:
                contrast_Dict = {'h':'hours', 'm':'minutes', 's':'seconds'}
                Addend = int(par_date[1][:-1]); key = contrast_Dict[par_date[1][-1:]]

            complete_date = (Pending_date if ('%H' in date_Format or '%M' in date_Format or '%S' in date_Format) else Pending_date.date()) +\
                datetime.timedelta(**{key:Addend})
            return str(complete_date)
        except Exception as error:
            return ""
    
    def Intercept_date(self, tran, fun) -> None:
        '''
            // *** Date data interception ***// Year/Month/Day/Hour/Min/Second
        '''
        try:
            parameter = tran[fun].split(',')
            I_format = '%Y' if 'Year' in parameter else '%m' if 'Month' in parameter else '%d' if 'Day' in parameter else '%H' if 'Hour' in parameter else '%M' if 'Min' in parameter else '%S'
            Time_Stamp = time.localtime(time.mktime(time.strptime(parameter[0], self.get_dateTimeFormat(parameter[0]))))  # mktime: 时间戳格式化 [字符串 → 日期对象 → 时间戳 → 结构体]
            return str(time.strftime(I_format, Time_Stamp))
        except Exception as error:
            return ""
    
    def Mktime_date(self, tran, fun) -> None:
        '''
            // *** Timestamp conversion ***//
        '''
        try:
            OPER_DATA = tran[fun]; HAND_DATA = time.mktime(time.strptime(OPER_DATA, self.get_dateTimeFormat(OPER_DATA)))
            return str(int(HAND_DATA))
        except Exception as error:
            return ""
    
    def get_thisWeek(self, tran, fun):
        '''
            // *** Get the date range of this week [start, end] *** //
        '''
        try:
            today = datetime.datetime.now()
            this_week_start = today - timedelta(days = today.weekday()); this_week_end = today + timedelta(days = 6 - today.weekday())
            return str(eval(f'this_week_{tran[fun]}').date())
        except Exception as error:
            return ""

    def get_thisMonth(self, tran, fun):
        '''
            // *** Get the date range of this month [start, end] *** //
        '''
        try:
            today = datetime.datetime.now()
            this_month_start = datetime.datetime(today.year, today.month, 1)
            this_month_end = datetime.datetime(today.year, today.month + 1, 1) - timedelta(days=1) + datetime.timedelta(hours=23, minutes=59, seconds=59)
            return str(eval(f'this_month_{tran[fun]}').date())
        except Exception as error:
            return ""

    def get_thisYear(self, tran, fun):
        '''
            // *** Get the date range of this year [start, end] *** //
        '''
        try:
            today = datetime.datetime.now()
            this_year_start = datetime.datetime(today.year, 1, 1)
            this_year_end = datetime.datetime(today.year + 1, 1, 1) - timedelta(days=1) + datetime.timedelta(hours=23, minutes=59, seconds=59)
            return str(eval(f'this_year_{tran[fun]}').date())
        except Exception as error:
            return ""

    def get_PrestoreData(self, tran= None, fun= None) -> None:
        ''' 
            // *** Pre stored data extraction ***//
              Pre stored data extraction, used in conjunction with getElementText keyword, takes out the temporarily stored data of getelementtext keyword and replaces the data 
            into the field value of "function operation value" in "use case step file".It is applicable to scenarios such as "the expected result to be compared is unclear" and 
            "the information to be entered is dependent" [delete, modify... And other operations].
        '''
        try:
            expectedText = PRIVATEDATA['ELEVALUE']
            _key = [key for key in expectedText.keys()][-1] if not tran else tran[fun]
            return expectedText[_key]
        except Exception as error:
            return ""