# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/11/2 16:15
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : security.py
@IDE     : PyCharm
------------------------------------
"""
from inhandtest.pages.er_device.functions.functions import InboundRules


class Security:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER805', language='en', page=None, **kwargs):
        self.inbound_rules = InboundRules(host, username, password, protocol, port, model, language, page, **kwargs)
