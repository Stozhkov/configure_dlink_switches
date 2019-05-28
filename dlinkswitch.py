from os import system
from abc import abstractmethod
from telnetlib import Telnet
from time import sleep
from terminal import Terminal
import socket


class DlinkSwitch:
    default_ip = '10.90.90.90'
    default_user = ''
    default_password = ''
    default_ip_gateway = ''

    def __init__(self, custom_ip_address, mgm_vlan):
        self.custom_ip_address = custom_ip_address

        if int(mgm_vlan) == int(1):
            self.default_ip_gateway = '10.0.2.250'
            self.ip_mask = '22'
        else:
            self.default_ip_gateway = str(custom_ip_address).split('.')[0:3]
            self.default_ip_gateway.append('10')
            self.default_ip_gateway = '.'.join(self.default_ip_gateway)
            self.ip_mask = '24'

        self.conn_t = Telnet()

    def __del__(self):
        self.conn_t.close()

    @staticmethod
    def __check_ping(ip_address):

        """
            Check of available ip address with ping command

        :param ip_address: ip address switch
        :return: True or False
        """

        response = system('ping -c 4 ' + ip_address + '  >/dev/null 2>&1')

        if response == 0:
            return True
        else:
            return False

    def check_ping_custom_ip(self):

        """
            Check of available custom ip address with ping command
        """

        return DlinkSwitch.__check_ping(self.custom_ip_address)

    def check_ping_default_ip(self):

        """
            Check of available default ip address with ping command
        """

        return DlinkSwitch.__check_ping(self.default_ip)

    def wait_after_reboot(self, ip_address):

        """
            Wait while the ip_address is not will be available

        :param ip_address: which ip_address we will be wait
        :return: return True when ip_address is available
        """

        while not self.__check_ping(ip_address):
            Terminal.print_terminal('reboot', 'wait')
            sleep(5)

        Terminal.print_terminal('reboot', 'Success')
        return True

    @abstractmethod
    def upgrade_firmware(self):
        pass

    @abstractmethod
    def configure_syslog(self):
        pass

    @abstractmethod
    def configure_ssh(self):
        pass

    @abstractmethod
    def configure_telnet(self):
        pass

    @abstractmethod
    def configure_lbd(self):
        pass

    @abstractmethod
    def configure_safeguard(self):
        pass

    @abstractmethod
    def configure_dhcp_filter(self):
        pass

    @abstractmethod
    def configure_traffic_control(self):
        pass

    @abstractmethod
    def configure_time_zone(self):
        pass

    @abstractmethod
    def configure_traffic_segmentation(self):
        pass

    @abstractmethod
    def configure_trusted_host(self):
        pass

    @abstractmethod
    def configure_snmp(self):
        pass

    @abstractmethod
    def configure_ip_address(self):
        pass

    @abstractmethod
    def configure_mgm_vlan(self):
        pass

    @abstractmethod
    def configure_users_vlan(self):
        pass

    @abstractmethod
    def delete_default_vlan(self):
        pass

    @abstractmethod
    def configure_account(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def reboot(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
