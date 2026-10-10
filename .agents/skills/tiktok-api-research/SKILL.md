---
name: tiktok-api-research
description: Research public US TikTok Shop products and videos using Kalodata Open API in a cloud environment.
---

# Kalodata affiliate research

Read AGENTS.md and CLOUD-RESEARCH.md. Use scripts/kalodata.py; the key comes only from KALODATA_API_KEY in private environment secrets. Official docs: https://www.kalodata.com/open-center/docs. Read the selected endpoint and pricing before each new query type.

Free connection test:
```sh
python3 scripts/kalodata.py --path /openapi/v1/credit/balance --output outputs/raw/balance.json
```

One page of affiliate product discovery:
```sh
python3 scripts/kalodata.py --path /openapi/v1/tiktok/product/rank --body '{"region":"US","language":"en-US","currency":"USD","date_range":"last7Day","page_number":1,"page_size":10,"sort_field":{"field":"revenue","type":"DESC"},"keyword":"solar power bank","is_affiliate":1,"need_extra":true}' --output outputs/raw/products.json
```

Replace the keyword with the user's category. The example is not permission to spend points during setup. Product rank supports a maximum 30-day date window. Use product IDs for exact details. Use video ranking/detail only after checking their current documented parameters.

Label revenue and sales as Kalodata estimates for the requested window. Report commission_rate as provider-reported, subject to verification in the creator's own TikTok account. Missing fields, samples, personalized offers and eligibility stay unknown. Save raw evidence and dated shortlist privately, never in this public repository. No automatic retries or pagination. Never send credentials to returned URLs. The upstream skills are general frameworks, not live data integrations.
