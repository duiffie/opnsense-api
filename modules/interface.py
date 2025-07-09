from core.api import api_call
import sys
import json

def list_interfaces(base_url, auth, proxies, debug=False):
    return api_call('GET', f"{base_url}/interfaces/overview/interfaces_info", auth, proxies, debug=debug)
