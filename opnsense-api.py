#!/usr/bin/env python3

import json
import sys
from cli.parser import create_parser
from core.config import load_config
from modules import alias, vip, firewall, interface, vlan

def main():
    parser = create_parser()
    args = parser.parse_args()

    base_url, auth, proxies = load_config(args.config)

    try:
        if args.cmd == 'list-alias':
            aliases = alias.list_aliases(base_url, auth, proxies, args.debug).get('rows', [])
            if args.name:
                filtered = [a for a in aliases if a['name'] == args.name]
                print(json.dumps(filtered, indent=2))
            else:
                print(json.dumps(aliases, indent=2))

        elif args.cmd == 'add-alias':
            content_str = '\n'.join(args.content)
            result = alias.add(base_url, auth, proxies, args.name, args.type, content_str, args.descr, args.enabled, args.debug)
            print(json.dumps(result, indent=2))
            if not args.no_reload:
                print(json.dumps(firewall.reload(base_url, auth, proxies, args.debug), indent=2))

        elif args.cmd == 'update-alias':
            uuid = args.uuid or alias.get_uuid_by_name(base_url, auth, proxies, args.search_name, args.debug)
            if not uuid:
                print(json.dumps({"error": "uuid of --search-name vereist"}, indent=2), file=sys.stderr)
                sys.exit(1)
            content_str = '\n'.join(args.content) if args.content else None
            result = alias.update(base_url, auth, proxies, uuid, name=args.name, type_=args.type,
                                  content=content_str, description=args.descr, enabled=args.enabled, debug=args.debug)
            print(json.dumps(result, indent=2))
            if not args.no_reload:
                print(json.dumps(firewall.reload(base_url, auth, proxies, args.debug), indent=2))

        elif args.cmd == 'delete-alias':
            uuid = args.uuid or alias.get_uuid_by_name(base_url, auth, proxies, args.search_name, args.debug)
            if not uuid:
                print(json.dumps({"error": "uuid of --search-name vereist"}, indent=2), file=sys.stderr)
                sys.exit(1)
            result = alias.delete(base_url, auth, proxies, uuid, args.debug)
            print(json.dumps(result, indent=2))
            if not args.no_reload:
                print(json.dumps(firewall.reload(base_url, auth, proxies, args.debug), indent=2))

        elif args.cmd == 'list-interfaces':
            interfaces = interface.list_interfaces(base_url, auth, proxies, args.debug).get('rows', [])
            if args.name:
                filtered = [i for i in interfaces if i.get('description') == args.name]
                print(json.dumps(filtered, indent=2))
            else:
                print(json.dumps(interfaces, indent=2))

        elif args.cmd == 'list-vlan':
            vlans = vlan.list_vlans(base_url, auth, proxies, args.debug).get('rows', [])
            if args.name:
                filtered = [v for v in vlans if v.get('descr') == args.name]
                print(json.dumps(filtered, indent=2))
            else:
                print(json.dumps(vlans, indent=2))

        elif args.cmd == 'list-vip':
            vips = vip.list_vips(base_url, auth, proxies, args.debug).get('rows', [])
            if args.name:
                filtered = [v for v in vips if v.get('descr') == args.name]
                print(json.dumps(filtered, indent=2))
            else:
                print(json.dumps(vips, indent=2))

        elif args.cmd == 'add-vip':
            result = vip.add(base_url, auth, proxies, args.type, args.subnet, args.interface, args.descr, args.enabled, args.debug)
            print(json.dumps(result, indent=2))
            if not args.no_reload:
                print(json.dumps(firewall.reload(base_url, auth, proxies, args.debug), indent=2))

        else:
            parser.print_help()

    except Exception as e:
        print(json.dumps({"error": "Onbekende fout", "details": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
