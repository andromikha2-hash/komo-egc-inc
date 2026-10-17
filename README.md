# Komo E.G.C Inc. — komoelectrical.ca

Static website for Komo E.G.C Inc., ECRA/ESA-licensed electrical contractor, Windsor-Essex, Ontario.

## How it works

- `build.py` generates every page into `site/`. No dependencies beyond Python 3.
- **All business facts live in the `BUSINESS` block at the top of `build.py`**: name, phone, email, licence, domain, hours, Google rating and form endpoint. Change them there and rebuild; every page, the JSON-LD schema, `llms.txt` and the sitemap update together. That keeps the name, phone and licence identical everywhere, which Google and AI engines reward.
- Services, service areas and FAQs are data lists (`SERVICES`, `TOWNS`, `GENERAL_FAQS`) in the same file.
- Styles and scripts: `src/assets/`.

```bash
python3 build.py                              # writes site/
cd site && python3 -m http.server 8000        # preview at http://localhost:8000
```

## What gets built

| Path | Purpose |
|---|---|
| `/` | Home: hero with licence title block, GC panel, capability matrix, service areas, FAQ |
| `/general-contractors/` | GC sub-contracting page, incl. "how to vet an electrical sub" checklist |
| `/services/` + 7 service pages | One page per scope (Whitespark 2026 #1 local organic factor) |
| `/service-areas/` + 6 town pages | Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg, Essex |
| `/projects/` | Gallery of real job photos |
| `/faq/`, `/about/`, `/contact/`, `/404.html` | |
| `robots.txt`, `sitemap.xml`, `llms.txt` | Crawl and AI-discovery files |

Every page carries JSON-LD: `Electrician` (with ECRA/ESA licence as `hasCredential`), `Service`, `FAQPage`, `BreadcrumbList`.

## Before launch

1. **Confirm licence #7015083** on the ESA lookup: https://findacontractor.esasafe.com/Home/ContractorSearch
2. **Set real hours** in `BUSINESS["hours"]` (left blank on purpose; wrong hours hurt Maps ranking).
3. **Contact is phone-only** (647-767-7815) by choice: no form, no email on the site.
4. **Photos:** 15 real job photos are in `src/assets/img/` (made by `scripts/prep_photos.py`, metadata stripped). Captions and alt text are in `PHOTOS` in `build.py`. To add more, put them in the photo pack, add them to `PICKS` in the script and to `PHOTOS`, then rebuild.
5. Deploy `site/` to a static host (Cloudflare Pages or Netlify, free) and point `komoelectrical.ca` at it.
6. Set the Google Business Profile website field to `https://komoelectrical.ca` and the business name to `Komo E.G.C Inc.`, then submit `https://komoelectrical.ca/sitemap.xml` in Google Search Console.

Research behind the structure: `docs/research/REA-competitive-intel.md`.
