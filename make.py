# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import logging

from optparse import (OptionParser, OptionGroup)

from setup import SETUP_KW_ARGS

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)

DEFAULT_DIST_DIR = "./tmp/dist_dir"
DEFAULT_PY_VENV_PATH = './tmp/venv'
LOG_LEVEL = 'DEBUG'

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

VERSION = SETUP_KW_ARGS["version"]
APP_NAME = SETUP_KW_ARGS["name"]

VERSION = '0.0.1'

USAGE = """ $ python3 %prog [options] [settings] [actions]

    beware: [settings] must precede [actions] to be effective.

    hand-made tool for interacting with the project in development.
    See: https://docs.pytest.org/en/latest/goodpractices.html#goodpractices
"""


def action_create_virt_env(option, opt_str, value, parser):
    "build (or re-build) and setup the python virtual env in <py_venv_path>."

    cmd_ = """(rm -fr {py_venv_path}/*;
    virtualenv -p {python_executable} {py_venv_path}; 
    . {py_venv_path}/bin/activate ; 
    pip install --upgrade pip ; 
    pip install wheel)
    """.format(python_executable=sys.executable, py_venv_path=parser.values.py_venv_path)

    os.system(cmd_)
    logging.warning("re-created virtual env in:{}".format(parser.values.py_venv_path))


def action_build(option, opt_str, value, parser):
    "build the python wheel of this project in <dist_dir>"

    wheel_fullname = '{}-{}-py3-none-any.whl'.format(APP_NAME, VERSION)

    os.system("rm -f {}/{}*".format(parser.values.dist_dir, wheel_fullname))

    setup_cmd = "{} setup.py bdist_wheel --dist-dir {}".format(sys.executable, parser.values.dist_dir)
    if parser.values.quiet:
        setup_cmd += " > /dev/null"
    os.system(setup_cmd)

    os.system("rm -fr build".format())
    os.system("rm -fr {}.egg-info".format(APP_NAME))


def action_install(option, opt_str, value, parser):
    "Install the wheel in <py_venv_path> virt env."

    activate = ". {}/bin/activate".format(parser.values.py_venv_path)
    wheel_fullname = '{}-{}-py3-none-any.whl'.format(APP_NAME, VERSION)

    uninstall_cmd = "{};pip uninstall -y {}".format(activate, APP_NAME)
    install_cmd = "{};pip install {}/{}".format(activate, parser.values.dist_dir, wheel_fullname)

    if parser.values.quiet:
        uninstall_cmd += " > /dev/null"
        install_cmd += " > /dev/null"

    os.system(uninstall_cmd)
    os.system(install_cmd)


def action_install_editable(option, opt_str, value, parser):
    " Install your package in “editable” mode by running from the same directory "
    "which lets you change your source code (both tests and application) and rerun tests "
    "at will. It installs your package using a symlink to your development code."

    activate = ". {}/bin/activate".format(parser.values.py_venv_path)
    wheel_fullname = '{}-{}-py3-none-any.whl'.format(APP_NAME, VERSION)

    install_cmd = "{};pip install -e .".format(activate)

    if parser.values.quiet:
        install_cmd += " > /dev/null"

    os.system(install_cmd)


def action_run(option, opt_str, value, parser):
    "import the package and print its version calling the virtenv interpreter. Just a minimal runtime check"

    cmd_ = '. {}/bin/activate;'.format(parser.values.py_venv_path)
    cmd_ += "python -c 'import serial_dispatcher; print (\"serial_dispatcher.__version__:{}\".format(serial_dispatcher.__version__))'"

    r = subprocess.run(cmd_, shell=True)


def action_run_test(option, opt_str, value, parser):
    "run tests in './test' directory, using pytest and 'test/test.ini' config file."


    
    cmd_ = ". {}/bin/activate; cd ./test/; pytest -k {}".format(parser.values.py_venv_path, parser.values.test_kind),
    logging.info(cmd_)
    r = subprocess.run(cmd_, shell=True)


def action_no_action(option, opt_str, value, parser):
    """ no action, just a placeholder for debug."""
    logging.warning("parser:{}".format(parser))


def parse_options():

    groups_ = {
        "Settings": [
            (["-q", "--quiet"],
             {'default': False, 'help': "don't log build messages, default=False"}),
            (["-v", "--py_venv_path"],
             {'default': DEFAULT_PY_VENV_PATH, 'help': "filesystem's path where to create the virt env, default={}".format(DEFAULT_PY_VENV_PATH)}),
            (["-d", "--dist_dir"],
             {'default': DEFAULT_DIST_DIR, 'help': "filesystem's path where to create temporarly the python package (wheel), default={}".format(DEFAULT_DIST_DIR)}),
            (["-k", "--test_kind"],
             {'default': 'develop', 'help': "with action -t; which kind of test you want to run [develop|host|target|builder...], default:develop (it is passed directly to pytest as -k options)"}),
        ],
        "Actions": [
            (["-c", "--create_virt_env"],
             {'action': "callback", 'callback': action_create_virt_env, 'help': action_create_virt_env.__doc__}),
            (["-b", "--build"],
             {'action': "callback", 'callback': action_build, 'help': action_build.__doc__}),
            (["-i", "--install"],
             {'action': "callback", 'callback': action_install, 'help': action_install.__doc__}),
            (["-t", "--run_test"],
             {'action': "callback", 'callback': action_run_test, 'help': action_run_test.__doc__}),
            (["-r", "--run"],
             {'action': "callback", 'callback': action_run, 'help': action_run.__doc__}),
            (["-e", "--install_editable"],
             {'action': "callback", 'callback': action_install_editable, 'help': action_install_editable.__doc__}),
            (["-n", "--no_action"],
             {'action': "callback", 'callback': action_no_action, 'help': action_no_action.__doc__}),
        ]
    }

    parser = OptionParser(usage=USAGE, version=VERSION)

    for k, v in groups_.items():
        group_instance = OptionGroup(parser, k)
        for item_ in v:
            group_instance.add_option(*item_[0], **item_[1])
        parser.add_option_group(group_instance)

    parser.parse_args()

if __name__ == '__main__':

    fmt_ = logging.Formatter('[%(asctime)s]'
                             '%(name)s:'
                             '%(levelname)s:'
                             '%(funcName)s() '
                             '%(filename)s:'
                             '%(lineno)d: '
                             '%(message)s ')

    ch = logging.StreamHandler()
    ch.setFormatter(fmt_)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(LOG_LEVEL)

    parse_options()
