#!/usr/bin/env python3
"""
Build the Kleen Xtar inner pages (blog, about, careers, terms, privacy).

Every page shares one nav, footer and closing band, so editing them here and
re-running keeps the whole site consistent.

    python3 tools/build_pages.py

Pages are written under SITE_DIR at clean URLs (e.g. test/blog/index.html is
served at /test/blog/). To move the site from /test to the root later, change
BASE to "" and SITE_DIR to the repo root, then re-run.
"""
import html
import json
import os
import re
import urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/test"                      # URL prefix of the site
SITE_DIR = os.path.join(REPO, "test")
NOINDEX = True                      # test pages stay out of Google

PHONE_HREF = "tel:+916363287727"
PHONE_TEXT = "+91 63632 87727"
WA_NUMBER = "916363287727"
PUBLISHED = "2026-11-24"            # blog publish date shown on posts

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='7' fill='%23000'/%3E%3Cpath d='M16 1C17 11 20 14.500 31 16C20 "
           "17.500 17 21 16 31C15 21 12 17.500 1 16C12 14.500 15 11 16 1Z' fill='%232E9BFF'/%3E%3C/svg%3E")

LIVE_AREAS = ["Yelahanka", "Hebbal", "Hennur", "Malleshwaram", "Indiranagar", "KR Puram", "Whitefield",
              "Marathahalli", "Koramangala", "Bellandur", "HSR Layout", "Sarjapur Road", "Jayanagar",
              "JP Nagar", "Bannerghatta Road", "Electronic City"]
SOON_AREAS = ["Rajarajeshwari Nagar", "Kanakapura Road", "Devanahalli", "Hoskote"]


def u(path=""):
    return BASE + path


def wa(text):
    return "https://wa.me/%s?text=%s" % (WA_NUMBER, urllib.parse.quote(text))


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- icons
ICON = {
    "wa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M4.5 19.5l1.2-3.6A8 8 0 1 1 8.6 18.8z"/><path d="M9 10.5h6M9 13.5h3.5"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.6 6 11a6 6 0 0 1-12 0c0-4.4 6-11 6-11z"/></svg>',
    "cloth": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M4 7l8-3 8 3v10l-8 3-8-3z"/><path d="M4 7l8 3 8-3M12 10v10"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v5c0 5-3 8.5-7 10-4-1.5-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg>',
    "rain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 15a4 4 0 0 1 .5-8 5.5 5.5 0 0 1 10.5 2 3 3 0 0 1-.5 6z"/><path d="M9 18l-1 2M13 18l-1 2M17 18l-1 2"/></svg>',
    "building": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M4 21V5l8-2v18M12 8h8v13M2 21h20"/><path d="M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2"/></svg>',
    "flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6A2 2 0 0 0 19 18l-5-9V3"/><path d="M7.5 15h9"/></svg>',
    "camera": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h4l2-3h6l2 3h4v11H3z"/><circle cx="12" cy="13" r="3.5"/></svg>',
    "person": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.5 4.3-6.5 8-6.5s7 2 8 6.5"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "unlock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 7.5-2"/></svg>',
}

# ---------------------------------------------------------------- shared chrome
NAV_ITEMS = [
    ("How we clean", "/#kx-process", None),
    ("Plans", "/#kx-plans", None),
    ("Services", "/#kx-services", None),
    ("Societies", "/#kx-societies", None),
    ("Areas", "/#kx-areas", None),
    ("Blog", "/blog/", "blog"),
    ("FAQ", "/#kx-faq", None),
]


def head(title, desc, extra=""):
    robots = '<meta name="robots" content="noindex,nofollow">\n' if NOINDEX else ""
    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
{robots}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#000000">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anek+Latin:wdth,wght@75..125,100..800&amp;display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Saira:ital,wdth,wght@0,75..125,400..900;1,75..125,400..900&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('/assets/kx.css')}">
<link rel="stylesheet" href="{u('/assets/kx-pages.css')}">
{extra}</head>
<body>
<div class="kx" id="kx-top">
<a class="kx-skip" href="#kx-main">Skip to content</a>
"""


def nav(active=None):
    on = ' class="is-on" aria-current="page"'
    desk = "\n".join(
        f'        <li><a href="{u(h)}"{on if k and k == active else ""}>{t}</a></li>'
        for t, h, k in NAV_ITEMS)
    mob = "\n".join(f'      <li><a href="{u(h)}">{t}</a></li>' for t, h, k in NAV_ITEMS)
    return f"""
<header class="kx-nav">
  <div class="kx-wrap kx-nav__in">
    <a class="kx-logo" href="{u('/')}" aria-label="Kleen Xtar home"><img src="{u('/assets/logo.webp')}" alt="Kleen Xtar" width="760" height="100"></a>
    <nav aria-label="Main">
      <ul class="kx-nav__links">
{desk}
      </ul>
    </nav>
    <div class="kx-nav__cta">
      <a class="kx-btn kx-btn--primary kx-btn--sm" href="{u('/#book')}">Book free trial</a>
      <button class="kx-burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="kx-mnav"><span></span><span></span></button>
    </div>
  </div>
  <div class="kx-mnav" id="kx-mnav">
    <ul>
{mob}
    </ul>
    <a class="kx-btn kx-btn--primary" href="{u('/#book')}">Book a free trial wash</a>
  </div>
</header>
"""


def band(title="Book tonight. Wake up to a clean car.",
         lead="Your first wash is free. Tell us where the car is parked and we’ll confirm your first morning on WhatsApp."):
    return f"""
<section class="kx-band" aria-labelledby="kx-band-h">
  <div class="kx-wrap">
    <h2 class="kx-h2" id="kx-band-h">{title}</h2>
    <p class="kx-lead">{lead}</p>
    <div class="kx-cta__acts">
      <a class="kx-btn kx-btn--primary" href="{u('/#book')}">Book a free trial wash</a>
      <a class="kx-btn kx-btn--line-light" href="{esc(wa('Hi Kleen Xtar, I’d like to book a free trial wash.'))}" target="_blank" rel="noopener">{ICON['wa']}Chat on WhatsApp</a>
    </div>
  </div>
</section>
"""


def footer():
    return f"""
</main>

<footer class="kx-foot">
  <div class="kx-wrap">
    <div class="kx-foot__top">
      <div class="kx-foot__about">
        <a class="kx-logo" href="{u('/')}" aria-label="Kleen Xtar home"><img src="{u('/assets/logo.webp')}" alt="Kleen Xtar" width="760" height="100" loading="lazy"></a>
        <p>Doorstep car cleaning for independent houses, villas and apartment societies in Bengaluru.</p>
        <div class="kx-foot__contact">
          <a href="{PHONE_HREF}">{PHONE_TEXT}</a>
        </div>
      </div>
      <div>
        <h4>Cleaning</h4>
        <ul><li><a href="{u('/#kx-plans')}">Monthly plans</a></li><li><a href="{u('/#kx-services')}">One-time services</a></li><li><a href="{u('/#kx-house')}">Household pricing</a></li><li><a href="{u('/#kx-societies')}">For societies</a></li></ul>
      </div>
      <div>
        <h4>Help</h4>
        <ul><li><a href="{u('/#kx-process')}">How we clean</a></li><li><a href="{u('/#kx-faq')}">FAQ</a></li><li><a href="{u('/#kx-areas')}">Check your area</a></li><li><a href="{u('/blog/')}">Car care blog</a></li></ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul><li><a href="{u('/about/')}">About us</a></li><li><a href="{u('/careers/')}">Join our crew</a></li><li><a href="{u('/terms/')}">Terms</a></li><li><a href="{u('/privacy/')}">Privacy</a></li></ul>
      </div>
    </div>
    <div class="kx-foot__bot"><span>© 2026 Kleen Xtar, Bengaluru</span><span>Where every ride shines.</span></div>
  </div>
</footer>

<div class="kx-mbar">
  <a class="kx-btn kx-btn--primary" href="{u('/#book')}">Book a free trial</a>
  <a class="kx-btn kx-btn--line-light" href="{esc(wa('Hi Kleen Xtar, I’d like to book a free trial wash.'))}" target="_blank" rel="noopener">{ICON['wa']}WhatsApp</a>
</div>
</div>
<script src="{u('/assets/kx-pages.js')}" defer></script>
</body>
</html>
"""


def phero(h1, lead, crumbs):
    c = "".join(f'<li><a href="{u(h)}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>' for t, h in crumbs)
    return f"""
<main id="kx-main">
<section class="kx-phero">
  <div class="kx-wrap">
    <ol class="kx-crumbs">{c}</ol>
    <h1 class="kx-h1">{h1}</h1>
    {f'<p class="kx-lead">{lead}</p>' if lead else ''}
  </div>
</section>
"""


def write(rel, content):
    path = os.path.join(SITE_DIR, rel, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", os.path.relpath(path, REPO))


def fmt_date(iso):
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    return f"{int(d)} {months[int(m) - 1]} {y}"


# ---------------------------------------------------------------- blog posts
POSTS = [
    {
        "slug": "daily-car-wiping-without-scratches",
        "tag": "Paint care",
        "icon": "cloth",
        "title": "Will a daily wipe scratch my car? How we clean every morning without swirl marks",
        "short": "Will a daily wipe scratch my car?",
        "desc": "Scratches come from grit dragged across paint, not from cleaning often. Here is the method our crew uses every morning to keep Bengaluru dust from turning into swirl marks.",
        "body": f"""
<p>It’s the first question most people ask before they book a daily clean. If someone wipes my car every morning, won’t the paint end up covered in fine scratches?</p>
<p>It can, if it’s done the usual way. A dry cloth, a quick wipe in circles and the same rag used on twenty cars is exactly how swirl marks are made. But the scratches don’t come from cleaning often. They come from <strong>dragging grit across the paint</strong>. Take the grit out of the picture and a daily clean is gentle.</p>

<h2>Why Bengaluru dust is hard on paint</h2>
<p>The dust that settles on a parked car overnight is fine and gritty. Under a cloth it behaves like very fine sandpaper. Press down and rub, and every particle leaves a tiny line in the clear coat. One morning won’t show it. A few months of mornings will, especially on dark cars under a streetlight.</p>

<h2>The four rules we follow on every car</h2>
<h3>1. Lift loose dust first, without pressing</h3>
<p>Before anything wet touches the car, a wide, soft microfibre duster goes over it from roof to bumper. It lifts the loose layer off instead of pushing it into the paint. This takes about three minutes and it’s the step most cleaners skip.</p>
<h3>2. Make the surface slippery</h3>
<p>Next comes a pH-neutral rinseless shampoo, one panel at a time, starting at the roof. It loosens the film of dirt that’s left and coats the paint, so the cloth glides instead of scraping. It’s safe on wax, ceramic coatings and paint protection film.</p>
<h3>3. Straight lines, fresh side every panel</h3>
<p>The cloth is folded so it has eight clean sides. Each panel is wiped in straight lines, never circles, and the cleaner turns to a fresh side after every panel. Dirt picked up from one panel never touches the next.</p>
<h3>4. A different cloth for every job</h3>
<p>Our crew carries four colours of microfibre and never mixes them:</p>
<ul>
  <li><strong>Blue</strong> for paint only</li>
  <li><strong>Lilac</strong> for glass and mirrors</li>
  <li><strong>Charcoal</strong> for wheels and tyres</li>
  <li><strong>Marigold</strong> for inside the cabin</li>
</ul>
<p>Wheels carry the heaviest grime, including brake dust. Keeping that cloth separate means it never ends up on your bonnet or windscreen.</p>

<h2>What happens to the cloths afterwards</h2>
<p>Every car gets a fresh set. Used cloths go into a sealed bag and are machine-washed at our hub. They are never shaken out and reused on the next car, which is how one gritty cloth spreads scratches down a whole row of parked cars.</p>

<div class="kx-note"><b>The short answer:</b> a daily clean doesn’t scratch paint. A dirty cloth does. Lift the dust, lubricate the surface, wipe in straight lines and use clean cloths, and your paint stays glossy.</div>

<h2>If your car already has swirl marks</h2>
<p>A daily clean keeps new ones from forming, but it can’t remove marks that are already there. For that, our <a href="{u('/#kx-services')}">wax and polish service</a> uses a clay bar and a machine polish to reduce light swirls and bring back the gloss, then seals the paint. It takes about three hours and starts from ₹1,999.</p>
""",
    },
    {
        "slug": "how-much-water-does-a-car-wash-use",
        "tag": "Water",
        "icon": "drop",
        "title": "2 litres or 150? How much water a car wash really uses in Bengaluru",
        "short": "2 litres or 150?",
        "desc": "A hose wash uses around 150 litres, a bucket wash 20 to 40. A rinseless daily clean uses about 2. Here’s what that means for one car and for a whole apartment society.",
        "body": f"""
<p>Every summer, Bengaluru apartment groups fill up with the same messages. Tanker prices are up, borewells are low and someone is washing their car with a hose in the basement again.</p>
<p>Washing a car doesn’t have to use much water at all. It depends entirely on the method.</p>

<h2>Water per wash, by method</h2>
<table>
  <thead><tr><th>Method</th><th class="n">Water per car</th></tr></thead>
  <tbody>
    <tr><td>Hose wash</td><td class="n">about 150 litres</td></tr>
    <tr><td>Bucket wash</td><td class="n">20 to 40 litres</td></tr>
    <tr><td>Our doorstep foam wash</td><td class="n">about 20 litres</td></tr>
    <tr><td>Our rinseless daily clean</td><td class="n">about 2 litres</td></tr>
  </tbody>
</table>

<h2>How a car gets clean with 2 litres</h2>
<p>A rinseless clean doesn’t rely on water to carry dirt away. The work is done by the shampoo and the cloth:</p>
<ol>
  <li>Loose dust is lifted off with a dry microfibre duster.</li>
  <li>A rinseless shampoo goes on one panel at a time. It loosens the remaining dirt and wraps around it so it doesn’t scratch.</li>
  <li>A folded microfibre cloth picks the dirt up, a fresh side for every panel.</li>
</ol>
<p>The two litres go into the wash solution and rinsing the cloth between panels, in two buckets with grit guards. There is no runoff, so there’s no puddle on your road and nothing running across the basement floor.</p>

<h2>What it adds up to in a society</h2>
<p>Take an apartment society where 60 cars are cleaned 26 times a month.</p>
<table>
  <tbody>
    <tr><td>Hose washing, 150 litres a car</td><td class="n">2,34,000 litres a month</td></tr>
    <tr><td>Rinseless clean, about 2 litres a car</td><td class="n">3,120 litres a month</td></tr>
    <tr><th>Water saved</th><th class="n">2,30,880 litres a month</th></tr>
  </tbody>
</table>
<p>At 6,000 litres a tanker, that’s about <strong>38 tanker loads a month</strong> that a society doesn’t have to buy. You can try your own numbers in the <a href="{u('/#kx-societies')}">society estimate</a> on our homepage.</p>

<h2>Where our water comes from</h2>
<p>Our crew carries water in sealed cans. In societies, we can use a tap the association approves instead, and we log what we use every day. No hose pipes, ever.</p>

<div class="kx-note"><b>When does a car need more than 2 litres?</b> After a road trip, the first rains or a lot of mud, a rinseless wipe isn’t enough. That’s what the doorstep foam wash is for: thick foam, a two-bucket mitt wash and a low-flow rinse, still about 20 litres in total.</div>
""",
    },
    {
        "slug": "rats-in-car-engine-bay",
        "tag": "Protection",
        "icon": "shield",
        "title": "Rats in the engine bay: the warning signs and how to protect a parked car",
        "short": "Rats in the engine bay",
        "desc": "A car parked near a garden, drain or open plot is a warm, quiet place for a rat. Here’s what to look for and how a monthly repellent treatment helps.",
        "body": f"""
<p>Ask around any Bengaluru society and someone will have a story. The car wouldn’t start, a warning light came on, and the mechanic found chewed wires and a nest of shredded paper on top of the engine.</p>
<p>A parked car is a warm, sheltered spot, and modern wiring is easy to chew through. Cars that sit near gardens, drains or open plots are the most likely to get visitors.</p>

<h2>Signs a rat has been in your car</h2>
<ul>
  <li>Droppings on the engine cover, battery or under the bonnet</li>
  <li>Bits of paper, cloth, leaves or plastic collected in a corner of the engine bay</li>
  <li>Chewed rubber, insulation or wire covering</li>
  <li>A new warning light on the dashboard, or a car that suddenly won’t start</li>
  <li>A bad smell through the AC vents</li>
  <li>Small footprints in the dust on the bonnet or windscreen</li>
</ul>
<p>If you see chewed wires or a warning light, take the car to your mechanic before driving it far. Damaged wiring can affect sensors, lights and starting.</p>

<h2>Simple things that help</h2>
<ul>
  <li>Don’t leave food, wrappers or pet food in the car or near where it’s parked.</li>
  <li>Drive the car regularly if you can. A car that sits for days is more inviting than one that moves every morning.</li>
  <li>Keep the area around the parking spot free of rubbish and loose cardboard.</li>
  <li>Open the bonnet and take a look every couple of weeks, especially after a long trip away.</li>
</ul>

<h2>What our rodent-repellent treatment does</h2>
<p>It takes about 30 minutes and starts from ₹399:</p>
<ol>
  <li>We check the engine bay for chewed wires and nests.</li>
  <li>A non-toxic repellent is sprayed on the wiring and hoses.</li>
  <li>Repellent tape goes around the wires rats chew most.</li>
  <li>We send a reminder on WhatsApp when it’s due again next month.</li>
</ol>
<p>Repellent wears off, so it works best as a monthly habit. It’s included every month on the <a href="{u('/#kx-plans')}">Daily Plus plan</a>, or you can book it on its own from our <a href="{u('/#kx-services')}">one-time services</a>.</p>

<div class="kx-note"><b>Your cleaner is also an early warning.</b> Every morning starts with a walk around the car before anything is touched. Anything new, like a mark, a soft tyre or droppings on the bonnet, gets a photo and a note on WhatsApp.</div>
""",
    },
    {
        "slug": "car-care-in-the-rains",
        "tag": "Seasonal",
        "icon": "rain",
        "title": "Rain, mud and damp smells: looking after your car through Bengaluru’s rainy months",
        "short": "Car care in the rains",
        "desc": "What happens to your daily clean when it pours, why the first rains are the time for a proper wash, and how to stop the cabin smelling damp.",
        "body": f"""
<p>Bengaluru rain doesn’t clean a car. It drops the dust that was in the air onto your paint, splashes mud up the sides and leaves water spots when it dries. And a car that’s wet inside for a few days starts to smell.</p>

<h2>What happens to your daily clean when it rains</h2>
<ul>
  <li><strong>Heavy rain:</strong> we wipe the glass and mirrors only, so you can see properly on the drive. The full clean moves to the end of your month, so you don’t lose it.</li>
  <li><strong>Light drizzle:</strong> the car is cleaned as usual.</li>
</ul>

<h2>Book a foam wash after the first rains</h2>
<p>The first heavy rain of the season brings down a lot of dust and leaves a muddy film low on the doors and in the wheel arches. A daily wipe isn’t meant to shift that. A doorstep foam wash is: thick foam soaks for five minutes, a two-bucket mitt wash goes over every panel, and the door edges, fuel lid and wheel arches get cleaned too. It takes 45 to 60 minutes, uses about 20 litres of water and starts from ₹499.</p>

<h2>Check your wipers before you need them</h2>
<p>Wiper blades harden in the summer heat and only show it when the rain starts. If they leave streaks or judder across the glass, replace them. Our cleaners note worn wiper blades in their morning walk-around photos, so you’ll usually hear about it before the first storm.</p>

<h2>Keep the cabin dry</h2>
<ul>
  <li>Take wet umbrellas and raincoats out of the car rather than leaving them on the floor.</li>
  <li>Lift the floor mats and let them dry if water has got under them.</li>
  <li>Run the AC for a few minutes before you park, which helps clear moisture.</li>
  <li>On a dry afternoon, leave the windows down for a while if the car is somewhere safe.</li>
</ul>

<h2>If the car already smells damp</h2>
<p>Air fresheners only cover the smell. Our <a href="{u('/#kx-services')}">ozone odour treatment</a> deals with it: the cabin is vacuumed and the source cleaned, an ozone generator runs in the closed car for 30 minutes, and the car is aired out for 15 minutes before anyone gets in. It takes about 45 minutes and starts from ₹699. If the seats or carpet are soaked, the interior deep clean shampoos and extracts the fabric and then leaves the car to dry with the windows down.</p>
""",
    },
    {
        "slug": "daily-car-cleaning-for-apartment-societies",
        "tag": "Societies",
        "icon": "building",
        "title": "How to bring daily car cleaning to your apartment society",
        "short": "Daily car cleaning for your society",
        "desc": "A guide for association members and facility managers: what to agree on, what to ask any car cleaning vendor, and how a free demo morning works.",
        "body": f"""
<p>In most societies, car cleaning happens informally. A few cleaners come and go, nobody knows exactly who is in the basement at 5 AM, and the association hears about it only when something goes wrong.</p>
<p>A single, organised crew solves most of that. Here’s how to set it up, whether you work with us or not.</p>

<h2>What to agree on first</h2>
<ul>
  <li><strong>A fixed morning window</strong>, so security knows when to expect the crew.</li>
  <li><strong>Where the crew signs in</strong>, every day, in the gate register.</li>
  <li><strong>The water source</strong>: an approved tap, or the vendor’s own cans. No hose pipes in the basement.</li>
  <li><strong>How keys are handled</strong> on interior days, and who logs them.</li>
  <li><strong>Who residents complain to</strong>, and how fast complaints should be closed.</li>
</ul>

<h2>Questions to ask any vendor</h2>
<ul>
  <li>Are the cleaners police-verified, and can we see their documents?</li>
  <li>Do they wear a uniform and carry photo ID?</li>
  <li>Is there a named supervisor the facility manager can call?</li>
  <li>What products do they use? Kerosene, diesel or washing powder should be a no.</li>
  <li>How much water does each car use, and where does it come from?</li>
  <li>Will they share insurance details and timings before the first wash?</li>
  <li>Will the association get a regular report on attendance and complaints?</li>
</ul>

<h2>How we start in a new society</h2>
<ol>
  <li><strong>We meet your association.</strong> We walk your parking with the facility manager and agree on timings, a water point and where the crew signs in.</li>
  <li><strong>A free demo morning.</strong> We clean up to 10 residents’ cars for free, so people can judge the work before anyone pays.</li>
  <li><strong>Residents sign up in a minute.</strong> A QR poster in each lift lobby opens a WhatsApp chat. No app and no paper forms.</li>
  <li><strong>Daily service begins.</strong> The crew arrives at the agreed time every morning. Attendance and complaints go to your facility manager each month.</li>
</ol>

<h2>What it costs</h2>
<p>Society rates start at 25 cars. For a society on the Daily plan, residents pay 15% less than the standard price per car. We send a proposal with per-car prices, crew size and timings after the walk-through. You can get a rough idea with the <a href="{u('/#kx-societies')}">estimate on our homepage</a>.</p>

<div class="kx-note"><b>Do we need the association’s permission?</b> For basement work, yes, and we handle it. We share crew documents, insurance details and timings with your facility manager before the first wash.</div>
""",
    },
    {
        "slug": "what-not-to-use-on-your-car",
        "tag": "Paint care",
        "icon": "flask",
        "title": "Kerosene on tyres, washing powder on paint: what not to put on your car",
        "short": "What not to put on your car",
        "desc": "Some cleaning habits make a car look good for a day and age it for years. Here are the ones to stop, and what we use instead.",
        "body": f"""
<p>Ask a cleaner how they get tyres so black, and the honest answer is often kerosene. It looks great for a day. Over months, it’s one of the worst things you can put on a car.</p>

<h2>What to keep away from your car</h2>
<h3>Kerosene or diesel on tyres</h3>
<p>Petroleum solvents soften and dry out rubber. Tyres treated this way crack on the sidewalls sooner, and the oily residue flings onto the paint when you drive, leaving spots along the doors.</p>
<h3>Washing powder or dish soap on paint</h3>
<p>Household detergents are made to strip grease. On a car, they strip wax and sealant too, leaving the paint unprotected and dull. Many are also strongly alkaline, which isn’t kind to rubber seals or plastic trim.</p>
<h3>Ammonia glass cleaners on tinted windows</h3>
<p>Ammonia can damage tinted film and dry out the rubber around the glass.</p>
<h3>One cloth for everything</h3>
<p>The same rag on wheels, paint and glass moves brake dust and grit straight onto your paint and windscreen.</p>
<h3>Water jets in the engine bay</h3>
<p>Spraying water around electrical parts invites trouble. An engine bay should be cleaned dry.</p>

<h2>What we use instead</h2>
<table>
  <thead><tr><th>Job</th><th>What goes on</th></tr></thead>
  <tbody>
    <tr><td>Paint</td><td>pH-neutral rinseless shampoo, safe on wax, ceramic coatings and PPF</td></tr>
    <tr><td>Glass and mirrors</td><td>Ammonia-free cleaner and a waffle-weave cloth, safe on tinted film</td></tr>
    <tr><td>Tyres</td><td>Water-based, non-greasy dressing</td></tr>
    <tr><td>Dashboard and trim</td><td>Interior cleaner with UV protection</td></tr>
    <tr><td>Engine bay</td><td>Low-moisture degreaser, brushed in and wiped off, with electrical parts covered</td></tr>
  </tbody>
</table>

<div class="kx-note"><b>Switching from an old cleaner?</b> Tell your new cleaner what was used before. Tyres that have had kerosene for months may already be dry, and a proper dressing helps, but deep cracks mean it’s time to have the tyres checked.</div>

<p>You can see every product and tool our crew carries in the <a href="{u('/#kx-kit')}">kit section</a> on our homepage.</p>
""",
    },
]


def reading_time(body):
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return max(2, round(words / 220))


def post_card(p, lead=False, level="h2"):
    return f"""
    <article class="kx-post{' kx-post--lead' if lead else ''}" data-tag="{esc(p['tag'])}">
      <div class="kx-post__art" aria-hidden="true">{ICON[p['icon']]}</div>
      <div class="kx-post__b">
        <span class="kx-eyebrow">{esc(p['tag'])}</span>
        <{level}><a href="{u('/blog/' + p['slug'] + '/')}">{esc(p['title'])}</a></{level}>
        <p>{esc(p['desc'])}</p>
        <span class="kx-post__m">{reading_time(p['body'])} min read</span>
      </div>
    </article>"""


def build_blog_index():
    tags = []
    for p in POSTS:
        if p["tag"] not in tags:
            tags.append(p["tag"])
    chips = '<button type="button" data-tag="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" data-tag="{esc(t)}" aria-pressed="false">{esc(t)}</button>' for t in tags)
    cards = post_card(POSTS[0], lead=True) + "".join(post_card(p) for p in POSTS[1:])
    out = head("Car care blog | Kleen Xtar, Bengaluru",
               "Practical car care for Bengaluru: daily cleaning without scratches, saving water, rats in the engine bay, the rainy season and more.")
    out += nav("blog")
    out += phero("Car care, the Bengaluru way",
                 "Short, practical guides from the crew that cleans cars across the city before 7:15 every morning. Dust, rain, rats, water and what actually works.",
                 [("Home", "/"), ("Blog", None)])
    out += f"""
<section class="kx-page kx-page--sky">
  <div class="kx-wrap">
    <div class="kx-tags" role="group" aria-label="Filter by topic">{chips}</div>
    <div class="kx-posts">{cards}
    </div>
  </div>
</section>
"""
    out += band() + footer()
    write("blog", out)


def build_post(p, i):
    others = [q for q in POSTS if q is not p]
    related = [q for q in others if q["tag"] == p["tag"]] + [q for q in others if q["tag"] != p["tag"]]
    related = related[:3]
    ld = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": p["title"], "description": p["desc"],
        "datePublished": PUBLISHED, "author": {"@type": "Organization", "name": "Kleen Xtar"},
        "publisher": {"@type": "Organization", "name": "Kleen Xtar"},
    }
    extra = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n"
    out = head(p["title"] + " | Kleen Xtar", p["desc"], extra)
    out += nav("blog")
    out += phero(esc(p["title"]), None, [("Home", "/"), ("Blog", "/blog/"), (esc(p["short"]), None)])
    out = out.replace("</h1>", f"""</h1>
    <div class="kx-meta"><span>{esc(p['tag'])}</span><span><time datetime="{PUBLISHED}">{fmt_date(PUBLISHED)}</time></span><span>{reading_time(p['body'])} min read</span></div>""", 1)
    out += f"""
<section class="kx-page">
  <div class="kx-wrap kx-art">
    <article class="kx-prose">
      <p class="kx-lead" style="color:#C9D5E6;max-width:none">{esc(p['desc'])}</p>
{p['body']}
    </article>
    <aside class="kx-side" aria-label="Book a clean">
      <div class="kx-card">
        <h2>Wake up to a clean car</h2>
        <p>Daily doorstep cleaning from ₹649 a month. Your first wash is free.</p>
        <a class="kx-btn kx-btn--primary" href="{u('/#book')}">Book a free trial wash</a>
        <a class="kx-btn kx-btn--line-light" href="{u('/#kx-plans')}">See plans and prices</a>
      </div>
      <div class="kx-card">
        <h3>Got a question?</h3>
        <p>Ask us on WhatsApp. We reply between 7 AM and 10 PM.</p>
        <a class="kx-btn kx-btn--line-light" href="{esc(wa('Hi Kleen Xtar, I just read “' + p['short'] + '” on your blog and have a question.'))}" target="_blank" rel="noopener">{ICON['wa']}Chat on WhatsApp</a>
      </div>
    </aside>
  </div>
</section>

<section class="kx-more" aria-labelledby="kx-more-h">
  <div class="kx-wrap">
    <h2 class="kx-h2" id="kx-more-h">Keep reading</h2>
    <div class="kx-posts">{''.join(post_card(q, level='h3') for q in related)}
    </div>
  </div>
</section>
"""
    out += band() + footer()
    write("blog/" + p["slug"], out)


# ---------------------------------------------------------------- about
def build_about():
    vals = [
        ("person", "The same cleaner every morning", "One person looks after your car, knows where it’s parked and notices when something changes."),
        ("camera", "A photo, every time", "Two photos on WhatsApp after every clean, with the time and your cleaner’s name. You don’t have to go down to check."),
        ("cloth", "Gentle on paint", "Loose dust first, a rinseless shampoo, straight-line wiping and a fresh set of cloths for every car."),
        ("drop", "Water is precious here", "About 2 litres a car for a daily clean, carried in by our crew. No hose pipes and no runoff."),
        ("shield", "A crew you can trust", "Every cleaner is police-verified, trained for two weeks alongside a senior crew lead, and works in uniform with photo ID."),
        ("unlock", "No lock-in", "Plans run month to month. Pause by WhatsApp when you travel, cancel any time before your next billing date."),
    ]
    vcards = "".join(f'<div class="kx-card kx-val">{ICON[i]}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in vals)
    live = "".join(f"<li>{a}</li>" for a in LIVE_AREAS)
    soon = "".join(f'<li class="is-soon">{a}, starting soon</li>' for a in SOON_AREAS)
    out = head("About us | Kleen Xtar, Bengaluru",
               "Kleen Xtar cleans cars at the doorstep across Bengaluru every morning, before 7:15 AM, with about 2 litres of water and a photo on WhatsApp.")
    out += nav()
    out += phero("Clean cars before Bengaluru wakes up",
                 "Kleen Xtar is a doorstep car cleaning service for independent houses, villas and apartment societies. Our crews clean cars where they’re parked, between 4:45 and 7:15 every morning, and send a photo when it’s done.",
                 [("Home", "/"), ("About us", None)])
    out += f"""
<section class="kx-page">
  <div class="kx-wrap">
    <div class="kx-grid4">
      <div class="kx-card kx-stat"><b>~2 L</b><small>of water for a daily clean, carried in by our crew</small></div>
      <div class="kx-card kx-stat"><b>7:15</b><small>AM, by when your photo arrives on WhatsApp</small></div>
      <div class="kx-card kx-stat"><b>7</b><small>steps on every car, in the same order, every morning</small></div>
      <div class="kx-card kx-stat"><b>{len(LIVE_AREAS)}</b><small>Bengaluru areas covered every morning</small></div>
    </div>
  </div>
</section>

<section class="kx-page kx-page--sky" aria-labelledby="kx-why-h">
  <div class="kx-wrap kx-art">
    <div class="kx-prose">
      <h2 id="kx-why-h" style="margin-top:0">Why we do it this way</h2>
      <p>Most people in Bengaluru leave for work with a dusty car, or rely on a cleaner who turns up when they can, uses whatever is to hand and is gone before anyone can check. Some use kerosene on the tyres and a single rag for the whole car.</p>
      <p>We wanted the opposite: a clean you can count on every morning, done properly, without wasting water and without anyone having to wake up for it.</p>
      <p>So every daily clean follows the same seven steps. The cleaner walks around the car first and photographs anything new. Loose dust comes off before anything wet touches the paint. Glass, wheels and cabin each get their own cloth. And the morning ends with a photo on your phone, not a knock on your door.</p>
      <p>Everything runs on WhatsApp: photos, reminders, pauses and invoices. There’s no app to install.</p>
      <p><a href="{u('/#kx-process')}">Follow one morning, step by step</a></p>
    </div>
    <aside class="kx-side">
      <div class="kx-card">
        <h2>Who we clean for</h2>
        <p><b style="color:#fff">Independent houses</b>: porch or street parking, no doorbell, no puddle.</p>
        <p><b style="color:#fff">Villa communities</b>: every car in the driveway in one visit, with household pricing.</p>
        <p><b style="color:#fff">Apartment societies</b>: a dedicated crew in your basement, with your association’s approval.</p>
        <a class="kx-btn kx-btn--line-light" href="{u('/#kx-who')}">See how it works for you</a>
      </div>
    </aside>
  </div>
</section>

<section class="kx-page" aria-labelledby="kx-vals-h">
  <div class="kx-wrap">
    <div class="kx-sech"><h2 class="kx-h2" id="kx-vals-h">What you can count on</h2></div>
    <div class="kx-grid3">{vcards}</div>
  </div>
</section>

<section class="kx-page kx-page--sky" aria-labelledby="kx-where-h">
  <div class="kx-wrap">
    <div class="kx-sech">
      <h2 class="kx-h2" id="kx-where-h">Where we work</h2>
      <p class="kx-lead">Our crews cover these areas every morning. <a class="kx-link" href="{u('/#kx-areas')}">Check your PIN code</a>.</p>
    </div>
    <ul class="kx-chips">{live}{soon}</ul>
  </div>
</section>

<section class="kx-page" aria-labelledby="kx-join-h">
  <div class="kx-wrap kx-grid2">
    <div class="kx-card">
      <h2 id="kx-join-h">Want to work with us?</h2>
      <p>We’re always looking for careful, reliable people for our morning crews.</p>
      <a class="kx-btn kx-btn--line-light" href="{u('/careers/')}">Join our crew</a>
    </div>
    <div class="kx-card">
      <h2>Run a society or villa community?</h2>
      <p>We start every new society with a free demo morning for up to 10 residents’ cars.</p>
      <a class="kx-btn kx-btn--line-light" href="{u('/#kx-societies')}">Bring us to your society</a>
    </div>
  </div>
</section>
"""
    out += band() + footer()
    write("about", out)


# ---------------------------------------------------------------- careers
def build_careers():
    apply_msg = "Hi Kleen Xtar, I’d like to join your crew.\nName:\nArea I live in:\nRole I’m interested in:\nExperience (if any):"
    roles = [
        ("Morning cleaner", "Full time, early mornings",
         "Clean the same set of cars every morning, in houses, villas or a society basement.",
         ["Follow our seven-step clean on every car",
          "Walk around each car first and photograph anything new",
          "Send two photos to each customer on WhatsApp after every clean",
          "Keep your kit clean and your cloths sorted by colour",
          "Be on time, every day. Customers count on it"]),
        ("Crew lead", "Full time",
         "Run a crew in an apartment society and be the named supervisor the facility manager calls.",
         ["Train new cleaners alongside you for their first two weeks",
          "Make sure the crew signs the gate register every morning",
          "Handle re-clean requests and complaints quickly",
          "Check work quality and keep attendance",
          "Experience in car cleaning or leading a team helps"]),
        ("Detailing technician", "Full time, daytime",
         "Do our deeper services at customers’ doorsteps: foam washes, interior deep cleans, polish and protection.",
         ["Foam washes, interior shampoo and extraction",
          "Machine polish, wax and sealant",
          "Headlight restoration and engine bay dry cleans",
          "Experience with a machine polisher is a plus",
          "We’ll train you on our methods and products"]),
    ]
    rcards = "".join(f"""
      <div class="kx-card kx-job">
        <span class="kx-job__tag">{tag}</span>
        <h3>{t}</h3>
        <p>{d}</p>
        <ul>{''.join(f'<li>{x}</li>' for x in li)}</ul>
        <a class="kx-btn kx-btn--primary" href="{esc(wa(apply_msg.replace('Role I’m interested in:', 'Role I’m interested in: ' + t)))}" target="_blank" rel="noopener">{ICON['wa']}Apply on WhatsApp</a>
      </div>""" for t, tag, d, li in roles)
    perks = [
        ("clock", "Your day starts early and ends early", "Daily cleans happen between 4:45 and 7:15 AM, so most of the day is your own."),
        ("person", "Two weeks of paid training", "You work alongside a senior crew lead until you’re confident on every step."),
        ("shield", "Uniform and photo ID", "You’ll look professional and customers and security will know who you are."),
        ("flask", "Proper kit and products", "Colour-coded microfibre, two buckets, a cordless vacuum and safe products. No kerosene, ever."),
        ("camera", "Your work gets seen", "Customers see your photos every morning and many rate the wash on WhatsApp."),
        ("building", "Steady routes", "The same cars, at the same time, close to where you work."),
    ]
    pcards = "".join(f'<div class="kx-card kx-val">{ICON[i]}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in perks)
    out = head("Join our crew | Careers at Kleen Xtar, Bengaluru",
               "Work with Kleen Xtar as a morning car cleaner, crew lead or detailing technician in Bengaluru. Apply on WhatsApp.")
    out += nav()
    out += phero("Join our morning crew",
                 "We clean cars across Bengaluru before the city wakes up. If you’re reliable, careful and like an early start, we’d like to meet you.",
                 [("Home", "/"), ("Join our crew", None)])
    out = out.replace('<p class="kx-lead">We clean', '<p class="kx-lead">We clean', 1)
    out += f"""
<section class="kx-page" aria-labelledby="kx-roles-h">
  <div class="kx-wrap">
    <div class="kx-sech">
      <h2 class="kx-h2" id="kx-roles-h">Open roles</h2>
      <p class="kx-lead">Tell us your name, the area you live in and the role you want. We’ll reply on WhatsApp.</p>
    </div>
    <div class="kx-grid3">{rcards}
    </div>
  </div>
</section>

<section class="kx-page kx-page--sky" aria-labelledby="kx-perks-h">
  <div class="kx-wrap">
    <div class="kx-sech"><h2 class="kx-h2" id="kx-perks-h">What working with us is like</h2></div>
    <div class="kx-grid3">{pcards}</div>
  </div>
</section>

<section class="kx-page" aria-labelledby="kx-hire-h">
  <div class="kx-wrap">
    <div class="kx-sech"><h2 class="kx-h2" id="kx-hire-h">How hiring works</h2></div>
    <ol class="kx-steps-list">
      <li><b>Message us</b><span>Send your name, area and the role you want on WhatsApp.</span></li>
      <li><b>Meet us</b><span>A short chat and a look at how you work with a car.</span></li>
      <li><b>Verification</b><span>We do a police verification for every member of our crew.</span></li>
      <li><b>Training</b><span>Two weeks alongside a senior crew lead, then your own route.</span></li>
    </ol>
  </div>
</section>
"""
    out += band("Ready to start?", "Message us on WhatsApp with your name and area. We reply between 7 AM and 10 PM.").replace(
        f'<a class="kx-btn kx-btn--primary" href="{u("/#book")}">Book a free trial wash</a>',
        f'<a class="kx-btn kx-btn--primary" href="{esc(wa(apply_msg))}" target="_blank" rel="noopener">Apply on WhatsApp</a>').replace(
        f'href="{esc(wa("Hi Kleen Xtar, I’d like to book a free trial wash."))}" target="_blank" rel="noopener">{ICON["wa"]}Chat on WhatsApp',
        f'href="{PHONE_HREF}">Call {PHONE_TEXT}')
    out += footer()
    write("careers", out)


# ---------------------------------------------------------------- legal
DRAFT = ('<div class="kx-draft" role="note"><span>⚠</span><span><b>Draft for review.</b> This page is written from how '
         'the service works on our website. Have it checked by a lawyer before launch, and fill in the items marked '
         '[to confirm].</span></div>')


def legal_page(slug, title, lead, desc, sections):
    toc = "".join(f'<li><a href="#{sid}">{t}</a></li>' for sid, t, _ in sections)
    body = "".join(f'<h2 id="{sid}">{t}</h2>\n{b}\n' for sid, t, b in sections)
    out = head(f"{title} | Kleen Xtar", desc)
    out += nav()
    out += phero(title, lead, [("Home", "/"), (title, None)])
    out += f"""
<section class="kx-page">
  <div class="kx-wrap kx-art">
    <div class="kx-prose">
      {DRAFT}
      <p><b style="color:#fff">Last updated:</b> {fmt_date(PUBLISHED)}</p>
{body}
    </div>
    <aside class="kx-side" aria-label="On this page">
      <div class="kx-card">
        <h2>On this page</h2>
        <ul class="kx-toc">{toc}</ul>
      </div>
      <div class="kx-card">
        <h3>Questions?</h3>
        <p>Message us on WhatsApp or call {PHONE_TEXT}.</p>
        <a class="kx-btn kx-btn--line-light" href="{esc(wa('Hi Kleen Xtar, I have a question about your ' + title.lower() + '.'))}" target="_blank" rel="noopener">{ICON['wa']}Chat on WhatsApp</a>
      </div>
    </aside>
  </div>
</section>
"""
    out += footer()
    write(slug, out)


def build_terms():
    S = [
        ("about", "About these terms", "<p>These terms apply when you book a free trial, a monthly plan or a one-time service with Kleen Xtar [registered business name and address, to confirm] in Bengaluru. By booking, you agree to them. We’ll tell you on WhatsApp before we change anything that affects your plan.</p>"),
        ("service", "Our service", "<ul><li>We clean your car where it’s parked: in your porch, on the street outside your gate, in your driveway or in your society’s parking.</li><li>Daily cleans happen between 4:45 and 7:15 AM, depending on your area. Your cleaner keeps roughly the same time every day.</li><li>After every clean, we send two photos on WhatsApp.</li><li>What each plan includes is listed on our <a href=\"" + u('/#kx-plans') + "\">plans section</a>. Daily cleans run Monday to Saturday.</li></ul>"),
        ("trial", "Free trial wash", "<p>Your first wash is free, one per household or car [to confirm]. There’s no obligation to buy a plan afterwards.</p>"),
        ("billing", "Plans, prices and payment", "<ul><li>Prices are per car, per month, and depend on car type. They’re shown on our website at the time you book.</li><li>Plans run month to month. There’s no lock-in period and no deposit.</li><li>Paying every 3 months saves 10%.</li><li>For more than one car at the same home, the second car is 10% off and every car after that is 15% off.</li><li>You can pay by UPI autopay, card or net banking. You get a GST invoice every month on WhatsApp and email.</li><li>Society rates start at 25 cars and are agreed in a written proposal with your association.</li></ul>"),
        ("pause", "Pausing, skipping and cancelling", "<ul><li>Send “pause” on WhatsApp with your dates. Paused and skipped days move to the end of your billing month, up to 15 days a month.</li><li>You can cancel any time before your next billing date. Your plan runs to the end of the month you’ve paid for. [Refunds for unused days, to confirm.]</li></ul>"),
        ("rain", "Rain days", "<p>On heavy rain days we wipe the glass and mirrors only, and the full clean moves to the end of your month. Light drizzle days are cleaned as usual.</p>"),
        ("reclean", "If you’re not happy with a wash", "<p>Send a photo on WhatsApp before 10 AM. Your cleaner comes back the same day and cleans it again at no charge. On the Alternate days plan, a re-clean happens on the next visit; on Daily Plus, within 4 hours.</p>"),
        ("keys", "Keys and access", "<ul><li>We only need your key on interior days. You can leave it with security, your housekeeper or in a lockbox.</li><li>Keys go into a sealed pouch and every handover is logged with the time.</li><li>You’re responsible for making sure our crew is allowed into your parking area. For societies, we arrange access with the association.</li></ul>"),
        ("car", "Your car", "<ul><li>Before the first clean, our cleaner walks around the car and photographs existing marks, scratches and dents. We do the same whenever we notice something new.</li><li>Please remove valuables from the car before interior days. [Liability for items left in the car, to confirm.]</li><li>If you believe we caused damage, tell us on WhatsApp within [24 hours, to confirm] with photos. We’ll look into it and reply in writing. [Liability limits and insurance cover, to confirm.]</li></ul>"),
        ("contact", "Contact", f"<p>WhatsApp or call <a href=\"{PHONE_HREF}\">{PHONE_TEXT}</a>. We reply between 7 AM and 10 PM. [Registered address and email, to confirm.]</p><p>These terms are governed by the laws of India, and courts in Bengaluru have jurisdiction [to confirm].</p>"),
    ]
    legal_page("terms", "Terms of service",
               "The plain-language rules for booking and using Kleen Xtar.",
               "Terms of service for Kleen Xtar doorstep car cleaning in Bengaluru: plans, payment, pausing, rain days, re-cleans and keys.", S)


def build_privacy():
    S = [
        ("who", "Who we are", "<p>Kleen Xtar [registered business name and address, to confirm] provides doorstep car cleaning in Bengaluru. This page explains what personal data we collect, why, and what you can ask us to do with it, in line with India’s Digital Personal Data Protection Act, 2023.</p>"),
        ("collect", "What we collect", "<ul><li><b>Contact details:</b> your name and phone number, and email if you give it for invoices.</li><li><b>Where your car is:</b> your address, area or PIN code, society name and parking spot.</li><li><b>Your car:</b> make, model, type and registration number [to confirm].</li><li><b>Photos:</b> photos of your car taken before and after each clean, and of any marks or issues we notice.</li><li><b>Messages:</b> your WhatsApp chats with us, including pause requests, ratings and complaints.</li><li><b>Payments:</b> your plan, invoices and payment status. Card and bank details are handled by our payment provider; we don’t store them.</li><li><b>Key handovers:</b> times and who handed over your key, on interior days.</li></ul>"),
        ("why", "Why we use it", "<ul><li>To schedule and carry out your cleans, and to send you photos and reminders.</li><li>To bill you and send GST invoices.</li><li>To handle re-cleans, complaints and damage reports.</li><li>To share monthly service reports with your society’s facility manager, if you’re on a society plan. These show cars cleaned and complaints, not your payment details.</li><li>To tell you about changes to your plan or our service. We’ll only send marketing messages if you agree, and you can stop them any time.</li></ul>"),
        ("share", "Who we share it with", "<ul><li><b>Your cleaner and crew lead</b>, who need your car details, parking spot and WhatsApp to do the job.</li><li><b>WhatsApp (Meta)</b>, which carries our messages and photos.</li><li><b>Our payment provider</b> [name, to confirm], to process payments.</li><li><b>Your society’s security or facility manager</b>, for gate access and key logs.</li><li>Authorities, if the law requires it.</li></ul><p>We don’t sell your personal data.</p>"),
        ("keep", "How long we keep it", "<p>We keep your details while you’re a customer and for [period, to confirm] afterwards, or longer where tax and accounting law requires us to keep invoices. Car photos are kept for [period, to confirm].</p>"),
        ("rights", "Your rights", "<p>You can ask us to:</p><ul><li>tell you what personal data we hold about you,</li><li>correct anything that’s wrong or out of date,</li><li>delete your data when you stop using our service, unless we have to keep it by law,</li><li>stop sending you marketing messages.</li></ul><p>Send your request on WhatsApp and we’ll reply within [30 days, to confirm]. If you’re not satisfied with our answer, you can complain to the Data Protection Board of India.</p>"),
        ("security", "Keeping it safe", "<p>Only the people who need your details to serve you can see them. Keys are kept in sealed pouches with every handover logged. [Describe where data is stored and who has access, to confirm.]</p>"),
        ("contact", "Contact", f"<p>For anything about your data, message or call <a href=\"{PHONE_HREF}\">{PHONE_TEXT}</a>. [Grievance officer name and email, to confirm.]</p>"),
    ]
    legal_page("privacy", "Privacy policy",
               "What we collect when you book with us, why, and how to ask us to change or delete it.",
               "How Kleen Xtar collects and uses personal data for doorstep car cleaning in Bengaluru.", S)


def sync_css():
    """Copy the homepage's inline <style> to assets/kx.css so inner pages always match it."""
    with open(os.path.join(SITE_DIR, "index.html"), encoding="utf-8") as f:
        css = re.search(r"<style>(.*?)</style>", f.read(), re.S).group(1)
    with open(os.path.join(SITE_DIR, "assets", "kx.css"), "w", encoding="utf-8") as f:
        f.write(css.strip() + "\n")
    print("synced test/assets/kx.css from the homepage")


if __name__ == "__main__":
    sync_css()
    build_blog_index()
    for i, p in enumerate(POSTS):
        build_post(p, i)
    build_about()
    build_careers()
    build_terms()
    build_privacy()
