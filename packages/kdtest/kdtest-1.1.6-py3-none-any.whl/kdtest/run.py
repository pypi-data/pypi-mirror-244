'''# built_in'''
import os, sys, threading, traceback, shutil, argparse
import colorama
colorama.init(autoreset=True)
'''# custom'''
from common import *
from product import version


def createFile(root, file, content):
    if os.path.exists(f"{root}\\{file}"):
        print("\033[33m file already exist！\033[0m")
        sys.exit(0)
    try:
        fileObject = open(f'{root}\\{file}', 'w', encoding="utf-8")
        fileObject.write(content)
        fileObject.close()
    except Exception as error:
        print("\033[31m Presetting file operation failed！\033[0m")
        sys.exit(2)
    print(f"\033[1;32m Creation completed！\033[0m {root}\{file}")

def processRun():
    from data.init_data import InitializationParameter  # 配置参数
    try:
        InitializationParameter()()
    except Exception as error:
        print(f"\033[35m Parameter configuration error！\033[0m");print(traceback.format_exc())
        sys.exit(2)
    
    from utils.environment_Configuration import EnvironmentConfiguration  # 测试环境
    try:
        EnvironmentConfiguration()(GSDSTORE['START']['browser'], GSDSTORE['START']['url'], GSDSTORE['START']['implicitlyWait'])
    except Exception as error:
        print(f"\033[35m Environment generation error！\033[0m");print(traceback.format_exc())
        sys.exit(2)
    
    from utils.log import log
    from cases.case_execution import collector, cases
    collector.run(); cases()()  # 测试用例执行

def install(path):
    print("Please wait until installation is underway....")
    iden = path.split("\\")[-1]
    try:
        cmd = f"cd {path} && pip install pipreqs && pipreqs . --encoding=utf8 --force && pip install -r requirements.txt"
        os.system(cmd)
    except:
        print("\n \033[31mThe installation failed. The following information is displayed:\033[0m"); print(traceback.format_exc()); return
    else:
        os.remove(f"{path}\\requirements.txt")
        shutil.copytree(path, f"{PROJECTROOT}\\plugins\\{iden}")
        print(f"\n \033[32m √ Installation complete！\033[0m {iden}")

def uninstall(key):
    print("Please later in the unloading....")
    PF = PROJECTROOT.split('\\')[0]
    try:
        cmd = f"{PF} && cd {PROJECTROOT}\\plugins\\{key} && pip install pipreqs && pipreqs . --encoding=utf8 --force && pip uninstall -r requirements.txt"
        os.system(cmd)
    except:
        print("\n \033[31mThe unload failed. The following information is displayed:\033[0m"); print(traceback.format_exc()); return
    else:
        shutil.rmtree(f"{PROJECTROOT}\\plugins\\{key}")
        print(f"\n \033[32m √ Unload complete！\033[0m {key}")

def run():

    root = os.getcwd()  # 根目录
    GSDSTORE['WORKPATH'] = {}
    GSDSTORE['WORKPATH']['ROOT'] = root
    GSDSTORE['WORKPATH']['PACKET'] = f"{root}\\{CASES}"

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--new", action='store_true', help="框架用例数据包生成")
    parser.add_argument("-c", "--change", action='store_true', help="框架自定义配置文件生成")
    parser.add_argument("-p", "--parameter", action='store_true', help="框架静态启动参数文件生成")
    parser.add_argument("--st", action='store_true', help="框架初始化清除脚本生成")
    parser.add_argument("--unit_new", action='store_true', help="框架插件包模板生成")
    parser.add_argument("--unit_show", action='store_true', help="显示框架中目前安装的插件")
    parser.add_argument("--unit_install", metavar='File_Path', action='append', help="框架插件包安装，传入参数为包路径；支持多参数", default=[])
    parser.add_argument("--unit_uninstall", metavar='Plug-in_Name', action='append', help="框架插件包卸载，传入参数为插件名；支持多参数", default=[])
    parser.add_argument("-v", "--version", action='version', version=f'kdtest v/{version}', help="显示版本号" )
    parser.add_argument("--log", metavar="Log_Name", action="store", help="生成的测试报告名称")
    parser.add_argument("--startup", action='store', nargs='?', const='startup', default='startup', choices=['startup'], help="框架启动")

    '''对各项进行处理'''
    args = parser.parse_args()
    if args.new:
        if not os.path.exists(f"{root}\\{CASES}"):
            os.makedirs(f"{root}\\{CASES}\\{ELE}用例元素节点文件夹")
            os.makedirs(f"{root}\\{CASES}\\{INTER}用例接口数据文件夹")
            shutil.copy(f"{PROJECTROOT}\\data\\static\\testCases.xlsx", f"{root}\\{CASES}")
            print(f"\033[32m Creation completed！\033[0m {root}\{CASES}")
        else:
            print("\033[33m folder already exists！\033[0m")
        sys.exit(0)
    
    if args.unit_new:
        if not os.path.exists(f"{root}\\{PIUG}"):
            os.makedirs(f"{root}\\{PIUG}\\{P}\\{P_E}")
            os.makedirs(f"{root}\\{PIUG}\\{P}\\{P_U}")
            createFile(f"{root}\\{PIUG}\\{P}", "__init__.py", "")
            createFile(f"{root}\\{PIUG}\\{P}", f'{P_INI}.ini', INI_CONTENT)
            createFile(f"{root}\\{PIUG}\\{P}", f"{P_M}.py", MODULE_CONTENT)
            createFile(f"{root}\\{PIUG}\\{P}\\{P_E}", f"{P_EY}.yaml", "")
        else:
            print("\033[33m folder already exists！\033[0m")
        sys.exit(0)
    
    if args.unit_show:
        pluginsList = os.listdir(f"{PROJECTROOT}\\plugins")
        if pluginsList:
            line = len('----------------------------------------')
            for index, item in enumerate(pluginsList):
                value = len(item)
                if not index:print('----------------------------------------')
                print(f"  Name  |{' '*(int((line-8-value)/2))}{item}{' '*(int((line-8-value)/2))}")
                print('----------------------------------------')
        else:
            print(f"\033[33m No plug-in is available! \033[0m")
        sys.exit(0) 
    
    if args.unit_install:
        for item in args.unit_install:
            if os.path.exists(item):
                iden = item.split("\\")[-1]
                if not os.path.exists(f"{PROJECTROOT}\\plugins\\{iden}"):
                    install(item)
                else:
                    switch = input(F"The plug-in package has been installed！, Whether to update: Y/N?")
                    if switch.upper() == "Y":
                        shutil.rmtree(f"{PROJECTROOT}\\plugins\\{iden}")
                        install(item)
                        continue
                    else:
                        continue
            else:
                print(f"\033[31m × File not found : \033[0m{item}")
                sys.exit(1)
        else:
            sys.exit(0)
    
    if args.unit_uninstall:
        for item in args.unit_uninstall:
            if os.path.exists(f"{PROJECTROOT}\\plugins\\{item}"):
                switch = input(F"Confirm whether to delete the plug-in: {item}: Y/N?")
                if switch.upper() == "Y":
                    uninstall(item)
            else:
                print(f"\033[31m × The plug-in was not found : \033[0m{item}")
                sys.exit(1)
        else:
            sys.exit(0)

    if args.change:
        createFile(root, f"{CHANGE}.py", CHANGE_CONTENT)
        sys.exit(0)
    
    if args.parameter:
        createFile(root, f"{PARA}.json", PARAMETERS_CONTENT)
        sys.exit(0)
    
    if args.st:
        createFile(root, f"{ST}.py", ST_CONTENT)
        sys.exit(0)
    
    if args.log:
        GSDSTORE['LOGNAME'] = args.log
    
    for item in [RE, RL, DOWN]:
        if not os.path.exists(f'{GSDSTORE["WORKPATH"]["ROOT"]}\\{item}'):
            os.makedirs(f"{GSDSTORE['WORKPATH']['ROOT']}\\{item}")

    if args.startup:
        print("***  Framework startup  ***")
        th_object_process = threading.Thread(target=processRun)
        th_object_process.start()
   

if __name__ == '__main__':
    # 0 表示命令执行成功, 1 表示命令执行有错误, 2 表示框架内部出错
    sys.exit(run())