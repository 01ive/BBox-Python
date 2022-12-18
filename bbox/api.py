import json
import requests
from . import error

# Patch to make it work under Linux (SSL weakness of the password)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

class Api:
    _session = None

    def _exception_handler(func):
        def inner_function(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
            except:
                raise error.Error('Communication problem with Bbox')
        return inner_function

    def _request_get(self, url):
        self._response = self._session.get(self.base_url + url)
        if self._response.status_code != 200:
            print(self._response)
            raise error.Error('Communication problem with Bbox')

    @_exception_handler
    def _request_post(self, url, data=None, token=False):
        token_string = ''
        if token:
            token_string = self.get_token()
            token_string = '?btoken=' + token_string
        self._response = self._session.post(self.base_url + url + token_string, data=data)
        if self._response.status_code != 200:
            print(self._response)
            raise error.Error('Communication problem with Bbox')

    def _request_put(self, url, data=None):
        self._response = self._session.put(self.base_url + url, data=data)
        if self._response.status_code != 200:
            print(self._response)
            raise error.Error('Communication problem with Bbox')

    def __init__(self):
        self.base_url = 'https://mabbox.bytel.fr/api/'
        self._response = None
        self._token = None

    def login(self, password):
        self._session = requests.Session()
        self._request_post('v1/login', {'password': password, 'remember': 0})

    def logout(self):
        self._request_post('v1/logout')

    def refresh_login(self):
        self._request_put('v1/login')

    def get_map(self):
        self._request_get('v1/map')
        data = json.loads(self._response.text)
        return data[0]

    def get_device(self):
        self._request_get('v1/device')
        data = json.loads(self._response.text)
        return data[0]

    def get_device_summary(self):
        self._request_get('v1/device/summary')
        data = json.loads(self._response.text)
        return data[0]

    def get_log(self):
        self._request_get('v1/device/log')
        data = json.loads(self._response.text)
        return data[0]

    def get_wan_stats(self):
        self._request_get('v1/wan/ip/stats')
        data = json.loads(self._response.text)
        return data[0]['wan']['ip']['stats']

    def get_lan_all_connected_devices(self):
        self._request_get('v1/hosts')
        data = json.loads(self._response.text)
        return data[0]

    def get_lan_all_connected_devices_lite(self):
        self._request_get('v1/hosts/lite')
        data = json.loads(self._response.text)
        return data[0]

    def host_command(self, host_id, command):
        self._request_post('v1/hosts/' + host_id, data={'action': command}, token=True)

    def get_token(self):
        self._request_get('v1/device/token')
        data = json.loads(self._response.text)
        self._token = data[0]['device']['token']
        return self._token

    def get_voice_mail_list(self):
        self._request_get('v1/voip/calllog/1')
        data = json.loads(self._response.text)
        return data

    def get_full_call_log(self):
        self._request_get('v1/voip/fullcalllog/1')
        data = json.loads(self._response.text)
        return data

    def get_voip_diag(self):
        self._request_get('v1/voip/diag')
        data = json.loads(self._response.text)
        return data

    def dial_number(self, number):
        self._request_post('v1/voip/dial/1', data={'number': number}, token=True)

    def ring_test(self):
        self._request_put('v1/voip/ringtest', data={'enable': 1})

    def get_dns_stats(self):
        self._request_get('v1/dns/stats')
        data = json.loads(self._response.text)
        return data

    def get_wireless_repeater(self):
        self._request_get('v1/wireless/repeater')
        data = json.loads(self._response.text)
        return data

    def get_firewall_rules(self):
        self._request_get('v1/firewall/rules')
        data = json.loads(self._response.text)
        return data

    def get_nat_rules(self):
        self._request_get('v1/nat/rules')
        data = json.loads(self._response.text)
        return data

    def put_nat_rules_id(self, nat_rule):
        self._request_put('v1/nat/rules' + str(nat_rule.id), data)
        data = json.loads(self._response.text)
        return data
