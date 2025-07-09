from core.api import api_call
from core.config import validate_subnet
import sys
import json

def list(base_url, auth, proxies, debug=False):
    return api_call('GET', f"{base_url}/interfaces/vip_settings/search_item", auth, proxies, debug=debug)

def get_uuid_by_descr(base_url, auth, proxies, descr, debug=False):
    vips = list(base_url, auth, proxies, debug).get('rows', [])
    for v in vips:
        if v.get('descr') == descr:
            return v.get('uuid')
    print(json.dumps({"error": "VIP niet gevonden", "descr": descr}), file=sys.stderr)
    sys.exit(1)

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
    return api_call('POST', f"{base_url}/interfaces/vip_settings/addItem", auth, proxies, data, debug)

def update(base_url, auth, proxies, uuid, type_=None, subnet=None, interface=None, descr=None, enabled=None, debug=False):
    data = {"virtualip": {}}
    if type_ is not None:
        data["virtualip"]["mode"] = type_
    if subnet is not None:
        validate_subnet(subnet)
        data["virtualip"]["subnet"] = subnet
    if interface is not None:
        data["virtualip"]["interface"] = interface
    if descr is not None:
        data["virtualip"]["descr"] = descr
    if enabled is not None:
        data["virtualip"]["enabled"] = "1" if enabled else "0"
    return api_call('POST', f"{base_url}/interfaces/vip_settings/set_item/{uuid}", auth, proxies, data, debug)

def delete(base_url, auth, proxies, uuid, debug=False):
    return api_call('POST', f"{base_url}/interfaces/vip_settings/del_item/{uuid}", auth, proxies, debug=debug)
