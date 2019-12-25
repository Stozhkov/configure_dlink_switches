from dlinkswitch import DlinkSwitch
from telnetlib import Telnet
from time import sleep
from terminal import Terminal
from abc import abstractmethod
from configparser import ConfigParser
import os


class DGS1210(DlinkSwitch):

    def __init__(self, parameters):
        super().__init__(parameters['custom_ip_address'], str(parameters['mgm_vlan']))
        self.mgm_vlan = str(parameters['mgm_vlan'])
        self.user_vlan = str(parameters['user_vlan'])
        self.user_name = parameters['user']
        self.password = parameters['password']
        self.ro_snmp_community = parameters['ro_snmp_community']
        self.rw_snmp_community = parameters['rw_snmp_community']

        try:
            config = ConfigParser()
            config.read(os.path.dirname(os.path.realpath(__file__)) + '/' + 'config.cfg')
            self.__server_ip = config.get('tftp', 'server_ip')
        except Exception as e:
            print(str(e), ' could not read configuration file')
            exit(0)

    @property
    @abstractmethod
    def input_wait_string(self):
        pass

    def make_instruction(self, instruction, not_wait=None):

        """
            Make the telnet command.

        :param instruction: The telnet command
        :param not_wait: It is a marker for waiting a response from switch/ Use then command return nothing.
        Be careful and do not use this marker with command like upgrade or download something!!!)
        :return: Nothing
        """

        self.conn_t.write(instruction.encode('ascii') + b'\n')
        if not_wait:
            Terminal.print_terminal(instruction, 'None')
            sleep(2)
        else:
            result = self.conn_t.read_until(self.input_wait_string)

            if int(str(result).find('Success')) != int('-1') or int(str(result).find('Done')) != int('-1'):
                Terminal.print_terminal(instruction, 'Success.')
            else:
                Terminal.print_terminal(instruction, 'Failure!')

    def upgrade_firmware(self):

        """
            Upgrade firmware

        :return: Nothing
        """
        # Now on the official support do not have more new firmware.

        print('Upgrade firmware')
        print('Now on the official support do not have more new firmware.')
        # print('  WARNING !!!')
        # print('  Do not power off the switch while firmware is upgrading.')
        # print('  Do not kill the process like "Ctrl + C".')
        # print('  It will damage the switch.')
        # print('  Wait success result!')
        # self.make_instruction('download firmware_fromTFTP ' + self.__server_ip + ' DGS110010MEV101B087FW\n\ry\n\r')

    def configure_syslog(self):

        """
            Configure syslog function

        :return: Nothing
        """

        print('Configure Syslog')
        self.make_instruction('enable syslog')
        self.make_instruction('create syslog host 1 ipaddress 10.0.2.45 udp_port 514 '
                              'severity all facility local0 state enable')

    def configure_ssh(self):

        """
            Configure SSH

        :return: Nothing
        """

        print('Configure SSH')
        self.make_instruction('enable ssh')

    def configure_telnet(self):

        """
            Configure Telnet

        :return: Nothing
        """

        print('Configure Telnet')
        self.make_instruction('enable telnet')

    def configure_safeguard(self):

        """
            Configure safeguard engine

        :return: Nothing
        """

        print('Configure safeguard engine')
        self.make_instruction('config safeguard_engine state enable')

    def configure_time_zone(self):

        """
            Configure time zone and SNTP client

        :return: Nothing
        """

        print('Configure Time zone')
        self.make_instruction('config time_zone operator + hour 3 min 0')
        self.make_instruction('config sntp primary 10.0.2.45')
        self.make_instruction('config sntp secondary 10.0.2.46')
        self.make_instruction('config sntp poll-interval 43200')
        self.make_instruction('enable sntp')

    def configure_trusted_host(self):

        """
            Configure trusted host

        :return: Nothing
        """

        print('Configure Trusted host')
        self.make_instruction('create trusted_host network 10.0.0.0/8')
        self.make_instruction('create trusted_host network 192.168.16.0/24')
        self.make_instruction('create trusted_host network 10.1.0.0/16')
        self.make_instruction('create trusted_host network 10.0.0.0/16')
        self.make_instruction('create trusted_host network 10.128.227.0/24')
        self.make_instruction('delete trusted_host network 10.0.0.0/8')

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
        self.make_instruction('create snmp view ReadWrite 1 view_type included')
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
        # conn_t.set_debuglevel(1)
        conn_t = Telnet(ip_address)
        conn_t.read_until(b"login:")
        conn_t.write(self.user_name.encode('ascii') + b"\n")
        conn_t.read_until(b"Password:")
        conn_t.write(self.password.encode('ascii') + b"\n")
        conn_t.read_until(self.input_wait_string)
        self.conn_t = conn_t
        Terminal.print_terminal('connect to ' + ip_address, 'Success.')

    def disconnect(self):

        """
            Disconnect with the switch (Make command 'logout'), and then close telnet connection

        :return: Nothing
        """

        print('Disconnect switch')
        self.make_instruction('logout', not_wait=True)
        self.conn_t.close()

    def hard_disconnect(self):

        """
            Close telnet connection without making command 'logout' (Need then reboot and change ip command)

        :return: Nothing
        """

        self.conn_t.close()

    def reboot(self):

        """
            Reboot switch

        :return: Nothing
        """

        print('Reboot switch')
        self.make_instruction('reboot force_agree', not_wait=True)

    def save(self):

        """
            Save configuration

        :return:
        """

        print('Save config')
        self.make_instruction('save')

    def configure_account(self):

        """
            Configure admin account

        :return: Nothing
        """

        print('Configure Admin account')
        self.conn_t.write(b'create account admin ' + self.user_name.encode('ascii') + b'\n')
        self.conn_t.read_until(b'Enter a case-sensitive new password:')
        self.conn_t.write(self.password.encode('ascii') + b'\n')
        self.conn_t.read_until(b'Enter the new password again for confirmation:')
        self.conn_t.write(self.password.encode('ascii') + b'\n')
        result = self.conn_t.read_until(self.input_wait_string)

        instruction = 'create account admin ' + self.user_name

        if int(str(result).find('Success')) != int('-1'):
            Terminal.print_terminal(instruction, 'Success.')
        else:
            Terminal.print_terminal(instruction, 'Fault')

    @abstractmethod
    def configure_users_vlan(self):
        pass

    @abstractmethod
    def configure_mgm_vlan(self):
        pass

    @abstractmethod
    def delete_default_vlan(self):
        pass

    @abstractmethod
    def configure_ip_address(self):
        pass

    @abstractmethod
    def configure_traffic_segmentation(self):
        pass

    @abstractmethod
    def configure_dhcp_filter(self):
        pass

    @abstractmethod
    def configure_traffic_control(self):
        pass

    @abstractmethod
    def configure_lbd(self):
        pass
