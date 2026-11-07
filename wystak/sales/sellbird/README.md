# Sellbird (formerly Harvey): WYSTAK's business finder

Open-source agent: https://github.com/ethanplusai/sellbird (set up at commit 867fb3b).
WYSTAK uses it **only to find businesses** in Udaipur: names, addresses, phones, websites and what their sites show.
Email is turned off (`channels.email.enabled: false`). Nothing is ever sent.

## Files here

- `sellbird.local.yaml`: WYSTAK's product, and the target list of 18 local business types in Udaipur (24.5854, 73.7125, 10 km).
- `product_knowledge.md`, `email_rules.md`: what WYSTAK is and the brand rules, in case Sellbird ever drafts anything.
- `osm-local-business-tags.patch`: Sellbird's free OpenStreetMap search only knew trades (roofers, dentists). This patch adds cafés, bakeries, sweet shops, ice cream, juice, restaurants, gyms, yoga, salons, barbers, spas, cinemas, bars, boutiques, pet shops and laundries. Sellbird's discovery tests still pass with it (222).

## Set up on your Mac (once)

```bash
git clone https://github.com/ethanplusai/sellbird.git && cd sellbird
git checkout 867fb3b && git apply ../SocialMedia/wystak/sales/sellbird/osm-local-business-tags.patch
python3.13 -m venv .venv && source .venv/bin/activate && pip install -e .
cp ../SocialMedia/wystak/sales/sellbird/sellbird.local.yaml .
cp ../SocialMedia/wystak/sales/sellbird/product_knowledge.md ../SocialMedia/wystak/sales/sellbird/email_rules.md skills/
sellbird signals --confirm free
```

## Use it

```bash
sellbird discover --estimate     # what it will search, and the cost ($0 on OpenStreetMap)
sellbird discover                # find the businesses and read their websites (free)
sellbird companies               # CSV of every business, with a fit score and why
sellbird export --all            # CSV of everything found
sellbird dashboard               # browse it all on the dashboard
```

For one type only, edit `icp.industries` in `sellbird.local.yaml`. For another city, change `geography` and `geo_coordinates`.
OpenStreetMap has few Udaipur listings. For a fuller list, use a paid source that shows its cost first:
`sellbird discover --provider dataforseo_listings --max-spend 2.00` (DataForSEO, about $0.37 per 1,000 businesses; add the login to `.env`).

## Why not in this cloud session

The OpenStreetMap search servers (Overpass) don't answer from the cloud container, and most business websites are blocked there. Run it on your Mac.
wystak.com is a JavaScript app, so `sellbird train` sees an empty page. The product facts were written by hand from the live site.
