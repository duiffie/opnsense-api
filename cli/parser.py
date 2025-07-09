import argparse
import os
from core.utils import str2bool

def create_parser():
    home_config_path = os.path.expanduser('~/.opnsense-api.ini')

    parser = argparse.ArgumentParser(description="OPNsense API-tool")
    parser.add_argument('--config', default=home_config_path, help=f"Pad naar configuratiebestand (standaard: {home_config_path})")
    parser.add_argument('--debug', action='store_true', help="Toon debug-output (API-aanroepen en responses)")
    parser.add_argument('--no-reload', action='store_true', help="Voorkom automatisch herladen firewall na wijziging")

    subparsers = parser.add_subparsers(dest='cmd', required=True)

    # Alias subparsers
    alias_parser = subparsers.add_parser('alias', help='Beheer aliases')
    alias_subparsers = alias_parser.add_subparsers(dest='action', required=True, help='Actie voor alias')

    alias_list = alias_subparsers.add_parser('list', help='Toon lijst met aliases')
    alias_list.add_argument('--name', help="Filter op aliasnaam")

    alias_add = alias_subparsers.add_parser('add', help='Voeg alias toe')
    alias_add.add_argument('--name', required=True)
    alias_add.add_argument('--type', required=True, choices=['host', 'network', 'port', 'urltable', 'geoip'])
    alias_add.add_argument('--content', required=True, nargs='+', help="Meerdere waarden toegestaan, gescheiden door spatie")
    alias_add.add_argument('--descr', default='')
    alias_add.add_argument('--enabled', action='store_true')

    alias_update = alias_subparsers.add_parser('update', help='Update bestaande alias')
    alias_update.add_argument('--uuid')
    alias_update.add_argument('--search-name')
    alias_update.add_argument('--name')
    alias_update.add_argument('--type', choices=['host', 'network', 'port', 'urltable', 'geoip'])
    alias_update.add_argument('--content', nargs='+', help="Meerdere waarden toegestaan, gescheiden door spatie")
    alias_update.add_argument('--descr')
    alias_update.add_argument('--enabled', type=str2bool, help="true of false")

    alias_delete = alias_subparsers.add_parser('delete', help='Verwijder alias')
    alias_delete.add_argument('--uuid')
    alias_delete.add_argument('--search-name')

    # Interface subparsers
    interfaces_parser = subparsers.add_parser('interfaces', help='Beheer interfaces')
    interfaces_subparsers = interfaces_parser.add_subparsers(dest='action', required=True, help='Actie voor interfaces')

    interfaces_list = interfaces_subparsers.add_parser('list', help='Toon lijst met interfaces')
    interfaces_list.add_argument('--name', help="Filter Interface op naam (descr)")

    # Vlan subparsers
    vlan_parser = subparsers.add_parser('vlan', help='Beheer VLANs')
    vlan_subparsers = vlan_parser.add_subparsers(dest='action', required=True, help='Actie voor VLAN')

    vlan_list = vlan_subparsers.add_parser('list', help='Toon lijst met VLANs')
    vlan_list.add_argument('--tag', help="Filter VLAN op tag (numeriek)")

    vlan_add = vlan_subparsers.add_parser('add', help='Voeg VLAN toe')
    vlan_add.add_argument('--tag', required=True, help="VLAN tag (nummer)")
    vlan_add.add_argument('--parent', required=True, help="Parent interface, bv. igb0")
    vlan_add.add_argument('--descr', default='', help="Beschrijving van VLAN")
    vlan_add.add_argument('--enabled', action='store_true', help="Activeer VLAN")

    vlan_delete = vlan_subparsers.add_parser('delete', help='Verwijder VLAN')
    vlan_delete.add_argument('--tag', required=True, help="VLAN tag om te verwijderen (gebruik voor lookup)")
    vlan_delete.add_argument('--uuid', help="Alternatief: directe UUID van VLAN")

    # VIP subparsers
    vip_parser = subparsers.add_parser('vip', help='Beheer VIPs')
    vip_subparsers = vip_parser.add_subparsers(dest='action', required=True, help='Actie voor VIP')

    vip_list = vip_subparsers.add_parser('list', help='Toon lijst met VIPs')
    vip_list.add_argument('--name', help="Filter VIP op naam (descr)")

    vip_add = vip_subparsers.add_parser('add', help='Voeg VIP toe')
    vip_add.add_argument('--type', required=True, choices=['ipalias'])
    vip_add.add_argument('--subnet', required=True)
    vip_add.add_argument('--interface', required=True)
    vip_add.add_argument('--descr', default='')
    vip_add.add_argument('--enabled', action='store_true')

    vip_update = vip_subparsers.add_parser('update', help='Update bestaande VIP')
    vip_update.add_argument('--uuid', help="UUID van de VIP (anders zoek op --name)")
    vip_update.add_argument('--name', dest='search_name', help="Zoek VIP op descr")
    vip_update.add_argument('--type', choices=['ipalias'], help="Mode van VIP")
    vip_update.add_argument('--subnet', help="Subnet in CIDR‑notatie")
    vip_update.add_argument('--interface', help="Interface waar VIP aan hangt")
    vip_update.add_argument('--descr', help="Nieuwe beschrijving")
    vip_update.add_argument('--enabled', type=str2bool, help="true of false")

    vip_delete = vip_subparsers.add_parser('delete', help='Verwijder VIP')
    vip_delete.add_argument('--uuid', help="UUID van de VIP (anders zoek op --name)")
    vip_delete.add_argument('--name', dest='search_name', help="Zoek VIP op descr")

    return parser
