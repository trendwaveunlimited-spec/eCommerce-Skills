"""Read-only Scrape Creators requests for local or cloud TikTok research."""
import argparse
import json
import os
from pathlib import Path
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPRedirectHandler

ALLOWED = {
    "/v1/account/credit-balance",
    "/v1/tiktok/shop/search",
    "/v1/tiktok/product",
    "/v1/tiktok/search/keyword",
}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(path, query, key):
    if path not in ALLOWED:
        raise ValueError("Endpoint is not in the read-only research allowlist.")
    if not isinstance(query, dict) or any(
        not isinstance(v, (str, int, float, bool)) for v in query.values()
    ):
        raise ValueError("Query must be a JSON object with scalar values.")
    params = {k: str(v).lower() if isinstance(v, bool) else v for k, v in query.items()}
    url = "https://api.scrapecreators.com" + path
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers={"x-api-key": key, "Accept": "application/json"})
    with build_opener(NoRedirect).open(req, timeout=60) as response:
        payload = json.load(response)
    if isinstance(payload, dict) and payload.get("success") is False:
        raise ValueError("Provider reported an unsuccessful request; no result saved.")
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", choices=sorted(ALLOWED))
    parser.add_argument("--query", default="{}", help="JSON query object")
    parser.add_argument("--output", help="Save response JSON to this file")
    parser.add_argument("--check-config", action="store_true", help="Check key presence without making a paid call")
    args = parser.parse_args()
    key = os.environ.get("SCRAPECREATORS_API_KEY", "").strip()
    if args.check_config:
        print("SCRAPECREATORS_API_KEY is " + ("configured" if key else "missing"))
        return 0 if key else 2
    if not args.path:
        parser.error("--path is required unless using --check-config")
    if not key:
        print("Missing SCRAPECREATORS_API_KEY. Add it in cloud secrets, never in source files.", file=sys.stderr)
        return 2
    try:
        query = json.loads(args.query)
        payload = request(args.path, query, key)
        result = {
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
            "provider": "Scrape Creators",
            "endpoint": args.path,
            "query": query,
            "data": payload,
        }
        serialized = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(serialized + "\n", encoding="utf-8")
            print("Saved response to " + str(output))
            if isinstance(payload, dict):
                print(json.dumps({k: payload[k] for k in ("credits_charged", "credits_remaining") if k in payload}))
        else:
            print(serialized)
        return 0
    except HTTPError as exc:
        print("Provider HTTP error " + str(exc.code) + "; request was not retried.", file=sys.stderr)
    except URLError:
        print("Network request failed; check cloud internet access. Request was not retried.", file=sys.stderr)
    except (ValueError, OSError):
        print("Request or output failed; check query, provider response, and output path. No automatic retry.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
