# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/11/30 17:48
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : vpn.py
@IDE     : PyCharm
------------------------------------
"""
from inhandtest.pages.er_device.functions.functions import IpsecVpn


class Vpn:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER805', language='en', page=None, **kwargs):
        self.ipsec_vpn = IpsecVpn(host, username, password, protocol, port, model, language, page, **kwargs)
