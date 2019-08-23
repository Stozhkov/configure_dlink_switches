import pymysql
import os
from configparser import ConfigParser


class NetworkBase:
    def __init__(self):
        try:
            config = ConfigParser()
            config.read(os.path.dirname(os.path.realpath(__file__)) + '/' + 'config.cfg')
            db_host = config.get('database', 'host')
            db_user_name = config.get('database', 'user')
            db_password = config.get('database', 'password')
            db_name = config.get('database', 'db')
        except Exception as e:
            print(str(e), ' could not read configuration file')
            exit(0)

        try:
            db = pymysql.connect(host=db_host,
                                 user=db_user_name,
                                 password=db_password,
                                 db=db_name)
            self.cursor = db.cursor()
        except Exception as e:
            print(str(e))
            exit(0)

    def get_next_ip_address(self, mgm_vlan):

        """
            Get next available ip address in the management network

        :param mgm_vlan: Int. VLAN of the management network
        :return: String. IP address
        """

        ip_address = ''

        if mgm_vlan == 1:
            sql = 'SELECT `ip` FROM `devices` WHERE `ip` LIKE \'10.0.%\' ORDER BY INET_ATON(`ip`) DESC LIMIT 1'
        else:
            sql = 'SELECT `ip` FROM `devices` WHERE `ip` LIKE \'10.1.' + str(mgm_vlan) + \
                  '%\' ORDER BY INET_ATON(`ip`) DESC LIMIT 1'

        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(str(e))
            exit(0)

        try:
            ip_address = str(list(self.cursor.fetchone())[0]).split('.')
        except TypeError:
            print('In the management VLAN ' + mgm_vlan + ' not found any switches')
            exit(0)

        next_ip_address = ip_address[0] + '.' + ip_address[1] + '.' + ip_address[2] + '.' + str(int(ip_address[3]) + 1)
        return next_ip_address

    def get_username(self):

        """
            Get default username from "Network"

        :return: IP address
        """

        sql = 'SELECT `value` FROM `default_values` WHERE `name` = \'default.access.username\''

        try:
            self.cursor.execute(sql)
            username = self.cursor.fetchone()[0]
        except Exception as e:
            print(str(e))
            exit(0)
        else:
            return username

    def get_password(self):

        """
            Get default password from "Network"

        :return: Password
        """

        sql = 'SELECT `value` FROM `default_values` WHERE `name` = \'default.access.password\''

        try:
            self.cursor.execute(sql)
            password = self.cursor.fetchone()[0]
        except Exception as e:
            print(str(e))
            exit(0)
        else:
            return password

    def get_ro_snmp_community(self):

        """
            Return default read only SNMP community name from "Network"

        :return: Read only SNMP community name
        """

        sql = 'SELECT `value` FROM `default_values` WHERE `name` = \'default.snmp.read\''

        try:
            self.cursor.execute(sql)
            ro_snmp_community = self.cursor.fetchone()[0]
        except Exception as e:
            print(str(e))
            exit(0)
        else:
            return ro_snmp_community

    def get_rw_snmp_community(self):

        """
            Return default read and write SNMP community from "Network"

        :return: Read and write SNMP community name
        """

        sql = 'SELECT `value` FROM `default_values` WHERE `name` = \'default.snmp.write\''

        try:
            self.cursor.execute(sql)
            rw_snmp_community = self.cursor.fetchone()[0]
        except Exception as e:
            print(str(e))
            exit(0)
        else:
            return rw_snmp_community
