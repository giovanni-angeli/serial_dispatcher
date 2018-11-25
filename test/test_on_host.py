# coding: utf-8

import os
import sys
import time
import logging
import traceback
import asyncio

import serial_dispatcher

def test():

    msg = "serial_dispatcher.__version__:{}".format(serial_dispatcher.__version__)
    print (msg)


if __name__ == '__main__':

    test()
