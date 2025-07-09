import requests
from requests.auth import HTTPBasicAuth
import urllib3
import sys
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def api_call(method, url, auth: HTTPBasicAuth, proxies=None, data=None, debug=False):
    try:
        if debug:
            print(f"\n➡️  API CALL: {method.upper()} {url}")
            if data:
                print("📤 Payload:")
                print(json.dumps(data, indent=2))

        r = requests.request(method, url, json=data, auth=auth,
                             verify=False, proxies=proxies if proxies else None, timeout=10)

        if debug:
            print(f"⬅️  Statuscode: {r.status_code}")
            try:
                print("📥 Response:")
                print(json.dumps(r.json(), indent=2))
            except ValueError:
                print("📥 Response (raw):", r.text)

        r.raise_for_status()
        return r.json()

    except requests.HTTPError:
        try:
            err_json = r.json()
        except Exception:
            err_json = {"error": f"HTTP {r.status_code} fout", "details": r.text}
        print(json.dumps(err_json, indent=2), file=sys.stderr)
        sys.exit(1)
    except requests.ConnectionError:
        print(json.dumps({"error": "Verbindingsfout", "details": "Controleer netwerk of proxy-instellingen."}, indent=2), file=sys.stderr)
        sys.exit(1)
    except requests.Timeout:
        print(json.dumps({"error": "Timeout", "details": "Verzoek duurde te lang."}, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": "Onbekende fout", "details": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)
