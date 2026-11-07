# Sellbird (formerly Harvey) set up for WYSTAK

Sellbird is an open-source outreach agent: https://github.com/ethanplusai/sellbird (tested at commit 867fb3b).
It finds businesses, reads their sites, finds the owner, verifies one email, drafts a short sequence and handles replies.
Every email waits in the Outbox for approval (`require_approval: true`).

This folder holds WYSTAK's trained files. The cloud session can't run Sellbird for real (no persistent loop, no Gmail login, and map and café sites are blocked), so run it on your own Mac.

## Run it on your machine

```bash
git clone https://github.com/ethanplusai/sellbird.git && cd sellbird
python3.13 -m venv .venv && source .venv/bin/activate && pip install -e .
cp ../SocialMedia/wystak/sales/sellbird/sellbird.local.yaml .
cp ../SocialMedia/wystak/sales/sellbird/email_rules.md ../SocialMedia/wystak/sales/sellbird/product_knowledge.md skills/
cp .env.example .env    # add the keys below
sellbird signals --confirm free
sellbird dashboard
```

## What it still needs from you

1. **Sender name.** `persona.name` is set to "Kushagra" (founder). Change it if someone else sends.
2. **A mailbox.** A Google Workspace mailbox on a second domain (not wystak.com), with 2-4 weeks of warmup, then `sellbird gmail auth`.
3. **A verifier key.** `REOON_API_KEY` (600 free a month). Without one, no email is ever sent.
4. **A discovery source for cafés.** The free OpenStreetMap source has no café or bakery category, so use a paid one:
   `sellbird discover --provider dataforseo_listings --max-spend 2.00` (DataForSEO, about $0.37 per 1,000 businesses, $1 free credit)
   or Serper (2,500 free searches). Each run shows the cost before it spends anything.
5. **A postal address** in `compliance.postal_address`, which is shown under cold emails.

## Why the website training was done by hand

wystak.com is a JavaScript app, so `sellbird train` gets an empty page. The product facts came from the rendered site
and `wystak/WYSTAK_Project_Context.md`, under the brand rules in CLAUDE.md
(no stats, no prices in email, no phone-number talk, Apple and Google Wallet with equal weight, no gendered pronouns).

## A note on fit

Owners of independent cafés in Bengaluru often answer an Instagram DM, a WhatsApp message or a visit at a quiet hour faster than a cold email.
Use Sellbird as a list builder (`sellbird export`, `sellbird companies`) and pick the channel per café.
