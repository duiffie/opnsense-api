from core.api import api_call
import sys
import json

def list_vlans(base_url, auth, proxies, debug=False):
    return api_call('GET', f"{base_url}/interfaces/vlan_settings/search_item", auth, proxies, debug=debug)
