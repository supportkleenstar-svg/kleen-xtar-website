#!/usr/bin/env python3
"""
Build the v2 "service" variation of the test homepage at test/v2/.

v2 is the trustworthy, daylight version for a service business:
white and light grey-blue sections, the logo's royal blue used only
for actions and accents, deep navy for text and for the header, hero
and footer (the logo has white lettering, so it needs a dark band).
No glow, sparkles, glass or neon.

It starts from test/index.html, removes the dark colour layers (keeping
the layout rules they carry) and adds the service theme, so content
changes made to the main page carry over:

    python3 tools/build_v2.py
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "test", "index.html")
OUT = os.path.join(REPO, "test", "v2", "index.html")


def cut(s, start, end):
    """Remove s[start:end) where start/end are marker strings; end is kept."""
    a = s.index(start)
    b = s.index(end, a)
    return s[:a] + s[b:]


SERVICE_CSS = """
/* =====================================================================
   v2 service theme: white, logo royal blue, navy
   ===================================================================== */
html,body{background:#fff}
.kx{
  color-scheme:light;
  --kx-brand:#0060F0; --kx-brand-2:#004ED0; --kx-navy:#0B1F44; --kx-navy-2:#0F2C62; --kx-soft:#7CC4FF;
  --kx-predawn:#0B1F44; --kx-night:#08172F; --kx-indigo:#123063;
  --kx-marigold:#0060F0; --kx-marigold-2:#004ED0; --kx-peach:#7CC4FF;
  --kx-rinse:#0060F0; --kx-rinse-ink:#0047B3; --kx-charcoal:#3C4566;
  --kx-sky:#F4F8FD; --kx-sky-2:#E9F1FB; --kx-foam:#FFFFFF;
  --kx-ink:#0F1B2D; --kx-slate:#4B5A70;
  --kx-line:#E2E9F2; --kx-line-2:#C9D6E6;
  --kx-on-dark:#FFFFFF; --kx-on-dark-2:#C5D3E8; --kx-line-dark:rgba(255,255,255,.16);
  --kx-ok:#0E8F5B; --kx-err:#C23B2B;
  --kx-fill:#0B1F44; --kx-on:#FFFFFF; --kx-card:#FFFFFF;
  --kx-shadow:0 18px 40px -24px rgba(15,40,90,.35);
  background:#fff; color:var(--kx-ink);
}

/* type: plain, readable, sentence case */
.kx :where(h1,h2,h3,h4),.kx-h{font-family:var(--kx-font)}
.kx-h1,.kx-h2{font-style:normal;text-transform:none;font-weight:760;font-stretch:84%;letter-spacing:-.012em;line-height:1.02}
.kx-h1{font-size:clamp(2.6rem,5.4vw,4.6rem)}
.kx-h2{font-size:clamp(2rem,3.8vw,3.2rem)}
.kx-grad{background:none;-webkit-text-fill-color:currentColor;color:var(--kx-soft);filter:none;animation:none;padding:0}
.kx-tagline{font-family:var(--kx-font);font-style:normal;letter-spacing:.02em;color:var(--kx-on-dark-2)}
.kx-head .kx-h2::after{content:"";display:block;width:56px;height:4px;margin-top:18px;border-radius:2px;background:var(--kx-brand)}
.kx-sec--night .kx-head .kx-h2::after,.kx-proc .kx-head .kx-h2::after{background:var(--kx-soft)}
.kx-link{color:var(--kx-rinse-ink)}
.kx-sec--night .kx-link,.kx-proc .kx-link,.kx-hero .kx-link{color:var(--kx-soft)}

/* buttons: solid brand blue, no glow */
.kx-btn--primary,.kx-btn--primary:hover{background:var(--kx-brand);color:#fff;text-shadow:none;box-shadow:0 8px 20px -10px rgba(0,70,200,.6)}
.kx-btn--primary:hover{background:var(--kx-brand-2)}
.kx-btn--line{border-color:var(--kx-line-2);color:var(--kx-ink)}
.kx-btn--line:hover{border-color:var(--kx-brand);color:var(--kx-brand)}
.kx-btn--line-light{border-color:rgba(255,255,255,.55);color:#fff;background:transparent}
.kx-btn--line-light:hover{border-color:#fff;background:rgba(255,255,255,.08)}
.kx-pf .kx-btn--line-light,.kx-sec--sky .kx-btn--line-light,.kx-sec--foam .kx-btn--line-light,.kx-mbar .kx-btn--line-light{border-color:var(--kx-line-2);color:var(--kx-ink)}
.kx-pf .kx-btn--line-light:hover,.kx-sec--sky .kx-btn--line-light:hover,.kx-sec--foam .kx-btn--line-light:hover{border-color:var(--kx-brand);color:var(--kx-brand);background:transparent}
.kx-btn--ink{background:var(--kx-navy);color:#fff}
.kx-btn--ink:hover{background:#123063}
.kx-fab{background:var(--kx-brand);color:#fff;box-shadow:0 10px 24px -8px rgba(0,70,200,.55)}

/* header */
.kx-nav.is-solid,.kx-nav.is-menu{background:var(--kx-navy);-webkit-backdrop-filter:none;backdrop-filter:none;box-shadow:0 1px 0 rgba(255,255,255,.08),0 8px 24px -12px rgba(0,0,0,.45)}
.kx-nav__links a{color:rgba(255,255,255,.82)}
.kx-nav__links a:hover{color:#fff}
.kx-nav__links a.is-on::after{background:var(--kx-soft);box-shadow:none}
.kx-mnav{background:var(--kx-navy)}
.kx-burger span{background:#fff}

/* hero: navy band for the logo */
.kx-hero{background:linear-gradient(180deg,#0B1F44 0%,#0F2C62 100%)}
.kx-hero::after{display:none}
.kx-hello{color:var(--kx-soft)}
.kx-hero__sub{color:var(--kx-on-dark-2)}
.kx-facts{color:#DCE6F4}
.kx-facts svg{color:var(--kx-soft)}
.kx-wipe,.kx-pstage{box-shadow:0 24px 60px -28px rgba(0,0,0,.55)}
.kx-squeegee{background:var(--kx-navy);box-shadow:0 0 0 2px #fff}
.kx-squeegee i{box-shadow:none}
.kx-notify,.kx-pnote{background:#fff;color:var(--kx-ink);box-shadow:0 18px 40px -18px rgba(0,0,0,.45)}
.kx-wipe__hint,.kx-tool{background:#fff;color:var(--kx-ink)}
.kx-step__time{color:var(--kx-soft)}
.kx-plan--feat .kx-ticks svg,.kx-sec--night .kx-ticks svg{color:var(--kx-soft)}

/* service strip under the hero */
.kx-pillars{background:#fff;border-bottom:1px solid var(--kx-line);box-shadow:0 10px 30px -24px rgba(15,40,90,.4)}
.kx-pillar{color:var(--kx-ink)}
.kx-pillar:hover{background:var(--kx-sky)}
.kx-pillar+.kx-pillar::before{width:1px;background:var(--kx-line);box-shadow:none}
.kx-pillar svg{color:var(--kx-brand);filter:none}
.kx-pillar b{font-family:var(--kx-font);font-style:normal;text-transform:none;letter-spacing:0;font-size:1.0625rem;font-weight:700}
.kx-pillar small{color:var(--kx-slate)}
@media (max-width:640px){.kx-pillar b{font-size:.875rem;letter-spacing:0}}

/* bands */
.kx-proc{background:var(--kx-navy)}
@media (max-width:980px){.kx .kx-proc__sticky{background:var(--kx-navy)}}
.kx-sec--night{background:var(--kx-navy)}
.kx-sec--night,.kx-proc{--kx-marigold:#7CC4FF;--kx-rinse:#7CC4FF}

/* cards */
.kx-plan{background:#fff}
.kx-plan,.kx-rev__card,.kx-tab,.kx-panel,.kx-svc__detail,.kx-kit__panel,.kx-house{box-shadow:0 1px 2px rgba(15,40,90,.06),0 12px 32px -22px rgba(15,40,90,.28)}
.kx-plan--feat{background:var(--kx-navy);color:#fff;border-color:var(--kx-navy);box-shadow:0 24px 50px -24px rgba(11,31,68,.6)}
.kx-tab[aria-selected="true"]{border-color:var(--kx-brand);box-shadow:inset 0 0 0 1px var(--kx-brand)}
.kx-qa__q i::before,.kx-qa__q i::after{background:var(--kx-navy)}
.kx-qa.is-open .kx-qa__q i::before,.kx-qa.is-open .kx-qa__q i::after{background:#fff}

/* interactions, kept calm */
.kx-glow{transition:border-color .2s,transform .2s,box-shadow .2s}
.kx-glow:hover{border-color:#9DBEF0}
.kx .kx-plan.kx-glow:hover,.kx .kx-rev__card.kx-glow:hover{transform:translateY(-3px);box-shadow:0 22px 44px -22px rgba(15,40,90,.4)}
.kx .kx-plan--feat.kx-glow:hover{border-color:var(--kx-navy)}
.kx-js .kx-rv{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}
.kx-js .kx-rv.is-in{opacity:1;transform:none}

/* closing band and footer */
.kx-cta{background:linear-gradient(180deg,#0B1F44,#0F2C62);padding:88px 0 96px}
.kx-cta__star{display:none}
.kx-foot{background:var(--kx-night);border-top:0}
.kx-mbar{background:#fff;-webkit-backdrop-filter:none;backdrop-filter:none;box-shadow:0 -1px 0 var(--kx-line),0 -8px 24px -12px rgba(15,40,90,.25)}

/* ---------- problem finder ---------- */
.kx-pf{background:var(--kx-sky)}
.kx-pf__grid{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.25fr);gap:28px;align-items:start}
.kx-pf__list{display:grid;gap:10px}
.kx-pf__item{display:flex;align-items:center;gap:14px;width:100%;padding:14px 16px;border-radius:var(--kx-r-md);border:1.5px solid var(--kx-line);background:#fff;color:var(--kx-ink);text-align:left;cursor:pointer;box-shadow:0 1px 2px rgba(15,40,90,.05)}
.kx-pf__item:hover{border-color:#9DBEF0}
.kx-pf__item b{display:block;font-weight:650;font-size:1.0313rem;line-height:1.25}
.kx-pf__item small{display:block;margin-top:2px;color:var(--kx-slate);font-size:.875rem}
.kx-pf__ico{flex:none;display:grid;place-items:center;width:42px;height:42px;border-radius:12px;background:#EAF2FF;color:var(--kx-brand);transition:background .2s,color .2s}
.kx-pf__ico svg{width:22px;height:22px}
.kx-pf__item::after{content:"";margin-left:auto;flex:none;width:9px;height:9px;border-top:2px solid currentColor;border-right:2px solid currentColor;transform:rotate(45deg);opacity:.3;transition:opacity .2s,transform .2s}
.kx-pf__item[aria-selected="true"]{border-color:var(--kx-brand);box-shadow:inset 0 0 0 1px var(--kx-brand),0 12px 28px -18px rgba(0,70,200,.5)}
.kx-pf__item[aria-selected="true"] .kx-pf__ico{background:var(--kx-brand);color:#fff}
.kx-pf__item[aria-selected="true"]::after{opacity:1;color:var(--kx-brand);transform:translateX(3px) rotate(45deg)}
.kx-pf__panel{position:sticky;top:calc(var(--kx-nav-h) + 24px);padding:32px;border-radius:var(--kx-r-lg);background:#fff;border:1px solid var(--kx-line);border-top:4px solid var(--kx-brand);box-shadow:0 24px 60px -30px rgba(15,40,90,.4)}
.kx-pf__in{animation:kx-rise .35s ease both}
.kx-pf__tag{display:inline-flex;align-items:center;gap:8px;font-size:.8125rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--kx-brand)}
.kx-pf__tag svg{width:14px;height:14px}
.kx-pf__panel h3{margin-top:10px;font-size:clamp(1.6rem,2.6vw,2.1rem);font-weight:760;font-stretch:86%;line-height:1.05;color:var(--kx-ink)}
.kx-pf__panel p{margin-top:12px;color:var(--kx-slate);max-width:52ch}
.kx-ba{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:22px}
.kx-ba div{padding:14px 16px;border-radius:14px;font-size:.9375rem;line-height:1.4}
.kx-ba span{display:block;margin-bottom:6px;font-size:.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.kx-ba__b{background:#F7F9FC;border:1px dashed var(--kx-line-2);color:var(--kx-slate)}
.kx-ba__b span{color:#7A8799}
.kx-ba__a{background:#EAF2FF;border:1px solid #9DBEF0;color:var(--kx-ink)}
.kx-ba__a span{color:var(--kx-rinse-ink)}
.kx-pf__facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;margin-top:18px;border-radius:14px;overflow:hidden;background:var(--kx-line);border:1px solid var(--kx-line)}
.kx-pf__facts div{padding:12px 14px;background:#fff}
.kx-pf__facts small{display:block;font-size:.75rem;color:var(--kx-slate)}
.kx-pf__facts b{display:block;margin-top:2px;color:var(--kx-ink);font-weight:680;font-size:.9688rem;line-height:1.25}
.kx-pf__acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
@media (max-width:980px){
  .kx-pf__grid{grid-template-columns:1fr}
  .kx-pf__list{grid-auto-flow:column;grid-auto-columns:min(78%,300px);overflow-x:auto;scroll-snap-type:x mandatory;padding:2px 2px 10px;scrollbar-width:none}
  .kx-pf__list::-webkit-scrollbar{display:none}
  .kx-pf__item{scroll-snap-align:start}
  .kx-pf__item::after{display:none}
  .kx-pf__panel{position:static;padding:24px}
}
@media (max-width:640px){
  .kx-ba{grid-template-columns:1fr}
  .kx-pf__facts{grid-template-columns:1fr}
  .kx-pf__acts .kx-btn{flex:1 1 100%}
}
@media (prefers-reduced-motion:reduce){
  .kx-js .kx-rv{opacity:1;transform:none;transition:none}
  .kx-pf__in{animation:none}
}
"""


def main():
    s = open(SRC, encoding="utf-8").read()

    # drop the dark colour sections of the old theme layer, keep its layout rules
    s = cut(s, "/* buttons */\n", "/* nav and logo */\n")
    s = cut(s, "/* surfaces */\n", "/* process sky: night to electric blue */\n")
    s = cut(s, "/* chat */\n", "/* closing section */\n")
    # drop the glow theme layer entirely; v2 brings its own problem-finder styles
    i = s.index("Logo theme: chrome white")
    a = s.rindex("/*", 0, i)
    b = s.index("</style>", a)
    s = s[:a] + SERVICE_CSS + s[b:]

    s = s.replace('<meta name="theme-color" content="#000000">', '<meta name="theme-color" content="#0B1F44">', 1)
    s = s.replace(".kx-glow{background-image", ".kx-glow-off{background-image")  # no cursor spotlight in v2
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(s)
    print("wrote test/v2/index.html")


if __name__ == "__main__":
    main()
