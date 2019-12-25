from dgs1210 import DGS1210


class DGS121028fl1a(DGS1210):

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

    input_wait_string = b'DGS-1210-28:5#'

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
