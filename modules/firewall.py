from core.api import api_call

def reload(base_url, auth, proxies, debug=False):
    return api_call('POST', f"{base_url}/firewall/filter_base/apply", auth, proxies, debug=debug)
