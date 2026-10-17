#!/usr/bin/env python3
"""Static site generator for Komo E.G.C Inc.

Every business fact (name, phone, licence, domain) lives in BUSINESS
below, so all pages, schema and listings stay identical. Run:

    python3 build.py

Output goes to site/, ready for any static host (Cloudflare Pages, Netlify,
GitHub Pages). No dependencies beyond the Python standard library.
"""
import datetime
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "site"
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------------------
# Business facts: the single source of truth. Change here, rebuild, done.
# ---------------------------------------------------------------------------
BUSINESS = {
    "name": "Komo E.G.C Inc.",
    "domain": "https://komoelectrical.ca",
    "phone_display": "647-767-7815",
    "phone_e164": "+16477677815",
    "phone_schema": "+1-647-767-7815",
    "licence": "7015083",  # ECRA/ESA contractor licence. Confirm at the ESA lookup before launch.
    "city": "Windsor",
    "region": "ON",
    "founded": "2019-11-05",
    "owner": "Sarmad Komo",
    "facebook": "https://www.facebook.com/p/KOMO-EGC-INC-certified-electrician-7015083-100083358471858/",
    # Real hours only. Leave None until confirmed; wrong hours hurt Maps ranking.
    # Example: [("Mo-Fr", "07:00", "17:00")]
    "hours": None,
    # Google rating as shown on the Google listing. Update when it changes; set None to hide.
    "google_rating": {"value": "5.0", "count": 10},
}
ESA_LOOKUP = "https://findacontractor.esasafe.com/Home/ContractorSearch"
B = BUSINESS
URL = B["domain"]
LIC = B["licence"]

# ---------------------------------------------------------------------------
# Services: one page each (Whitespark 2026: #1 local organic factor).
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "commercial-tenant-fit-outs",
        "name": "Commercial Tenant Fit-Outs",
        "h1": "Commercial tenant fit-out electrical, shell to Certificate of Acceptance.",
        "title": "Commercial Tenant Fit-Out Electrician, Windsor-Essex",
        "short": "Shell to finished electrical for retail, office and plaza units.",
        "sectors": ["Commercial"],
        "system": "120/208V 3Ø · 120/240V 1Ø",
        "intro": "Komo E.G.C Inc. takes tenant fit-outs from bare shell to an energized, inspected space. We work from your electrical drawings or the landlord's base-building information, price the scope line by line, and sequence rough-in so insulation, drywall and ceilings are never waiting on us.",
        "scope": [
            "New panels, sub-panels and distribution for the unit",
            "Branch circuits, receptacles and dedicated equipment circuits",
            "Lighting layouts, switching and occupancy controls",
            "Emergency lighting and exit signs",
            "Data and low-voltage rough-in (boxes and conduit)",
            "Storefront lighting and exterior sign power",
            "Coordination with the landlord's base-building electrical",
        ],
        "sites": ["Retail units and plazas", "Offices and professional suites", "Cafés and quick-service food", "Showrooms"],
        "faqs": [
            ("Can you work to the landlord's tenant criteria?", "Yes. We review the landlord's tenant criteria and base-building electrical before quoting, so the fit-out matches what the building can supply."),
            ("Who files the ESA notification on a fit-out?", f"We do, under Komo E.G.C Inc.'s ECRA/ESA contractor licence #{LIC}. We book the inspections and hand over the Certificate of Acceptance at closeout."),
            ("Can you price from drawings before a site visit?", "Yes. Send the electrical drawings and we return a line-item price with exclusions listed. A site walk confirms existing conditions before the contract is signed."),
        ],
        "related": ["restaurant-kitchen-electrical", "panel-service-upgrades"],
    },
    {
        "slug": "600v-three-phase-power",
        "name": "600V Three-Phase Power",
        "h1": "347/600V three-phase services, distribution and transformers.",
        "title": "600V Three-Phase Electrical Contractor, Windsor-Essex",
        "short": "347/600V services, distribution, transformers and feeders.",
        "sectors": ["Commercial", "Industrial"],
        "system": "347/600V 3Ø · 120/208V 3Ø",
        "intro": "Industrial and larger commercial buildings in Windsor-Essex commonly run on 347/600V three-phase power. Komo E.G.C Inc. installs and upgrades that power: service entrance equipment, distribution, step-down transformers to 120/208V, and the feeders that tie it all together.",
        "scope": [
            "Service entrance and main disconnect installation and upgrades",
            "Distribution panels and splitters",
            "Step-down transformers, 600V to 120/208V",
            "Feeders in rigid or EMT conduit and cable tray",
            "Fused disconnects for equipment",
            "Utility coordination for disconnects and reconnects",
        ],
        "sites": ["Warehouses and distribution centres", "Manufacturing and tool and die shops", "Multi-tenant industrial buildings", "Large retail and commercial buildings"],
        "faqs": [
            ("Do you work on 600V systems?", "Yes. Komo E.G.C Inc. installs and upgrades 347/600V three-phase services and distribution, including step-down transformers to 120/208V, machine feeds, motor controls and VFDs."),
            ("Can you add a transformer to feed 120/208V equipment in a 600V building?", "Yes. We size, install and connect the step-down transformer and the panel it feeds, filed with ESA under our licence."),
            ("Do you coordinate the utility shutdown?", "Yes. We coordinate the disconnect and reconnect with the utility serving the address and schedule the shutdown around your operations."),
        ],
        "related": ["machine-hookups-motor-controls", "warehouse-led-lighting-retrofits"],
    },
    {
        "slug": "restaurant-kitchen-electrical",
        "name": "Restaurant & Kitchen Electrical",
        "h1": "Restaurant and commercial kitchen electrical, built for opening day.",
        "title": "Restaurant & Commercial Kitchen Electrician, Windsor-Essex",
        "short": "Hood control panels, equipment circuits and dining-room lighting.",
        "sectors": ["Commercial"],
        "system": "120/208V 3Ø",
        "intro": "Restaurants pack a lot of load into a small footprint: cooking equipment, refrigeration, hood fans, dish machines and dining-room lighting on one service. Komo E.G.C Inc. wires kitchens and front-of-house so the equipment runs and the space passes inspection on the opening schedule.",
        "scope": [
            "Hood fan and make-up air wiring, including hood control panels",
            "Dedicated circuits and connections for cooking, refrigeration and dish equipment",
            "Panel upgrades or additions when new equipment exceeds the existing service",
            "Feature, pendant and decorative lighting for dining rooms",
            "Exterior and sign lighting",
            "Coordination with kitchen equipment suppliers and mechanical trades",
        ],
        "sites": ["Full-service restaurants", "Cafés and bakeries", "Quick-service and takeout", "Bars and lounges"],
        "faqs": [
            ("Do you wire hood control panels?", "Yes. We wire hood fans, make-up air and the hood control panel, and coordinate with the hood installer so interlocks are connected before inspection."),
            ("Can you tell me if my service can handle new kitchen equipment?", "Yes. We review the load from the equipment schedule and tell you whether the service, the panel or both need an upgrade before you order equipment."),
            ("Do you work from the kitchen supplier's drawings?", "Yes. We work from the supplier's equipment schedule and rough-in drawings so connection points land where the equipment sits."),
        ],
        "related": ["commercial-tenant-fit-outs", "panel-service-upgrades"],
    },
    {
        "slug": "warehouse-led-lighting-retrofits",
        "name": "Warehouse LED Lighting Retrofits",
        "h1": "Warehouse LED retrofits without shutting the floor down.",
        "title": "Warehouse LED Lighting Retrofit Electrician, Windsor-Essex",
        "short": "High-bay LED replacements and lighting controls.",
        "sectors": ["Commercial", "Industrial"],
        "system": "347V · 120V lighting circuits",
        "intro": "Old metal-halide and fluorescent high-bays cost more to run and take longer to light. Komo E.G.C Inc. replaces them with LED high-bays and adds controls, working zone by zone around your shifts so the floor stays in operation.",
        "scope": [
            "High-bay and low-bay LED fixture replacement",
            "Lighting circuit rework on 347V or 120V",
            "Occupancy and daylight controls",
            "Exterior wall packs and parking lot lighting",
            "Emergency lighting updates",
            "Lift and access planning for high ceilings",
        ],
        "sites": ["Warehouses and distribution", "Manufacturing floors", "Shops and garages", "Large-format retail"],
        "faqs": [
            ("Can you retrofit without shutting the warehouse down?", "Yes. We work in zones and around shift schedules so only the area being retrofitted is affected at any time."),
            ("Do LED retrofits qualify for incentives?", "Ontario's Save on Energy program has offered retrofit incentives for qualifying projects. Eligibility and amounts are set by the program, so check its current rules. We can supply the fixture counts and wattages an application needs."),
            ("What voltage do warehouse LED fixtures run on?", "In 600V buildings, warehouse lighting usually runs on 347V. Smaller buildings often use 120V. We match fixtures to the existing circuits or rework the circuits."),
        ],
        "related": ["600v-three-phase-power", "commercial-tenant-fit-outs"],
    },
    {
        "slug": "machine-hookups-motor-controls",
        "name": "Machine Hookups & Motor Controls",
        "h1": "Machine hookups, motor controls and VFDs.",
        "title": "Machine Hookup & Motor Control Electrician, Windsor-Essex",
        "short": "Equipment feeds, disconnects, motor controls and VFDs.",
        "sectors": ["Industrial"],
        "system": "600V 3Ø · 208V 3Ø",
        "intro": "New equipment doesn't earn anything until it's powered. Komo E.G.C Inc. runs the feeds, installs the disconnects and connects motors and controls for machines being installed, moved or replaced.",
        "scope": [
            "Power feeds and disconnects for new or relocated machines",
            "CNC, press, compressor and conveyor connections",
            "Motor starters and motor control wiring",
            "Variable frequency drive (VFD) installation",
            "Control panel wiring",
            "Machine relocation and decommissioning",
        ],
        "sites": ["Tool and die and machine shops", "Manufacturing plants", "Fabrication shops", "Warehouses with conveyors"],
        "faqs": [
            ("Can you hook up a machine we're moving between buildings?", "Yes. We disconnect and make safe at the old location, run a new feed and disconnect at the new one, and reconnect the machine."),
            ("Do you install VFDs?", "Yes. We install and wire variable frequency drives for motors, including the supply, motor leads and control connections."),
            ("Can you work during a planned shutdown?", "Yes. We schedule machine and feed work into your planned shutdown windows."),
        ],
        "related": ["600v-three-phase-power", "panel-service-upgrades"],
    },
    {
        "slug": "panel-service-upgrades",
        "name": "Panel & Service Upgrades",
        "h1": "Panel and service upgrades, commercial and residential.",
        "title": "Panel & Service Upgrade Electrician, Windsor-Essex",
        "short": "Commercial panel work and residential 100A to 200A upgrades.",
        "sectors": ["Commercial", "Residential"],
        "system": "120/240V 1Ø · 120/208V 3Ø · 600V",
        "intro": "When a building needs more capacity or its equipment is at end of life, the panel and service are where the work starts. Komo E.G.C Inc. replaces and adds panels for commercial buildings and upgrades homes from 100A to 200A service.",
        "scope": [
            "Residential service upgrades, 100A to 200A",
            "Panel replacements and sub-panels",
            "Commercial panel additions and distribution changes",
            "Switchgear maintenance and thermal imaging",
            "Meter base and service mast replacement",
            "Utility disconnect and reconnect coordination",
        ],
        "sites": ["Homes adding EV chargers, heat pumps or additions", "Offices and retail", "Industrial buildings"],
        "faqs": [
            ("Do I need a permit for a panel upgrade?", f"Yes. In Ontario, panel and service work needs an ESA notification. Komo E.G.C Inc. files it under licence #{LIC} and books the inspection."),
            ("Do you coordinate with the utility?", "Yes. Service upgrades need the utility to disconnect and reconnect. We arrange it with the utility serving the address."),
            ("What is thermal imaging for?", "Infrared scanning finds loose connections and overloaded breakers by the heat they give off, before they fail. It is done with the equipment energized and under load."),
        ],
        "related": ["generators-transfer-switches", "commercial-tenant-fit-outs"],
    },
    {
        "slug": "generators-transfer-switches",
        "name": "Generators & Transfer Switches",
        "h1": "Generator connections and transfer switches.",
        "title": "Generator & Transfer Switch Electrician, Windsor-Essex",
        "short": "Standby generator connections and transfer switches.",
        "sectors": ["Commercial", "Residential"],
        "system": "120/240V · 120/208V · 600V",
        "intro": "A transfer switch lets a generator carry the loads that matter without backfeeding the utility. Komo E.G.C Inc. installs transfer switches and connects standby and portable generators for homes and businesses.",
        "scope": [
            "Automatic transfer switch installation",
            "Manual transfer switches and generator inlets for portable units",
            "Standby generator electrical connection",
            "Load selection: which circuits stay on during an outage",
            "Restaurant and refrigeration backup circuits",
        ],
        "sites": ["Homes", "Restaurants and food storage", "Offices and small commercial"],
        "faqs": [
            ("Can I plug a portable generator into my house?", "Only through a transfer switch, or an approved interlock with a generator inlet. Plugging into an outlet can backfeed the utility lines and endanger line workers. We install the inlet and transfer equipment and file the work with ESA."),
            ("Do you install the generator itself?", "We handle the electrical side: transfer switch, wiring and connection. For gas-fired standby units, a licensed gas fitter makes the gas connection."),
        ],
        "related": ["panel-service-upgrades", "restaurant-kitchen-electrical"],
    },
]
SVC = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------------------
# Service areas: six municipalities, each with real local detail.
# ---------------------------------------------------------------------------
TOWNS = [
    {
        "slug": "windsor", "name": "Windsor", "wiki": "https://en.wikipedia.org/wiki/Windsor,_Ontario",
        "intro": "Komo E.G.C Inc. is based in Windsor and works across the city: commercial units along the main corridors, industrial buildings in the east end, and homes from Riverside to South Windsor.",
        "places": ["Downtown", "Walkerville", "Riverside", "East Riverside", "Forest Glade", "Sandwich", "South Windsor"],
        "local": "In Windsor, service upgrades are coordinated with ENWIN Utilities, the city's electricity distributor. We arrange the disconnect and reconnect as part of the job.",
        "focus": ["commercial-tenant-fit-outs", "restaurant-kitchen-electrical", "600v-three-phase-power", "machine-hookups-motor-controls"],
    },
    {
        "slug": "tecumseh", "name": "Tecumseh", "wiki": "https://en.wikipedia.org/wiki/Tecumseh,_Ontario",
        "intro": "Tecumseh combines established neighbourhoods with one of the region's busiest industrial areas in Oldcastle, home to tool and die shops, fabricators and warehouses.",
        "places": ["Tecumseh", "Oldcastle", "St. Clair Beach"],
        "local": "Industrial work in Oldcastle is mostly 600V three-phase: machine feeds, motor controls, transformers and high-bay lighting. We schedule it around production.",
        "focus": ["machine-hookups-motor-controls", "600v-three-phase-power", "warehouse-led-lighting-retrofits", "panel-service-upgrades"],
    },
    {
        "slug": "lasalle", "name": "LaSalle", "wiki": "https://en.wikipedia.org/wiki/LaSalle,_Ontario",
        "intro": "LaSalle is one of the fastest-growing towns in Essex County. Komo E.G.C Inc. handles retail and office fit-outs in its plazas and service upgrades in its established neighbourhoods.",
        "places": ["LaSalle", "Malden Road corridor", "Front Road"],
        "local": "Growth brings new tenants into new and existing plazas. We fit out those units and upgrade older homes adding EV chargers, heat pumps or additions.",
        "focus": ["commercial-tenant-fit-outs", "panel-service-upgrades", "restaurant-kitchen-electrical", "generators-transfer-switches"],
    },
    {
        "slug": "lakeshore", "name": "Lakeshore", "wiki": "https://en.wikipedia.org/wiki/Lakeshore,_Ontario",
        "intro": "Lakeshore stretches along Lake St. Clair from the Tecumseh border to Lighthouse Cove. Komo E.G.C Inc. works in its town centres and across its rural and industrial properties.",
        "places": ["Belle River", "Emeryville", "Puce", "Comber", "Stoney Point", "Lighthouse Cove"],
        "local": "Rural shops and farm buildings often need new services, sub-panels and three-phase feeds. Belle River and Emeryville bring commercial fit-outs and restaurant work.",
        "focus": ["600v-three-phase-power", "panel-service-upgrades", "commercial-tenant-fit-outs", "generators-transfer-switches"],
    },
    {
        "slug": "amherstburg", "name": "Amherstburg", "wiki": "https://en.wikipedia.org/wiki/Amherstburg",
        "intro": "Amherstburg, founded in 1796, is one of the oldest towns in Ontario. Its historic main street mixes restaurants, shops and older buildings that often need electrical upgrades before a new tenant moves in.",
        "places": ["Downtown Amherstburg", "Sandwich Street", "Richmond Street"],
        "local": "Older buildings mean existing wiring to assess before a fit-out. We review what's there, price what needs to change, and file the work with ESA.",
        "focus": ["restaurant-kitchen-electrical", "commercial-tenant-fit-outs", "panel-service-upgrades", "generators-transfer-switches"],
    },
    {
        "slug": "essex", "name": "Essex", "wiki": "https://en.wikipedia.org/wiki/Essex,_Ontario",
        "intro": "The Town of Essex takes in Essex Centre, Harrow, McGregor and Colchester. Komo E.G.C Inc. works on its main-street businesses, light industrial buildings and rural properties.",
        "places": ["Essex Centre", "Harrow", "McGregor", "Colchester"],
        "local": "Expect a mix of single-phase main-street commercial and three-phase light industrial. We price both from drawings or a site walk.",
        "focus": ["commercial-tenant-fit-outs", "600v-three-phase-power", "panel-service-upgrades", "warehouse-led-lighting-retrofits"],
    },
]


# ---------------------------------------------------------------------------
# Job photos (real Komo projects, from the Facebook page). Files are made by
# scripts/prep_photos.py: <key>-480.webp and <key>-900.webp, 3:4 portrait.
# "w" is the real width of the larger file (originals top out at 720px).
# Captions never name a client; in-progress shots say so.
# ---------------------------------------------------------------------------
PHOTOS = {
    "bakery-fit-out": ("Bakery interior with pendant lights, display cases and a black-and-white checkered floor under an open white ceiling", "Bakery fit-out: pendant and display-case lighting", 900),
    "restaurant-counter-lighting": ("Restaurant service counter with patterned tile, recessed lights and track lighting under a dark ceiling", "Restaurant counter: recessed and track lighting", 900),
    "restaurant-dining-lighting": ("Restaurant dining room with decorative ceiling panels and lighting over the tables", "Restaurant dining-room lighting", 900),
    "linear-ceiling-lighting": ("Wood-slat ceiling with linear LED strips above a reception counter, fit-out in progress", "Linear LED in a wood-slat ceiling (in progress)", 900),
    "track-lighting-install": ("Track lights and recessed fixtures in a commercial unit ceiling, installation in progress", "Commercial unit: track and recessed lighting (in progress)", 900),
    "exposed-conduit-lighting": ("Track lighting run on exposed conduit under an open black ceiling, installation in progress", "Track lighting on exposed conduit (in progress)", 900),
    "chandelier-feature-lighting": ("Tall atrium ceiling with blue cove lighting, recessed lights and a spiral chandelier", "Feature lighting: cove, recessed and chandelier", 900),
    "residential-recessed-lighting": ("Vaulted living-room ceiling with rows of recessed pot lights", "Residential pot lights in a vaulted ceiling", 900),
    "electrician-at-work": ("Komo electrician on a ladder working at a wall-mounted panel, with conduit running down a block wall", "On site: panel and conduit work", 900),
    "commercial-panel": ("Commercial breaker panel on a block wall with the cover off during installation", "Commercial panel installation", 900),
    "distribution-panel": ("Distribution panel with a full row of breakers and conductors routed to the terminals", "Distribution panel", 720),
    "fused-disconnect": ("Open three-pole fused disconnect switch with cartridge fuses and feeder conductors", "Fused disconnect switch", 720),
    "control-panel": ("Open control panel with contactors, relays, terminal blocks and a controller board, neatly wired", "Control panel wiring", 900),
    "motor-contactors": ("Enclosure with a row of motor contactors and their wiring, cover removed", "Motor contactor enclosure", 720),
    "residential-panel": ("Residential breaker panel with new circuits terminated, mounted on a plywood backboard", "Residential panel install", 720),
}
SERVICE_PHOTOS = {
    "commercial-tenant-fit-outs": "track-lighting-install",
    "600v-three-phase-power": "fused-disconnect",
    "restaurant-kitchen-electrical": "restaurant-counter-lighting",
    "warehouse-led-lighting-retrofits": "exposed-conduit-lighting",
    "machine-hookups-motor-controls": "motor-contactors",
    "panel-service-upgrades": "distribution-panel",
}

GENERAL_FAQS = [
    ("Is Komo E.G.C Inc. a licensed electrical contractor in Ontario?", f"Yes. Komo E.G.C Inc. holds ECRA/ESA Electrical Contractor Licence #{LIC}. You can verify it on the Electrical Safety Authority's contractor lookup."),
    ("Do you sub-contract to general contractors?", "Yes. We take electrical scopes from general contractors and project managers on commercial fit-outs, restaurants, retail, office and warehouse projects across Windsor-Essex. Call with the scope and schedule for a line-item price."),
    ("Do you work on 600V three-phase systems?", "Yes. We install and upgrade 347/600V three-phase services and distribution, including step-down transformers to 120/208V, machine feeds, motor controls and VFDs."),
    ("Which areas do you serve?", "Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg and Essex, plus the rest of Essex County, Ontario."),
    ("Who files the ESA notification and books inspections?", f"We do. Komo E.G.C Inc. files the ESA notification of work under licence #{LIC}, books inspections and hands over the Certificate of Acceptance at closeout."),
    ("Can you provide WSIB clearance and a certificate of insurance?", "Yes. We provide a WSIB clearance certificate and a certificate of insurance for your project file before mobilization."),
    ("How do you price a job?", "From drawings or a site walk. You get a line-item quote with exclusions stated, so you can compare, carry and change-order cleanly."),
    ("Do you do residential work?", "Yes, mainly service and panel upgrades, generator transfer switches and renovation wiring. Most of our work is commercial and industrial."),
]

# ---------------------------------------------------------------------------
# Schema helpers
# ---------------------------------------------------------------------------
def area_served():
    out = [{"@type": "City", "name": t["name"], "sameAs": t["wiki"]} for t in TOWNS]
    out.append({"@type": "AdministrativeArea", "name": "Essex County, Ontario", "sameAs": "https://en.wikipedia.org/wiki/Essex_County,_Ontario"})
    return out


def business_node():
    node = {
        "@type": "Electrician",
        "@id": f"{URL}/#business",
        "name": B["name"],
        "legalName": B["name"],
        "url": f"{URL}/",
        "telephone": B["phone_schema"],
        "foundingDate": B["founded"],
        "founder": {"@type": "Person", "name": B["owner"]},
        "description": "ECRA/ESA-licensed electrical contractor sub-contracting to general contractors and serving businesses across Windsor-Essex County, Ontario: tenant fit-outs, 347/600V three-phase power, restaurant electrical, warehouse LED retrofits, machine hookups and service upgrades.",
        "address": {"@type": "PostalAddress", "addressLocality": B["city"], "addressRegion": B["region"], "addressCountry": "CA"},
        "areaServed": area_served(),
        "hasCredential": {
            "@type": "EducationalOccupationalCredential",
            "name": "Electrical Contractor Licence (ECRA/ESA)",
            "credentialCategory": "license",
            "identifier": LIC,
            "recognizedBy": {"@type": "Organization", "name": "Electrical Safety Authority", "url": "https://esasafe.com"},
        },
        "knowsAbout": ["Ontario Electrical Safety Code"] + [s["name"] for s in SERVICES],
        "sameAs": [B["facebook"]],
        "image": [f"{URL}/assets/img/{k}-900.webp" for k in ("electrician-at-work", "bakery-fit-out", "control-panel")],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Electrical contracting services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{URL}/services/{s['slug']}/"}}
                for s in SERVICES
            ],
        },
    }
    if B["hours"]:
        node["openingHoursSpecification"] = [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, o, c in B["hours"]
        ]
    return node


def breadcrumb_node(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{URL}{path}"} for i, (name, path) in enumerate(trail)
        ],
    }


def faq_node(faqs, path):
    return {
        "@type": "FAQPage",
        "@id": f"{URL}{path}#faq",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }


# ---------------------------------------------------------------------------
# HTML fragments
# ---------------------------------------------------------------------------
e = html.escape
NAV = [
    ("Services", "/services/"),
    ("General Contractors", "/general-contractors/"),
    ("Service Areas", "/service-areas/"),
    ("Projects", "/projects/"),
    ("FAQ", "/faq/"),
    ("About", "/about/"),
    ("Contact", "/contact/"),
]


def head(title, desc, path, graph):
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=1, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{URL}{path}">
<meta name="geo.region" content="CA-ON">
<meta name="geo.placename" content="Windsor, Ontario">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(B['name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{URL}{path}">
<meta property="og:locale" content="en_CA">
<meta name="theme-color" content="#12181d">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500&family=Public+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/styles.css">
<script type="application/ld+json">
{schema}
</script>
</head>"""


def strip():
    rating = ""
    if B["google_rating"]:
        r = B["google_rating"]
        rating = f'<span>{r["value"]}★ Google rating · {r["count"]} reviews</span>'
    return f"""<div class="strip band">
  <div class="wrap">
    <span>ECRA/ESA Licence <b>#{LIC}</b> · <a href="{ESA_LOOKUP}" rel="noopener" target="_blank">verify</a></span>
    {rating}
    <span>WSIB clearance on request</span>
    <span>Windsor · Tecumseh · LaSalle · Lakeshore · Amherstburg · Essex</span>
  </div>
</div>"""


def header(active):
    links = "\n      ".join(
        f'<a href="{p}"{" aria-current=\"page\"" if active == p else ""}>{n}</a>' for n, p in NAV
    )
    return f"""<a class="skip" href="#main">Skip to content</a>
{strip()}
<header class="site-head band">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{e(B['name'])} home">KOMO E.G.C<span>INC</span></a>
    <nav class="nav" aria-label="Main">
      {links}
    </nav>
    <a class="call-btn" href="tel:{B['phone_e164']}">Call {B['phone_display']}</a>
    <details class="menu">
      <summary>Menu</summary>
      <nav aria-label="Mobile">
        {links}
        <a href="tel:{B['phone_e164']}">Call {B['phone_display']}</a>
      </nav>
    </details>
  </div>
</header>"""


def footer():
    svc = "\n".join(f'<li><a href="/services/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    towns = "\n".join(f'<li><a href="/service-areas/{t["slug"]}/">Electrician in {t["name"]}</a></li>' for t in TOWNS)
    return f"""<footer class="foot band">
  <div class="wrap">
    <div>
      <a class="brand" href="/">KOMO E.G.C<span>INC</span></a>
      <ul style="margin-top:14px">
        <li>{e(B['name'])}</li>
        <li>Licensed electrical contractor · ECRA/ESA #{LIC}</li>
        <li>Windsor, Ontario · Serving Essex County</li>
        <li><a href="tel:{B['phone_e164']}">{B['phone_display']}</a></li>
      </ul>
    </div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Service areas</h2><ul>{towns}</ul></div>
    <div><h2>Company</h2><ul>
      <li><a href="/general-contractors/">For general contractors</a></li>
      <li><a href="/projects/">Projects</a></li>
      <li><a href="/faq/">FAQ</a></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/contact/">Contact</a></li>
      <li><a href="{ESA_LOOKUP}" rel="noopener" target="_blank">Verify our ESA licence</a></li>
      <li><a href="{B['facebook']}" rel="noopener" target="_blank">Facebook</a></li>
    </ul></div>
    <div class="legal"><span>© {datetime.date.today().year} {e(B['name'])} All rights reserved.</span><span>ECRA/ESA Licence #{LIC}</span></div>
  </div>
</footer>
<script src="/assets/main.js" defer></script>
</body>
</html>"""


def crumbs(trail):
    items = []
    for i, (name, path) in enumerate(trail):
        if i == len(trail) - 1:
            items.append(f'<li aria-current="page">{e(name)}</li>')
        else:
            items.append(f'<li><a href="{path}">{e(name)}</a></li>')
    return f'<div class="band"><nav class="wrap crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav></div>'


def faq_block(faqs, open_first=True):
    out = []
    for i, (q, a) in enumerate(faqs):
        out.append(f'<details{" open" if (i == 0 and open_first) else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>')
    return f'<div class="faq">{"".join(out)}</div>'


def cta_band(heading="Call with the scope. Get a number."):
    return f"""<section class="sec band">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="label">Request pricing</p><h2>{e(heading)}</h2></div>
      <div class="cta-row">
        <a class="call-btn" href="tel:{B['phone_e164']}">Call {B['phone_display']}</a>
        <button class="copy-num" type="button" data-copy="{B['phone_display']}">Copy number</button>
      </div>
    </div>
  </div>
</section>"""


def page(path, title, desc, body, graph, active=None, trail=None):
    full_title = f"{title} | {B['name']}"
    graph = [business_node()] + graph
    if trail:
        graph.append(breadcrumb_node(trail))
    parts = [head(full_title, desc, path, graph), "<body>", header(active)]
    if trail:
        parts.append(crumbs(trail))
    parts += [f'<main id="main">{body}</main>', footer()]
    target = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    if path.endswith(".html"):
        target = OUT / path.strip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(parts), encoding="utf-8")
    PAGES.append(path)


def photo(key, eager=False, sizes="(max-width: 860px) 50vw, 33vw"):
    alt, cap, w = PHOTOS[key]
    big = min(900, w)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="photo"><img src="/assets/img/{key}-900.webp" '
            f'srcset="/assets/img/{key}-480.webp 480w, /assets/img/{key}-900.webp {big}w" sizes="{sizes}" '
            f'width="{big}" height="{round(big * 4 / 3)}" alt="{e(alt)}" {load} decoding="async">'
            f'<figcaption>{e(cap)}</figcaption></figure>')


def gallery(keys):
    return '<div class="gallery">' + "".join(photo(k) for k in keys) + "</div>"


PAGES = []

TITLEBLOCK = f"""<aside class="titleblock" aria-label="Licence and credentials">
  <div class="tb-head"><strong>Contractor credentials</strong><span class="label">Sheet E-000</span></div>
  <dl>
    <div class="full"><dt>Licensed electrical contractor</dt><dd>{e(B['name'])}</dd></div>
    <div class="full"><dt>ECRA/ESA contractor licence</dt><dd class="lic">#{LIC}</dd></div>
    <div><dt>WSIB</dt><dd>Clearance certificate on request</dd></div>
    <div><dt>Insurance</dt><dd>Certificate of insurance on request</dd></div>
    <div><dt>Voltage classes</dt><dd class="num">120/240V · 120/208V · 347/600V</dd></div>
    <div><dt>Phases</dt><dd class="num">1Ø and 3Ø</dd></div>
    <div class="full"><dt>Service area</dt><dd>Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg, Essex</dd></div>
  </dl>
  <svg class="sld" viewBox="0 0 360 96" role="img" aria-label="Single-line diagram: 600V service, main disconnect, step-down transformer to a 120/208V panel">
    <line class="k" x1="14" y1="40" x2="70" y2="40"/><circle class="dot" cx="14" cy="40" r="3"/><text x="4" y="62">UTIL</text>
    <rect class="k" x="70" y="28" width="34" height="24"/><text x="74" y="44">MTR</text>
    <line class="k" x1="104" y1="40" x2="140" y2="40"/><line class="k" x1="140" y1="40" x2="156" y2="30"/><line class="k" x1="158" y1="40" x2="186" y2="40"/>
    <text x="128" y="62">MAIN</text><text x="126" y="76">600V 3Ø</text>
    <circle class="k" cx="200" cy="40" r="12"/><circle class="k" cx="216" cy="40" r="12"/><text x="186" y="70">XFMR</text>
    <line class="k" x1="228" y1="40" x2="268" y2="40"/><rect class="k" x="268" y="24" width="60" height="32"/><text x="276" y="44">PNL-A</text><text x="262" y="76">120/208V</text>
    <line class="k" x1="328" y1="40" x2="352" y2="40"/><line class="k" x1="352" y1="30" x2="352" y2="50"/>
  </svg>
  <div class="tb-foot"><span class="label">Issued for: GC prequalification</span><a class="label" href="{ESA_LOOKUP}" rel="noopener" target="_blank">Verify licence ↗</a></div>
</aside>"""

GC_COMMITMENTS = """<div class="gc-grid">
  <article><span class="label">Schedule</span><h3>Staffed to your schedule</h3><p>Crew size and start dates are set from your project schedule before mobilization. Rough-in is sequenced ahead of insulation and board so no trade waits on us.</p></article>
  <article><span class="label">Code</span><h3>Built to the OESC</h3><p>Installed to the Ontario Electrical Safety Code, with conduit, fill and bonding laid out to pass the first inspection.</p></article>
  <article><span class="label">Inspections</span><h3>ESA handled by us</h3><p>We file the ESA notification under our licence, book inspections against your timeline, and meet the inspector on site.</p></article>
  <article><span class="label">Estimating</span><h3>Line-item pricing</h3><p>Quotes are itemized by scope so you can compare, carry and change-order cleanly. Exclusions are written down, not discovered later.</p></article>
</div>"""

GC_INCLUDES = f"""<ul class="checks">
  <li>ESA notification of work filed under licence #{LIC}</li>
  <li>WSIB clearance certificate before mobilization</li>
  <li>Certificate of insurance for your project file</li>
  <li>Long-lead material flagged at award, not at rough-in</li>
  <li>Marked-up drawings for as-builts at closeout</li>
  <li>ESA Certificate of Acceptance in the closeout package</li>
</ul>"""

GC_STEPS = """<ol class="steps">
  <li><div><b>Drawing review and site walk</b><span>E-sheets, panel schedules and site conditions checked against the scope.</span></div></li>
  <li><div><b>Line-item quote</b><span>Itemized price, exclusions stated, lead-time items called out.</span></div></li>
  <li><div><b>ESA notification and utility coordination</b><span>Filed under our licence; utility disconnects and reconnects arranged.</span></div></li>
  <li><div><b>Rough-in</b><span>Sequenced to your schedule and inspected before cover.</span></div></li>
  <li><div><b>Trim-out and energize</b><span>Devices, fixtures, equipment connections, panel directories.</span></div></li>
  <li><div><b>Final inspection and closeout</b><span>Certificate of Acceptance and as-builts handed over.</span></div></li>
</ol>"""


def matrix():
    rows = []
    for s in SERVICES:
        tags = "".join(f'<span class="tag{" c" if t == "Commercial" else ""}">{t}</span>' for t in s["sectors"])
        rows.append(
            f'<tr><th scope="row"><a href="/services/{s["slug"]}/">{e(s["name"])}</a></th><td>{tags}</td>'
            f'<td class="spec">{e(s["system"])}</td><td>{e(s["short"])}</td><td>{e(", ".join(s["sites"][:3]))}</td></tr>'
        )
    return f"""<div class="table-scroll">
  <table class="matrix wide">
    <caption>{e(B['name'])} · Scope schedule · Windsor-Essex County, Ontario</caption>
    <thead><tr><th scope="col">Scope</th><th scope="col">Sector</th><th scope="col">System</th><th scope="col">Typical work</th><th scope="col">Typical sites</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>
<p class="note">All work installed under ECRA/ESA Licence #{LIC} to the Ontario Electrical Safety Code. Scope not listed? Call {B['phone_display']} with the drawings.</p>"""


def town_cards():
    return '<div class="cards">' + "".join(
        f'<a href="/service-areas/{t["slug"]}/"><h3>{t["name"]}</h3><p>{e(", ".join(t["places"][:4]))}</p><span class="more">Electrician in {t["name"]} →</span></a>'
        for t in TOWNS
    ) + "</div>"


def service_cards(slugs=None):
    items = [SVC[s] for s in slugs] if slugs else SERVICES
    cards = [
        f'<a href="/services/{s["slug"]}/"><span class="label">{e(" · ".join(s["sectors"]))}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">{e(s["system"])}</span></a>'
        for s in items
    ]
    if not slugs:
        # The full list is 7 scopes; an 8th "not listed" card fills a 4 x 2 grid.
        cards.append(f'<a href="/contact/"><span class="label">Anything else</span><h3>Scope not listed?</h3><p>Call {B["phone_display"]} with the scope. If it is electrical and in Essex County, ask.</p><span class="more">Contact →</span></a>')
    cols = {2: " c2", 4: " c4", 8: " c4"}.get(len(cards), "")
    return f'<div class="cards{cols}">' + "".join(cards) + "</div>"


def sec(label, h2, intro, content, cls="", hid=None):
    hid_attr = f' id="{hid}"' if hid else ""
    return f"""<section class="sec band {cls}"{hid_attr}>
  <div class="wrap">
    <div class="sec-head"><div><p class="label">{label}</p><h2>{h2}</h2></div><p>{intro}</p></div>
    {content}
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def build_home():
    body = f"""<section class="hero band">
  <div class="wrap">
    <div>
      <p class="label">Licensed electrical contractor · Windsor-Essex, Ontario</p>
      <h1>Electrical crews that <em>hold your schedule</em> and build to pass ESA the first time.</h1>
      <p class="lede">{e(B['name'])} is an ECRA/ESA-licensed electrical contractor working for general contractors, project managers and business owners across Windsor-Essex. We take tenant fit-outs, restaurants, warehouses and 347/600V three-phase work from rough-in to Certificate of Acceptance.</p>
      <div class="cta-row">
        <a class="call-btn" href="tel:{B['phone_e164']}">Call {B['phone_display']}</a>
        <button class="copy-num" type="button" data-copy="{B['phone_display']}">Copy number</button>
      </div>
      <div class="callout">
        <span class="label">General contractors</span>
        <strong>Call with your scope and schedule. You get a line-item electrical price and a crew plan built around your milestones.</strong>
        <a href="/general-contractors/">How we work with GCs →</a>
      </div>
    </div>
    {TITLEBLOCK}
  </div>
</section>
{sec("For general contractors &amp; project managers", "Your schedule is the contract.", "An electrical sub that misses rough-in holds up insulation, drywall and every trade behind it. We plan crews against your milestones, show up when the board says, and close out with the paperwork in order.",
     GC_COMMITMENTS + f'<div class="split"><div><h3>Every sub-contract includes</h3>{GC_INCLUDES}</div><div><h3>How a scope runs</h3>{GC_STEPS}</div></div>', cls="inverse", hid="gc")}
{sec("Technical capabilities", "What we install, at what voltage, and where.", "Commercial, industrial and residential scopes we self-perform across Windsor-Essex. Every scope is filed with ESA and inspected.", matrix(), hid="capabilities")}
{sec("Recent work", "Real jobs, real panels.", "Fit-outs, lighting and panel work from recent Komo projects.", gallery(["bakery-fit-out", "restaurant-counter-lighting", "control-panel", "restaurant-dining-lighting", "electrician-at-work", "distribution-panel"]) + '<p class="note"><a href="/projects/">All projects →</a></p>', hid="work")}
{sec("Service area · Essex County, Ontario", "Six municipalities, one crew list.", "Based in Windsor and dispatched to job sites across Essex County.", town_cards(), hid="areas")}
{sec("Questions GCs and owners ask", "Straight answers.", "The details a GC needs for prequalification and an owner needs before signing.", faq_block(GENERAL_FAQS[:5]) + '<p class="note"><a href="/faq/">All questions →</a></p>', hid="faq")}
{cta_band()}"""
    page(
        "/",
        "Electrical Contractor Windsor-Essex · GC Sub-Contracting",
        f"ECRA/ESA-licensed electrical contractor (#{LIC}) for general contractors and businesses in Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg and Essex. Tenant fit-outs, 600V three-phase, LED retrofits.",
        body,
        [faq_node(GENERAL_FAQS[:5], "/"), {"@type": "WebSite", "@id": f"{URL}/#website", "url": f"{URL}/", "name": B["name"], "publisher": {"@id": f"{URL}/#business"}, "inLanguage": "en-CA"}],
        active="/",
    )


def build_gc():
    vet = [
        ("ECRA/ESA contractor licence", f"Only a Licensed Electrical Contractor can be hired for electrical work in Ontario. Ask for the 7-digit number and check it on ESA's lookup. Ours is #{LIC}."),
        ("Who files the ESA notification", "The contractor doing the work must file it. Make sure it's filed under the sub's licence, not left to you."),
        ("WSIB clearance and insurance", "Get a current WSIB clearance certificate and a certificate of insurance before the sub mobilizes."),
        ("Commercial and three-phase experience", "Fit-outs, kitchens and 600V distribution are different from house wiring. Ask what they've done in the last year."),
        ("Itemized pricing", "A line-item quote with exclusions stated is the only way to compare bids and price change orders cleanly."),
    ]
    vet_html = '<ol class="steps">' + "".join(f"<li><div><b>{e(t)}</b><span>{e(d)}</span></div></li>" for t, d in vet) + "</ol>"
    gc_faqs = [GENERAL_FAQS[1], GENERAL_FAQS[4], GENERAL_FAQS[5], GENERAL_FAQS[6]]
    body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">For general contractors &amp; project managers</p>
  <h1>An electrical sub that keeps your job moving.</h1>
  <p class="lede">{e(B['name'])} takes electrical scopes from general contractors across Windsor-Essex: commercial fit-outs, restaurants, retail, offices and warehouses. Licensed, insured, and organized around your schedule.</p>
  <div class="cta-row"><a class="call-btn" href="tel:{B['phone_e164']}">Call {B['phone_display']}</a></div>
</div></section>
{sec("What you get", "Schedule, code, inspections, pricing.", "Four things decide whether an electrical sub helps or hurts your job.", GC_COMMITMENTS + f'<div class="split"><div><h3>Every sub-contract includes</h3>{GC_INCLUDES}</div><div><h3>How a scope runs</h3>{GC_STEPS}</div></div>', cls="inverse")}
{sec("Prequalification", "How to vet an electrical sub in Ontario.", "Five checks before you award an electrical scope. We meet all five.", vet_html + f'<p class="note"><a href="{ESA_LOOKUP}" rel="noopener" target="_blank">Check any contractor on ESA\'s licence lookup ↗</a></p>')}
{sec("Scopes we take", "What we self-perform.", "Every scope below is installed by our crews, not re-subbed.", service_cards())}
{sec("GC questions", "Before you call.", "", faq_block(gc_faqs))}
{cta_band("Call with the scope. Get a line-item price.")}"""
    trail = [("Home", "/"), ("General Contractors", "/general-contractors/")]
    page("/general-contractors/", "Electrical Sub-Contractor for General Contractors, Windsor-Essex",
         f"Licensed electrical sub-contractor (ECRA/ESA #{LIC}) for general contractors in Windsor-Essex. ESA notifications, WSIB and insurance certificates, line-item pricing, schedule-driven crews.",
         body, [faq_node(gc_faqs, "/general-contractors/")], active="/general-contractors/", trail=trail)


def build_services():
    trail = [("Home", "/"), ("Services", "/services/")]
    body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">Services</p>
  <h1>Commercial, industrial and residential electrical.</h1>
  <p class="lede">Seven scopes {e(B['name'])} self-performs across Windsor-Essex, each filed with ESA under licence #{LIC}.</p>
</div></section>
{sec("Scope schedule", "Capabilities at a glance.", "Voltage, sector and typical sites for each scope.", matrix(), cls="flush")}
{sec("Service pages", "Pick a scope.", "Each page lists what's included, typical sites and common questions.", service_cards())}
{cta_band()}"""
    page("/services/", "Electrical Services, Windsor-Essex",
         "Tenant fit-outs, 600V three-phase power, restaurant electrical, warehouse LED retrofits, machine hookups, panel upgrades and generator transfer switches across Windsor-Essex.",
         body, [], active="/services/", trail=trail)

    for s in SERVICES:
        path = f"/services/{s['slug']}/"
        trail = [("Home", "/"), ("Services", "/services/"), (s["name"], path)]
        scope = "".join(f"<li>{e(x)}</li>" for x in s["scope"])
        sites = "".join(f"<li>{e(x)}</li>" for x in s["sites"])
        body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">{e(" · ".join(s["sectors"]))} · {e(s["system"])}</p>
  <h1>{e(s["h1"])}</h1>
  <p class="lede">{e(s["intro"])}</p>
  <div class="cta-row"><a class="call-btn" href="tel:{B['phone_e164']}">Call {B['phone_display']}</a></div>
</div></section>
<section class="sec band"><div class="wrap two-col">
  <div class="prose">
    <h2>What's included</h2>
    <ul class="checks">{scope}</ul>
    <h2>Typical sites</h2>
    <ul>{sites}</ul>
    <h2>Permits and inspection</h2>
    <p>Every {e(s["name"].lower())} job is filed with the Electrical Safety Authority under {e(B['name'])}'s contractor licence #{LIC}. We book the inspections and hand over the Certificate of Acceptance when the work passes.</p>
  </div>
  <aside class="aside-box">
    {photo(SERVICE_PHOTOS[s["slug"]], sizes="(max-width: 900px) 100vw, 400px") if s["slug"] in SERVICE_PHOTOS else ""}
    <p class="label">Spec</p>
    <h2>{e(s["name"])}</h2>
    <p class="num">{e(s["system"])}</p>
    <p>Serving Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg and Essex.</p>
    <a class="call-btn" href="tel:{B['phone_e164']}">Call {B['phone_display']}</a>
  </aside>
</div></section>
{sec("Questions", f"{e(s['name'])}: common questions.", "", faq_block(s["faqs"]))}
{sec("Related", "Related scopes.", "", service_cards(s["related"]))}
{cta_band()}"""
        graph = [
            {"@type": "Service", "@id": f"{URL}{path}#service", "name": s["name"], "serviceType": s["name"], "description": s["intro"],
             "provider": {"@id": f"{URL}/#business"}, "areaServed": area_served(), "url": f"{URL}{path}"},
            faq_node(s["faqs"], path),
        ]
        page(path, s["title"], f"{s['short']} {B['name']}, ECRA/ESA #{LIC}, serving Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg and Essex.",
             body, graph, active="/services/", trail=trail)


def build_towns():
    trail = [("Home", "/"), ("Service Areas", "/service-areas/")]
    body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">Service areas · Essex County, Ontario</p>
  <h1>Electrician for Windsor and Essex County.</h1>
  <p class="lede">{e(B['name'])} is based in Windsor and works in six municipalities across Essex County.</p>
</div></section>
{sec("Municipalities", "Where we work.", "Pick your town for local detail and the work we do there.", town_cards(), cls="flush")}
{cta_band()}"""
    page("/service-areas/", "Service Areas: Windsor & Essex County Electrician",
         "Electrical contractor serving Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg and Essex, Ontario.",
         body, [], active="/service-areas/", trail=trail)

    for t in TOWNS:
        path = f"/service-areas/{t['slug']}/"
        trail = [("Home", "/"), ("Service Areas", "/service-areas/"), (t["name"], path)]
        places = ", ".join(t["places"])
        faqs = [
            (f"Do you serve all of {t['name']}?", f"Yes. {B['name']} works throughout {t['name']}, including {places}."),
            (f"Do you take commercial work in {t['name']}?", f"Yes. In {t['name']} we take {', '.join(SVC[s]['name'].lower() for s in t['focus'][:3])}, and more. Call {B['phone_display']}."),
            (f"Who handles the ESA notification for a job in {t['name']}?", f"We do. Every job in {t['name']} is filed with ESA under licence #{LIC}, and we book the inspection."),
        ]
        body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">Service area · {t['name']}, Ontario</p>
  <h1>Electrician in {t['name']}, Ontario.</h1>
  <p class="lede">{e(t['intro'])}</p>
  <div class="cta-row"><a class="call-btn" href="tel:{B['phone_e164']}">Call {B['phone_display']}</a></div>
</div></section>
<section class="sec band"><div class="wrap two-col">
  <div class="prose">
    <h2>Working in {t['name']}</h2>
    <p>{e(t['local'])}</p>
    <h2>Communities we cover</h2>
    <ul>{"".join(f"<li>{e(p)}</li>" for p in t["places"])}</ul>
  </div>
  <aside class="aside-box">
    <p class="label">{t['name']} · Essex County</p>
    <h2>{e(B['name'])}</h2>
    <p>Licensed electrical contractor · ECRA/ESA #{LIC}</p>
    <a class="call-btn" href="tel:{B['phone_e164']}">Call {B['phone_display']}</a>
  </aside>
</div></section>
{sec("Common work", f"What we do in {t['name']}.", "", service_cards(t["focus"]))}
{sec("Questions", f"{t['name']} questions.", "", faq_block(faqs))}
{cta_band()}"""
        graph = [
            {"@type": "Service", "@id": f"{URL}{path}#service", "name": f"Electrical contracting in {t['name']}, Ontario", "serviceType": "Electrician",
             "provider": {"@id": f"{URL}/#business"}, "areaServed": {"@type": "City", "name": t["name"], "sameAs": t["wiki"]}, "url": f"{URL}{path}"},
            faq_node(faqs, path),
        ]
        page(path, f"Electrician in {t['name']}, Ontario",
             f"Licensed electrical contractor in {t['name']}, Ontario (ECRA/ESA #{LIC}). {', '.join(SVC[s]['name'] for s in t['focus'][:3])}. Call {B['phone_display']}.",
             body, graph, active="/service-areas/", trail=trail)


def build_faq():
    trail = [("Home", "/"), ("FAQ", "/faq/")]
    body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">FAQ</p>
  <h1>Questions about working with {e(B['name'])}.</h1>
</div></section>
{sec("Licensing, scope and process", "Straight answers.", f'Licence #{LIC} can be checked on <a href="{ESA_LOOKUP}" rel="noopener" target="_blank">ESA\'s contractor lookup</a>.', faq_block(GENERAL_FAQS), cls="flush")}
{cta_band()}"""
    page("/faq/", "Electrical Contractor FAQ",
         f"Licensing, ESA notifications, WSIB, insurance, pricing and service areas for {B['name']}, ECRA/ESA #{LIC}, Windsor-Essex.",
         body, [faq_node(GENERAL_FAQS, "/faq/")], active="/faq/", trail=trail)


def build_about():
    trail = [("Home", "/"), ("About", "/about/")]
    year = B["founded"][:4]
    body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">About</p>
  <h1>{e(B['name'])}</h1>
  <p class="lede">A Windsor-based licensed electrical contractor, incorporated in {year}, working for general contractors, businesses and homeowners across Essex County.</p>
</div></section>
<section class="sec band flush"><div class="wrap two-col">
  <div class="prose">
    {photo("electrician-at-work", eager=True, sizes="(max-width: 900px) 100vw, 560px")}
    <h2>What we do</h2>
    <p>{e(B['name'])} installs and upgrades electrical systems for commercial, industrial and residential buildings: tenant fit-outs, restaurant kitchens, 347/600V three-phase power, machine hookups, warehouse LED retrofits, panel upgrades and generator transfer switches.</p>
    <p>Most of our work comes through general contractors and business owners who need the electrical scope done on schedule, filed with ESA and closed out with the paperwork in order.</p>
    <h2>How we work</h2>
    <ul class="checks">
      <li>Every job filed with the Electrical Safety Authority under our own licence</li>
      <li>Line-item quotes with exclusions written down</li>
      <li>Crews scheduled to your milestones</li>
      <li>Certificate of Acceptance handed over at closeout</li>
    </ul>
  </div>
  <aside class="titleblock">
    <div class="tb-head"><strong>Company record</strong><span class="label">Sheet E-001</span></div>
    <dl>
      <div class="full"><dt>Legal name</dt><dd>{e(B['name'])}</dd></div>
      <div class="full"><dt>ECRA/ESA contractor licence</dt><dd class="lic">#{LIC}</dd></div>
      <div><dt>Incorporated</dt><dd>{year}</dd></div>
      <div><dt>Based in</dt><dd>Windsor, Ontario</dd></div>
      <div class="full"><dt>Owner</dt><dd>{e(B['owner'])}</dd></div>
      <div class="full"><dt>Service area</dt><dd>Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg, Essex</dd></div>
    </dl>
    <div class="tb-foot"><span class="label">{B['phone_display']}</span><a class="label" href="{ESA_LOOKUP}" rel="noopener" target="_blank">Verify licence ↗</a></div>
  </aside>
</div></section>
{cta_band()}"""
    page("/about/", "About", f"{B['name']} is a Windsor-based ECRA/ESA-licensed electrical contractor (#{LIC}) serving general contractors and businesses across Essex County since {year}.",
         body, [], active="/about/", trail=trail)


def build_contact():
    trail = [("Home", "/"), ("Contact", "/contact/")]
    body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">Contact</p>
  <h1>Call with the scope. Get a number.</h1>
  <p class="lede">The fastest way to reach {e(B['name'])} is by phone. Tell us the scope, the site and your schedule, and we'll set up a site walk or price it from your drawings.</p>
</div></section>
<section class="sec band flush"><div class="wrap contact-grid">
  <div class="direct">
    <p class="label">Call</p>
    <a class="big num" href="tel:{B['phone_e164']}">{B['phone_display']}</a>
    <div class="cta-row"><a class="call-btn" href="tel:{B['phone_e164']}">Call now</a><button class="copy-num" type="button" data-copy="{B['phone_display']}">Copy number</button></div>
  </div>
  <aside class="titleblock">
    <div class="tb-head"><strong>Before you call</strong><span class="label">Sheet E-002</span></div>
    <dl>
      <div class="full"><dt>Have ready</dt><dd>Site address, type of work, target start date, and whether drawings exist</dd></div>
      <div class="full"><dt>ECRA/ESA contractor licence</dt><dd class="lic">#{LIC}</dd></div>
      <div class="full"><dt>Service area</dt><dd>Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg, Essex</dd></div>
    </dl>
    <div class="tb-foot"><span class="label">{B['phone_display']}</span><a class="label" href="{ESA_LOOKUP}" rel="noopener" target="_blank">Verify licence ↗</a></div>
  </aside>
</div></section>"""
    page("/contact/", "Contact",
         f"Call {B['name']} at {B['phone_display']} for electrical pricing in Windsor-Essex. ECRA/ESA licence #{LIC}.",
         body, [], active="/contact/", trail=trail)


def build_projects():
    trail = [("Home", "/"), ("Projects", "/projects/")]
    fitouts = ["bakery-fit-out", "restaurant-counter-lighting", "restaurant-dining-lighting", "linear-ceiling-lighting",
               "track-lighting-install", "exposed-conduit-lighting", "chandelier-feature-lighting", "residential-recessed-lighting", "electrician-at-work"]
    panels = ["commercial-panel", "distribution-panel", "fused-disconnect", "control-panel", "motor-contactors", "residential-panel"]
    body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">Projects</p>
  <h1>Recent work.</h1>
  <p class="lede">Photos from {e(B['name'])} jobs: restaurant and retail fit-outs, lighting installs, panels and control wiring. Some show work in progress, and the captions say so.</p>
</div></section>
{sec("Fit-outs and lighting", "Restaurants, retail and feature lighting.", "Commercial interiors from rough-in to finished space.", gallery(fitouts), cls="flush")}
{sec("Panels and controls", "Distribution, disconnects and control wiring.", "Equipment close-ups, unretouched.", gallery(panels))}
{cta_band()}"""
    graph = [{"@type": "ImageGallery", "@id": f"{URL}/projects/#gallery", "name": f"{B['name']} recent work",
              "about": {"@id": f"{URL}/#business"},
              "image": [{"@type": "ImageObject", "contentUrl": f"{URL}/assets/img/{k}-900.webp", "caption": PHOTOS[k][1]} for k in fitouts + panels]}]
    page("/projects/", "Recent Electrical Projects, Windsor-Essex",
         f"Photos of recent {B['name']} electrical work: restaurant and retail fit-outs, lighting, panels, disconnects and control wiring.",
         body, graph, active="/projects/", trail=trail)


def build_404():
    body = f"""<section class="page-hero band"><div class="wrap">
  <p class="label">404</p>
  <h1>That page isn't on the drawings.</h1>
  <p class="lede">Try the <a href="/services/">services</a>, the <a href="/service-areas/">service areas</a>, or call {B['phone_display']}.</p>
</div></section>"""
    page("/404.html", "Page not found", "Page not found.", body, [])
    PAGES.remove("/404.html")


def build_support_files():
    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "# AI answer engines are welcome to read and cite this site.\n"
        + "".join(f"User-agent: {bot}\nAllow: /\n\n" for bot in ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bingbot"])
        + f"Sitemap: {URL}/sitemap.xml\n",
        encoding="utf-8",
    )
    urls = "".join(f"  <url><loc>{URL}{p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in PAGES)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
        encoding="utf-8",
    )
    svc = "\n".join(f"- [{s['name']}]({URL}/services/{s['slug']}/): {s['short']} System: {s['system']}." for s in SERVICES)
    towns = "\n".join(f"- [Electrician in {t['name']}]({URL}/service-areas/{t['slug']}/)" for t in TOWNS)
    (OUT / "llms.txt").write_text(
        f"""# {B['name']}

> {B['name']} is an ECRA/ESA-licensed electrical contractor (licence #{LIC}) based in Windsor, Ontario, Canada. It sub-contracts to general contractors and works for business owners and homeowners across Essex County: Windsor, Tecumseh, LaSalle, Lakeshore, Amherstburg and Essex. Phone {B['phone_display']}.

Key facts:
- Legal name: {B['name']}
- ECRA/ESA Electrical Contractor Licence: #{LIC} (verify: {ESA_LOOKUP})
- Voltage classes: 120/240V single-phase, 120/208V and 347/600V three-phase
- Files ESA notifications under its own licence, books inspections, hands over the Certificate of Acceptance
- Provides WSIB clearance and a certificate of insurance before mobilization
- Incorporated {B['founded'][:4]}

## Services
{svc}

## Service areas
{towns}

## Pages
- [General contractors]({URL}/general-contractors/): how {B['name']} works as an electrical sub
- [FAQ]({URL}/faq/)
- [About]({URL}/about/)
- [Contact]({URL}/contact/)
""",
        encoding="utf-8",
    )
    (OUT / "assets" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#12181d"/>'
        '<path d="M18 3 7 18h7l-2 11 11-15h-7z" fill="#f2c200"/></svg>',
        encoding="utf-8",
    )


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "src" / "assets", OUT / "assets")
    build_home()
    build_gc()
    build_services()
    build_towns()
    build_projects()
    build_faq()
    build_about()
    build_contact()
    build_404()
    build_support_files()
    print(f"Built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    main()
