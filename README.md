# cprima-forge.github.io

The public site, at **https://forge.cprima.net**. Static, and public — every
committed byte is served and clonable.

## What lives here

```
index.html          landing
products/           renders the catalog; hardcodes no product, price or tier
licence/            request a key; posts to the licence service
assets/site.css     the identity: Solarized Light, orange bar
api/v1/             MACHINE-READABLE. Generated — see below
CNAME               forge.cprima.net
```

## `api/v1/` is generated, not authored

`catalog.json` and the schemas beside it are produced by
`cprima-catalog/tools/build.py` and copied in. Editing them here is editing a
build output: the next build overwrites it.

Versioned because an extension that reads `catalog.json` is installed on
someone's machine for years and cannot be updated in lockstep with this site, so
a `v2` has to be able to exist beside `v1`. The pages are *not* versioned — a
browser always fetches the current one.

## The pages render data they fetch

Adding a product or changing a price is a catalog edit and a rebuild, never an
HTML edit. If a page hardcodes an offer, that is a bug.

The licence form holds no secret and cannot: minting a licence needs an admin
token and sending mail needs a provider token, so it posts to a Cloudflare
Worker that holds both. It never displays a key — the email is what proves the
address works.

## Never commit here

- **Font Awesome or Web Awesome Pro assets.** This repository is public;
  committing them redistributes paid, licence-restricted files to anyone who
  clones it. Both load from their CDN with a kit code domain-locked to
  `forge.cprima.net`, which is why the code itself is safe in the HTML.
- **The npm auth token** that fetches them. Usually leaks via `.npmrc`.
- **Virtualenvs.** `tools/*/` carry them; `.gitignore` excludes them.

## Local preview

```bash
python -m http.server 8765
```

`/api/v1/catalog.json` must exist first — run `build.py` in the catalog repo.
