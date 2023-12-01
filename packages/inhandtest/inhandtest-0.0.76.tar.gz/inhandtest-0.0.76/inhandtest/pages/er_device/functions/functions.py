# -*- coding: utf-8 -*-
# @Time    : 2023/11/30 16:18:00
# @Author  : Pane Li
# @File    : functions.py
"""
functions

"""
import allure
from inhandtest.base_page import BasePage
from inhandtest.pages.er_device.functions.functions_locators import FunctionsLocators


class LanOrLocalNetwork(BasePage):

    @allure.step('配置lan')
    def config(self, **kwargs):
        """

        :param kwargs:
           lan_resource:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        name: str
                        ip_mode: 'check'|'uncheck'
                        vlan_only_mode: 'check'|'uncheck'
                        standard: 'check'|'uncheck'
                        guest: 'check'|'uncheck'
                        vlan: int
                        ip_address_mask: str, '192.168.2.1/24'
                        dhcp_server: 'enable'|'disable'
                        dhcp_ip_range_start_ip: str, '192.168.2.1'
                        dhcp_ip_range_end_ip: str, '192.168.2.254'
                        ipv6: 'disable'| 'auto'| 'static_ip'
                        ipv6_address: str, '2001:db8::1'
                        ipv6_prefix_length: int
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        if self.model == 'EAP600':
            self.access_menu('config.lan')
        else:
            self.access_menu('local_network')
            result = []
            for value in kwargs.get('lan_resource')[0]:
                if isinstance(value, dict) and value.get('ip_address_mask'):
                    value_ = value.pop('ip_address_mask')
                    value.update({'ip_address': value_.split('/')[0], 'mask': value_.split('/')[1]})
                result.append(value)
            if result:
                kwargs.update({'lan_resource': [tuple(result)]})
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).lan_or_localnetwork, kwargs)


class Internet(BasePage):

    @allure.step('配置internet')
    def config(self, **kwargs):
        """
        配置internet
        :param kwargs:
            uplink_table:
            [($action, **kwarg)] ex: [('delete_all', )],
            [('delete', '$interface')]
            [('edit', '$interface', $new)]
            [('add', {'name': '$interface', 'ip_address_mask': ''})]
            action: add|delete|delete_all|edit|exist
                    name: str, 'WAN2'| 'Wi-Fi(STA)'
                    (当对接口进行编辑时, 不传入name参数, ex:[('edit', $interface, $new)], 删除同理
                    $interface: 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular')
                以下为WAN1/WAN2和Wi-Fi(STA)公共参数:
                    ipv4_type: 'dhcp'|'static_ip'| 'pppoe'
                    ipv4_address: str, ip, ex:'192.168.2.100'
                    mask: str, mask, ex:'255.255.255.0'
                    ipv4_gateway_address: str, ex:'192.168.2.1'
                    main_dns: str, ex:'223.5.5.5'
                    secondary_dns: str, ex:'223.5.5.5'
                    mtu: int, ex:1500
                以下为配置WAN1/WAN2独有参数:
                    pppoe_user_name: str,
                    pppoe_password: str,
                    local_ip_address: str,
                    remote_ip_address: str,
                    ipv6_type: 'dhcp'|'static_ip'| 'auto'
                    ipv6_address: str, ip, ex:'2001:db8::1'
                    prefix_length: str, ex:'64'
                    ipv6_gateway_address: str, ex:'2001:db8::1'
                    main_ipv6_dns: str, ex:'2001:db8::1'
                    secondary_ipv6_dns: str, ex:'2001:db8::1'
                以下为配置Wi-Fi(STA)独有参数:
                    band: '2.4g'|'5g'
                    ssid: str
                    security: 'open'|'wpa_psk'|'wpa2_psk'| 'wpa_wpa2_psk'
                    encryption: 'ccmp'|'ccmp_tkip'
                    wlan_password: str
                以下为配置Cellular独有参数:
                (编辑Cellular时, 传参方式ex:[('edit', 'Cellular', {'work_mode': $work_mode, 'sim1':**kwargs,
                'sim2':**kwargs})])
                    work_mode: 'only_sim1'|'only_sim2'|'dual_mode'
                    primary_card: 'sim1'|'sim2'
                    cellular_mtu_mode: 'auto'|'manual'
                    cellular_mtu_input: int, ex:1500
                    sim1/sim2:dict
                        dialing_parameters: 'auto'|'manual'
                        service_type: 'auto'| '2g'| '3g'| '4g'| '5g_sa'| '4g&5g'
                        5g_type: service_type=auto时有'sa'|'nsa'| 'sa_nsa',
                                service_type=4g&5g时有'sa_nsa_lte'|'nsa_lte'|'sa_lte', 其他值无该参数
                        pin_code: str
                        ims: 'auto'|'enable'| 'disable'
                        ip_type: 'ipv4'|'ipv6'| 'ipv4&ipv6'
                        apn: str
                        authentication: 'auto'|'pap'| 'chap'| 'ms_chap'| 'ms_chapv2'
                        username: str
                        password: str
                以下为所有接口的公共参数:
                    status: 'enable'|'disable'
                    nat: 'check'|'uncheck'
                    save: True, False or dict
                    cancel: True, False or dict
                    text_messages: str or list
                    tip_messages: str or list
            policy:
                [('policy', {'usage_traffic': $param, 'sim1': **kwargs, 'sim2': **kwargs})]})]
                sim1/sim2: dict
                    threshold_enable: 'enable'|'disable'
                    threshold_input: int
                    threshold_unit: 'mb'|'gb'|'kb'
                    monthly_reset_day: int, 1-31
                    action: 'notification'| 'only_cloud_management_traffic'
                    usage_of_the_month: int, 流量校准时填入
                    usage_of_the_month_unit: 'mb'|'gb'|'kb', 流量校准时填入
                abnormal_card_switching_time: int, seconds
                reuse_the_primary_card: str or list, 'usage'| 'time'| 'date'
                usage_traffic: int
                usage_traffic_unit: 'mb'|'gb'
                using_time: float, hours, 0.5-240
                switching_day_of_month, int, 1-31
            link_detection: 'enable'|'disable'
            detection_address_1: str
            detection_address_2: str
            link_backup: 'check'|'uncheck'
            failover_mode: 'immediately_switch'| 'delayed_switch'| 'do_not_switch'
            delay_number: int, 5-60s
            load_balancing: 'enable'|'disable'
            save: True, False or dict
            reset: True, False or dict
            text_messages: str or list
            tip_messages: str or list
        :return:
        """

        def get_value(value):
            def get_sim1_sim2(value_):
                if isinstance(value_, dict):
                    sim1, sim2 = {'sim1': value_.get('sim1')}, {'sim2': value_.get('sim2')}
                    for param in [sim1, sim2]:
                        if param:
                            for k, v in param.items():
                                if v:
                                    value_.pop(k)
                                    if value_.get('work_mode') == 'dual_mode':
                                        v.update({f'tab': True})
                                    elif 'usage_of_the_month' in v.keys() or 'usage_traffic_unit' in v.keys():
                                        v.update({f'modify': True, f'usage_of_the_month_confirm': True})
                                    value_.update({f"{k}_{key}": value for key, value in param.get(k).items()})
                return value_

            if isinstance(value, tuple):
                result = []
                [result.append(i) for i in value]
                if len(value) > 1:
                    if 'edit' in result[0]:
                        values = result[2]
                        result[2] = get_sim1_sim2(values)
                    else:
                        values = result[1]
                        result[1] = get_sim1_sim2(values)
                    return [tuple(result)]

        for i in ['uplink_table', 'policy']:
            params = kwargs.get(i)
            if params:
                kwargs.pop(i)
                for value in params:
                    get_value(value)
            kwargs.update({i: params})
        self.access_menu('internet')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).internet, kwargs)


class InboundRules(BasePage):

    @allure.step('配置入站规则')
    def config(self, **kwargs):
        """
        :param kwargs:
           inbound_rules:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                [('insert_row_up, 'test', {'name':'test1', 'protocol':'TCP'})] insert_row_up| insert_row_down, 向上插入|向下插入
                [('edit', 'Default', {'permit': True})]默认规则编辑
                action: add|delete|delete_all|edit|exist|insert_row_up| insert_row_down
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        interface: 'WAN1'|'WAN2'|'Cellular'|'WI-Fi(STA)'
                        protocol: 'any'|'tcp'|'udp'|'icmp'|'custom'
                        protocol_input: int
                        source: 'any'|'custom'
                        source_input: str, '192.168.2.1/24'
                        src_port: 'any'|'custom'
                        src_port_input: int
                        destination: 'any'|'custom'
                        destination_input: str, '192.168.2.1/24'
                        dst_port: 'any'|'custom'
                        dst_port_input: int
                        permit: True|False
                        deny: True|False
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        self.access_menu('security.firewall.inbound_rules')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).inbound_rules, kwargs)

class IpsecVpn(BasePage):

    @allure.step("编辑ipsec VPN")
    def config(self, **kwargs):
        """
        :param kwargs:
            ipsec_vpn:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        ike_version: 'ikev1'|'ikev2'
                        negotiation_mode: 'main_mode'|'agressive_mode'
                        pre_shared_key: str
                        uplink_interface: str, 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular'
                        peer_address: str, ip or domain name
                        tunnel_mode: 'tunnel'|'transmission'
                        local_subnet: list, ['192.168.2.0',], 最多支持四个子网
                        remote_subnet: list, ['192.168.2.0',], 最多支持四个子网
                        local_identity: 'auto'|'ip_address'|'fqdn'|'user_fqdn'
                        local_identity_id: str
                        peer_identity: 'auto'|'ip_address'|'fqdn'|'user_fqdn'
                        peer_identity_id: str
                        ike_policy_encryption: 'AES128'|'AES192'|'AES256'|'3DES'|'DES'
                        ike_policy_authentication: 'SHA1'|'SHA2-256'|'SHA2-384'|'SHA2-512'|'MD5'
                        ike_policy_dh_groups: int, 1|2|5|14|15|16|19|20|21|24
                        ike_policy_lifetime: int, 60-86400
                        ike_policy_peer_status_detect: 'enable'|'disable'
                        ike_policy_dpd_interval: int, 1-60
                        ike_policy_dpd_timeout: int, 10-3600
                        ipsec_policy_security_protocol: 'ESP'|'AH'
                        ipsec_policy_encryption: 'AES128'|'AES192'|'AES256'|'3DES'|'DES'
                        ipsec_policy_authentication: 'SHA1'|'SHA2-256'|'SHA2-384'|'SHA2-512'|'MD5'
                        ipsec_policy_pfs_groups: str or int, 'OFF'|1|2|5|14|15|16|19|20|21|24
                        ipsec_policy_lifetime: int, 60-86400
                        save: True, False, dict
                        cancel: True, False, dict
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        self.access_menu('vpn.ipsec_vpn')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).ipsec_vpn, kwargs)