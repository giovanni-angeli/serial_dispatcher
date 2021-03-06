# coding: utf-8


import os
import sys
import time
import logging
import traceback
import asyncio

import serial_dispatcher

from serial_dispatcher.dispatcher import Dispatcher

def check_version():

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, '../serial_dispatcher', '__version__'), encoding='utf-8') as f:
        expected__version__ = f.read().strip()

    assert (expected__version__ == serial_dispatcher.__version__)


def _setup_virtual_serial_ports():

    tmp_pth = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tmp')

    vsp_0_IN = os.path.join(tmp_pth, 'vsp_0_IN')
    vsp_0_OUT = os.path.join(tmp_pth, 'vsp_0_OUT')
    vsp_1_IN = os.path.join(tmp_pth, 'vsp_1_IN')
    vsp_1_OUT = os.path.join(tmp_pth, 'vsp_2_OUT')

    external_cmds = [
        'socat -d -d pty,rawer,echo=0,link={} pty,rawer,echo=0,link={}  & '.format(vsp_0_IN, vsp_0_OUT),
        'socat -d -d pty,rawer,echo=0,link={} pty,rawer,echo=0,link={}  & '.format(vsp_1_IN, vsp_1_OUT),
    ]

    if not os.path.exists(tmp_pth):
        os.makedirs(tmp_pth)

    for cmd_ in external_cmds:
        logging.warning(cmd_)
        os.system(cmd_)

    return ((vsp_0_IN, vsp_0_OUT), (vsp_1_IN, vsp_1_OUT))

def _teardown_virtual_serial_ports():

    os.system('killall socat')


async def _async_test_with_virtual_ports(time_to_live):

    ((vsp_0_IN, vsp_0_OUT), (vsp_1_IN, vsp_1_OUT)) = _setup_virtual_serial_ports()
    time.sleep(.1)

    SETTINGS_IN = {
        'name': 'D_IN',
        'endpoints': [
            {
                'name': 'camera_in',
                'data_port': (vsp_0_IN, {'baudrate': 115200}),
            },
            {
                'name': 'motor_in',
                'data_port': (vsp_1_IN, {'baudrate': 9600}),
            },
        ]
    }

    SETTINGS_OUT = {
        'name': 'D_OUT',
        'endpoints': [
            {
                'name': 'camera_out',
                'data_port': (vsp_0_OUT, {'baudrate': 115200}),
            },
            {
                'name': 'motor_out',
                'data_port': (vsp_1_OUT, {'baudrate': 9600}),
            },
        ]
    }

    d_IN = Dispatcher(SETTINGS_IN)
    d_OUT = Dispatcher(SETTINGS_OUT)

    await d_IN .open()
    await d_OUT.open()

    t0 = time.time()
    while 1:
        
        if time.time() - t0 > time_to_live:
            break

        logging.warning("Running...")
        await asyncio.sleep(1)
        d_OUT.write_to_serial('camera_out', b'ABCDEFGHIJKLM\r\n')
        await asyncio.sleep(1)
        d_OUT.write_to_serial('motor_out', b'NOPQRSTUVWXYZ\r\n')

    await d_IN .close()
    await d_OUT.close()

    _teardown_virtual_serial_ports()


def check_with_virtual_ports(time_to_live=5):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_async_test_with_virtual_ports(time_to_live))
    except:
        logging.warning(traceback.format_exc())
