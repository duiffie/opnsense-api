import configparser
import sys
import ipaddress
import json
import os
from requests.auth import HTTPBasicAuth

def load_config(path):
    if not os.path.exists(path):
        print(f"❌ Fout: Configuratiebestand niet gevonden in path: {path}")
        print("   Gebruik --config om een alternatief pad op te geven, of plaats het bestand op de standaardlocatie.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(path)
    try:
        base_url = config['api']['base_url'].rstrip('/')
        auth = HTTPBasicAuth(config['api']['key'], config['api']['secret'])
    except KeyError as e:
        print(json.dumps({"error": f"Ontbrekende configuratieparameter: {e}"}), file=sys.stderr)
        sys.exit(1)

    proxies = None
    if 'proxy' in config:
        proxies = {k: v for k, v in config.items('proxy') if v}
        if not proxies:
            proxies = None

    return base_url, auth, proxies

def validate_subnet(subnet_str):
    try:
        ipaddress.ip_network(subnet_str)
    except ValueError as e:
        print(json.dumps({"error": "Ongeldig subnet", "details": str(e)}), file=sys.stderr)
        sys.exit(1)
