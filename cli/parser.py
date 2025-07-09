import argparse
import os
import sys
from core.utils import str2bool

def create_parser():
    home_config_path = os.path.expanduser('~/.opnsense-api.ini')

    p = argparse.ArgumentParser(description="OPNsense API-tool voor aliassen en VIP’s")
    p.add_argument('--config', default=home_config_path, help=f"Pad naar configuratiebestand (standaard: {home_config_path})")
    p.add_argument('--debug', action='store_true', help="Toon debug-output (API-aanroepen en responses)")
    p.add_argument('--no-reload', action='store_true', help="Voorkom automatisch herladen firewall na wijziging")
    sp = p.add_subparsers(dest='cmd', required=True)

    # Aliassen
    pl = sp.add_parser('list-alias')
    pl.add_argument('--name', help="Filter op aliasnaam")

    pa = sp.add_parser('add-alias')
    pa.add_argument('--name', required=True)
    pa.add_argument('--type', required=True, choices=['host', 'network', 'port', 'urltable', 'geoip'])
    pa.add_argument('--content', required=True, nargs='+', help="Meerdere waarden toegestaan, gescheiden door spatie")
    pa.add_argument('--descr', default='')
    pa.add_argument('--enabled', action='store_true')

    pu = sp.add_parser('update-alias')
    pu.add_argument('--uuid')
    pu.add_argument('--search-name')
    pu.add_argument('--name')
    pu.add_argument('--type', choices=['host', 'network', 'port', 'urltable', 'geoip'])
    pu.add_argument('--content', nargs='+', help="Meerdere waarden toegestaan, gescheiden door spatie")
    pu.add_argument('--descr')
    pu.add_argument('--enabled', type=str2bool, help="true of false")

    pd = sp.add_parser('delete-alias')
    pd.add_argument('--uuid')
    pd.add_argument('--search-name')

    # Interfaces
    pi = sp.add_parser('list-interfaces')
    pi.add_argument('--name', help="Filter Interface op naam (descr)")

    # Vlans
    plvl = sp.add_parser('list-vlan')
    plvl.add_argument('--tag', help="Filter Vlan op tag")

    # VIPs
    plv = sp.add_parser('list-vip')
    plv.add_argument('--name', help="Filter VIP op naam (descr)")

    pv = sp.add_parser('add-vip')
    pv.add_argument('--type', required=True, choices=['ipalias'])
    pv.add_argument('--subnet', required=True)
    pv.add_argument('--interface', required=True)
    pv.add_argument('--descr', default='')
    pv.add_argument('--enabled', action='store_true')

    return p
