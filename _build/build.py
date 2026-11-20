# -*- coding: utf-8 -*-
"""Génère le site statique MH Event V2 (pages HTML à la racine du dépôt).
Lancer depuis la racine :  python3 _build/build.py"""
import os, re, json, html as H
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
IMG = "assets/img"
_dims = {}

def dims(name):
    if name not in _dims:
        p = f"{IMG}/{name}.webp"
        if not os.path.exists(p):
            raise SystemExit(f"Image manquante : {name}")
        _dims[name] = Image.open(p).size
    return _dims[name]

def img(name, alt, sizes="100vw", eager=False, cls=""):
    w, h = dims(name)
    mw, mh = Image.open(f"{IMG}/{name}-m.webp").size
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{IMG}/{name}-m.webp" srcset="{IMG}/{name}-m.webp {mw}w, {IMG}/{name}.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{H.escape(alt)}" {load} decoding="async">')

def ph(name, alt, shape="p", sizes="(min-width:960px) 45vw, 100vw", eager=False, pos=None):
    st = f' style="--pos:{pos}"' if pos else ""
    i = img(name, alt, sizes, eager)
    if pos:
        i = i.replace("<img ", f'<img style="object-position:{pos}" ', 1)
    return f'<div class="ph {shape}">{i}</div>'

def duo(front, alt_f, back, alt_b, rev=False):
    return (f'<div class="duo{" rev" if rev else ""}"><div class="b">{img(back, alt_b, "(min-width:960px) 30vw, 62vw")}</div>'
            f'<div class="f">{img(front, alt_f, "(min-width:960px) 34vw, 68vw")}</div></div>')

def esc(s):
    return H.escape(s, quote=True)

SITE = "https://tpepin74-cpu.github.io/mh-event/"
PHONE = "06 14 46 61 83"
TEL = "tel:+33614466183"
MAIL = "contact@mh-event.fr"

ICONS = {
 "hotels": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 17h16M5.5 17a6.5 6.5 0 0 1 13 0M12 10.5V8.8M10.4 8.6h3.2M3 20h18"/></svg>',
 "entreprises": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="7.5" width="17" height="12"/><path d="M9 7.5V5h6v2.5M3.5 12.5h17"/></svg>',
 "particuliers": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9.2" cy="13.6" r="5.4"/><circle cx="14.8" cy="13.6" r="5.4"/><path d="M8 5.6l1.2-1.6 1.2 1.6"/></svg>',
 "realisations": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5l7 8.5-7 8.5-7-8.5z"/><path d="M12 8.2l3.9 3.8-3.9 3.8-3.9-3.8z"/></svg>',
}
SOC = {
 "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/></svg>',
 "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4v11H3zM9.5 9.5h3.8v1.6h.06c.53-1 1.83-2 3.77-2 4.03 0 4.77 2.65 4.77 6.1v5.3h-4v-4.7c0-1.12-.02-2.56-1.56-2.56-1.56 0-1.8 1.22-1.8 2.48v4.78h-4z"/></svg>',
 "facebook": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.5H16l.4-3h-2.9V8.6c0-.87.25-1.46 1.5-1.46h1.6V4.46A21 21 0 0 0 14.27 4.3c-2.3 0-3.87 1.4-3.87 3.98v2.22H7.8v3h2.6V21z"/></svg>',
}
CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>'
DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M12 4v15M6 13l6 6 6-6"/></svg>'

# ---------------------------------------------------------------- gabarit commun
NAV = [
 ("index.html", "Accueil", []),
 ("entreprises.html", "Entreprises", [("entreprises-team-building.html", "Team building"), ("entreprises-hotes-hotesses.html", "Hôtes & hôtesses")]),
 ("hotels.html", "Hôtels", [("hotels-team-building.html", "Team building"), ("hotels-hotes-hotesses.html", "Hôtes & hôtesses")]),
 ("particuliers.html", "Particuliers", [("particuliers-mariages.html", "Mariages & privé"), ("particuliers-hotes-hotesses.html", "Hôtes & hôtesses")]),
 ("realisations.html", "Réalisations", []),
 ("agence-mathilde-heyral.html", "L'agence", []),
 ("blog.html", "Blog", []),
 ("contact.html", "Contact", []),
]
TABS = [("hotels", "hotels.html", "Hôtels"), ("entreprises", "entreprises.html", "Entreprise"),
        ("particuliers", "particuliers.html", "Particulier"), ("realisations", "realisations.html", "Réalisations")]

def head(title, desc, canon, extra=""):
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://mh-event.fr/{canon}">
<meta name="theme-color" content="#F6F1E8">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="MH Event">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{SITE}assets/img/og.jpg">
<link rel="icon" href="assets/img/favicon-48.png" type="image/png"><link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<link rel="preload" href="assets/fonts/cormorant-garamond-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/hanken-grotesk-latin-300-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/img/logo-bordeaux.webp" as="image">
<link rel="stylesheet" href="assets/css/mh.css">
<script>window.__mhT0=Date.now();(function(h){{h.classList.add("js");try{{if(!sessionStorage.getItem("mh-v")){{h.classList.add("ld-first");sessionStorage.setItem("mh-v","1")}}}}catch(e){{h.classList.add("ld-first")}}}})(document.documentElement)</script>
{extra}</head>'''

def header(light=False):
    return f'''<div class="loader" aria-hidden="true"><img src="assets/img/logo-bordeaux.webp" width="1000" height="626" alt=""></div>
<a class="skip" href="#main">Aller au contenu</a>
<header class="hdr{" light" if light else ""}">
 <div class="hdr-in">
  <button class="menu-btn" type="button" data-menu aria-controls="menu" aria-label="Ouvrir le menu"><i></i><b>Menu</b></button>
  <a class="logo" href="index.html" aria-label="MH Event, accueil"><img class="lw" src="assets/img/logo-pierre.webp" width="1000" height="626" alt="MH Event"><img class="lb" src="assets/img/logo-bordeaux.webp" width="1000" height="626" alt=""></a>
  <div class="hdr-r"><a href="contact.html">Contact</a><a class="btn" href="devis.html">Devis</a></div>
 </div>
</header>'''

def menu(cur):
    items = []
    for href, label, subs in NAV:
        ac = ' aria-current="page"' if href == cur or any(s[0] == cur for s in subs) else ""
        sub = ""
        if subs:
            sub = '<div class="m-sub">' + "".join(f'<a href="{h}">{l}</a>' for h, l in subs) + "</div>"
        items.append(f'<li><a href="{href}"{ac}>{label}</a>{sub}</li>')
    return f'''<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menu" aria-hidden="true">
 <div class="m-media"><video muted loop playsinline preload="none" data-src="assets/video/hero.mp4" poster="assets/img/hero-poster.jpg" aria-hidden="true"></video><img class="m-logo" src="assets/img/logo-pierre.webp" width="1000" height="626" alt=""></div>
 <div class="m-panel">
  <div class="m-top"><span class="label">MH Event · Nîmes, Aix, Marseille</span><button class="m-close" type="button" data-menu-close aria-label="Fermer le menu">{CLOSE}</button></div>
  <ul class="m-nav">{"".join(items)}</ul>
  <div class="m-foot"><a class="btn" href="devis.html">Demander un devis</a><a href="{TEL}">{PHONE}</a><a href="mailto:{MAIL}">{MAIL}</a></div>
 </div>
</div>'''

def tabbar(active):
    out = []
    for key, href, label in TABS:
        ac = ' aria-current="page"' if key == active else ""
        out.append(f'<a href="{href}"{ac}><span class="ic">{ICONS[key]}</span><span class="t">{label}</span></a>')
    return f'<nav class="tabbar" aria-label="Accès rapide">{"".join(out)}</nav>'

def footer():
    return f'''<footer class="ftr">
 <div class="wrap">
  <div class="ftr-top">
   <a class="ftr-logo" href="index.html" aria-label="MH Event, accueil"><img src="assets/img/logo-pierre.webp" width="1000" height="626" alt="MH Event" loading="lazy"></a>
   <div class="ftr-soc">
    <a href="https://www.instagram.com/mathilde_heyral_event/" target="_blank" rel="noopener" aria-label="Instagram MH Event">{SOC["instagram"]}</a>
    <a href="https://www.linkedin.com/company/mh-event-mathildeheyral/" target="_blank" rel="noopener" aria-label="LinkedIn MH Event">{SOC["linkedin"]}</a>
   </div>
  </div>
  <hr>
  <nav class="ftr-links" aria-label="Liens utiles"><a href="faq.html">FAQ</a><a href="realisations.html">Réalisations</a><a href="blog.html">Blog</a><a href="mentions-legales.html">Mentions légales</a></nav>
  <div class="ftr-bot"><span>© <span data-year>2026</span> MH Event · SAS HACHEVOT</span><a href="{TEL}">{PHONE}</a><a href="mailto:{MAIL}">{MAIL}</a><span>7 rue Tédenat, 30900 Nîmes</span></div>
 </div>
</footer>'''

CHAT = f'''<button class="chat-fab" type="button" data-chat aria-controls="chat">Concierge</button>
<div class="scrim" aria-hidden="true"></div>
<section class="chat" id="chat" role="dialog" aria-modal="false" aria-label="Concierge MH Event" aria-hidden="true">
 <div class="chat-head"><span class="av" aria-hidden="true"><img src="assets/img/sceau.webp" alt="" width="240" height="240"></span><div><b>Le concierge</b><span>répond à partir des contenus du site</span></div><button class="icon-btn" type="button" data-chat-close aria-label="Fermer le concierge">{CLOSE}</button></div>
 <div class="chat-log" aria-live="polite"></div>
 <div class="quick"></div>
 <form class="chat-form"><label class="sr" for="chat-in">Votre question</label><input class="input" id="chat-in" type="text" autocomplete="off" placeholder="Posez votre question…"><button class="btn" type="submit" aria-label="Envoyer"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button></form>
</section>'''

def page(fname, title, desc, body, cur=None, tab=None, light=False, bodycls="", extra_head="", after=""):
    canon = "" if fname == "index.html" else fname.replace(".html", "")
    cls = f' class="{bodycls}"' if bodycls else ""
    out = (head(title, desc, canon, extra_head) + f"\n<body{cls}>\n" + header(light) + "\n" + after +
           f'<main id="main">\n{body}\n</main>\n' + footer() + "\n" + menu(cur or fname) + "\n" + tabbar(tab) + "\n" + CHAT +
           '\n<script src="assets/js/mh.js" defer></script>\n<script src="assets/js/chat.js" defer></script>\n</body>\n</html>\n')
    open(fname, "w", encoding="utf-8").write(out)
    PAGES.append(fname)

PAGES = []

# ---------------------------------------------------------------- blocs
def hero_photo(name, alt, label, title, lead="", crumbs=None, pos=None, short=True, actions=""):
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Fil d\'Ariane">' + '<span aria-hidden="true">◆</span>'.join(f'<a href="{h}">{l}</a>' for h, l in crumbs) + "</nav>"
    i = img(name, alt, "100vw", eager=True)
    if pos:
        i = i.replace("<img ", f'<img style="object-position:{pos}" ', 1)
    ld = f'<p class="lead">{lead}</p>' if lead else ""
    return f'''<section class="hero{" short" if short else ""}">
 <div class="hero-media">{i}</div>
 <div class="hero-body">{cr}<p class="label">{label}</p><h1 class="t-xl">{title}</h1>{ld}{actions}</div>
 <a class="hero-down" href="#suite" aria-label="Découvrir la suite">{DOWN}</a>
</section>'''

def head_block(label, title, lead="", center=False, h="t-h2", tag="h2"):
    ld = f'<p class="lead fade">{lead}</p>' if lead else ""
    return f'<div class="stack{" center" if center else ""}"><p class="label fade">{label}</p><{tag} class="{h} fade">{title}</{tag}><div class="rule fade" aria-hidden="true"><i></i></div>{ld}</div>'

def rows(items):
    out = []
    for i, it in enumerate(items, 1):
        t, p = it[0], it[1]
        pr = f'<span class="pr">{it[2]}</span>' if len(it) > 2 and it[2] else '<span></span>'
        out.append(f'<li class="fade"><span class="n">{i:02d}</span><h3>{t}</h3><p>{p}</p>{pr}</li>')
    return '<ol class="rows">' + "".join(out) + "</ol>"

def doors(items, stag=True):
    out = []
    for i, (href, name, alt, title, p) in enumerate(items, 1):
        out.append(f'<a class="door" href="{href}">{ph(name, alt, "p", "(min-width:860px) 40vw, 100vw")}<div class="cap"><span class="n">{i:02d}</span><h3 class="t-h3">{title}</h3><p>{p}</p></div></a>')
    return f'<div class="doors{" stag" if stag else ""}" style="--n:{len(items)}">' + "".join(out) + "</div>"

def gallery(items):
    return '<div class="gal">' + "".join(ph(n, a, "", "(min-width:760px) 50vw, 100vw") for n, a in items) + "</div>"

def bleed(name, alt, label="", title="", link=None, pos=None):
    i = img(name, alt, "100vw")
    if pos:
        i = i.replace("<img ", f'<img style="object-position:{pos}" ', 1)
    cap = ""
    if title:
        lk = f'<a class="link" href="{link[0]}">{link[1]}</a>' if link else ""
        cap = f'<div class="cap on-dark"><p class="label">{label}</p><h2 class="t-h2">{title}</h2>{lk}</div>'
    return f'<section class="bleed{" shade" if title else ""}">{i}{cap}</section>'

def cta(title="Et si on en <em>parlait</em>&nbsp;?", lead="Une idée précise ou une envie encore floue&nbsp;: racontez-la. Mathilde vous rappelle sous 24 à 48&nbsp;h.", dark=False, devis="devis.html"):
    return f'''<section class="sec{" bg-cypres on-dark" if dark else ""}"><div class="wrap cta">
 <p class="label fade">Devis gratuit · réponse sous 48 h</p><h2 class="t-xl fade">{title}</h2><p class="lead fade">{lead}</p>
 <div class="actions fade"><a class="btn" href="{devis}">Demander un devis</a><a class="btn line" href="{TEL}">{PHONE}</a></div>
 <p class="meta fade"><a href="mailto:{MAIL}">{MAIL}</a> · 7 rue Tédenat, Nîmes</p>
</div></section>'''

def faq(qs):
    return '<div class="faq">' + "".join(f'<details><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in qs) + "</div>"

def logos(names):
    lab = {"golden-tulip": "Golden Tulip", "pasino-grand": "Pasino Grand Aix-en-Provence", "odalys-city": "Odalys City", "odalys-euromed": "Odalys Euromed",
           "nimes-tourisme": "Nîmes Tourisme", "golfe-saint-tropez": "Golfe de Saint-Tropez", "reseau-entreprendre": "Réseau Entreprendre Provence",
           "cci-pays-arles": "CCI Pays d'Arles", "hotels-de-nimes": "Les Hôtels de Nîmes", "entent": "ENTENT", "gepa": "GEPA", "sowell": "SoWell",
           "alcrys": "Alcrys", "michel-biet": "Michel Biet", "festival-gastronomie": "Festival de la gastronomie", "cds-groupe": "CDS Groupe",
           "domaine-robert": "Domaine Robert", "stars-metiers": "Stars & Métiers"}
    out = []
    for n in names:
        w, h = Image.open(f"{IMG}/clients/{n}.webp").size
        out.append(f'<li><img src="{IMG}/clients/{n}.webp" width="{w}" height="{h}" alt="{esc(lab[n])}" loading="lazy" decoding="async"></li>')
    return '<ul class="logos fade">' + "".join(out) + "</ul>"
