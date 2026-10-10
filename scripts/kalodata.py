"""Read-only Kalodata Open API client for affiliate product research."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, HTTPRedirectHandler

BASE = 'https://www.kalodata.com'
ALLOWED = {'/openapi/v1/credit/balance', '/openapi/v1/tiktok/product/rank',
           '/openapi/v1/tiktok/product/detail', '/openapi/v1/tiktok/video/rank',
           '/openapi/v1/tiktok/video/detail'}

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def request(path, body, key):
    if path not in ALLOWED or not isinstance(body, dict):
        raise ValueError('Use an allowed research endpoint and JSON object.')
    balance = path == '/openapi/v1/credit/balance'
    if balance and body:
        raise ValueError('Balance takes no parameters.')
    req = Request(BASE + path, data=None if balance else json.dumps(body).encode('utf-8'),
                  method='GET' if balance else 'POST',
                  headers={'secret-key': key, 'Content-Type': 'application/json;charset=UTF-8',
                           'Accept': 'application/json'})
    with build_opener(NoRedirect).open(req, timeout=60) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or payload.get('success') is not True:
        raise ValueError('Provider returned an unsuccessful response.')
    return payload

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--path', choices=sorted(ALLOWED))
    parser.add_argument('--body', default='{}', help='JSON body; never include credentials')
    parser.add_argument('--output')
    parser.add_argument('--check-config', action='store_true')
    args = parser.parse_args()
    key = os.environ.get('KALODATA_API_KEY', '').strip()
    if args.check_config:
        print('KALODATA_API_KEY is ' + ('configured' if key else 'missing'))
        return 0 if key else 2
    if not args.path:
        parser.error('--path is required')
    if not key:
        print('Add KALODATA_API_KEY in environment secrets.', file=sys.stderr)
        return 2
    try:
        body = json.loads(args.body)
        payload = request(args.path, body, key)
        result = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
                  'provider': 'Kalodata', 'endpoint': args.path, 'request': body, 'data': payload}
        serialized = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            path = Path(args.output)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(serialized + '\n', encoding='utf-8')
            print('Saved response to ' + str(path))
        else:
            print(serialized)
        return 0
    except HTTPError as exc:
        print('Kalodata HTTP ' + str(exc.code) + '; no retry.', file=sys.stderr)
    except (URLError, ValueError, OSError):
        print('Kalodata request/output failed; no retry. Check key, credits, parameters and network.', file=sys.stderr)
    return 1

if __name__ == '__main__':
    sys.exit(main())
