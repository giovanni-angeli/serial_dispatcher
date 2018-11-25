# coding: utf-8

from .common import check_version, check_with_virtual_ports

def test_ver():    

    check_version()

def test_comm():    

    check_with_virtual_ports(time_to_live=4)
