from core.api import api_call
import sys
import json

def list_interfaces(base_url, auth, proxies, debug=False):
    return api_call('GET', f"{base_url}/interfaces/get", auth, proxies, debug=debug)
