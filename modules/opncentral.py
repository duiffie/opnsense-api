from core.api import api_call
import sys
import json

def list_devices(base_url, auth, proxies, debug=False):
    return api_call('GET', f"{base_url}/opncentral/host_provisioning/list_devices", auth, proxies, debug=debug)

def reconfigure(base_url, auth, proxies, debug=False):
    devices = list_devices(base_url, auth, proxies, debug)
    data = {"hosts": {}}
    for index, item in enumerate(devices):
        data["hosts"][index] = item["id"]
    return api_call('POST', f"{base_url}/opncentral/host_provisioning/reconfigure", auth, proxies, data, debug=debug)
