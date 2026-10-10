---
name: tiktok-api-research
description: Research public US TikTok Shop products and TikTok videos using the existing Scrape Creators API in a cloud environment.
---

# TikTok API research

Use the helper at scripts/scrape_creators.py from the repository root. Credentials come only from SCRAPECREATORS_API_KEY in the environment. The Windows DPAPI credential file is local-only and must not be copied or committed.

Read the relevant current provider documentation before calling:
- Product discovery: https://docs.scrapecreators.com/v1/tiktok/shop/search/ — query, page, region.
- Product details: https://docs.scrapecreators.com/v1/tiktok/product/ — url, region.
- Video discovery: https://docs.scrapecreators.com/v1/tiktok/search/keyword/ — check its current parameters.

Example single-page product search:
```sh
python3 scripts/scrape_creators.py --path /v1/tiktok/shop/search --query '{"query":"solar power bank","page":1,"region":"US"}' --output outputs/raw/solar-power-bank.json
```

Example exact product check:
```sh
python3 scripts/scrape_creators.py --path /v1/tiktok/product --query '{"url":"EXACT_PRODUCT_URL","region":"US"}' --output outputs/raw/product.json
```

The examples are not instructions to spend credits during setup. Validate configuration first and make a single live call only when testing is authorized. Stop on authentication, insufficient-credit, or network errors. Never change to an unrelated API or paid service automatically. Do not fetch remote URLs returned by the API without checking relevance; never send the key to those URLs.

Produce an evidence-backed affiliate shortlist following AGENTS.md. Public engagement and lifetime sold counts are not a sales trend. The upstream research skills offer general frameworks and do not provide API access.
