'''# Third_party'''
from dominate.tags import *
from dominate.util import raw
from dominate.util import text
from logging.handlers import RotatingFileHandler
'''# built_in'''
import os, time, logging, dominate, traceback
'''# custom'''
from common import GSDSTORE, CASESDATA, RL, RE
from product import version


class Stats:

    def __init__(self) -> None:
        self.start_time = None
        self.end_time = None

    def test_start(self):
        self.start_time = time.time()

    def test_end(self):
        self.end_time = time.time()


class ConsoleLogger:

    def __repr__(self) -> str:
        return "控制台日志记录器"
    
    def __init__(self) -> None:
        return

    def test_end(self):
        print(f"\n\n  ========= 总耗时 : {stats.end_time - stats.start_time:.3f} 秒 =========\n")
        print(f"\n  用例总数量 : {CASESDATA['total']}")
        print(f"\n  预备执行用例数量 : {CASESDATA['prepare']}")
        print(f"\n  实际执行用例数量 : {CASESDATA['implement']}")
        print(f"\n  \033[32m通过 : {CASESDATA['passNum']}\033[0m")
        print(f"\n  \033[31m失败 : {CASESDATA['failNum']}\033[0m")
        print(f"\n  异常 : {CASESDATA['abnormalNum']}")
        print(f"\n  阻塞 : {CASESDATA['prepare'] - CASESDATA['implement']}\n")

    def debug(self, msg):
        print(f"\n \033[32m{msg}\033[0m" if 'Pass' in msg else f"\n \033[31m{msg}\033[0m" if 'Fail' in msg else f"\n {msg}")
    
    def exceptinfo(self, msg): print(traceback.format_exc())


class TextLogger(object):

    def __repr__(self) -> str:
        return "文本日志记录器"
    
    def __init__(self) -> None:
        return
    
    def test_start(self):
        textStartTime = time.strftime(TIME_FORMAT, time.localtime(stats.start_time))
        logger.info(f"\n\n  ========= 测试开始 : {textStartTime} =========\n")

    def test_end(self):
        textEndTime = time.strftime(TIME_FORMAT, time.localtime(stats.end_time))
        logger.info(f"\n\n  ========= 测试结束 : {textEndTime} =========\n")
        logger.info(f"\n  总耗时  : {stats.end_time - stats.start_time:.3f} 秒\n")
        logger.info(f"\n  用例总数量 : {CASESDATA['total']}")
        logger.info(f"\n  预备执行用例数量 : {CASESDATA['prepare']}")
        logger.info(f"\n  实际执行用例数量 : {CASESDATA['implement']}")
        logger.info(f"\n  通过 : {CASESDATA['passNum']}")
        logger.info(f"\n  失败 : {CASESDATA['failNum']}")
        logger.info(f"\n  异常 : {CASESDATA['abnormalNum']}")
        logger.info(f"\n  阻塞 : {CASESDATA['prepare'] - CASESDATA['implement']}\n")

    def info(self, msg):logger.info(msg)

    def debug(self, msg):logger.debug(msg)
    
    def exceptinfo(self, msg):logger.exception(msg)


class HtmlLogger(object):

    def __repr__(self) -> str:
        return "HTML日志记录器"

    def __init__(self) -> None:
        self.doc = None
        self.collect_table_box_left = None
        self.collect_chart_box_right = None
        self.detail_box = None
        self.detail_result_title = None
        self.detail_result_table = None
        self.activity = None
        self.log_file_name = f"{GSDSTORE['LOGNAME']}" if 'LOGNAME' in GSDSTORE.keys() else f"测试报告{time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(stats.start_time))}"

    def test_start(self):
        with open(os.path.join(os.path.dirname(__file__),'log.css'),encoding='utf8') as f: _css = f.read()
        with open(os.path.join(os.path.dirname(__file__),'log.js'),encoding='utf8') as f: _js = f.read()
        self.doc = dominate.document(title=f"{self.log_file_name}")
        self.doc.head.add(meta(charset='UTF-8'), style(raw(_css)), script(raw(_js),type='text/javascript'))
        row_box = self.doc.body.add(div(_class='row'));row_box.add(h1(f"{self.log_file_name} - kdtest v{version}"))
        collect_box = row_box.add(div(_class='collect-box'));collect_box.add(h3("汇总结果："))
        self.collect_table_box_left, self.collect_chart_box_right = collect_box.add(table(_class='table-box-left'), div(_class='chart-box-right'))
        self.detail_box = row_box.add(div(_class='detail-box'));self.detail_box.add(h3("执行详情："))
    
    def test_end(self):
        htmlStartTime = time.strftime(TIME_FORMAT, time.localtime(stats.start_time))
        htmlEndTime = time.strftime(TIME_FORMAT, time.localtime(stats.end_time))
        table = {
            "测试开始时间" : htmlStartTime,"测试结束时间" : htmlEndTime,"总耗时" : f"{stats.end_time - stats.start_time:.3f} 秒",
            "用例总数量": CASESDATA['total'],"预备执行用例数量" : CASESDATA['prepare'], "实际执行用例数量" : CASESDATA['implement'],
            "通过" : CASESDATA['passNum'],"失败" : CASESDATA['failNum'],"异常" : CASESDATA['abnormalNum'],"阻塞" : CASESDATA['prepare'] - CASESDATA['implement'],
            "自定义插件捕获失败" : CASESDATA['plugin'],"用例初始化失败	" : CASESDATA['suite_setup'],"用例清除失败	" : CASESDATA['suite_teardown'],
        }
        chart = {
            "用例通过条数": {"num": CASESDATA['passNum'],"per": round(CASESDATA['passNum']/(CASESDATA['prepare'] if CASESDATA['prepare'] else 1) * 100, 2),"css": "PASS"},
            "用例失败条数": {"num": CASESDATA['failNum'],"per": round(CASESDATA['failNum']/(CASESDATA['prepare'] if CASESDATA['prepare'] else 1) * 100, 2),"css": "FAIL"},
            "用例异常条数": {"num": CASESDATA['abnormalNum'],"per": round(CASESDATA['abnormalNum']/(CASESDATA['prepare'] if CASESDATA['prepare'] else 1) * 100, 2),"css": "ABNORMAL"},
            "用例阻塞条数": {"num": CASESDATA['prepare'] - CASESDATA['implement'],"per": round((CASESDATA['prepare'] - CASESDATA['implement'])/(CASESDATA['prepare'] if CASESDATA['prepare'] else 1) * 100, 2),"css": "CHOKE"}
        }
        for key in table.keys():  # 表格
            with self.collect_table_box_left: trObject = tr();trObject.add(td(key), td(table[key]))
        for key in chart.keys():  # 图表
            with self.collect_chart_box_right:
                item = div(_class="chart-item")
                item.add(span(f"{key}：{chart[key]['num']}"),div(div(f"{chart[key]['per']}%", _class=f"lining {chart[key]['css']}", style=f"width: {chart[key]['per']}%;"), _class="epiboly"))
        with open(f"{GSDSTORE['WORKPATH']['ROOT']}\\{RE}\\{self.log_file_name}.html", 'w', encoding='utf8') as f: f.write(self.doc.render()) 
        try:os.startfile(f"{GSDSTORE['WORKPATH']['ROOT']}\\{RE}\\{self.log_file_name}.html")
        except:
            try:os.system(f"{GSDSTORE['WORKPATH']['ROOT']}\\{RE}\\{self.log_file_name}.html")
            except:pass

    def frame_init(self):
        '''框架初始化'''
        executeTime = time.strftime(TIME_FORMAT, time.localtime(stats.end_time))
        self.activity = self.detail_box.add(div(_class="content-item-box"))
        self.activity.add( div(span("框架初始化", _class="name"), span(executeTime, _class="time"), _class="case-title-box"))
    
    def case_init(self):
        '''用例初始化'''
        executeTime = time.strftime(TIME_FORMAT, time.localtime(stats.end_time))
        self.activity = self.detail_box.add(div(_class="content-item-box"))
        self.activity.add(div(span("用例执行初始化 __suite_setup__()", _class="name"), span(executeTime, _class="time"), _class="case-title-box"))
    
    def case_sheet(self, name):
        '''单条用例执行结果'''
        executeTime = time.strftime(TIME_FORMAT, time.localtime(stats.end_time))
        content_item_box = self.detail_box.add(div(_class="content-item-box"))
        self.case_title = content_item_box.add(div(_class="case-title-box", _fold="fold", _onclick="boxFold(this)"));self.detail_result_title = self.case_title.add(span("", _class="result PASS"))
        self.case_arrows = self.case_title.add(span(_class="arrows"));self.case_title.add(span(f"用例名称：{name}", _class="name", _title=name),span(f"{executeTime}", _class="time"))
        self.case_result_box = content_item_box.add(div(_class="case-result-box case-fold-true"));self.activity = self.case_result_box
    
    def case_start(self):
        header = {"操作步骤说明": "width:20%;", "操作关键字": "width:15%;", "元素定位信息": "width=20%;", "操作值": "width=20%;", "执行结果": "", "异常信息": "width:20%;"}
        self.detail_result_table = self.case_result_box.add(table(_class="detail-result-table"));self.detail_result_table.add(tr(th(key, _style=header[key]) for key in header.keys()))

    def case_step(self, cell):
        '''单条用例步骤执行结果'''
        self.detail_result_table.add(tr(td(str(cell[key][0]).replace("None",""), _class=cell[key][1]) for key in cell.keys()))
    
    def case_result(self, result):
        with self.detail_result_title:text(result);attr(_class=f"result {result}")
        if result != 'PASS': 
            with self.case_arrows:attr(_style="transform: rotate(45deg) translateY(-50%); transform-origin: right top;")
            with self.case_title:attr(_fold="")
            with self.case_result_box:attr(_class=f"case-result-box case-fold-false")
    
    def case_clear(self):
        '''用例执行清除'''
        executeTime = time.strftime(TIME_FORMAT, time.localtime(stats.end_time))
        self.activity = self.detail_box.add(div(_class="content-item-box"))
        self.activity.add(div(span("用例执行清除  __suite_teardown__()", _class="name"), span(executeTime, _class="time"), _class="case-title-box"))
    
    def info(self, msg):self.activity.add(div(str(msg), _class="extra"))

    def exceptinfo(self, msg):
        msg = msg + f"{traceback.format_exc()}"
        self.activity.add(div(pre(msg,_class="extra"),_class="case-information-box"))


TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logFile = os.path.join(f"{GSDSTORE['WORKPATH']['ROOT']}\\{RL}",'testresult.log')
handler = RotatingFileHandler(logFile, maxBytes=1024*1024*30, backupCount=3, encoding='utf8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt="%(message)s")
handler.setFormatter(formatter)
handler.doRollover()
logger.addHandler(handler)  # 加载handlers对象
stats = Stats()
from utils.log.trusteeship import trusteeship
trusteeship.register([stats, ConsoleLogger(), TextLogger(), HtmlLogger()])