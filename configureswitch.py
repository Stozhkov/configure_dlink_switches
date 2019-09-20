#!/usr/bin/env python3

from des3200reva18 import DES3200RevA18
from des3200revc18 import DES3200RevC18
from des3200reva26 import DES3200RevA26
from des3200revc26 import DES3200RevC26
from des3200reva28 import DES3200RevA28
from des3200revc28 import DES3200RevC28
from des3200revc52 import DES3200RevC52
from dgs110010me import DGS110010me
from network import NetworkBase
from terminal import Terminal
from time import sleep


def print_info():
    print()
    print('Parameters for configuring')
    print('{:.<20} {:<15}'.format('IP address', ip_address))
    print('{:.<20} {:<15}'.format('Management VLAN', mgm_vlan))
    print('{:.<20} {:<15}'.format('Users VLAN', user_vlan))
    print('{:.<20} {:<15}'.format('Username', username))
    print('{:.<20} {:<15}'.format('Password', password))
    print('{:.<20} {:<15}'.format('SNMP ro community', ro_snmp_community))
    print('{:.<20} {:<15}'.format('SNMP rw community', rw_snmp_community))
    print()


try:
    print('\nThe script will configure the switch d-link with received parameters.')
    print('All that you need is specify management and users VLAN\'s and choice a model.\n')

    network = NetworkBase()

    mgm_vlan = Terminal.get_from_user_management_vlan()
    user_vlan = Terminal.get_from_user_users_vlan()

    if mgm_vlan == user_vlan:
        print('Management VLAN and user VLAN can not be the same!')
        exit(0)

    ip_address = Terminal.get_from_user_ip_address() or network.get_next_ip_address(mgm_vlan)

    username = network.get_username()
    password = network.get_password()
    ro_snmp_community = network.get_ro_snmp_community()
    rw_snmp_community = network.get_rw_snmp_community()

    print('\nChoice the model of switch that we will configure.\n')
    print('List of available models:')
    print('1. DES-3200-18 rev. A or B')
    print('2. DES-3200-26 rev. A or B')
    print('3. DES-3200-28 rev. A or B')
    print('4. DES-3200-18 rev. C')
    print('5. DES-3200-26 rev. C')
    print('6. DES-3200-28 rev. C')
    print('7. DES-3200-52 rev. C')
    print('8. DGS-1100-10ME')

    choice = 0

    try:
        choice = int(input('Your choice: '))
    except ValueError:
        print('Choices not available madel of switch')
        exit(0)

    if choice == 1:
        switch = DES3200RevA18(ip_address, mgm_vlan, user_vlan, username, password, ro_snmp_community, rw_snmp_community)
    elif choice == 2:
        switch = DES3200RevA26(ip_address, mgm_vlan, user_vlan, username, password, ro_snmp_community, rw_snmp_community)
    elif choice == 3:
        switch = DES3200RevA28(ip_address, mgm_vlan, user_vlan, username, password, ro_snmp_community, rw_snmp_community)
    elif choice == 4:
        switch = DES3200RevC18(ip_address, mgm_vlan, user_vlan, username, password, ro_snmp_community, rw_snmp_community)
    elif choice == 5:
        switch = DES3200RevC26(ip_address, mgm_vlan, user_vlan, username, password, ro_snmp_community, rw_snmp_community)
    elif choice == 6:
        switch = DES3200RevC28(ip_address, mgm_vlan, user_vlan, username, password, ro_snmp_community, rw_snmp_community)
    elif choice == 7:
        switch = DES3200RevC52(ip_address, mgm_vlan, user_vlan, username, password, ro_snmp_community, rw_snmp_community)
    elif choice == 8:
        switch = DGS110010me(ip_address, mgm_vlan, user_vlan, username, password, ro_snmp_community, rw_snmp_community)
    else:
        exit(0)

    print_info()

    print('Start configuring\n')

    if switch.check_ping_default_ip():
        switch.connect(ip='default')
        switch.upgrade_firmware()
        switch.reboot()
        switch.hard_disconnect()
        sleep(5)
        switch.wait_after_reboot(switch.default_ip)

        switch.connect(ip='default')
        switch.configure_mgm_vlan()
        switch.configure_ip_address()
        switch.hard_disconnect()
    else:
        print('Currently not available switch with default ip.')
        exit(0)

    sleep(5)

    if switch.check_ping_custom_ip():
        switch.connect(ip='custom')
        switch.configure_syslog()
        switch.configure_ssh()
        switch.configure_telnet()
        switch.configure_lbd()
        switch.configure_safeguard()
        switch.configure_dhcp_filter()
        switch.configure_traffic_control()
        switch.configure_time_zone()
        switch.configure_traffic_segmentation()
        switch.configure_trusted_host()
        switch.configure_snmp()
        switch.configure_account()
        switch.configure_users_vlan()
        switch.delete_default_vlan()
        switch.save()
        switch.disconnect()
    else:
        print('Currently not available switch with ip', switch.custom_ip_address)
        exit(0)

    print('\nConfiguring is done.')
    print_info()
except KeyboardInterrupt:
    print('\n\nProgram was closed by user command.')
