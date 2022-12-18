# https://api.bbox.fr/doc/apirouter/index.html

import json
from . import api


def init_parameter(api_name, method_type):
    apis = myBbox.get_map()
    var = dict()
    for api in apis['apis']:
        if api['api'] == api_name and api['method'] == method_type:
            for param in api['params']:
                name = param['name']
                if param['type'] == 'number':
                    value = 0
                else:
                    value = ''
                var[name] = value
    return var


class Bbox(api.Api):
    _bbox_session = 0

    def __init__(self, password=None):
        super().__init__()
        if self._bbox_session == 0:
            self.login(password)
        else:
            self.refresh_login()
        self._bbox_session += 1

    def __del__(self):
        self._bbox_session -= 1
        if self._bbox_session == 0:
            self.logout()

    def get_host_id(self, name):
        hosts_list = self.get_lan_all_connected_devices_lite()
        for host in hosts_list['hosts']['list']:
            if host['hostname'] == name:
                host_id = str(host['id'])
                break
        else:
            host_id = ''
        return host_id

    def host_wakeup(self, name):
        host_id = self.get_host_id(name)
        self.host_command(host_id, 'wakeup')

    def host_ping(self, name):
        host_id = self.get_host_id(name)
        self.host_command(host_id, 'ping')

    def list_active_host(self, host_parameters=['hostname']):
        host_list = list()
        hosts = self.get_lan_all_connected_devices()
        for host in hosts['hosts']['list']:
            if host['active'] == 1:
                host_list.append(host)
        return host_list

    def is_host_active(self, name):
        host_list = list()
        hosts = self.get_lan_all_connected_devices()
        for host in hosts['hosts']['list']:
            if (host['hostname'] == name) and (host['active'] == 1):
                return True
        return False

    def list_call_log(self):
        call_log = self.get_full_call_log()
        return call_log[0]['calllog']


if __name__ == "__main__":
    with open('../secret.json', 'r') as secret_file:
        secret = json.load(secret_file)

    myBbox = Bbox(secret['bbox'])


    def test_service(info):
        print(json.dumps(info, indent=2, sort_keys=True))


    apis = myBbox.get_map()
    with open('../api.txt', 'w') as f:
        f.write(json.dumps(apis, indent=2, sort_keys=True))

    # myBbox.host_wakeup("geremy-OptiPlex-360")
    # myBbox.host_ping("geremy-OptiPlex-360")

    test_service(myBbox.get_wan_stats())
    test_service(myBbox.get_device())
    test_service(myBbox.get_device_summary())
    test_service(myBbox.get_log())

    test_service(myBbox.get_lan_all_connected_devices())
    test_service(myBbox.get_lan_all_connected_devices_lite())

    test_service(myBbox.get_voice_mail_list())
    test_service(myBbox.get_full_call_log())
    test_service(myBbox.get_voip_diag())

    test_service(myBbox.get_dns_stats())
    test_service(myBbox.refresh_login())

    test_service(myBbox.get_wireless_repeater())

    token = myBbox.get_token()
    print(token)

    test_service(myBbox.get_firewall_rules())
    test_service(myBbox.get_nat_rules())

    myBbox.logout()
