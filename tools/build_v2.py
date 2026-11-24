#!/usr/bin/env python3
"""
Build the v2 colour variation of the test homepage at test/v2/.

v2 = royal-blue base (the deep blue of the logo) instead of black, frosted
glass cards, a sparkle pattern from the logo's star, swoosh light streaks
and bright cyan buttons with navy text.

It copies test/index.html and layers a theme over it, so content changes
made to the main page carry over:

    python3 tools/build_v2.py
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "test", "index.html")
OUT = os.path.join(REPO, "test", "v2", "index.html")

STARS = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E"
         "%3Cpath d='M24 12c.5 5 2 6.6 7 7.2-5 .6-6.5 2.2-7 7.2-.5-5-2-6.6-7-7.2 5-.6 6.5-2.2 7-7.2z' fill='%2330D8F0' fill-opacity='.16'/%3E"
         "%3Cpath d='M98 92c.3 2.6 1 3.4 3.6 3.7-2.6.3-3.3 1.1-3.6 3.7-.3-2.6-1-3.4-3.6-3.7 2.6-.3 3.3-1.1 3.6-3.7z' fill='%23ffffff' fill-opacity='.18'/%3E"
         "%3Ccircle cx='86' cy='30' r='1' fill='%23ffffff' fill-opacity='.22'/%3E"
         "%3Ccircle cx='40' cy='104' r='.9' fill='%2330D8F0' fill-opacity='.3'/%3E"
         "%3Ccircle cx='124' cy='62' r='.7' fill='%23ffffff' fill-opacity='.2'/%3E%3C/svg%3E\")")

CSS = """
/* =====================================================================
   v2: royal blue, glass, sparkles and swooshes
   ===================================================================== */
.kx{
  --kx-royal:#0A2A8C; --kx-royal-2:#061C66; --kx-navy:#03113F; --kx-cyan:#30D8F0;
  --kx-card:rgba(255,255,255,.06); --kx-line:rgba(255,255,255,.14); --kx-line-2:rgba(160,230,255,.32);
  --kx-on-dark-2:#C3D4F2; --kx-slate:#A9BEDD;
  --kx-stars:%(stars)s;
  --kx-swoosh:linear-gradient(163deg,transparent 44%%,rgba(48,216,240,.12) 48.5%%,rgba(255,255,255,.08) 49.2%%,transparent 53%%);
  background:var(--kx-navy); color:#EAF2FF;
}
body{background:#03113F}

/* surfaces */
.kx-hero{background:var(--kx-stars),radial-gradient(60%% 60%% at 80%% 40%%,rgba(48,216,240,.28),transparent 70%%),var(--kx-swoosh),linear-gradient(180deg,#03113F 0%%,#0A2A8C 100%%)}
.kx-hero::after{background:linear-gradient(90deg,transparent,#fff 40%%,#30D8F0 60%%,transparent);box-shadow:0 0 24px 3px rgba(48,216,240,.8)}
.kx-pillars{background:#061C66;border-bottom:1px solid rgba(255,255,255,.12)}
.kx-pillar:hover{background:rgba(48,216,240,.1)}
.kx-pillar+.kx-pillar::before{background:linear-gradient(180deg,transparent,#30D8F0,transparent)}
.kx-sec--sky{background:var(--kx-stars),var(--kx-swoosh),linear-gradient(180deg,#0A2A8C 0%%,#061C66 100%%)}
.kx-sec--foam,.kx-sec--night,.kx-pf{background:var(--kx-stars),radial-gradient(50%% 50%% at 90%% 0,rgba(48,216,240,.14),transparent 70%%),#03113F}
.kx-proc{background:#03113F}
@media (max-width:980px){.kx-proc__sticky{background:#03113F}}
.kx-cta{background:var(--kx-stars),radial-gradient(70%% 70%% at 50%% 100%%,rgba(48,216,240,.4),transparent 72%%),linear-gradient(180deg,#061C66,#0A2A8C)}
.kx-foot{background:#020B2C;border-top:1px solid rgba(48,216,240,.4)}
.kx-nav.is-solid,.kx-nav.is-menu{background:rgba(3,17,63,.88);box-shadow:0 1px 0 rgba(48,216,240,.4),0 10px 34px -18px rgba(48,216,240,.6)}
.kx-mnav{background:#03113F}
.kx-mbar{background:rgba(3,17,63,.95);box-shadow:0 -1px 0 rgba(48,216,240,.45)}

/* type: solid white headlines, accent runs white to cyan */
.kx-h1,.kx-h2{background:none;-webkit-text-fill-color:#fff;color:#fff;text-shadow:0 2px 24px rgba(0,40,140,.5)}
.kx-grad{background:linear-gradient(100deg,#fff 0%%,#9FEFFC 30%%,#30D8F0 60%%,#9FEFFC 80%%,#fff 100%%);background-size:220%% 100%%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 0 16px rgba(48,216,240,.55))}
.kx-lead,.kx-hero__sub{color:#C3D4F2}
.kx-hello,.kx-step__time,.kx-pf__tag,.kx-ba__a span,.kx-eyebrow{color:#30D8F0}
.kx-head .kx-h2::after,.kx-pf .kx-h2::after{background:linear-gradient(90deg,#fff,#30D8F0 50%%,transparent);box-shadow:0 0 14px rgba(48,216,240,.9)}

/* buttons: bright cyan, navy text */
.kx-btn--primary,.kx-btn--primary:hover{background:linear-gradient(180deg,#9FEFFC 0%%,#30D8F0 45%%,#00B4F0 100%%);color:#021047;text-shadow:none;box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 0 0 1px rgba(255,255,255,.35),0 10px 30px -8px rgba(48,216,240,.85)}
.kx-btn--primary:hover{box-shadow:inset 0 1px 0 rgba(255,255,255,.8),0 0 0 1px rgba(255,255,255,.6),0 12px 40px -4px rgba(48,216,240,1)}
.kx-btn--line-light{border-color:rgba(255,255,255,.45);color:#fff}
.kx-btn--line-light:hover,.kx-btn--line:hover{border-color:#30D8F0;background:rgba(48,216,240,.1)}
.kx-btn--ink{background:#fff;color:#021047}
.kx-fab{background:linear-gradient(180deg,#9FEFFC,#30D8F0 45%%,#00B4F0);color:#021047;box-shadow:0 0 30px rgba(48,216,240,.8)}
.kx-nav__links a{color:rgba(255,255,255,.82)}
.kx-nav__links a:hover{color:#9FEFFC}
.kx-nav__links a.is-on::after{background:#30D8F0;box-shadow:0 0 10px #30D8F0}
.kx-link{color:#9FEFFC}

/* glass cards */
.kx-tab,.kx-panel,.kx-kit__panel,.kx-svc__detail,.kx-rev__card,.kx-code div,.kx-bill,.kx-house,.kx-plan,.kx-pf__item,.kx-calc,.kx-phone{background-color:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.kx-house{background-color:rgba(2,12,50,.45)}
.kx-glow{background-image:radial-gradient(420px circle at var(--mx,-999px) var(--my,-999px),rgba(48,216,240,.18),transparent 45%%)}
.kx-glow:hover{border-color:rgba(48,216,240,.6)}
.kx-plan--feat{background:linear-gradient(180deg,rgba(48,216,240,.22),rgba(255,255,255,.06) 60%%);border-color:#30D8F0;box-shadow:0 0 0 1px rgba(48,216,240,.5),0 26px 70px -24px rgba(48,216,240,.8)}
.kx-tab[aria-selected="true"],.kx-pf__item[aria-selected="true"]{background-color:rgba(48,216,240,.14);border-color:#30D8F0;box-shadow:inset 0 0 0 1px rgba(48,216,240,.6),0 0 30px -10px rgba(48,216,240,.9)}
.kx-pf__ico{background:rgba(255,255,255,.08);color:#9FEFFC}
.kx-pf__item[aria-selected="true"] .kx-pf__ico{background:linear-gradient(180deg,#9FEFFC,#30D8F0 45%%,#00B4F0);color:#021047}
.kx-pf__item small{color:#A9BEDD}
.kx-pf__panel{background:linear-gradient(180deg,rgba(48,216,240,.16),rgba(3,17,63,.6) 60%%);border-color:rgba(48,216,240,.55);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
.kx-pf__facts{background:rgba(255,255,255,.14)}
.kx-pf__facts div{background:#05195A}
.kx-ba__b{background:rgba(0,0,0,.18);color:#A9BEDD}
.kx-ba__a{background:rgba(48,216,240,.14);border-color:rgba(48,216,240,.6)}
.kx-svc__item[aria-expanded="true"]{background:linear-gradient(90deg,rgba(48,216,240,.3),rgba(255,255,255,.04));color:#fff}
.kx-svc__item:hover{background:rgba(48,216,240,.1)}
.kx-table,.kx-table tbody tr{background:rgba(2,12,50,.5)}
.kx-stars{color:#30D8F0}

/* forms and overlays */
.kx-check,.kx-counter__ctl button,.kx-rev__nav button,.kx-fld input,.kx-fld select,.kx-fld textarea,.kx-opt,.kx-day,.kx-wk button,.kx-wap__opts button,.kx-notify-form input,.kx-search{background:rgba(2,12,50,.55);color:#F2F6FC;border-color:rgba(255,255,255,.18)}
.kx-opt[aria-pressed="true"],.kx-wap__opts button[aria-pressed="true"]{background:rgba(48,216,240,.16);border-color:#30D8F0;box-shadow:inset 0 0 0 1px #30D8F0}
.kx-sheet,.kx-wap{background:#061C66;box-shadow:0 0 0 1px rgba(48,216,240,.35),0 30px 90px -20px rgba(0,0,0,.6)}
.kx-sum{background:rgba(255,255,255,.07)}
.kx-x{background:rgba(255,255,255,.12)}
.kx-wap__h{background:#03113F}
.kx-wap__preview,.kx-msg--me{background:#0A3FC0}
.kx-modal{background:rgba(2,10,40,.7)}
.kx-map{background:radial-gradient(circle at 50%% 46%%,#0A3FC0,#03113F 74%%);box-shadow:0 0 0 1px rgba(48,216,240,.35)}
.kx-pin.is-soon .kx-dot{fill:#03113F}
"""


def main():
    s = open(SRC, encoding="utf-8").read()
    s = s.replace("</style>", (CSS % {"stars": STARS}) + "</style>", 1)
    s = s.replace('<meta name="theme-color" content="#000000">', '<meta name="theme-color" content="#03113F">', 1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(s)
    print("wrote test/v2/index.html")


if __name__ == "__main__":
    main()
