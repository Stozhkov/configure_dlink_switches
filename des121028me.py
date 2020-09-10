from dgs1210 import DGS1210
from telnetlib import Telnet
from terminal import Terminal


class DES121028me(DGS1210):

    def __init__(self, parameters):
        super().__init__(parameters)

    input_wait_string = b'DES-1210-28/ME:5#'

    def configure_dhcp_filter(self):

        """
            Configure DHCP filter

        :return: Nothing
        """

        print('Configure DHCP filter')
        self.make_instruction('config filter dhcp_server ports 1-24 state enable')
        self.make_instruction('config filter dhcp_server illegal_server_log_suppress_duration 30min')

    def upgrade_firmware(self):
        pass

    def configure_snmp(self):

        """
            Configure SNMP

        :return: Nothing
        """

        print('Configure SNMP')
        self.make_instruction('enable snmp')
        self.make_instruction('disable snmp authenticate_traps')
        self.make_instruction('config snmp coldstart_traps disable')
        self.make_instruction('config snmp warmstart_traps disable')
        self.make_instruction('disable snmp linkchange_traps')
        self.make_instruction('config snmp linkchange_traps ports 1-10 enable')
        self.make_instruction('disable snmp port_security_violation traps')
        self.make_instruction('disable snmp LBD traps')
        self.make_instruction('disable snmp firmware_upgrade_state traps')
        self.make_instruction('disable snmp duplicate_ip_detected traps')
        self.make_instruction('disable community_encryption')
        self.make_instruction('delete snmp user ReadOnly v1')
        self.make_instruction('delete snmp user ReadOnly v2c')
        self.make_instruction('delete snmp user ReadWrite v1')
        self.make_instruction('delete snmp user ReadWrite v2c')
        self.make_instruction('delete snmp group ReadOnly v1')
        self.make_instruction('delete snmp group ReadOnly v2c')
        self.make_instruction('delete snmp group ReadWrite v1')
        self.make_instruction('delete snmp group ReadWrite v2c')
        self.make_instruction('delete snmp view ReadWrite 1')
        self.make_instruction('create snmp user ReadOnly ReadOnly v1')
        self.make_instruction('create snmp user ReadOnly ReadOnly v2c')
        self.make_instruction('create snmp user ReadWrite ReadWrite v1')
        self.make_instruction('create snmp user ReadWrite ReadWrite v2c')
        self.make_instruction('create snmp group ReadOnly v1 read_view ReadWrite notify_view ReadWrite')
        self.make_instruction('create snmp group ReadOnly v2c read_view ReadWrite notify_view ReadWrite')
        self.make_instruction(
            'create snmp group ReadWrite v1 read_view ReadWrite write_view ReadWrite notify_view ReadWrite')
        self.make_instruction(
            'create snmp group ReadWrite v2c read_view ReadWrite write_view ReadWrite notify_view ReadWrite')
        self.make_instruction('create snmp view ReadWrite 1 1 view_type included')
        self.make_instruction('delete snmp all_community')
        self.make_instruction('create snmp community ' + self.ro_snmp_community + ' ReadOnly')
        self.make_instruction('create snmp community ' + self.rw_snmp_community + ' ReadWrite')

    def connect(self, ip='default'):

        """
            Connect with telnet protocol to switch

        :param ip: Expected 'default' or 'custom' string.
        :return: Nothing
        """

        print('Connect to switch')
        ip_address = ''
        if ip == 'default':
            ip_address = self.default_ip
        elif ip == 'custom':
            ip_address = self.custom_ip_address
        # print(ip_address)
        conn_t = Telnet(ip_address)
        # conn_t.set_debuglevel(1)
        conn_t.read_until(b"UserName:")
        # print(1)
        conn_t.write(self.user_name.encode('ascii') + b"\n")
        conn_t.read_until(b"Password:")
        # print(2)

        conn_t.write(self.password.encode('ascii') + b"\n")
        conn_t.read_until(self.input_wait_string)
        # print(3)

        self.conn_t = conn_t
        Terminal.print_terminal('connect to ' + ip_address, 'Success.')

    def configure_lbd(self):

        """
            Configure Loopback detection

        :return: Nothing
        """

        print('Configure Loopback detection')
        self.make_instruction('enable loopdetect')
        self.make_instruction('config loopdetect lbd_recover_time 60 interval_time 10')
        self.make_instruction('config loopdetect mode portbase')
        self.make_instruction('config loopdetect ports 1-24 state enable')

    def configure_dhcp_filter(self):

        """
            Configure DHCP filter

        :return: Nothing
        """

        print('Configure DHCP filter')
        print('DGS110010me does not support DHCP filtering.')

    def configure_traffic_control(self):

        """
            Configure traffic control

        :return: Nothing
        """

        print('Configure Traffic control')
        self.make_instruction('config traffic control 1-24 broadcast enable')
        self.make_instruction('config traffic control 1-24 multicast enable')
        self.make_instruction('config traffic control 1-24 action drop threshold 64')
        self.make_instruction('config traffic control 25-28 action drop')
        self.make_instruction('config traffic trap none')

    def configure_traffic_segmentation(self):

        """
            Configure traffic segmentation

        :return: Nothing
        """

        print('Configure Traffic segmentation')
        self.make_instruction('config traffic_segmentation 1-24 forward_list 25-28')
        self.make_instruction('config traffic_segmentation 25-28 forward_list 1-28')

    def configure_ip_address(self):

        """
            Configure custom ip address

        :return: Nothing
        """

        print('Configure IP address')
        self.make_instruction('create iproute default ' + self.default_ip_gateway)

        if int(self.mgm_vlan) == int(1):
            self.make_instruction('config ipif System ipaddress ' + self.custom_ip_address + '/' +
                                  self.ip_mask + ' vlan default', not_wait=True)
        else:
            self.make_instruction('config ipif System ipaddress ' + self.custom_ip_address + '/' +
                                  self.ip_mask + ' vlan mgm_' + self.mgm_vlan, not_wait=True)

    def configure_mgm_vlan(self):

        """
            Create management VLAN on the switch, configure management VLAN

        :return: Nothing
        """

        print('Configure management VLAN')
        if int(self.mgm_vlan) == int(1):
            self.make_instruction('config vlan default delete 1-24')
            self.make_instruction('config vlan default add tagged 25-28')
        else:
            self.make_instruction('create vlan mgm_' + self.mgm_vlan + ' tag ' + self.mgm_vlan)
            self.make_instruction('config vlan mgm_' + self.mgm_vlan + ' add tagged 25-28')

    def configure_users_vlan(self):

        """
            Create users VLAN on the switch, configure users VLAN

        :return: Nothing
        """

        print('Configure users VLAN')
        self.make_instruction('create vlan vlan' + self.user_vlan + ' tag ' + self.user_vlan)
        self.make_instruction('config vlan vlan' + self.user_vlan + ' add tagged 25-28')
        self.make_instruction('config vlan vlan' + self.user_vlan + ' add untagged 1-24')

    def delete_default_vlan(self):

        """
            Delete default VLAN from switch if he will not use.

        :return: Nothing
        """

        if int(self.mgm_vlan) != int(1):
            print('Delete default VLAN')
            self.make_instruction('config vlan default delete 1-28')
