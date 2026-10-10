# TikTok research in Codex Cloud

## Environment setup

Repository: trendwaveunlimited-spec/eCommerce-Skills

- Python 3; no third-party dependencies required.
- Add SCRAPECREATORS_API_KEY through the cloud environment's secret controls. Never put its value in this repository, a prompt, or a command argument.
- For environments supporting network secrets, allow only api.scrapecreators.com for that secret. HTTPS port 443 is used by the helper. The proxy can replace the placeholder header with the real value.
- Enable network access to api.scrapecreators.com and docs.scrapecreators.com. Broader network access is unnecessary for the included helper.
- Check: `python3 scripts/scrape_creators.py --check-config`.
- Compile check: `python3 -m py_compile scripts/scrape_creators.py`.
- After the key and internet access are configured, verify one authorized product-search call and review the returned credits charged.
- Publish the prepared environment and start future research from that published environment.

## Research request

"Research US TikTok Shop products for my affiliate content. Follow AGENTS.md and use my Scrape Creators API. Start with one search page for the product category I give you. Save raw evidence and a dated shortlist with exact product links, price, seller, reviews, sales evidence and its time window, content angles, and unknown commission/sample eligibility. Do not publish or contact sellers."

## Staying in the cloud

Select Cloud and this published environment when starting research. Adding the repository to GitHub alone does not change a local chat into a cloud task. The local Windows key and personal local skills are not automatically synced. This repository carries the cloud research instructions and API helper.

The GitHub fork is public. Keep research files in the task's private workspace and download important outputs. Do not commit credentials or private reports.
