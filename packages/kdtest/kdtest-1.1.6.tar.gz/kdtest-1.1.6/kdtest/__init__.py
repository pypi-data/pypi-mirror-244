import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(os.path.dirname(os.path.realpath(__file__))+'\\action')
# sys.path.append(os.path.dirname(os.path.realpath(__file__))+'\\cases')
# sys.path.append(os.path.dirname(os.path.realpath(__file__))+'\\data')
# sys.path.append(os.path.dirname(os.path.realpath(__file__))+'\\Interface')
# sys.path.append(os.path.dirname(os.path.realpath(__file__))+'\\plugins')
# sys.path.append(os.path.dirname(os.path.realpath(__file__))+'\\utils')
from reference import GSTORE, INFO
from utils.decorator import reset_implicitlyWait, setInterval