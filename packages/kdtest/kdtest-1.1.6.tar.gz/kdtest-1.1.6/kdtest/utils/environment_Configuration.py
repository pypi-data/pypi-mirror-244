'''# Third_party'''
from selenium import webdriver
'''# custom'''
from common import GSDSTORE, DOWN
from reference import GSTORE
from action.page_Action import KeyWordTest


class EnvironmentConfiguration:

    def __repr__(self) -> str:
        return "测试环境配置"

    def __init__(self) -> None:
        '''浏览器预配置'''
        GSDSTORE["WORKPATH"]["downloadPath"] = f'{GSDSTORE["WORKPATH"]["ROOT"]}\\{DOWN}'

    def __call__(self, browser=None, url=None, implicitly=None):
        '''Edge浏览器暂不支持“启动参数设置”'''
        if browser == 'Chrome':
            __chrome_options__ = webdriver.ChromeOptions()
            __chrome_prefs__ = {'profile.default_content_settings.popups': 0, 'download.default_directory': f'{GSDSTORE["WORKPATH"]["ROOT"]}\\{DOWN}', "download.prompt_for_download": False}
            __chrome_options__.add_experimental_option('prefs', __chrome_prefs__)
            driver = webdriver.Chrome(options = __chrome_options__)
            '''try:
                driver = webdriver.Chrome(options = chrome_Options)
            except Exception as error:
                from webdriver_manager.chrome import ChromeDriverManager
                driver = webdriver.Chrome(options = chrome_Options, executable_path=ChromeDriverManager().install())'''

        elif browser == 'IE':
            __ie_options__ = webdriver.IeOptions()
            __ie_prefs__ = {"download.default_directory": f'{GSDSTORE["WORKPATH"]["ROOT"]}\\{DOWN}', "download.prompt_for_download": False}
            __ie_options__.add_additional_option('prefs', __ie_prefs__)
            driver = webdriver.Ie(options = __ie_options__)
            '''try:
                driver = webdriver.Ie(options = ie_Options)
            except Exception as error:
                from webdriver_manager.microsoft import IEDriverManager
                driver = webdriver.Ie(options=ie_Options, executable_path=IEDriverManager().install())'''

        elif browser == 'Edge':
            from msedge.selenium_tools import Edge, EdgeOptions
            __edge_options__ = EdgeOptions(); __edge_options__.use_chromium = True
            __edge_options__.add_experimental_option("prefs", {"download.default_directory": f'{GSDSTORE["WORKPATH"]["ROOT"]}\\{DOWN}'})
            driver = Edge(options=__edge_options__)
            '''try:
                driver = Edge(options=options)
            except Exception as error:
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install(), options=options)'''
            
        elif browser == 'Firefox':
            import os
            __firefox_options__ = webdriver.FirefoxProfile(); 
            __firefox_options__.set_preference("browser.download.folderList",2)
            __firefox_options__.set_preference("browser.download.manager.showWhenStarting",False)
            __firefox_options__.set_preference('browser.download.dir', f'{GSDSTORE["WORKPATH"]["ROOT"]}\\{DOWN}')
            driver = webdriver.Firefox(firefox_profile=__firefox_options__, service_log_path=os.devnull)
            '''try:
                driver = webdriver.Firefox(firefox_profile=firefox_Options, service_log_path=os.devnull)
            except Exception as error:
                from webdriver_manager.firefox import GeckoDriverManager
                driver = webdriver.Firefox(firefox_profile=firefox_Options, executable_path=GeckoDriverManager().install())'''

        driver.get(url)  # 打开被测系统
        driver.implicitly_wait(int(implicitly))  # 隐式等待
        driver.maximize_window()  # 窗口最大化

        GSTORE['driver'], GSDSTORE['driver'] = [driver, driver]
        keyWord = KeyWordTest(); GSTORE['keyWord'], GSDSTORE['keyWord'] = [keyWord, keyWord]