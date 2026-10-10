# Kalodata research in Codex Cloud

Repository: trendwaveunlimited-spec/eCommerce-Skills

- Python 3, no package dependencies.
- Store KALODATA_API_KEY only in private environment secrets. Allow its use only for www.kalodata.com over HTTPS.
- Enable internet access to www.kalodata.com.
- Configuration: python3 scripts/kalodata.py --check-config
- Free live connection check: python3 scripts/kalodata.py --path /openapi/v1/credit/balance --output outputs/raw/balance.json
- Official API documentation: https://www.kalodata.com/open-center/docs
- Product ranking uses POST /openapi/v1/tiktok/product/rank with region US, language en-US, currency USD, date_range last7Day, page_number 1, page_size 10, sort_field {"field":"revenue","type":"DESC"}. Add keyword and is_affiliate 1 for affiliate discovery. Ranking date windows cannot exceed 30 days.
- Use the documented endpoint fields; read current pricing before spending points. No automatic retry or pagination.
- Generate Key on Kalodata invalidates a previous key, so get explicit confirmation before replacing one.
- Publish the prepared environment after configuration and validation. Start future research in Cloud using that environment.

Research prompt: Research US TikTok Shop affiliate products using my Kalodata API. Follow AGENTS.md. Start with one page for my category and save dated raw evidence and an affiliate shortlist. Include sales/revenue period, reported commission, seller, product IDs, creator fit and uncertainties. Do not post or contact anyone.

This is a public fork: never commit keys or private research outputs. Local Windows files and credentials are not automatically synced to cloud. The older Scrape Creators helper remains optional and is not used by this Kalodata workflow.
