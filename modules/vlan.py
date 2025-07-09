from core.api import api_call
import sys
import json

def list_vlans(base_url, auth, proxies, debug=False):
    return api_call('GET', f"{base_url}/interfaces/vlan_settings/search_item", auth, proxies, debug=debug)

def get_uuid_by_tag(base_url, auth, proxies, tag, debug=False):
    vlans = list_vlans(base_url, auth, proxies, debug).get('rows', [])
    for v in vlans:
        if str(v.get('tag')) == str(tag):
            return v.get('uuid')
    print(json.dumps({"error": "VLAN niet gevonden", "tag": tag}), file=sys.stderr)
    sys.exit(1)


def add(base_url, auth, proxies, tag, parent_interface, descr, enabled, debug=False):
    data = {
        "vlan": {
            "enabled": "1" if enabled else "0",
            "tag": str(tag),
            "if": parent_interface,
            "descr": descr
        }
    }
    return api_call('POST', f"{base_url}/interfaces/vlan_settings/addItem", auth, proxies, data, debug)

def update(base_url, auth, proxies, uuid, tag=None, parent_interface=None, descr=None, enabled=None, debug=False):
    data = {"vlan": {}}
    if tag is not None: data['vlan']['tag'] = str(tag)
    if parent_interface: data['vlan']['if'] = parent_interface
    if descr is not None: data['vlan']['descr'] = descr
    if enabled is not None: data['vlan']['enabled'] = "1" if enabled else "0"
    return api_call('POST', f"{base_url}/interfaces/vlan_settings/set_item/{uuid}", auth, proxies, data, debug)

def delete(base_url, auth, proxies, uuid, debug=False):
    return api_call('POST', f"{base_url}/interfaces/vlan_settings/del_item/{uuid}", auth, proxies, debug=debug)
