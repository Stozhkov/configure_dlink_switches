from dgs1100 import DGS1100


class DGS110010me(DGS1100):

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

    input_wait_string = b'DGS-1100-10/ME:5#'

    def configure_lbd(self):

        """
            Configure Loopback detection

        :return: Nothing
        """

        print('Configure Loopback detection')
        self.make_instruction('enable loopdetect')
        self.make_instruction('config loopdetect lbd_recover_time 60 interval_time 10')
        self.make_instruction('config loopdetect mode portbase')
        self.make_instruction('config loopdetect ports 1-8 state enable')

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
        self.make_instruction('config traffic control 1-8 broadcast enable')
        self.make_instruction('config traffic control 1-8 multicast enable')
        self.make_instruction('config traffic control 1 action drop threshold 64')
        self.make_instruction('config traffic control 2 action drop threshold 64')
        self.make_instruction('config traffic control 3 action drop threshold 64')
        self.make_instruction('config traffic control 4 action drop threshold 64')
        self.make_instruction('config traffic control 5 action drop threshold 64')
        self.make_instruction('config traffic control 6 action drop threshold 64')
        self.make_instruction('config traffic control 7 action drop threshold 64')
        self.make_instruction('config traffic control 8 action drop threshold 64')
        self.make_instruction('config traffic control 9 action drop')
        self.make_instruction('config traffic control 10 action drop')
        self.make_instruction('config traffic trap none')

    def configure_traffic_segmentation(self):

        """
            Configure traffic segmentation

        :return: Nothing
        """

        print('Configure Traffic segmentation')
        self.make_instruction('config traffic_segmentation 1-8 forward_list 9-10')
        self.make_instruction('config traffic_segmentation 9-10 forward_list 1-10')

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
            self.make_instruction('config vlan default delete 1-8')
            self.make_instruction('config vlan default add tagged 9-10')
        else:
            self.make_instruction('create vlan mgm_' + self.mgm_vlan + ' tag ' + self.mgm_vlan)
            self.make_instruction('config vlan mgm_' + self.mgm_vlan + ' add tagged 9-10')

    def configure_users_vlan(self):

        """
            Create users VLAN on the switch, configure users VLAN

        :return: Nothing
        """

        print('Configure users VLAN')
        self.make_instruction('create vlan vlan' + self.user_vlan + ' tag ' + self.user_vlan)
        self.make_instruction('config vlan vlan' + self.user_vlan + ' add tagged 9-10')
        self.make_instruction('config vlan vlan' + self.user_vlan + ' add untagged 1-8')

    def delete_default_vlan(self):

        """
            Delete default VLAN from switch if he will not use.

        :return: Nothing
        """

        if int(self.mgm_vlan) != int(1):
            print('Delete default VLAN')
            self.make_instruction('config vlan default delete 1-10')
