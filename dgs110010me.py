from dlinkswitch import DlinkSwitch
from telnetlib import Telnet
# from time import sleep


class DGS110011ME(DlinkSwitch):

    def __init__(self,
                 custom_ip_address,
                 mgm_vlan,
                 user_vlan,
                 user,
                 password,
                 snmp_community):
        super().__init__(custom_ip_address, mgm_vlan)
        self.mgm_vlan = mgm_vlan
        self.user_vlan = user_vlan
        self.user_name = user
        self.password = password
        self.snmp_community = snmp_community

    input_wait_string = b'DGS-1100-10/ME:5# '

    def __make_instruction(self, instruction):
        self.conn_t.write(instruction.encode('ascii') + b'\n\r')
        self.conn_t.read_until(self.input_wait_string)

    def upgrade_firmware(self):
        # self.__make_instruction('download firmware_fromTFTP 10.90.90.91 DGS110010MEV101B087FW\n\ry')
        self.conn_t.write(b'download firmware_fromTFTP 10.90.90.91 DGS110010MEV101B087FW\n\ry\n\r')
        self.conn_t.read_until(b"DGS-1100-10/ME:5# ")

    def configure_switch(self):
        pass

    def connect(self):
        conn_t = Telnet(self.default_ip)
        conn_t.set_debuglevel(1)
        conn_t.read_until(b"login:")
        conn_t.write(self.user_name.encode('ascii') + b"\n")
        conn_t.read_until(b"Password:")
        conn_t.write(self.password.encode('ascii') + b"\n")
        conn_t.read_until(b"DGS-1100-10/ME:5# ")
        self.conn_t = conn_t

    def reboot(self):
        self.conn_t.write(b'reboot force_agree\n\r')
        self.conn_t.read_until(b"DGS-1100-10/ME:5# ", 5)

    def save(self):
        self.conn_t.write(b'save config\n\r')
        self.conn_t.read_until(b"DGS-1100-10/ME:5# ", 5)

    def configure_ip_address(self):

        """
            Create management VLAN on the switch, configure management VLAN and set custom ip address
        """

        self.conn_t.write(b'create vlan mgm_' + self.mgm_vlan + b' tag ' + self.mgm_vlan + b'\n\r')
        self.conn_t.read_until(b"DGS-1100-10/ME:5# ", 5)
        self.conn_t.write(b'config vlan mgm_' + self.mgm_vlan + b' add tagged 9-10\n\r')
        self.conn_t.read_until(b"DGS-1100-10/ME:5# ", 5)
        self.conn_t.write(b'delete iproute default\n\r')
        self.conn_t.read_until(b"DGS-1100-10/ME:5# ", 5)
        self.conn_t.write(b'create iproute default ' + self.default_ip_gateway + b'\n\r')
        self.conn_t.read_until(b"DGS-1100-10/ME:5# ", 5)
        self.conn_t.write(b'config ipif System ipaddress ' + self.custom_ip_address + b'/' +
                          self.ip_mask + b' vlan mgm_' + self.mgm_vlan + b'\n\r')
        self.conn_t.read_until(b"DGS-1100-10/ME:5# ", 5)

    def configure_account(self):
        pass
