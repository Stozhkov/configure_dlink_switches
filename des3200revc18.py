from des3200revc import DES3200RevC


class DES3200RevC18(DES3200RevC):

    def __init__(self,
                 custom_ip_address,
                 mgm_vlan,
                 user_vlan,
                 user,
                 password,
                 ro_snmp_community,
                 rw_snmp_community):
        super().__init__(custom_ip_address,
                         mgm_vlan,
                         user_vlan,
                         user,
                         password,
                         ro_snmp_community,
                         rw_snmp_community)

    input_wait_string = b'DES-3200-18:admin#'

    def configure_lbd(self):

        """
            Configure Loopback detection

        :return: Nothing
        """

        print('Configure Loopback detection')
        self.make_instruction('enable loopdetect')
        self.make_instruction('config loopdetect recover_timer 60 interval 10 mode port-based')
        self.make_instruction('config loopdetect ports 1-16 state enable')

    def configure_dhcp_filter(self):

        """
            Configure DHCP filter

        :return: Nothing
        """

        print('Configure DHCP filter')
        self.make_instruction('config filter dhcp_server ports 1-16 state enable')
        self.make_instruction('config filter dhcp_server trap_log enable')
        self.make_instruction('config filter dhcp_server illegal_server_log_suppress_duration 30min')

    def configure_traffic_control(self):

        """
            Configure traffic control

        :return: Nothing
        """

        print('Configure Traffic control')
        self.make_instruction('config traffic trap both')
        self.make_instruction('config traffic control 1-16 broadcast enable')
        self.make_instruction('config traffic control 1-16 multicast enable')
        self.make_instruction('config traffic control 1-16 unicast enable')

    def configure_traffic_segmentation(self):

        """
            Configure traffic segmentation

        :return: Nothing
        """

        print('Configure Traffic segmentation')
        self.make_instruction('config traffic_segmentation 1-16 forward_list 17-18')
        self.make_instruction('config traffic_segmentation 17-18 forward_list 1-18')

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
            self.make_instruction('config vlan default delete 1-16')
            self.make_instruction('config vlan default add tagged 17-18')
        else:
            self.make_instruction('create vlan mgm_' + self.mgm_vlan + ' tag ' + self.mgm_vlan)
            self.make_instruction('config vlan mgm_' + self.mgm_vlan + ' add tagged 17-18')

    def configure_users_vlan(self):

        """
            Create users VLAN on the switch, configure users VLAN

        :return: Nothing
        """

        print('Configure users VLAN')
        self.make_instruction('create vlan vlan' + self.user_vlan + ' tag ' + self.user_vlan)
        self.make_instruction('config vlan vlan' + self.user_vlan + ' add tagged 17-18')
        self.make_instruction('config vlan vlan' + self.user_vlan + ' add untagged 1-16')

    def delete_default_vlan(self):

        """
            Delete default VLAN from switch if he will not use.

        :return: Nothing
        """

        if int(self.mgm_vlan) != int(1):
            print('Delete default VLAN')
            self.make_instruction('config vlan default delete 1-18')
