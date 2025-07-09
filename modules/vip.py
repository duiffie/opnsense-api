from core.api import api_call
from core.config import validate_subnet
import sys
import json

def list_vips(base_url, auth, proxies, debug=False):
    return api_call('GET', f"{base_url}/interfaces/vip_settings/search_item", auth, proxies, debug=debug)

def add(base_url, auth, proxies, type_, subnet, interface, descr, enabled, debug=False):
    validate_subnet(subnet)
    data = {
        "virtualip": {
            "enabled": "1" if enabled else "0",
            "mode": type_,
            "subnet": subnet,
            "interface": interface,
            "descr": descr
        }
    }
    return api_call('POST', f"{base_url}/firewall/virtualip/addVirtualIp", auth, proxies, data, debug)
