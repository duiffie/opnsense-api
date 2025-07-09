from core.api import api_call
import sys
import json

def list(base_url, auth, proxies, debug=False):
    return api_call('GET', f"{base_url}/firewall/alias/search_item", auth, proxies, debug=debug)

def get_uuid_by_name(base_url, auth, proxies, name, debug=False):
    aliases = list(base_url, auth, proxies, debug).get('rows', [])
    for a in aliases:
        if a['name'] == name:
            return a['uuid']
    print(json.dumps({"error": "Alias niet gevonden", "name": name}), file=sys.stderr)
    sys.exit(1)

def add(base_url, auth, proxies, name, type_, content, desc, enabled, debug=False):
    data = {
        "alias": {
            "enabled": "1" if enabled else "0",
            "name": name,
            "type": type_,
            "content": content,
            "description": desc
        }
    }
    return api_call('POST', f"{base_url}/firewall/alias/addItem", auth, proxies, data, debug)

def update(base_url, auth, proxies, uuid, name=None, type_=None, content=None, description=None, enabled=None, debug=False):
    data = {"alias": {}}
    if name: data["alias"]["name"] = name
    if type_: data["alias"]["type"] = type_
    if content: data["alias"]["content"] = content
    if description is not None: data["alias"]["description"] = description
    if enabled is not None: data["alias"]["enabled"] = "1" if enabled else "0"
    return api_call('POST', f"{base_url}/firewall/alias/set_item/{uuid}", auth, proxies, data, debug)

def delete(base_url, auth, proxies, uuid, debug=False):
    return api_call('POST', f"{base_url}/firewall/alias/del_item/{uuid}", auth, proxies, debug=debug)
