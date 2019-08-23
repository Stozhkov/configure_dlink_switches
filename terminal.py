from termcolor import colored
from abc import ABC
import re


class Terminal(ABC):

    @staticmethod
    def print_terminal(instruction, result):

        """
            Print in the terminal the result string with formatting

        :param instruction: The instruction which was executed
        :param result: Result of the executing (Success, Fault or something else)
        :return: Nothing
        """

        if result == 'Success':
            colour = 'green'
        elif result == 'Fault':
            colour = 'red'
        else:
            colour = 'yellow'

        instruction = re.sub("^\s+|\n|\r|\s+$", ' ', instruction)
        instruction = '  ' + instruction

        print('{:.<80}'.format(instruction[:78]), '[' + colored('{:^7}'.format(result), colour) + ']')

    @staticmethod
    def get_from_user_management_vlan():
        while True:
            try:
                mgm_vlan = int(input('Input management VLAN: '))
            except ValueError:
                print('VLAN is not a number')
            else:
                if 0 < int(mgm_vlan) < 4095:
                    return mgm_vlan
                else:
                    print('Vlan', mgm_vlan, 'can not exist!')

    @staticmethod
    def get_from_user_users_vlan():
        while True:
            try:
                user_vlan = int(input('Input users VLAN: '))
            except ValueError:
                print('VLAN is not a number')
            else:
                if 0 < int(user_vlan) < 4095:
                    return user_vlan
                else:
                    print('Vlan', user_vlan, 'can not exist!')

    @staticmethod
    def get_from_user_ip_address():
        while True:

            choice = 0

            print("\nDo you have IP address or you need new IP address?")
            print('1. I have IP address')
            print('2. I need new IP address')

            try:
                choice = int(input('Your choice 1 or 2: ') or 0)
            except ValueError:
                print('Choice is not legal')
                exit(0)

            if choice == 1:

                while True:
                    ip_address = input('Input IP address:')

                    if re.match('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
                                ip_address):
                        return ip_address
                    else:
                        print('IP address is not valid')

            elif choice == 2:
                return False
            else:
                print('Choice ' + str(choice) + ' is not legal')
