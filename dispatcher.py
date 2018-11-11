# coding: utf-8

import os
import sys
import time
import logging
import traceback
import asyncio
from concurrent import futures

import serial_asyncio


class Dispatcher(object):

    def __init__(self, settings):
        
        """
        example_settings = {
            'name': 'in',
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
        """

        self.settings = settings
        self.name = settings.get('name', 'unknown')

        self.serial_endpoints = {}

        self.tasks = []

        self.endpoints = {}

    async def open(self):

        logging.warning("Opening...")

        for d in self.settings['endpoints']:

            try:
                _reader, _writer = await serial_asyncio.open_serial_connection(url=d['data_port'][0], **d['data_port'][1])
                self.serial_endpoints[d['name']] = (_reader, _writer)
                tsk_ = asyncio.ensure_future(self._serial_handler(_reader, d['name']))
                self.tasks.append(tsk_)
            except Exception:
                logging.error(traceback.format_exc())

        logging.warning("Open.")

    async def close(self):

        logging.warning("Closing...")

        for t in self.tasks:
            t.cancel()
            await asyncio.gather(t)

        logging.warning("Closed.")

    def write_to_serial(self, endpoint_name, out_buff):

        self.serial_endpoints[endpoint_name][1].write(out_buff)

    async def _serial_handler(self, _reader, endpoint_name):
        try:
            while 1:
                msg = await _reader.readuntil(b'\n')
                self._dispatch_serial_pack(endpoint_name, msg)
        except futures._base.CancelledError:
            # ~ this is raised on closing
            logging.warning("cancelled")
        except asyncio.streams.IncompleteReadError:
            # ~ this also is raised on closing while reading
            logging.info(traceback.format_exc())
        except Exception:
            logging.error(traceback.format_exc())

    def _dispatch_serial_pack(self, endpoint_name, pack):
        
        """ this should be reimplemented in a derived class. """

        logging.warning("name:{}, endpoint_name:{}, dispatching pack:{}".format(self.name, endpoint_name, pack))
