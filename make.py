
import os
import sys
import time
import logging
import traceback

HERE = os.path.join(os.path.abspath(os.path.dirname(__file__)))
VENV_PATH = os.path.join(HERE, 'VENV')

info_msg = """ BEFORE STARTING, you should run:
    $ sudo apt install virtualenv
    $ sudo apt install socat
"""

def make_venv():
    
    cmd_ = """cd {here};
    (rm -fr {venv_path}/*; 
    virtualenv -p python3 {venv_path}; 
    . {venv_path}/bin/activate ; 
    pip install --upgrade pip ; 
    pip install wheel;
    pip install -r ./requirements.txt)
    """.format(here=HERE, venv_path=VENV_PATH)
    
    os.system(cmd_)
    
def run_test():
    
    cmd_ = "(. {venv_path}/bin/activate ;python ./test.py);".format(venv_path=VENV_PATH) 
        
    print(cmd_)
    os.system(cmd_)
    
def main():
    
    print(info_msg)
    
    if 'make_venv' in sys.argv:
        make_venv()
    
    if 'run_test' in sys.argv:
        run_test()
    
main()
