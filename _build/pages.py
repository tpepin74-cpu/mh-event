# -*- coding: utf-8 -*-
"""Accueil, entrées (Entreprises, Hôtels, Particuliers), pages de services, agence, réalisations.
Règle : aucun texte n'est copié d'une page à l'autre ; chaque page vise sa propre recherche."""
from build import *
from events import EVENTS, vignette
from urllib.parse import quote

EV = {e["slug"]: e for e in EVENTS}
CITIES = ["Nîmes", "Aix-en-Provence", "Marseille", "Saint-Tropez", "Montpellier", "Avignon", "Arles", "Gard", "Provence"]
AUD = {"entreprises": ("Entreprises", "entreprises/"), "hotels": ("Hôtels", "hotels/"), "particuliers": ("Particuliers", "particuliers/")}

def dv(t):
    return "devis/?type=" + quote(t)

def pick4(slugs, cat, path=""):
    """Toujours 4 réalisations : celles choisies, puis celles du même service, puis du même type de client."""
    out = [x for x in slugs if x in EV]
    for e in EVENTS:
        if len(out) >= 4: break
        if path and e.get("svc") == path and e["slug"] not in out: out.append(e["slug"])
    for e in EVENTS:
        if len(out) >= 4: break
        if e["cat"] == cat and e["slug"] not in out: out.append(e["slug"])
    for e in EVENTS:
        if len(out) >= 4: break
        if e["slug"] not in out: out.append(e["slug"])
    return out[:4]

def vign_block(slugs, cat, path="", title="Nos <em>réalisations</em>", label="Réalisations"):
    sl = pick4(slugs, cat, path)
    return (f'<section class="sec bg-pierre"><div class="wrap"><div class="stack" style="margin-bottom:clamp(40px,5vw,64px)">'
            f'<p class="label fade">{label}</p><h2 class="t-h2 fade">{title}</h2></div>'
            f'<div class="vign four">{"".join(vignette(EV[x]) for x in sl)}</div>'
            f'<div class="actions fade" style="margin-top:40px"><a class="link" href="realisations/">Toutes les réalisations</a></div></div></section>')

def strip_tags(s):
    return re.sub("<[^>]+>", "", s).replace("&amp;", "&")

def service_ld(S, path):
    o = {"@context": "https://schema.org", "@type": "Service", "name": S["name"], "serviceType": S["stype"],
         "description": S["desc"], "url": DOMAIN + path, "provider": {"@id": DOMAIN + "#agence"}, "areaServed": S.get("area", CITIES)}
    if S.get("price"):
        o["offers"] = {"@type": "Offer", "priceCurrency": "EUR",
                       "priceSpecification": {"@type": "PriceSpecification", "minPrice": S["price"], "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}
    return o

def service_page(path, S):
    aud_label, aud_path = AUD[S["aud"]]
    crumbs = [(aud_path, aud_label)] + S.get("mid", []) + [(path, S["crumb"])]
    devis = dv(S["devis"])
    hero = hero_photo(S["hero"][0], S["hero"][1], S.get("kicker", aud_label), S["h1"], S["lead"],
                      pos=S["hero"][2] if len(S["hero"]) > 2 else None, actions=hero_actions(devis))
    incl = '<ul class="incl fade">' + "".join(f"<li>{x}</li>" for x in S["incl"]) + "</ul>"
    intro = f'''<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block(S["k2"], S["h2"], S["intro"])}{incl}</div>
 {duo(S["duo"][0][0], S["duo"][0][1], S["duo"][1][0], S["duo"][1][1])}
</div></section>'''
    form = ""
    if S.get("rows"):
        note = f'<p class="small fade" style="margin-top:24px">{S["note"]}</p>' if S.get("note") else ""
        form = f'''<section class="sec flush"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(36px,4vw,64px)"><p class="label fade">{S.get("rows_k", "Formules")}</p><h2 class="t-h2 fade">{S["rows_h"]}</h2></div>
 {rows(S["rows"])}{note}
</div></section>'''
    faqs = f'''<section class="sec"><div class="wrap two">
 <div class="stack"><p class="label fade">Questions fréquentes</p><h2 class="t-h2 fade">{S["faq_h"]}</h2></div>
 {faq(S["faq"])}
</div></section>'''
    rel = f'<section class="sec tight" style="padding-top:0"><div class="wrap">{links_row(S["related"])}</div></section>'
    body = (hero + intro + form + cta_band(S["band"], devis) + S.get("extra", "") + vign_block(S.get("real", []), S["aud"], path)
            + faqs + rel + cta(S["cta_t"], S["cta_p"], devis=devis))
    page(path, S["title"], S["desc"], body, crumbs=crumbs, tab=S["aud"], tone="light",
         jsonld=[service_ld(S, path), faq_ld(S["faq"])])

def hub_page(path, H):
    devis = dv(H["devis"])
    hero = hero_photo(H["hero"][0], H["hero"][1], H["kicker"], H["h1"], H["lead"],
                      pos=H["hero"][2] if len(H["hero"]) > 2 else None, actions=hero_actions(devis))
    intro = f'''<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block(H["k2"], H["h2"], H["intro"])}</div>
 {duo(H["duo"][0][0], H["duo"][0][1], H["duo"][1][0], H["duo"][1][1])}
</div></section>'''
    svc = f'''<section class="sec flush"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Nos services</p><h2 class="t-h2 fade">{H["svc_h"]}</h2></div>
 {cards(H["cards"])}
</div></section>'''
    lg = (f'<section class="sec tight"><div class="wrap"><p class="label center fade" style="margin-bottom:40px">Ils nous font confiance</p>{logos(H["logos"])}</div></section>'
          if H.get("logos") else "")
    body = (hero + intro + svc + cta_band(H["band"], devis) + vign_block(H["real"], H["tab"], title=H.get("real_h", "Nos <em>réalisations</em>"))
            + lg + cta(H["cta_t"], H["cta_p"], devis=devis))
    page(path, H["title"], H["desc"], body, crumbs=[(path, H["crumb"])], tab=H["tab"], tone="light",
         jsonld=[{"@context": "https://schema.org", "@type": "CollectionPage", "name": H["title"], "description": H["desc"], "url": DOMAIN + path,
                  "about": {"@id": DOMAIN + "#agence"},
                  "hasPart": [{"@type": "WebPage", "url": DOMAIN + c[0], "name": strip_tags(c[3])} for c in H["cards"]]}])

# ================================================================ ACCUEIL
def home():
    CITIES = ["Nîmes", "Aix-en-Provence", "Marseille", "Saint-Tropez", "Montpellier", "Avignon", "Arles"]
    hero = f'''<section class="hero hero-v hero-home" aria-labelledby="h-title">
 <div class="hero-media"><video autoplay muted loop playsinline preload="auto" poster="assets/img/hero-poster.jpg" aria-hidden="true"><source src="assets/video/hero.mp4" type="video/mp4"></video></div>
 <div class="hero-body"><div class="hh">
  <h1 class="hh-h" id="h-title"><span class="hh-t"><span>Agence</span> <span>événementielle</span></span> <span class="hh-c">{"".join(f'<span>{c}<i class="sr">{", " if k < len(CITIES)-1 else ""}</i></span>' for k, c in enumerate(CITIES))}</span></h1>
  <p class="lead">Séminaires, team building, journées bien-être, soirées, hôtels et mariages.</p>
  <div class="entries"><a class="btn green" href="entreprises/">Une entreprise</a><a class="btn green" href="hotels/">Un hôtel</a><a class="btn green" href="particuliers/">Un particulier</a></div>
 </div></div>
 <button class="v-pause" type="button" aria-pressed="false" aria-label="Mettre la vidéo en pause"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z" fill="currentColor"/></svg></button>
 <a class="hero-down" href="#suite" aria-label="Découvrir la suite">{DOWN}</a>
</section>'''

    fears = [
        ("Perdre", "son temps", "«&nbsp;Je vais encore devoir tout gérer moi-même.&nbsp;»", "pb-temps"),
        ("Le déjà-vu", "", "«&nbsp;Encore une soirée qui ressemble à toutes les autres.&nbsp;»", "pb-deja-vu"),
        ("Le silence", "le jour J", "«&nbsp;Au moment critique, personne ne répondra.&nbsp;»", "pb-silence"),
        ("Le dérapage", "du budget", "«&nbsp;La facture n'aura rien à voir avec le devis.&nbsp;»", "pb-budget"),
        ("Votre image", "en jeu", "«&nbsp;Devant mes invités, je n'ai pas le droit à l'erreur.&nbsp;»", "pb-image"),
    ]
    acc = "".join(
        f'<li class="acc-i{" on" if i == 0 else ""}" tabindex="0" aria-expanded="{"true" if i == 0 else "false"}"><span class="acc-n" aria-hidden="true"></span>'
        f'<span class="acc-v" aria-hidden="true">{w}</span>'
        f'<div class="acc-c"><p class="acc-w"><span>{w}</span>{f" <i>{w2}</i>" if w2 else ""}</p><p class="acc-q">{q}</p></div><b class="acc-p" aria-hidden="true"></b></li>'
        for i, (w, w2, q, im) in enumerate(fears))
    pains_html = f'''<section class="pbs" id="problematiques" aria-labelledby="pb-t"><div class="pbs-st"><div class="wrap pbs-in">
 <p class="label pbs-l">Choisir une agence événementielle</p>
 <h2 class="pbs-t" id="pb-t"><span>Plusieurs</span> <span>problématiques</span></h2>
 <p class="pbs-w">{"".join(f'<span class="pw"><b>{w}</b>{f" <i>{w2}</i>" if w2 else ""}</span>' for (w, w2, q, im) in fears)}</p>
 <p class="pbs-c">Ces craintes, nous les connaissons par cœur. <em>Et nous avons les solutions.</em></p>
</div></div></section>'''

    picks = [e for e in EVENTS if e["slug"] in ("golden-night-golden-tulip-marseille", "diner-gala-pasino-aix-en-provence", "mariage-domaine-aix-en-provence")]
    qs = [
        ("Dans quelles villes intervient votre agence événementielle ?", "Basée à Nîmes, l'agence organise vos événements à Aix-en-Provence, Marseille, Nîmes, Saint-Tropez, Montpellier, Avignon et Arles, partout en Provence et dans le Gard, et se déplace dans toute la France."),
        ("Quels événements organisez-vous ?", "Pour les entreprises : séminaires, team building, journées bien-être, soirées, Christmas party, inaugurations, conférences et hôtes et hôtesses. Pour les hôtels : soirées vitrines, Déjeuner Corpo et animations. Pour les particuliers : mariages, coordination du jour J et fêtes privées."),
        ("Le devis est-il payant ?", "Non. Le devis est gratuit, détaillé poste par poste et sans engagement. Mathilde vous répond sous 24 à 48 h ouvrées."),
        ("Qui sera mon interlocuteur ?", "Mathilde Heyral, fondatrice de MH Event, du premier appel jusqu'au dernier invité. Pas d'intermédiaire entre vous et la personne qui pilote votre événement."),
        ("Proposez-vous une organisation complète ou à la carte ?", "Les deux : une organisation clé en main, ou seulement les prestations dont vous avez besoin (lieu, hôtesses, animation, coordination)."),
    ]
    body = hero + f'''
<nav class="snav" aria-label="Sections de la page"><ol>{"".join(f'<li><a href="#{i}"><span>{t}</span></a></li>' for i, t in [("suite","Vos besoins"),("problematiques","Vos problématiques"),("solutions","Nos solutions"),("prestations","Nos prestations"),("confiance","Ils nous font confiance"),("intervention","Où nous intervenons"),("questions","Vos questions")])}</ol></nav>
<section class="sec you" id="suite"><div class="wrap">
 <div class="band">
  <div class="band-t"><p class="label">Vos besoins</p><h2 class="band-h">Vous souhaitez organiser un événement <em>à votre image.</em></h2></div>
 </div>
 <div class="prof"><a class="pf" href="entreprises/"><div class="pf-m">{img("seminaire-seminaire-groupe-entreprise-sourire-discussion", "Échanges entre collaborateurs lors d'un événement d'entreprise en plein air", "(min-width:860px) 33vw, 100vw")}</div><div class="pf-c"><span class="pf-n">01</span><h3 class="pf-t">Événements <em>d'entreprise</em></h3><p>Fédérer vos équipes, remercier vos clients, marquer une inauguration.</p><span class="pf-l">Découvrir</span></div></a><a class="pf" href="hotels/"><div class="pf-m">{img("hotel-chanteur-opera-soiree-hotel-mh-event", "Chanteur lyrique lors d'une soirée en hôtel", "(min-width:860px) 33vw, 100vw")}</div><div class="pf-c"><span class="pf-n">02</span><h3 class="pf-t">Animation <em>d'hôtels</em></h3><p>Remplir vos salons et faire parler de votre établissement.</p><span class="pf-l">Découvrir</span></div></a><a class="pf" href="particuliers/"><div class="pf-m">{img("mariage-shooting-mariage-couple-sourire-domaine-montpellier", "Jeunes mariés souriants dans l'allée d'un domaine près de Montpellier", "(min-width:860px) 33vw, 100vw")}</div><div class="pf-c"><span class="pf-n">03</span><h3 class="pf-t">Mariages <em>&amp; fêtes privées</em></h3><p>Une fête qui vous ressemble, que vous vivez au lieu de la gérer.</p><span class="pf-l">Découvrir</span></div></a></div>
</div></section>

{pains_html}

<section class="sol" id="solutions">
 <div class="solv"><video class="lazy-v" muted loop playsinline preload="none" poster="assets/img/solutions-poster.webp" aria-hidden="true"><source data-src="assets/video/solutions.mp4" type="video/mp4"></video>
  <div class="solv-o"><p class="label">Notre réponse</p><h2 class="solv-t">Nos solutions</h2></div></div>
 <div class="sec sol-b"><div class="wrap">
  <ol class="sola"><li class="sa on" tabindex="0" aria-expanded="true"><span class="sa-n">01</span><div class="sa-b"><h3 class="sa-t">Vous déléguez tout</h3><p class="sa-d">Lieu, prestataires, planning, accueil : Mathilde coordonne tout et vous tient informé, sans vous noyer.</p></div><b class="sa-p" aria-hidden="true"></b></li><li class="sa" tabindex="0" aria-expanded="false"><span class="sa-n">02</span><div class="sa-b"><h3 class="sa-t">Rien n'est sur catalogue</h3><p class="sa-d">Thème, scénographie, artistes, tenues des hôtesses : chaque événement est pensé pour votre public.</p></div><b class="sa-p" aria-hidden="true"></b></li><li class="sa" tabindex="0" aria-expanded="false"><span class="sa-n">03</span><div class="sa-b"><h3 class="sa-t">Une seule personne, du début à la fin</h3><p class="sa-d">Celle qui écoute votre projet est celle qui le pilote le jour J.</p></div><b class="sa-p" aria-hidden="true"></b></li><li class="sa" tabindex="0" aria-expanded="false"><span class="sa-n">04</span><div class="sa-b"><h3 class="sa-t">Un budget clair dès le départ</h3><p class="sa-d">Devis gratuit, détaillé poste par poste, sans engagement et sans surprise.</p></div><b class="sa-p" aria-hidden="true"></b></li></ol>
 </div></div>
</section>

<section class="sec flush" id="prestations"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(48px,6vw,88px)"><p class="label fade">Nos prestations</p><h2 class="t-h2 fade">Les prestations de notre agence <em>événementielle</em></h2></div>
 {cards([
   ("entreprises/seminaire/", "seminaire-mh-event-organisation-seminaire-montpellier", "Séminaire sous chapiteau près de Montpellier", "Séminaires", "Lieu, hébergement, programme et temps forts, clés en main."),
   ("entreprises/team-building/", "tb-team-building-marche-des-senteurs-mh-event-avril-2026", "La Marche des senteurs dans les calanques", "Team building", "Quinze activités, du littoral aux manades de Camargue."),
   ("entreprises/soiree-entreprise/", "hotel-soiree-fin-annee-entreprise-alcrys-decembre-2025", "Soirée de fin d'année d'entreprise", "Soirées &amp; inaugurations", "Galas, Christmas party, lancements et inaugurations."),
   ("entreprises/journee-bien-etre/", "bienetre-cours-yoga-evenement-bien-etre", "Cours de yoga en terrasse", "Journées bien-être", "Yoga, relaxation sonore, Pilates : des équipes qui respirent."),
   ("hotels/animation-dynamisation/", "hotel-soiree-saxophone-lounge-hotel-marseille-dynamisation", "Soirée saxophone lounge en hôtel à Marseille", "Animation d'hôtels", "Soirées vitrines et Déjeuner Corpo pour faire venir du monde."),
   ("particuliers/mariage/", "mariage-organisation-mariage-domaine-aix-juillet-2025", "Mariage dans un domaine près d'Aix", "Mariages", "Organisation complète ou coordination du jour J."),
 ])}
</div></section>

{cta_band("Un devis gratuit, détaillé, sous 48 heures.", "devis/")}

<section class="sec bg-pierre proof" id="confiance"><div class="wrap">
 {head_block("Ils nous font confiance", "Les réalisations de l'agence, <em>de Marseille à Nîmes</em>", "Hôtels, grandes entreprises, réseaux d'entrepreneurs, collectivités et futurs mariés : quelques réalisations récentes.", center=True)}
 <ul class="figs fade"><li><b>5,0</b><span>sur 35 avis Google</span></li><li><b>{len(EVENTS)}</b><span>réalisations à découvrir</span></li><li><b>48 h</b><span>pour recevoir votre devis</span></li></ul>
 <div class="vign">{"".join(vignette(e) for e in picks)}</div>
 <div style="margin-top:clamp(64px,8vw,120px)">{logos(["golden-tulip","pasino-grand","odalys-euromed","entent","golfe-saint-tropez","reseau-entreprendre","gepa","cci-pays-arles"])}</div>
 <figure class="quote fade" style="margin-top:clamp(64px,8vw,120px)"><div class="rule" aria-hidden="true"><i></i></div><blockquote>« Mathilde transforme chaque moment en une expérience unique, fluide et parfaitement orchestrée. »</blockquote>
 <figcaption class="who">Lucie Lauzel · avis Google · <a href="https://share.google/i5QVzxkjr3eyGyZ6x" target="_blank" rel="noopener" style="color:var(--bordeaux)">5,0 sur 35 avis</a></figcaption></figure>
 <div class="actions center fade" style="margin-top:clamp(48px,6vw,80px);justify-content:center"><a class="btn line" href="realisations/">Toutes les réalisations</a></div>
</div></section>

<section class="sec seo" id="intervention"><div class="wrap">
 {head_block("Partout dans le Sud", "Agence événementielle à Nîmes, Aix-en-Provence, <em>Marseille et Saint-Tropez</em>", "MH Event est une agence événementielle basée à Nîmes. Elle organise les événements d'entreprise, les animations d'hôtels et les mariages dans les grandes villes du Sud de la France.", center=True)}
 <ul class="cityg"><li class="fade"><h3>Agence événementielle à Nîmes</h3><p>Le siège de l'agence, rue Tédenat. Partenaire de l'Office de Tourisme et des Congrès de Nîmes, MH Event y a créé des <a href="entreprises/team-building/nimes/">team building exclusifs</a>.</p></li><li class="fade"><h3>Agence événementielle à Aix-en-Provence</h3><p>Dîner de gala au Pasino, événement GEPA, déjeuners corporate et <a href="entreprises/team-building/aix-en-provence/">parcours dans le centre historique</a>.</p></li><li class="fade"><h3>Agence événementielle à Marseille</h3><p>Golden Night au Golden Tulip Marseille Euromed, soirées Odalys Euromed, Réseau Entreprendre : l'agence anime les <a href="hotels/animation-dynamisation/">hôtels</a> et les réseaux d'affaires.</p></li><li class="fade"><h3>Agence événementielle à Saint-Tropez</h3><p>Les Rencontres économiques du nautisme du Golfe de Saint-Tropez : scénographie, accueil et <a href="entreprises/hotes-hotesses/">hôtesses</a>.</p></li><li class="fade"><h3>Agence événementielle à Montpellier</h3><p><a href="entreprises/seminaire/">Séminaires</a> sous chapiteau et mariages en domaine dans l'Hérault.</p></li><li class="fade"><h3>Agence événementielle à Avignon</h3><p>Conférences et afterworks d'entreprise, comme la conférence Michel Biet.</p></li><li class="fade"><h3>Agence événementielle à Arles</h3><p>Le salon Li Rescountre d'Aqui avec la CCI Pays d'Arles, et des <a href="entreprises/team-building/camargue/">immersions en manade en Camargue</a>.</p></li></ul>
 <div class="seo-in">
 <div class="prose fade">
   <h2>Une agence événementielle pour les entreprises, les hôtels et les particuliers</h2>
   <p>Pour les entreprises, l'agence conçoit des <a href="entreprises/seminaire/">séminaires</a>, des <a href="entreprises/team-building/">team building</a> à Nîmes, Aix-en-Provence, en <a href="entreprises/team-building/camargue/">Camargue</a> ou au <a href="entreprises/team-building/pont-du-gard/">Pont du Gard</a>, des <a href="entreprises/soiree-entreprise/">soirées d'entreprise</a>, des <a href="entreprises/inauguration/">inaugurations</a> et met à disposition des <a href="entreprises/hotes-hotesses/">hôtes et hôtesses</a>.</p>
   <p>Les hôtels lui confient l'<a href="hotels/animation-dynamisation/">animation de leur établissement</a> et leurs <a href="hotels/dejeuner-corpo/">Déjeuners Corpo</a> ; les particuliers, leur <a href="particuliers/mariage/">mariage</a>, la <a href="particuliers/coordination-jour-j/">coordination du jour J</a> ou une <a href="particuliers/anniversaire-fete-privee/">fête privée</a>.</p>
 </div>
 <div class="seo-faq" id="questions"><h2 class="label fade">Questions fréquentes sur l'agence</h2>{faq(qs)}<div class="actions fade" style="margin-top:28px"><a class="link" href="faq/">Toutes les questions</a></div></div>
 </div>
</div></section>
{cta(title="Parlons de <em>votre événement</em>&nbsp;?", dark=True, devis="devis/")}
<section class="sec team"><div class="wrap">
 {head_block("L'agence", "Une agence événementielle à taille humaine, <em>tout sur mesure</em>", "Créée par Mathilde Heyral, danseuse classique, cheffe hôtesse au Grand Prix de France de F1 et juriste, pour répondre précisément à vos craintes.", center=True)}
 <div class="actions center fade" style="margin-top:28px;justify-content:center"><a class="btn line" href="agence/">Découvrir l'agence et l'équipe</a></div>
</div></section>'''
    page("", "Agence événementielle Nîmes, Aix, Marseille, Saint-Tropez | MH Event",
         "MH Event, agence événementielle à Nîmes, Aix-en-Provence, Marseille, Saint-Tropez, Montpellier, Avignon et Arles : séminaires, team building, soirées, hôtels, mariages. Devis gratuit.",
         body, bodycls="home", jsonld=[AGENCY, {"@context": "https://schema.org", "@type": "WebSite", "name": "MH Event", "url": DOMAIN}, faq_ld(qs)])

# ================================================================ ENTREPRISES
def entreprises():
    hub_page("entreprises/", dict(
        title="Événements d'entreprise à Aix, Marseille, Nîmes | MH Event",
        desc="Séminaires, soirées, Christmas party, inaugurations, team building et hôtesses : MH Event organise vos événements d'entreprise en Provence et dans le Gard.",
        crumb="Entreprises", tab="entreprises", kicker="Entreprises", devis="Séminaire",
        hero=("seminaire-seminaire-groupe-entreprise-sourire-discussion", "Séminaire d'entreprise en plein air", "50% 40%"),
        h1="Événements <em>d'entreprise</em>", lead="Vous fixez le cap. MH Event s'occupe de tout le reste.",
        k2="Une seule interlocutrice", h2="De A <em>à</em> Z",
        intro="Conception, lieu, prestataires, équipes d'accueil et pilotage le jour J : des devis clairs, des plannings tenus, à Aix-en-Provence, Marseille, Nîmes et partout dans le Sud.",
        duo=[("seminaire-mh-event-organisation-seminaire-montpellier", "Séminaire sous chapiteau près de Montpellier"), ("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca", "Inauguration de la machine PULSE chez ENTENT")],
        svc_h="Ce que nous <em>organisons</em>",
        cards=[
         ("entreprises/seminaire/", "seminaire-pique-nique-entreprise-plage-avril-2026", "Pique-nique d'entreprise sur la plage", "Séminaires <em>&amp; conventions</em>", "Un ou deux jours, résidentiel ou non, clé en main."),
         ("entreprises/soiree-entreprise/", "afterwork-soiree-entrepeneurs-encheres-pasino-aix", "Dîner de gala au Pasino d'Aix-en-Provence", "Soirées <em>&amp; galas</em>", "Dîners-spectacles, soirées à thème, cocktails."),
         ("entreprises/christmas-party/", "hotel-soiree-fin-annee-entreprise-alcrys-decembre-2025", "Soirée de fin d'année d'entreprise", "Christmas <em>party</em>", "Journée, soirée et nuit : décembre se réserve en septembre."),
         ("entreprises/inauguration/", "lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-2", "Invités découvrant une machine lors d'une inauguration", "Inaugurations <em>&amp; lancements</em>", "Locaux, machine, produit : le jour où l'on vous découvre."),
         ("entreprises/journee-bien-etre/", "bienetre-cours-yoga-evenement-bien-etre", "Cours de yoga face aux collines", "Journées <em>bien-être</em>", "Yoga, relaxation sonore, massages pour vos équipes."),
         ("entreprises/conference-salon-afterwork/", "afterwork-conference-wiko-afterwork-aix", "Conférence devant un public à Aix-en-Provence", "Conférences, salons <em>&amp; afterworks</em>", "Réseaux, conférences, salons professionnels."),
         ("entreprises/team-building/", "tb-team-building-eveil-corporal-mh-event-cohesion", "Éveil corporel sur la plage", "Team <em>building</em>", "Quinze créations, dès 28 € HT par personne."),
         ("entreprises/hotes-hotesses/", "hotesses-hotesses-mh-event-pasino-aix-tenues-noires", "Hôtesses en tenue noire au Pasino", "Hôtes <em>&amp; hôtesses</em>", "Les Angelines, formées par une ancienne cheffe hôtesse."),
        ],
        band="Un séminaire, une soirée, une inauguration ? Devis sous 48 heures.",
        real=["inauguration-pulse-entent", "soiree-o-delice-ligue-football", "rencontres-economiques-nautisme-saint-tropez"],
        logos=["entent", "gepa", "pasino-grand", "reseau-entreprendre", "golfe-saint-tropez", "cci-pays-arles", "alcrys", "michel-biet"],
        cta_t="Votre prochain <em>événement</em>", cta_p="Date, nombre de participants, ville : trois informations suffisent pour un premier devis."))

def services_entreprises():
    service_page("entreprises/seminaire/", dict(
        aud="entreprises", crumb="Séminaires & conventions", name="Organisation de séminaires et conventions", stype="Organisation de séminaire d'entreprise",
        title="Organisation de séminaire à Aix, Marseille, Nîmes | MH Event",
        desc="Séminaire d'un ou deux jours, résidentiel ou non : lieu, hébergement, plénière, team building, soirée et transport. Devis sous 48 h, Provence et Gard.",
        devis="Séminaire", hero=("seminaire-mh-event-organisation-seminaire-montpellier", "Chapiteau dressé pour un séminaire dans la garrigue"),
        h1="Séminaires <em>&amp; conventions</em>", lead="Un ou deux jours qui fédèrent, sans que vous ayez à gérer la logistique.",
        k2="Séminaire clé en main", h2="Le lieu, le rythme, <em>l'énergie</em>",
        intro="MH Event construit votre séminaire autour de vos objectifs : un lieu qui vous ressemble, une plénière bien tenue, des temps forts qui restent. Domaines, mas, hôtels ou sites patrimoniaux comme le Musée de la Romanité, les Jardins de la Fontaine ou le Pont du Gard.",
        incl=["Recherche et réservation du lieu", "Hébergement et privatisation de chambres", "Plénière, déjeuners, walking lunch", "Team building et éveil corporel du matin", "Soirée, cocktail dînatoire, transport en car", "Hôtesses d'accueil et coordination sur site"],
        duo=[("seminaire-pique-nique-entreprise-plage-avril-2026", "Pique-nique d'entreprise sur la plage"), ("seminaire-seminaire-groupe-entreprise-sourire-discussion", "Collaborateurs en discussion pendant un séminaire")],
        rows_k="Trois formats", rows_h="Votre <em>séminaire</em>",
        rows=[("Séminaire d'une journée", "Accueil café, plénière, déjeuner, atelier ou team building l'après-midi."),
              ("Séminaire résidentiel", "Deux jours et une nuit : soirée privatisée, réveil yoga ou Pilates, retour en car."),
              ("Convention", "Grand groupe, scénographie de la plénière, équipes d'accueil et d'émargement.")],
        note="Exemple : une Christmas party résidentielle d'environ 140 personnes à Nîmes en 2026, avec chambres privatisées, walking lunch, cocktail dînatoire et car de 53 places.",
        band="Dates, effectif, ville : recevez une proposition de séminaire sous 48 heures.",
        faq_h="Organiser <em>un séminaire</em>",
        faq=[("Combien de temps à l'avance faut-il organiser un séminaire ?", "Idéalement trois à six mois avant, pour réserver le lieu et l'hébergement. Un séminaire plus proche reste possible : MH Event vous dit franchement ce qui est faisable."),
             ("Pouvez-vous trouver le lieu du séminaire ?", "Oui. MH Event cherche et réserve domaines, mas, hôtels et lieux patrimoniaux à Nîmes, Aix-en-Provence, Marseille, au Pont du Gard et en Camargue."),
             ("Le team building peut-il être intégré au séminaire ?", "Oui, en demi-journée ou en réveil du matin : quinze activités existent, de la Marche des senteurs à l'immersion en manade.")],
        related=[("entreprises/team-building/", "Team building"), ("entreprises/journee-bien-etre/", "Journées bien-être"), ("entreprises/soiree-entreprise/", "Soirées & galas"), ("entreprises/hotes-hotesses/", "Hôtes & hôtesses")],
        cta_t="Votre <em>séminaire</em>", cta_p="Racontez vos objectifs et vos contraintes : Mathilde revient vers vous avec une première proposition."))

    service_page("entreprises/soiree-entreprise/", dict(
        aud="entreprises", crumb="Soirées & galas", name="Soirées d'entreprise et dîners de gala", stype="Organisation de soirée d'entreprise",
        title="Soirée d'entreprise et dîner de gala | MH Event",
        desc="Soirées à thème, dîners-spectacles, galas et cocktails pour vos équipes, clients ou partenaires, à Marseille, Aix-en-Provence et Nîmes.",
        devis="Soirée d'entreprise", hero=("hotel-chanteur-opera-soiree-hotel-mh-event", "Chanteur lyrique pendant une soirée d'entreprise", "50% 30%"),
        h1="Soirées <em>&amp; galas</em>", lead="Une soirée dont vos invités parlent encore le lendemain.",
        k2="Soirées clé en main", h2="Un thème, <em>une émotion</em>",
        intro="Dîner-spectacle, gala de partenaires, cocktail de clients : MH Event imagine le thème, choisit les artistes et orchestre la soirée, avec des équipes en tenue accordée à l'univers.",
        incl=["Choix du lieu et privatisation", "Thème, décor de table, ambiance", "Artistes : chanteurs lyriques, musiciens, comédiens", "Traiteur et cocktail", "Hôtesses, vestiaire, placement", "Collecte des contacts, avec accord RGPD"],
        duo=[("hotel-pianiste-soiree-opera-hotel-blanc", "Soprano et pianiste pendant une soirée"), ("hotel-soiree-feria-groupe-live-hotel-sowell-nimes", "Groupe live pendant une soirée")],
        rows_k="Thèmes possibles", rows_h="Quelques <em>univers</em>",
        rows=[("Opéra et champagne", "Chanteurs lyriques et pianiste."), ("Gatsby", "Dîner-spectacle années folles."), ("Nuit andalouse", "Harpe et danseuse de flamenco."),
              ("Comedy Club, cabaret, mentalisme", "Dîners-spectacles."), ("Cluedo géant", "Six comédiens, une enquête grandeur nature.")],
        band="Une soirée à organiser ? Thème, date et nombre d'invités suffisent pour commencer.",
        real=["soiree-o-delice-ligue-football", "diner-gala-pasino-aix-en-provence", "soiree-reseau-entreprendre-marseille"], faq_h="Avant <em>la soirée</em>",
        faq=[("Quel budget prévoir pour une soirée d'entreprise ?", "Il dépend du lieu, du nombre d'invités et des artistes. MH Event vous remet un devis détaillé, poste par poste, avant tout engagement."),
             ("Pouvez-vous organiser une soirée pour quarante personnes ?", "Oui. La Soirée Ô Délice de la Ligue de la Méditerranée de Football réunissait une quarantaine de convives autour d'un mini-concert lyrique."),
             ("Les tenues des équipes sont-elles adaptées au thème ?", "Toujours : tablier japonais, marinière, cravate en soie brodée du logo MH, selon l'univers de la soirée.")],
        related=[("entreprises/christmas-party/", "Christmas party"), ("entreprises/hotes-hotesses/", "Hôtes & hôtesses"), ("entreprises/seminaire/", "Séminaires & conventions")],
        cta_t="Votre <em>soirée</em>", cta_p="Un thème en tête, ou tout à imaginer : Mathilde vous propose un univers et un devis."))

    service_page("entreprises/christmas-party/", dict(
        aud="entreprises", crumb="Christmas party", name="Christmas party et soirée de fin d'année d'entreprise", stype="Organisation de Christmas party",
        title="Christmas party et soirée de fin d'année | MH Event",
        desc="Christmas party à Marseille, Nîmes ou Aix : journée, soirée et nuit, soirée Hiver blanc, réveil Pilates. Décembre se réserve dès septembre.",
        devis="Christmas party", hero=("hotel-soiree-fin-annee-entreprise-alcrys-decembre-2025", "Soirée de fin d'année d'entreprise"),
        h1="Christmas <em>party</em>", lead="Décembre se réserve en septembre.",
        k2="Fin d'année", h2="Clore l'année <em>ensemble</em>",
        intro="Une soirée, ou une journée complète avec nuit sur place : MH Event organise la fin d'année de vos équipes, du thème au réveil du lendemain. L'hiver 2025, le lobby de l'Odalys Euromed à Marseille est devenu une station de ski pour une soirée raclette.",
        incl=["Journée, soirée et nuit sur place", "Soirée Hiver blanc : danseuses, chanteur, DJ", "Décor de fin d'année et photocall", "Réveil Pilates ou yoga le lendemain", "Hébergement et transport en car", "Hôtesses d'accueil et vestiaire"],
        duo=[("hotel-groupement-personnes-soiree-evenement-hotel-marseille", "Invités réunis pour une soirée en hôtel"), ("hotel-applaudissement-rires-groupe-soiree-evenement", "Collaborateurs qui rient et applaudissent")],
        rows_k="Formules", rows_h="Votre fin <em>d'année</em>",
        rows=[("Soirée de fin d'année", "Cocktail ou dîner, animation, DJ."), ("Soirée Hiver blanc", "Danseuses, chanteur et DJ, environ 100 personnes.", "4 300 € HT"),
              ("Christmas party résidentielle", "Journée, soirée, nuit et réveil bien-être, pour un grand groupe.")],
        band="Réservez votre date de décembre dès maintenant.",
        real=["soiree-fin-annee-alcrys", "odalys-euromed-marseille"], faq_h="Préparer <em>décembre</em>",
        faq=[("Quand réserver sa Christmas party ?", "Dès septembre : les lieux et les artistes de décembre partent vite. Plus tôt vous posez la date, plus le choix est large."),
             ("Peut-on organiser la soirée dans nos locaux ?", "Oui. MH Event transforme vos locaux ou un hôtel avec un décor de fin d'année, un traiteur et des animations."),
             ("Proposez-vous une formule avec nuit ?", "Oui : journée, soirée, nuit sur place et réveil Pilates ou yoga, comme pour une Christmas party d'environ 140 personnes à Nîmes en 2026.")],
        related=[("entreprises/soiree-entreprise/", "Soirées & galas"), ("entreprises/seminaire/", "Séminaires & conventions"), ("entreprises/hotes-hotesses/", "Hôtes & hôtesses")],
        cta_t="Votre <em>Christmas party</em>", cta_p="Date, nombre de collaborateurs, envie de nuit sur place ou non : c'est tout ce qu'il faut pour commencer."))

    service_page("entreprises/inauguration/", dict(
        aud="entreprises", crumb="Inaugurations & lancements", name="Inauguration et lancement de produit", stype="Organisation d'inauguration",
        title="Inauguration d'entreprise et lancement de produit | MH Event",
        desc="Inauguration de locaux, de machine ou lancement de produit en Provence : scénographie, accueil, cadeaux, photographe et musiciens. Références ENTENT, Maison Elise P.",
        devis="Inauguration", hero=("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-4", "Équipe réunie lors d'une inauguration industrielle"),
        h1="Inaugurations <em>&amp; lancements</em>", lead="Le jour où vos clients, vos équipes et la presse vous découvrent.",
        k2="Scénographie et accueil", h2="Un lieu qui <em>se révèle</em>",
        intro="Nouveaux locaux, nouvelle machine, nouveau produit : MH Event transforme un atelier ou une boutique en lieu de réception et soigne chaque détail du parcours invité.",
        incl=["Scénographie du lieu", "Accueil, émargement, vestiaire", "Cadeaux invités", "Photographe et vidéaste", "Musiciens et traiteur", "Coordination le jour J"],
        duo=[("lancement-soiree-inauguration-entreprise-cabries-paca-3", "Invités en blanc lors d'une inauguration à Cabriès"), ("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-1", "Remise d'un cadeau lors d'une inauguration")],
        band="Une inauguration à préparer ? Parlez-en à Mathilde.",
        real=["inauguration-pulse-entent", "inauguration-maison-elise-p-cabries", "salon-gastronomie-chateauneuf"], faq_h="Réussir <em>son inauguration</em>",
        faq=[("Pouvez-vous inaugurer un site industriel ?", "Oui. Pour l'inauguration de la machine PULSE chez ENTENT à Vitrolles, l'atelier a été transformé en lieu de réception."),
             ("Gérez-vous les invitations et l'accueil ?", "MH Event gère l'accueil, l'émargement, le vestiaire et la remise des cadeaux, avec des hôtes et hôtesses formés."),
             ("Peut-on filmer l'événement ?", "Oui : photographe et vidéaste font partie des prestations possibles, pour vos réseaux et votre communication.")],
        related=[("entreprises/hotes-hotesses/", "Hôtes & hôtesses"), ("entreprises/soiree-entreprise/", "Soirées & galas"), ("entreprises/conference-salon-afterwork/", "Conférences, salons & afterworks")],
        cta_t="Votre <em>inauguration</em>", cta_p="Date, lieu, nombre d'invités : Mathilde vous propose un déroulé et un devis."))

    service_page("entreprises/journee-bien-etre/", dict(
        aud="entreprises", crumb="Journées bien-être", name="Journée bien-être en entreprise", stype="Organisation de journée bien-être",
        title="Journée bien-être en entreprise en Provence | MH Event",
        desc="Journée bien-être pour vos équipes : yoga, relaxation sonore, massages, Pilates et ateliers, dans un domaine ou dans vos locaux, en Provence et dans le Gard.",
        devis="Journée bien-être", hero=("bienetre-cours-pilates-evenement-bien-etre", "Cours de Pilates pendant une journée bien-être"),
        h1="Journées <em>bien-être</em>", lead="Une journée pour souffler, ensemble.",
        k2="Qualité de vie au travail", h2="Le corps, <em>l'esprit</em>",
        intro="Une journée pensée pour relâcher les tensions et recharger l'énergie de l'équipe, dans un domaine, au bord de l'eau ou dans vos locaux, avec des intervenantes diplômées.",
        incl=["Yoga et Pilates", "Relaxation sonore aux bols", "Massages", "Ateliers créatifs", "Déjeuner et pauses", "Lieu et coordination"],
        duo=[("bienetre-atelier-sonore-nature-relaxation", "Relaxation sonore en plein air"), ("bienetre-cours-yoga-evenement-bien-etre", "Cours de yoga en terrasse face aux collines")],
        rows_k="Prix HT par personne", rows_h="Les formats <em>bien-être</em>",
        rows=[("Instant Zen Détente", "Yoga flow, relaxation sonore, moodboard collaboratif, 2 h 30 à 3 h.", "dès 47 €"),
              ("Instant Zen Active", "Yoga dynamique, ateliers de confiance, méditation.", "dès 49 €"),
              ("Breathwork", "Respiration consciente avec une sophrologue, 3 à 10 personnes.", "dès 39 €"),
              ("Yoga et énergie collective", "Séance jusqu'à 12 personnes.", "300 € la séance")],
        band="Offrez une vraie pause à vos équipes.",
        faq_h="Une journée <em>qui repose</em>",
        faq=[("Faut-il être sportif pour participer ?", "Non. Les séances sont accessibles à tous les niveaux ; pour les grands groupes, le yoga se pratique même debout, sans tapis."),
             ("Peut-on organiser la journée dans nos locaux ?", "Oui, en intérieur comme en extérieur. MH Event peut aussi trouver un domaine ou un lieu au bord de l'eau."),
             ("Combien de participants ?", "De 3 à 80 personnes selon l'atelier ; le nombre de coachs suit la taille du groupe.")],
        related=[("entreprises/team-building/", "Team building"), ("entreprises/seminaire/", "Séminaires & conventions"), ("entreprises/christmas-party/", "Christmas party")],
        cta_t="Votre journée <em>bien-être</em>", cta_p="Nombre de participants, lieu souhaité, date : un devis vous revient sous 48 heures.", price=39))

    service_page("entreprises/conference-salon-afterwork/", dict(
        aud="entreprises", crumb="Conférences, salons & afterworks", name="Organisation de conférences, salons et afterworks", stype="Organisation de conférence et salon professionnel",
        title="Conférence, salon et afterwork d'entreprise | MH Event",
        desc="Conférences, salons professionnels, rencontres économiques et afterworks de réseaux d'entrepreneurs à Aix, Marseille, Avignon, Arles et Saint-Tropez.",
        devis="Conférence ou salon", hero=("institution-discours-scene-scenographie-golfe-saint-tropez", "Scène des Rencontres économiques du nautisme à Saint-Tropez"),
        h1="Conférences, salons <em>&amp; afterworks</em>", lead="Faire se rencontrer les bonnes personnes, au bon endroit.",
        k2="Événements professionnels", h2="Du débat <em>au réseau</em>",
        intro="Rencontres économiques, salon de producteurs, conférence, afterwork de réseau : MH Event conçoit la scène, accueille les intervenants et fait circuler les invités.",
        incl=["Scénographie de la scène", "Accueil des intervenants et du public", "Hôtes et hôtesses de conférence", "Passage micro et régie", "Cocktail et afterwork", "Collecte des contacts"],
        duo=[("afterwork-intervention-fondateur-wiko-conference-image-de-marque", "Intervention sur l'image de marque"), ("institution-evenement-institutionnel-salon-arles-li-rescountre-dacqui", "Salon Li Rescountre d'Aqui à Arles")],
        band="Une conférence ou un salon en préparation ?",
        real=["rencontres-economiques-nautisme-saint-tropez", "salon-li-rescountre-d-aqui-arles", "conference-michel-biet-avignon"], faq_h="Organiser <em>un événement pro</em>",
        faq=[("Quels événements professionnels organisez-vous ?", "Conférences, rencontres économiques, salons, forums, afterworks de réseaux d'entrepreneurs et soirées de clubs d'affaires."),
             ("Pouvez-vous gérer une journée de débats ?", "Oui. Les Rencontres économiques du nautisme à Saint-Tropez ont réuni seize intervenants pour cinq heures de débats, avec scénographie et hôtesses MH Event."),
             ("Travaillez-vous avec les collectivités ?", "Oui : chambres de commerce, offices de tourisme et collectivités font partie des clients, comme la CCI Pays d'Arles.")],
        related=[("entreprises/hotes-hotesses/", "Hôtes & hôtesses"), ("entreprises/inauguration/", "Inaugurations & lancements"), ("entreprises/soiree-entreprise/", "Soirées & galas")],
        cta_t="Votre <em>événement pro</em>", cta_p="Format, public, date : Mathilde vous propose une organisation et un devis."))

# ---------------------------------------------------------------- team building
TB_ROWS = [
 ("Instant Zen Détente", "Yoga flow, relaxation sonore, moodboard. 5 à 80 personnes.", "dès 47 €"),
 ("Instant Zen Active", "Yoga dynamique, confiance, méditation. 5 à 80 personnes.", "dès 49 €"),
 ("La Fabrique des couleurs", "Colorimétrie des personnalités, création collective. 5 à 25 personnes.", "dès 45 €"),
 ("Speed Meeting", "Binômes animés par une sophrologue. 10 à 34 personnes.", "dès 28 €"),
 ("Olympiades et défis", "Parcours, tir à la corde, coach sportif. 4 à 20 personnes.", "dès 30 €"),
 ("Yoga et énergie collective", "45 min à 1 h, jusqu'à 12 personnes.", "300 € la séance"),
 ("Relaxation sonore", "Bols et vibrations, 4 à 36 personnes.", "dès 30 €"),
 ("Breathwork", "Respiration consciente, 3 à 10 personnes.", "dès 39 €"),
 ("Le Circuit des poètes · Nîmes", "Parcours poétique exclusif.", "dès 55 €"),
 ("Sur la route des Crocodiles · Nîmes", "Énigmes en quatre étapes.", "dès 50 €"),
 ("La Marche des senteurs · Nîmes", "Jardins de la Fontaine.", "dès 39 €"),
 ("La Marche des senteurs · Pont du Gard", "Garrigue et yoga.", "dès 45 €"),
 ("Immersion en manade · Camargue", "Trois formules, transport compris.", "57 à 80 €"),
 ("Aix-périence · Aix", "Fontaines, impro, flash mob.", "dès 50 €"),
 ("Parcours gourmand · Aix", "Sur les pas du Roi René.", "dès 70 €"),
]

def team_building():
    service_page("entreprises/team-building/", dict(
        aud="entreprises", crumb="Team building", name="Team building en Provence et dans le Gard", stype="Team building",
        title="Team building en Provence : 15 activités dès 28 € | MH Event",
        desc="Quinze team buildings originaux à Nîmes, Aix-en-Provence, au Pont du Gard et en Camargue : bien-être, cohésion, patrimoine. Dès 28 € HT par personne.",
        devis="Team building", hero=("tb-team-building-eveil-corporal-mh-event-cohesion", "Éveil corporel sur la plage"),
        h1="Team <em>building</em>", lead="Quinze créations originales, clés en main, dès 28 € HT par personne.",
        k2="Catalogue 2026", h2="Des expériences <em>qui soudent</em>",
        intro="Toutes les activités sont conçues par MH Event et animées par des professionnels : coachs, sophrologues, professeure de yoga, guides. Elles s'adaptent au lieu, au nombre de participants et à vos objectifs.",
        incl=["Conception et mise en place", "Intervenants qualifiés", "Coordination sur site", "Adaptable en séminaire", "Intérieur ou extérieur", "De 3 à 240 participants"],
        duo=[("tb-team-building-yoga-relaxation-sonore", "Yoga et relaxation sonore dans l'herbe"), ("tb-team-building-sport-olympiades-marseille", "Olympiades d'entreprise à Marseille")],
        rows_k="Prix HT par personne", rows_h="Les quinze <em>activités</em>",
        rows=TB_ROWS, note="Options : accueil café dès 10 €, déjeuner dès 30 €, coordination sur site dès 250 € la demi-journée, hôtesse d'accueil (voir Hôtes &amp; hôtesses).",
        extra=f'''<section class="sec"><div class="wrap"><div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Par destination</p><h2 class="t-h2 fade">Où <em>partir</em></h2></div>
 {cards([
   ("entreprises/team-building/nimes/", "tb-team-building-crocodiles-nimes-mh-event", "Sur la route des Crocodiles à Nîmes", "À <em>Nîmes</em>", "Trois parcours exclusifs au cœur du patrimoine."),
   ("entreprises/team-building/aix-en-provence/", "tb-team-building-speed-meeting-hotel-renaissance-aix", "Team building à Aix-en-Provence", "À <em>Aix-en-Provence</em>", "Fontaines, impro, calissons."),
   ("entreprises/team-building/pont-du-gard/", "tb-team-building-marche-des-senteurs-mh-event-avril-2026", "Marche des senteurs", "Au <em>Pont du Gard</em>", "Yoga et garrigue au pied du monument."),
   ("entreprises/team-building/camargue/", "tb-team-building-visite-manade-taureaux-camargue", "Visite de manade en Camargue", "En <em>Camargue</em>", "Une journée en manade, jusqu'à 240 personnes."),
 ])}</div></section>''',
        band="Votre team building, conçu pour votre équipe.",
        faq_h="Bon <em>à savoir</em>",
        faq=[("Combien coûte un team building ?", "Les activités démarrent à 28 € HT par personne pour le Speed Meeting et vont jusqu'à 80 € HT pour l'immersion complète en manade, transport compris."),
             ("Pourquoi certaines activités sont-elles exclusives à Nîmes ?", "Elles ont été conçues à la demande de l'Office de Tourisme et des Congrès de Nîmes, dont MH Event est partenaire depuis 2026."),
             ("Pouvez-vous animer un team building dans notre hôtel de séminaire ?", "Oui. La plupart des activités bien-être et cohésion se jouent partout, en intérieur comme en extérieur.")],
        related=[("entreprises/seminaire/", "Séminaires & conventions"), ("entreprises/journee-bien-etre/", "Journées bien-être")] + TB_CITIES,
        cta_t="Votre équipe, <em>autrement</em>", cta_p="Nombre de participants, ville, date : Mathilde vous conseille l'activité qui correspond à vos objectifs.", price=28))

    mid = [("entreprises/team-building/", "Team building")]
    service_page("entreprises/team-building/nimes/", dict(
        aud="entreprises", mid=mid, crumb="Nîmes", name="Team building à Nîmes", stype="Team building", area=["Nîmes", "Gard"],
        title="Team building à Nîmes : 3 parcours exclusifs | MH Event",
        desc="Team building à Nîmes : Circuit des poètes, route des Crocodiles et Marche des senteurs aux Jardins de la Fontaine. Conçus avec l'Office de Tourisme, dès 39 € HT.",
        devis="Team building Nîmes", hero=("tb-team-building-crocodiles-nimes-mh-event", "Équipe sur la route des Crocodiles à Nîmes"),
        h1="Team building <em>à Nîmes</em>", lead="Trois parcours que l'on ne vit qu'à Nîmes.",
        k2="Partenaire de l'Office de Tourisme", h2="Le patrimoine, <em>en équipe</em>",
        intro="Des Arènes aux Jardins de la Fontaine, MH Event a conçu avec l'Office de Tourisme et des Congrès de Nîmes trois expériences qui font découvrir la ville en travaillant la cohésion. Une première pour une agence événementielle.",
        incl=["Parcours exclusifs", "Guides et intervenants", "Énigmes et défis d'équipe", "De 5 à 60 participants", "Déjeuner en option", "Combinable avec un séminaire"],
        duo=[("tb-team-building-marche-des-senteurs-mh-event-avril-2026", "Marche sensorielle en plein air"), ("tb-img-8004", "Atelier d'équipe en intérieur")],
        rows_k="Prix HT par personne", rows_h="Les parcours <em>nîmois</em>",
        rows=[("Le Circuit des poètes", "Daudet, Bigot, Reboul, Mistral : poésie déclamée jusqu'aux Jardins de la Fontaine. 2 h 30 à 3 h, 5 à 36 personnes.", "dès 55 €"),
              ("Sur la route des Crocodiles", "Quatre étapes, quatre compétences, de la place du Marché à l'abribus de Philippe Starck. 2 h 30 à 3 h, 5 à 36 personnes.", "dès 50 €"),
              ("La Marche des senteurs", "Yoga doux puis marche sensorielle aux Jardins de la Fontaine. 2 à 3 h, 5 à 60 personnes.", "dès 39 €")],
        band="Un séminaire à Nîmes ? Ajoutez-y un parcours exclusif.",
        faq_h="Team building <em>à Nîmes</em>",
        faq=[("Faut-il bien connaître Nîmes pour participer ?", "Non : les parcours sont pensés pour les équipes venues d'ailleurs comme pour les Nîmois, qui redécouvrent leur ville."),
             ("Que se passe-t-il en cas de pluie ?", "MH Event adapte le parcours ou propose une solution de repli, à valider ensemble avant l'événement."),
             ("Peut-on enchaîner avec un déjeuner ?", "Oui, dès 30 € HT par personne, dans un lieu proche du parcours.")],
        related=[("entreprises/team-building/pont-du-gard/", "Team building au Pont du Gard"), ("entreprises/team-building/camargue/", "Team building en Camargue"), ("entreprises/seminaire/", "Séminaires & conventions")],
        cta_t="Votre team building <em>à Nîmes</em>", cta_p="Date, nombre de participants et parcours souhaité : devis sous 48 heures.", price=39))

    service_page("entreprises/team-building/aix-en-provence/", dict(
        aud="entreprises", mid=mid, crumb="Aix-en-Provence", name="Team building à Aix-en-Provence", stype="Team building", area=["Aix-en-Provence", "Bouches-du-Rhône"],
        title="Team building à Aix-en-Provence | MH Event",
        desc="Team building à Aix-en-Provence : Aix-périence entre fontaines, impro filmée et flash mob, ou Parcours gourmand sur les pas du Roi René. Dès 50 € HT.",
        devis="Team building Aix-en-Provence", hero=("tb-team-building-speed-meeting-hotel-renaissance-aix", "Équipe réunie à Aix-en-Provence"),
        h1="Team building <em>à Aix-en-Provence</em>", lead="La ville des fontaines, terrain de jeu de vos équipes.",
        k2="Deux créations aixoises", h2="Aix, <em>autrement</em>",
        intro="Deux parcours exclusifs dans le centre historique d'Aix-en-Provence : l'un mise sur la créativité et le rire, l'autre sur la gourmandise et l'histoire. À combiner avec un séminaire en hôtel ou en domaine.",
        incl=["Parcours dans le centre historique", "Défis créatifs ou dégustations", "Animateurs sur place", "De 8 à 70 participants", "Déjeuner en option", "Coordination MH Event"],
        duo=[("tb-img-8023", "Atelier de cohésion en intérieur"), ("tb-team-building-sport-olympiades-marseille", "Défi sportif en équipe")],
        rows_k="Prix HT par personne", rows_h="Les parcours <em>aixois</em>",
        rows=[("Aix-périence", "Chasse aux fontaines, impro filmée et flash mob place des Prêcheurs. 2 h 30 à 3 h, 10 à 70 personnes.", "dès 50 €"),
              ("Parcours gourmand et défis royaux", "Sur les pas du Roi René : tapenade, fougasse, calissons. 2 h 30 à 3 h, 8 à 50 personnes.", "dès 70 €")],
        band="Un séminaire à Aix ? Ajoutez une après-midi qui marque.",
        faq_h="Team building <em>à Aix</em>",
        faq=[("Où se déroulent les parcours ?", "Dans le centre historique d'Aix-en-Provence, à pied, entre fontaines, places et artisans."),
             ("Le Parcours gourmand convient-il à tous ?", "Oui ; signalez à l'avance les allergies et régimes particuliers pour adapter les dégustations."),
             ("Peut-on partir de notre hôtel ?", "Oui, MH Event organise le départ depuis votre lieu de séminaire.")],
        related=[("entreprises/team-building/nimes/", "Team building à Nîmes"), ("entreprises/seminaire/", "Séminaires & conventions"), ("entreprises/journee-bien-etre/", "Journées bien-être")],
        cta_t="Votre team building <em>à Aix</em>", cta_p="Dites-nous la date et l'effectif : Mathilde vous propose le parcours adapté.", price=50))

    service_page("entreprises/team-building/pont-du-gard/", dict(
        aud="entreprises", mid=mid, crumb="Pont du Gard", name="Team building au Pont du Gard", stype="Team building", area=["Pont du Gard", "Gard", "Nîmes", "Avignon"],
        title="Team building au Pont du Gard : Marche des senteurs | MH Event",
        desc="Team building au Pont du Gard : yoga puis marche sensorielle dans la garrigue et les plantes méditerranéennes, 5 à 60 personnes, dès 45 € HT.",
        devis="Team building Pont du Gard", hero=("tb-team-building-marche-des-senteurs-mh-event-avril-2026", "Marche des senteurs en pleine nature"),
        h1="Team building <em>au Pont du Gard</em>", lead="Au pied d'un monument de deux mille ans, dans la garrigue.",
        k2="Exclusif MH Event", h2="La garrigue, <em>en silence</em>",
        intro="La Marche des senteurs du Pont du Gard commence par une séance de yoga, puis emmène l'équipe à la découverte des plantes méditerranéennes. Un format qui se décline aussi en bord de mer, dans les calanques.",
        incl=["Yoga en plein air", "Marche sensorielle guidée", "Plantes de la garrigue", "De 5 à 60 participants", "Séminaire sur place possible", "Coordination MH Event"],
        duo=[("tb-team-building-yoga-relaxation-sonore", "Séance de yoga dans l'herbe"), ("bienetre-cours-yoga-evenement-bien-etre", "Yoga en terrasse face aux collines")],
        rows_k="Prix HT par personne", rows_h="La Marche <em>des senteurs</em>",
        rows=[("Au Pont du Gard", "Yoga, garrigue et plantes méditerranéennes. 2 à 3 h, 5 à 60 personnes.", "dès 45 €"),
              ("En bord de mer", "Version plus randonnée, face à la mer, plantes du littoral.", "sur devis")],
        band="Un séminaire dans le Gard ? Commencez par une marche.",
        faq_h="Au <em>Pont du Gard</em>",
        faq=[("Faut-il être bon marcheur ?", "Non, la marche est douce et accessible ; la version bord de mer est un peu plus sportive."),
             ("Peut-on organiser le séminaire sur place ?", "Oui : MH Event a écrit un guide pour organiser un séminaire au Pont du Gard, à lire sur le blog."),
             ("Quelle saison choisir ?", "Le printemps et l'automne sont idéaux ; l'été, la marche se fait tôt le matin.")],
        related=[("blog/seminaire-pont-du-gard/", "Organiser un séminaire au Pont du Gard"), ("entreprises/team-building/nimes/", "Team building à Nîmes"), ("entreprises/team-building/camargue/", "Team building en Camargue")],
        cta_t="Votre marche <em>au Pont du Gard</em>", cta_p="Date et nombre de participants : Mathilde revient vers vous sous 48 heures.", price=45))

    service_page("entreprises/team-building/camargue/", dict(
        aud="entreprises", mid=mid, crumb="Camargue", name="Team building en Camargue, immersion en manade", stype="Team building", area=["Camargue", "Saint-Gilles", "Gard", "Nîmes"],
        title="Team building en Camargue : immersion en manade | MH Event",
        desc="Team building en Camargue avec la Manade Aubanel : trois formules de 57 à 80 € HT, repas camarguais, transport en car depuis Nîmes, jusqu'à 240 personnes.",
        devis="Team building Camargue", hero=("tb-team-building-visite-manade-taureaux-camargue", "Visite de manade en Camargue"),
        h1="Team building <em>en Camargue</em>", lead="Une journée en manade, des taureaux aux gardians.",
        k2="Avec la Manade Aubanel", h2="Les traditions, <em>vécues</em>",
        intro="À Saint-Gilles, la Manade Aubanel ouvre ses prés à vos équipes : calèche, chevaux camarguais, tri des taureaux par les gardians, repas de spécialités. Transport en car aller-retour inclus depuis Nîmes.",
        incl=["Transport en car depuis votre hôtel", "Accueil à la manade", "Visite en calèche", "Démonstrations des gardians", "Repas camarguais en option", "Jusqu'à 240 participants"],
        duo=[("tb-team-building-balade-chevaux-equipe", "Balade à cheval en équipe"), ("dejeuner-img-9076", "Repas servi en extérieur")],
        rows_k="Prix HT par personne, transport compris", rows_h="Trois <em>formules</em>",
        rows=[("Découverte", "Accueil, histoire de la manade, calèche, balade à pied et à cheval, 2 heures.", "dès 57 €"),
              ("Tri des taureaux", "La Découverte, plus le tri des taureaux en plein champ par les gardians.", "dès 70 €"),
              ("Immersion complète", "Le tri, plus une simulation d'abrivado jusqu'aux arènes.", "dès 80 €")],
        note="Repas camarguais dès 39 € HT par personne (demi-tarif enfant). Animation flamenco ou musiciens dès 800 €, musiciens et danseuses 950 €, démonstration de razeteur sur devis.",
        band="Une journée en manade pour votre séminaire ?",
        faq_h="En <em>Camargue</em>",
        faq=[("Le transport est-il compris ?", "Oui : le car aller-retour depuis votre hôtel est inclus dans le prix, sur une base de départ de Nîmes."),
             ("Combien de personnes peut accueillir la manade ?", "Jusqu'à environ 240 personnes, très grands groupes compris."),
             ("Peut-on y déjeuner ?", "Oui, avec un repas de spécialités camarguaises : gardiane de taureau, riz de Camargue, vins et café.")],
        related=[("entreprises/team-building/nimes/", "Team building à Nîmes"), ("entreprises/team-building/pont-du-gard/", "Team building au Pont du Gard"), ("entreprises/seminaire/", "Séminaires & conventions")],
        cta_t="Votre journée <em>en manade</em>", cta_p="Effectif, date et formule : devis sous 48 heures.", price=57))

# ---------------------------------------------------------------- hôtes & hôtesses
def hotesses():
    service_page("entreprises/hotes-hotesses/", dict(
        aud="entreprises", crumb="Hôtes & hôtesses", name="Hôtes et hôtesses d'accueil événementiel", stype="Hôtesses d'accueil événementiel",
        title="Hôtesses d'accueil événementiel à Marseille, Aix | MH Event",
        desc="Les Angelines : hôtes et hôtesses d'accueil sélectionnés et formés pour vos salons, congrès, conventions et soirées. Dès 26 € HT de l'heure, 4 h minimum.",
        devis="Hôtesses", hero=("hotesses-hotesses-marinieres-nautique-saint-tropez-rencontres-economiques", "Hôtesse MH Event en marinière à Saint-Tropez", "50% 30%"),
        h1="Hôtes <em>&amp; hôtesses</em>", lead="Le premier sourire de votre événement.",
        k2="Les Angelines", h2="Formées par une <em>cheffe hôtesse</em>",
        intro="Mathilde a commencé comme hôtesse au Grand Prix de France de F1. Elle sélectionne, forme et coache ses équipes avec la même exigence, et les habille selon le thème de votre événement, jamais en uniforme classique.",
        incl=["Accueil, émargement, badges", "Accueil VIP et placement en salle", "Hôtesses de conférence, passage micro", "Vestiaire, documents et cadeaux", "Animations commerciales sur stand", "Cheffe hôtesse et régie sur site"],
        duo=[("hotesses-hotesses-mh-event-marche", "Hôtesses MH Event en tailleur noir"), ("hotesses-89fd2f99-4d59-40f7-8307-bdfc0a64e9ea", "Hôtesses préparant l'accueil")],
        rows_k="Conditions", rows_h="Tarifs <em>et modalités</em>",
        rows=[("Mission de jour", "Par hôte ou hôtesse.", "26 € HT / h"), ("Mission de nuit", "De 22 h à 7 h, majoration selon la convention collective.", "32,50 € HT / h"),
              ("Durée minimale", "4 heures par hôte ou hôtesse. Forfait de déplacement en sus."),
              ("Repas", "Une collation est à prévoir si la mission couvre un repas, par vous ou par MH Event.")],
        note="Démarche responsable : rémunération supérieure aux standards du marché, missions déclarées, minimum d'heures garanti, tenues valorisantes.",
        band="Date, horaires, nombre d'hôtesses : réservez votre équipe.",
        real=["evenement-gepa-aix-en-provence", "soiree-reseau-entreprendre-marseille", "rencontres-economiques-nautisme-saint-tropez"], faq_h="Réserver <em>des hôtesses</em>",
        faq=[("Quel est le tarif d'une hôtesse d'accueil ?", "26 € HT de l'heure en journée et 32,50 € HT la nuit, avec quatre heures minimum par hôte ou hôtesse et un forfait de déplacement."),
             ("Que faut-il pour un devis ?", "La date, les horaires, le nombre d'hôtes ou d'hôtesses, les missions et la tenue souhaitée."),
             ("Quels événements couvrez-vous ?", "Salons, congrès, forums, conventions, inaugurations, remises de diplômes, soirées de gala et séminaires en hôtel.")],
        related=[("entreprises/conference-salon-afterwork/", "Conférences, salons & afterworks"), ("entreprises/inauguration/", "Inaugurations & lancements"), ("hotels/hotes-hotesses/", "Hôtesses pour hôtels"), ("particuliers/hotes-hotesses/", "Hôtesses pour mariages et réceptions")],
        cta_t="Réservez vos <em>Angelines</em>", cta_p="Quelques informations suffisent : Mathilde vous confirme l'équipe et le devis sous 48 heures.", price=26))

# ================================================================ HÔTELS
def hotels():
    hub_page("hotels/", dict(
        title="Animation et événements pour hôtels | MH Event",
        desc="MH Event fait vivre les hôtels : soirées vitrines toute l'année, soirées séminaires à vendre, Déjeuner Corpo et séminaires découverte, à Marseille, Aix et Nîmes.",
        crumb="Hôtels", tab="hotels", kicker="Hôtels", devis="Soirée en hôtel",
        hero=("hotel-lobby-luxe", "Hall d'un hôtel de luxe éclairé en soirée"),
        h1="Faire vivre <em>votre</em> hôtel", lead="Un bar qui se remplit, une clientèle locale qui revient, des contrats MICE qui suivent.",
        k2="La spécialité de MH Event", h2="Un lieu <em>de vie</em>",
        intro="Votre hôtel n'est plus seulement un lieu où l'on dort : c'est une adresse où l'on sort, où l'on se réunit, où l'on revient. MH Event conçoit et anime vos événements toute l'année.",
        duo=[("hotel-soiree-saxophone-lounge-hotel-marseille-dynamisation", "Soirée saxophone Lounge en hôtel"), ("hotel-pianiste-soiree-opera-hotel-blanc", "Pianiste lors d'une soirée Opéra et champagne")],
        svc_h="Pour les <em>hôtels</em>",
        cards=[
         ("hotels/animation-dynamisation/", "hotel-comedy-show-marseille-juin-2026", "Comedy Club dans un hôtel de Marseille", "Animation <em>&amp; dynamisation</em>", "Une à deux soirées vitrines par mois, ouvertes au public."),
         ("hotels/soirees-seminaires/", "hotel-chanteur-opera-soiree-hotel-mh-event", "Chanteur lyrique en soirée", "Soirées <em>séminaires</em>", "Un catalogue chiffré pour vos commerciaux, dès 1 590 € HT."),
         ("hotels/dejeuner-corpo/", "dejeuner-img-9036", "Invités d'un Déjeuner Corpo au Golden Tulip", "Déjeuner <em>Corpo</em>", "Faire découvrir l'hôtel à 50 professionnels locaux."),
         ("hotels/seminaires-decouverte/", "hotel-discussion-invites-evenements-hotel-odalys-euromed", "Invités en conversation dans un hôtel", "Séminaires <em>découverte</em>", "Accueillir des acheteurs, décrocher des contrats."),
         ("hotels/team-building/", "tb-team-building-speed-meeting-hotel-renaissance-aix", "Speed Meeting dans un hôtel d'Aix-en-Provence", "Team <em>building</em>", "Une expérience à ajouter à vos offres séminaires."),
         ("hotels/hotes-hotesses/", "hotesses-1dd14db4-c9e9-425f-9873-2b419e3f39b3", "Hôtesses à l'accueil d'un événement en hôtel", "Hôtes <em>&amp; hôtesses</em>", "Renforts d'accueil pour vos événements."),
        ],
        band="Parlons de la programmation de votre hôtel.",
        real=["golden-night-golden-tulip-marseille", "escale-mediterraneenne-golden-tulip", "odalys-euromed-marseille"],
        logos=["golden-tulip", "odalys-euromed", "odalys-city", "sowell", "hotels-de-nimes", "pasino-grand", "nimes-tourisme", "cds-groupe"],
        cta_t="Parlons de <em>votre</em> hôtel", cta_p="Votre établissement, vos objectifs, votre saison : Mathilde vous propose un programme."))

def services_hotels():
    service_page("hotels/animation-dynamisation/", dict(
        aud="hotels", crumb="Animation & dynamisation", name="Animation et dynamisation d'hôtel", stype="Animation d'hôtel",
        title="Animation d'hôtel et soirées à thème | MH Event",
        desc="Programmation annuelle de soirées vitrines pour hôtels : Comedy Club, blind test, casino, piano-bar, guinguette. Référence : Golden Night au Golden Tulip Marseille.",
        devis="Animation d'hôtel", hero=("hotel-comedy-show-marseille-juin-2026", "Comedy Club au Golden Tulip Marseille Euromed", "50% 30%"),
        h1="Animation <em>&amp; dynamisation</em>", lead="Une à deux soirées par mois pour faire de votre hôtel une adresse.",
        k2="Programmation annuelle", h2="Du passage, <em>toute l'année</em>",
        intro="MH Event construit votre programme sur l'année, avec planning, descriptif et devis par soirée. Des soirées vitrines ouvertes au public qui font tourner le bar et le restaurant, attirent une clientèle locale et nourrissent vos réseaux sociaux.",
        incl=["Programme annuel et planning", "Thèmes renouvelés chaque mois", "Artistes et animateurs", "Communication de la soirée", "Accueil et service en renfort", "Bilan après chaque soirée"],
        duo=[("hotel-soiree-guinguette-terrasse-hotel-marseille-dynamisation", "Guinguette en terrasse d'hôtel"), ("hotel-soiree-saxophone-lounge-hotel-marseille-dynamisation-1", "Saxophoniste en soirée Lounge")],
        rows_k="Soirées vitrines", rows_h="Quelques <em>idées</em>",
        rows=[("Comedy Club", "Stand-up dans les salons ou sur le rooftop."), ("Quiz et blind test", "Des équipes, un animateur, des lots."), ("Casino", "Tables de jeu et ambiance."),
              ("Piano-bar et guinguette", "Musique live au bar ou en terrasse."), ("Ciné-club immersif, soirée ski, années 80-90", "Des thèmes qui changent chaque mois.")],
        band="Vous voulez remplir votre bar en semaine ?",
        real=["golden-night-golden-tulip-marseille", "golden-plus-concept", "soiree-feria-sowell-nimes"], faq_h="Animer <em>son hôtel</em>",
        faq=[("Combien coûte une soirée de dynamisation ?", "Chaque soirée fait l'objet d'un devis, dans le cadre d'un programme sur l'année : le prix dépend du thème, des artistes et de la fréquence."),
             ("La soirée doit-elle être gratuite pour le public ?", "Pas forcément. Les Golden Night du Golden Tulip Marseille Euromed sont gratuites et ouvertes à tous ; d'autres hôtels choisissent une entrée payante ou un menu."),
             ("Quel engagement est demandé ?", "Un engagement sur la durée, pour installer un rendez-vous que la clientèle locale attend chaque mois.")],
        related=[("hotels/soirees-seminaires/", "Soirées séminaires"), ("hotels/dejeuner-corpo/", "Déjeuner Corpo"), ("blog/soirees-dynamisation-hotel/", "Remplir son bar en hiver")],
        cta_t="Votre <em>programme</em>", cta_p="Votre hôtel, votre clientèle, votre saison : Mathilde vous propose un calendrier de soirées."))

    service_page("hotels/soirees-seminaires/", dict(
        aud="hotels", crumb="Soirées séminaires", name="Catalogue de soirées séminaires pour hôtels", stype="Soirée séminaire en hôtel",
        title="Soirées séminaires pour hôtels : catalogue et prix | MH Event",
        desc="Catalogue de soirées privatisées à intégrer à vos offres séminaires : Opéra et champagne, Nuit andalouse, Kermesse, Gatsby, Cluedo géant. Dès 1 590 € HT.",
        devis="Soirée séminaire", hero=("hotel-soiree-live-painting-hotel-odalys-euromed-marseille", "Soirée live painting dans un hôtel de Marseille"),
        h1="Soirées <em>séminaires</em>", lead="Une soirée originale, prête à glisser dans vos propositions commerciales.",
        k2="Pour vos commerciaux", h2="Vendez <em>une expérience</em>",
        intro="MH Event remet à votre équipe commerciale un catalogue de soirées privatisées. Quand elle construit une offre de séminaire, elle y ajoute la soirée ; MH Event l'organise de A à Z, avec des artistes locaux. Versions Marseille et Nîmes.",
        incl=["Catalogue remis à vos commerciaux", "Prix indicatifs pour vos devis", "Artistes et prestataires locaux", "Organisation de A à Z", "Soirée privatisée pour le groupe", "Déclinaison par ville"],
        duo=[("hotel-live-painting-raphael-federici-saxophoniste", "Live painting accompagné d'un saxophoniste"), ("hotel-comedy-club-malik-fares", "Humoriste sur scène lors d'une soirée")],
        rows_k="Prix indicatifs HT", rows_h="Le <em>catalogue</em>",
        rows=[("Nuit andalouse", "Harpe et danseuse de flamenco.", "2 850 €"), ("Opéra et champagne", "Chanteurs lyriques et pianiste.", "3 650 €"),
              ("Kermesse", "Puissance 4 géant, Mölkky, chamboule-tout.", "1 590 €"), ("Cluedo géant", "Six comédiens, une enquête grandeur nature.", "≈ 2 600 €"),
              ("Gatsby", "Dîner-spectacle années folles.", "≈ 5 000 €"), ("Le Vernissage", "Live painting.", "3 100 €"),
              ("Velvet Lounge · Piano Club", "Saxophone ou piano.", "1 850 · 2 400 €"), ("Hiver blanc", "Danseuses, chanteur, DJ, environ 100 personnes.", "4 300 €"),
              ("Quiz, blind test, casino", "Jeux et animations.", "dès 1 790 €"), ("Comedy Club, cabaret, mentalisme", "Dîners-spectacles.", "sur devis")],
        band="Recevez le catalogue pour votre équipe commerciale.",
        real=["odalys-euromed-marseille"], faq_h="Le <em>catalogue</em>",
        faq=[("Qui vend la soirée au client ?", "Votre équipe commerciale, dans sa proposition de séminaire. MH Event organise ensuite la soirée de A à Z."),
             ("Les prix sont-ils fixes ?", "Ce sont des prix indicatifs HT ; le devis final dépend de la date, du lieu et du nombre de participants."),
             ("Existe-t-il une version pour notre ville ?", "Le catalogue existe en version Marseille et Nîmes, avec des artistes locaux ; d'autres villes sont possibles.")],
        related=[("hotels/animation-dynamisation/", "Animation & dynamisation"), ("hotels/team-building/", "Team building pour hôtels"), ("hotels/seminaires-decouverte/", "Séminaires découverte")],
        cta_t="Votre <em>catalogue</em>", cta_p="Demandez le catalogue de soirées séminaires pour votre hôtel.", price=1590))

    service_page("hotels/dejeuner-corpo/", dict(
        aud="hotels", crumb="Déjeuner Corpo", name="Déjeuner Corpo, déjeuner de prospection pour hôtels", stype="Déjeuner d'affaires en hôtel",
        title="Déjeuner Corpo : faire découvrir votre hôtel | MH Event",
        desc="Un déjeuner immersif de 2 h à 2 h 30 pour 50 professionnels locaux : chambres, salles, restauration, contacts récupérés. Trois packs de 2 400 à 3 900 € HT.",
        devis="Déjeuner Corpo", hero=("dejeuner-img-9064", "Invitées en marinière lors de l'Escale Méditerranéenne"),
        h1="Déjeuner <em>Corpo</em>", lead="Deux heures pour que 50 décideurs locaux découvrent votre hôtel.",
        k2="Prospection locale", h2="Un déjeuner <em>qui prospecte</em>",
        intro="Un parcours dans votre établissement, pensé comme une expérience : vos invités visitent les chambres, les salles de séminaire, goûtent la restauration et profitent des extérieurs. MH Event récupère leurs contacts, avec leur accord, pour vos commerciaux.",
        incl=["Concept et thème du déjeuner", "Invitation de 50 professionnels locaux", "Parcours de découverte de l'hôtel", "Animation et jeu concours", "Staff en tenue accordée au thème", "Contacts récupérés pour vos commerciaux"],
        duo=[("dejeuner-img-9052", "Buffet en terrasse"), ("dejeuner-img-9067", "Accueil des invités avec un sac cadeau")],
        rows_k="Trois packs HT", rows_h="Votre <em>Déjeuner Corpo</em>",
        rows=[("Durée", "2 h à 2 h 30, à l'heure du déjeuner."), ("Invités", "Environ 50 professionnels locaux."), ("Packs", "Trois niveaux selon le concept et les animations.", "2 400 à 3 900 €")],
        band="Remplissez vos salles de séminaire avec des clients locaux.",
        real=["escale-mediterraneenne-golden-tulip", "dejeuner-corporate-odalys-aix", "golden-tulip-festival"], faq_h="Le <em>Déjeuner Corpo</em>",
        faq=[("Qui invite les professionnels ?", "MH Event et l'hôtel construisent ensemble la liste d'invités : entreprises, agences, institutions locales."),
             ("Que récupère l'hôtel ?", "Les contacts des invités, avec leur autorisation d'être recontactés, et du contenu pour ses réseaux."),
             ("Quels thèmes ont déjà été réalisés ?", "L'Escale Méditerranéenne au Golden Tulip Marseille Euromed, une Kermesse à l'Odalys Euromed et un Cirque à l'Odalys d'Aix-en-Provence.")],
        related=[("hotels/seminaires-decouverte/", "Séminaires découverte"), ("hotels/animation-dynamisation/", "Animation & dynamisation"), ("hotels/hotes-hotesses/", "Hôtes & hôtesses")],
        cta_t="Votre <em>Déjeuner Corpo</em>", cta_p="Choisissez votre pack : Mathilde vous propose un concept pour votre hôtel.", price=2400))

    service_page("hotels/seminaires-decouverte/", dict(
        aud="hotels", crumb="Séminaires découverte", name="Séminaires découverte et éductours pour hôtels", stype="Éductour hôtelier",
        title="Séminaire découverte et éductour pour hôtels | MH Event",
        desc="Accueillir des acheteurs, agences et entreprises de toute la France pour leur faire vivre votre hôtel : déjeuner, visite, team building, soirée, nuit et rendez-vous.",
        devis="Séminaire découverte", hero=("hotel-soiree-inauguration-hotel-odalys-euromed-janvier-2025", "Invités réunis dans un hôtel de Marseille"),
        h1="Séminaires <em>découverte</em>", lead="Faire vivre votre hôtel à ceux qui le recommanderont.",
        k2="Acheteurs et agences", h2="Vivre l'hôtel <em>avant de le vendre</em>",
        intro="L'hôtel accueille un groupe d'acheteurs (agences événementielles, entreprises) venus de toute la France, voire de l'étranger. MH Event conçoit leur séjour pour qu'ils vivent l'établissement et rencontrent les partenaires locaux. Le format se joue dans un hôtel ou entre plusieurs hôtels d'une même ville.",
        incl=["Programme du séjour", "Déjeuner et visite thématisée", "Team building", "Soirée et nuit sur place", "Rendez-vous avec les partenaires locaux", "Format multi-hôtels possible"],
        duo=[("hotel-discussion-invites-evenements-hotel-odalys-euromed", "Invités en conversation dans un hôtel"), ("dejeuner-dejeuner-affaire-discussions-hotel-juin-2026", "Déjeuner d'affaires dans un hôtel")],
        band="Des acheteurs à convaincre ? Organisons leur séjour.",
        faq_h="Le séminaire <em>découverte</em>",
        faq=[("Qui sont les invités ?", "Des acheteurs : agences événementielles et entreprises qui organisent des séminaires, venus de toute la France ou de l'étranger."),
             ("Plusieurs hôtels peuvent-ils s'associer ?", "Oui : le séjour peut se partager entre plusieurs hôtels d'une même ville, avec un programme commun."),
             ("Quels partenaires locaux rencontrent-ils ?", "Les prestataires qui font vivre vos séminaires : traiteurs, lieux, activités, selon le programme que vous choisissez.")],
        related=[("hotels/dejeuner-corpo/", "Déjeuner Corpo"), ("hotels/soirees-seminaires/", "Soirées séminaires"), ("hotels/team-building/", "Team building pour hôtels")],
        cta_t="Votre séminaire <em>découverte</em>", cta_p="Nombre d'acheteurs, dates, hôtels partenaires : Mathilde construit le programme."))

    service_page("hotels/team-building/", dict(
        aud="hotels", crumb="Team building", name="Team building à proposer dans les offres séminaires d'un hôtel", stype="Team building en hôtel",
        title="Team building pour hôtels et offres séminaires | MH Event",
        desc="Proposez à vos clients séminaires un team building clé en main dans votre hôtel ou à proximité : Speed Meeting, Instant Zen, Olympiades, éveil corporel.",
        devis="Team building en hôtel", hero=("tb-img-6306-2", "Séance de yoga sous une voûte de pierre"),
        h1="Team building <em>pour vos clients</em>", lead="Une expérience de plus dans vos propositions de séminaire.",
        k2="Pour les hôtels", h2="Un séminaire <em>plus vendeur</em>",
        intro="Vos commerciaux ajoutent un team building à leur offre ; MH Event l'anime dans vos salles, vos jardins ou à quelques minutes de l'hôtel. Vos clients repartent avec un souvenir, votre hôtel avec un séminaire réussi.",
        incl=["Activités dans l'hôtel ou à proximité", "Prix par personne pour vos devis", "Animation par des professionnels", "Coordination avec vos équipes", "Intérieur ou extérieur", "Réveil bien-être le matin"],
        duo=[("tb-team-building-speed-meeting-hotel-renaissance-aix", "Speed Meeting dans un hôtel d'Aix-en-Provence"), ("tb-team-building-fabrique-des-couleurs-marche-consciente-the-camp", "La Fabrique des couleurs")],
        rows_k="Les plus demandés en hôtel", rows_h="Quatre <em>activités</em>",
        rows=[("Speed Meeting", "Pour briser la glace en début de séminaire.", "dès 28 €"), ("Instant Zen Détente", "Pour une après-midi qui recharge.", "dès 47 €"),
              ("Olympiades et défis", "Pour une salle ou un jardin.", "dès 30 €"), ("Éveil corporel du matin", "Yoga ou Pilates avant la plénière.", "sur devis")],
        band="Ajoutez un team building à vos offres séminaires.",
        faq_h="Team building <em>en hôtel</em>",
        faq=[("Les activités se tiennent-elles dans l'hôtel ?", "La plupart, oui : en salle, en terrasse ou dans le jardin. D'autres se jouent à proximité, comme la Marche des senteurs."),
             ("Comment l'intégrer à nos devis ?", "MH Event vous transmet des prix par personne que vos commerciaux reprennent directement dans leurs propositions."),
             ("Où voir toutes les activités ?", "Le catalogue complet des quinze team buildings est présenté sur la page Team building entreprises.")],
        related=[("entreprises/team-building/", "Le catalogue complet"), ("hotels/soirees-seminaires/", "Soirées séminaires"), ("hotels/hotes-hotesses/", "Hôtes & hôtesses")],
        cta_t="Enrichissez <em>vos offres</em>", cta_p="Recevez les fiches des activités et les prix pour vos commerciaux.", price=28))

    service_page("hotels/hotes-hotesses/", dict(
        aud="hotels", crumb="Hôtes & hôtesses", name="Hôtes et hôtesses pour les événements d'hôtels", stype="Hôtesses d'accueil en hôtel",
        title="Hôtesses d'accueil pour hôtels et séminaires | MH Event",
        desc="Renforts d'accueil pour vos séminaires, soirées vitrines et Déjeuners Corpo : hôtes, hôtesses, barmans et serveurs formés, en tenue accordée à votre événement.",
        devis="Hôtesses", hero=("hotesses-img-9066", "Hôtesse MH Event en marinière lors d'un déjeuner en hôtel", "50% 30%"),
        h1="L'accueil <em>de vos clients</em>", lead="Des renforts élégants les jours où votre hôtel reçoit.",
        k2="Les Angelines en hôtel", h2="Votre maison, <em>leur discrétion</em>",
        intro="Quand vous accueillez un séminaire, une soirée vitrine ou un Déjeuner Corpo, les Angelines renforcent votre réception : émargement, orientation, vestiaire, service. Au Golden Tulip Marseille Euromed, tout le staff était en marinière pour l'Escale Méditerranéenne.",
        incl=["Accueil des séminaires", "Orientation dans l'hôtel", "Vestiaire des soirées", "Parcours des Déjeuners Corpo", "Barmans et serveurs en renfort", "Cheffe hôtesse en lien avec vos équipes"],
        duo=[("hotesses-1c340331-35d4-48c7-8dc5-86eb8c68496c", "Hôtesse à l'accueil d'un hôtel"), ("hotesses-702fe5a0-dd3e-4cf4-9ede-d07c6874c02f", "Deux hôtesses à l'accueil")],
        band="Un événement dans votre hôtel ? Réservez l'accueil.",
        real=["escale-mediterraneenne-golden-tulip"], faq_h="Hôtesses <em>en hôtel</em>",
        faq=[("Les hôtesses travaillent-elles avec notre réception ?", "Oui : une cheffe hôtesse fait le lien avec vos équipes pour que l'accueil reste fluide."),
             ("Pouvez-vous fournir des barmans ?", "Oui, ainsi que des serveurs et des mixologues pour vos soirées."),
             ("Quel tarif ?", "Dès 26 € HT de l'heure en journée, quatre heures minimum ; le détail des conditions figure sur la page Hôtes & hôtesses entreprises.")],
        related=[("entreprises/hotes-hotesses/", "Conditions et tarifs détaillés"), ("hotels/dejeuner-corpo/", "Déjeuner Corpo"), ("hotels/animation-dynamisation/", "Animation & dynamisation")],
        cta_t="L'accueil <em>de votre hôtel</em>", cta_p="Date, horaires, nombre de personnes : devis sous 48 heures.", price=26))

# ================================================================ PARTICULIERS
def particuliers():
    hub_page("particuliers/", dict(
        title="Organisation d'événements privés et mariages | MH Event",
        desc="Mariages, coordination du jour J, anniversaires et fêtes privées en Provence et dans le Gard, avec la même exigence que pour les entreprises.",
        crumb="Particuliers", tab="particuliers", kicker="Particuliers", devis="Mariage",
        hero=("mariage-organisation-mariage-domaine-aix-juillet-2025", "Mariage dans un domaine près d'Aix-en-Provence"),
        h1="Vos plus beaux <em>moments</em>", lead="Mariages, anniversaires, fêtes de famille, en Provence et dans le Gard.",
        k2="MH Wedding &amp; privé", h2="Pensés <em>pour vous</em>",
        intro="Un planning tenu, des prestataires choisis, et vous, présents à chaque instant de votre fête.",
        duo=[("mariage-photo-mariage-shooting-robe-blanche", "Mariée en robe blanche dans un domaine"), ("prive-bal-masque-evement-prive", "Couple masqué devant une voiture ancienne")],
        svc_h="Pour <em>vous</em>",
        cards=[
         ("particuliers/mariage/", "mariage-shooting-mariage-couple-sourire-domaine-montpellier", "Mariés souriants dans une allée de domaine", "Wedding <em>planner</em>", "Organisation complète de votre mariage, dès 3 500 €."),
         ("particuliers/coordination-jour-j/", "mariage-ceremonie-mariage-juillet-2025", "Cérémonie de mariage", "Coordination <em>du jour J</em>", "Vous profitez, Mathilde orchestre."),
         ("particuliers/anniversaire-fete-privee/", "prive-anniversaire-30-ans-bateau-marseille", "Anniversaire de 30 ans en bateau", "Anniversaires <em>&amp; fêtes</em>", "30 ans, baptême, fête de famille, soirée à thème."),
         ("particuliers/hotes-hotesses/", "hotesses-f25d5f7f-b901-4e6d-abb2-1578bbd3a3e4-2", "Hôtesses MH Event", "Hôtes <em>&amp; hôtesses</em>", "Accueil, vestiaire, service pour vos invités."),
        ],
        band="Une date, un lieu rêvé ? Parlons de votre fête.",
        real=["mariage-domaine-aix-en-provence", "bal-masque-h9ritage-valmousse", "anniversaire-30-ans-bateau-marseille"], real_h="Vos <em>fêtes</em>",
        cta_t="Racontez-nous <em>votre</em> projet", cta_p="Une date, un lieu rêvé, un nombre d'invités : quelques mots suffisent."))

def services_particuliers():
    service_page("particuliers/mariage/", dict(
        aud="particuliers", crumb="Wedding planner", name="Wedding planner en Provence et dans le Gard", stype="Organisation de mariage",
        title="Wedding planner en Provence et dans le Gard | MH Event",
        desc="Organisation complète de mariage en Provence et dans le Gard dès 3 500 € : prestataires, visites, dégustations, budget. Mariages sur plusieurs jours, devis en anglais.",
        devis="Mariage", hero=("mariage-photo-maries-mariage-gruissan-2024", "Mariés face à la mer"),
        h1="Wedding <em>planner</em>", lead="Vous vous dites oui, Mathilde s'occupe du reste.",
        k2="MH Wedding · Gard &amp; Provence", h2="Un mariage <em>qui vous ressemble</em>",
        intro="Ancienne wedding planner du Domaine du Grand Lauron, à Cadenet, Mathilde organise des mariages en Provence et dans le Gard, souvent sur plusieurs jours : welcome party, mariage, brunch, pool party.",
        incl=["Recherche et réservation des prestataires", "Visites, dégustations, essais", "Visites techniques du lieu", "Suivi du budget", "Rétroplanning", "Présence le jour J"],
        duo=[("mariage-mariage-ceremonie-laique-domaine", "Cérémonie laïque dans un domaine"), ("mariage-bouquet-mariage-domaine-herault-montpellier", "Bouquet de mariée posé sur un muret")],
        rows_k="Idées signature", rows_h="Les <em>détails</em>",
        rows=[("Bar à cocktails du Sud", "Pour le vin d'honneur."), ("Braséros", "Pour l'apéritif à la tombée du jour."), ("Tables rondes fleuries", "Et charm bar pour les invités."),
              ("Livre d'or polaroid", "Et coin beauté : coiffeuse, massage, shooting."), ("Photographe et drone", "Pour garder chaque moment.")],
        band="Votre mariage commence par une conversation.",
        real=["mariage-domaine-aix-en-provence", "mariage-gruissan"], faq_h="Questions de <em>futurs mariés</em>",
        faq=[("Combien coûte un wedding planner ?", "L'organisation complète démarre à 3 500 €. Le devis précise les prestations comprises selon votre projet."),
             ("Organisez-vous des mariages pour des couples vivant à l'étranger ?", "Oui, avec un devis et un planning en anglais : de nombreux couples étrangers choisissent la Provence."),
             ("Peut-on organiser le mariage sur plusieurs jours ?", "Oui : welcome party la veille, mariage, brunch ou pool party le lendemain.")],
        related=[("particuliers/coordination-jour-j/", "Coordination du jour J"), ("particuliers/hotes-hotesses/", "Hôtesses pour mariage"), ("particuliers/anniversaire-fete-privee/", "Anniversaires & fêtes")],
        cta_t="Racontez-nous <em>votre mariage</em>", cta_p="Date, lieu, nombre d'invités : Mathilde vous rappelle pour en parler.", price=3500,
        area=["Provence", "Gard", "Aix-en-Provence", "Nîmes", "Montpellier", "Marseille"]))

    service_page("particuliers/coordination-jour-j/", dict(
        aud="particuliers", crumb="Coordination du jour J", name="Coordination du jour J de mariage", stype="Coordination de mariage",
        title="Coordination du jour J de mariage en Provence | MH Event",
        desc="Vous avez tout organisé ? Mathilde reprend votre planning, rencontre vos prestataires et orchestre votre mariage de l'installation à la fin de soirée.",
        devis="Coordination jour J", hero=("mariage-maries-danse-ouverture-bal-mariage-gard", "Ouverture de bal d'un mariage dans le Gard", "50% 35%"),
        h1="Coordination <em>du jour J</em>", lead="Vous avez tout préparé ; le jour venu, vous profitez.",
        k2="Le jour J", h2="Présents, <em>pas occupés</em>",
        intro="Quelques semaines avant le mariage, Mathilde reprend votre planning et rencontre vos prestataires. Le jour J, elle est sur place de l'installation à la fin de soirée, pour que personne ne vienne vous chercher.",
        incl=["Reprise du planning", "Rencontre des prestataires", "Rétroplanning détaillé", "Présence dès l'installation", "Gestion des imprévus", "Jusqu'à la fin de soirée"],
        duo=[("mariage-installation-tables-mariage-gruissan", "Installation des tables d'un mariage"), ("mariage-mariage-vin-honneur-gruissan", "Vin d'honneur au bord de l'eau")],
        band="La date approche ? Il est encore temps.",
        real=["mariage-gruissan"], faq_h="La coordination <em>du jour J</em>",
        faq=[("Quand faire appel à une coordinatrice ?", "Idéalement deux à trois mois avant le mariage, pour reprendre le planning et rencontrer vos prestataires sereinement."),
             ("Quel est le tarif ?", "La coordination du jour J est sur devis, selon la durée de présence et la taille du mariage."),
             ("Et si nous avons déjà nos prestataires ?", "C'est le principe : Mathilde travaille avec les prestataires que vous avez choisis.")],
        related=[("particuliers/mariage/", "Organisation complète"), ("particuliers/hotes-hotesses/", "Hôtesses pour mariage")],
        cta_t="Votre <em>jour J</em>", cta_p="Date et lieu du mariage : Mathilde vous dit si elle est disponible."))

    service_page("particuliers/anniversaire-fete-privee/", dict(
        aud="particuliers", crumb="Anniversaires & fêtes", name="Organisation d'anniversaires et de fêtes privées", stype="Organisation de fête privée",
        title="Organisation d'anniversaire et de fête privée | MH Event",
        desc="Anniversaire de 30 ou 40 ans, baptême, fête de famille ou soirée à thème privée (Gatsby, guinguette, casino) à Marseille, Aix, Nîmes et en Provence.",
        devis="Anniversaire", hero=("prive-anniversaire-30-ans-bateau-marseille", "Anniversaire de 30 ans en bateau au large de Marseille"),
        h1="Anniversaires <em>&amp; fêtes</em>", lead="Une fête à votre image, sans rien gérer.",
        k2="Fêtes privées", h2="Votre fête, <em>en grand</em>",
        intro="À domicile, en domaine ou en mer : MH Event reprend les soirées qui font son succès auprès des entreprises, en version privée, et s'occupe de tout, du lieu au dernier invité.",
        incl=["Choix du lieu", "Thème et décor", "Traiteur ou food truck", "Musique et animations", "Accueil et service", "Coordination de la fête"],
        duo=[("prive-pancarte-accueil-bapteme", "Pancarte d'accueil d'un baptême"), ("prive-mh-event-evenement-food-truck-2024", "Réception privée avec food truck")],
        rows_k="Idées de fêtes", rows_h="À chaque <em>occasion</em>",
        rows=[("Anniversaires", "30 ans, 40 ans, en mer, en domaine ou à la maison."), ("Baptêmes et fêtes de famille", "Accueil, décor, repas."),
              ("Soirées à thème", "Gatsby, guinguette, casino, kermesse, opéra."), ("Bal masqué", "Comme le bal H9RITAGE au Château de Valmousse.")],
        band="Une fête à préparer ? Dites-nous tout.",
        real=["anniversaire-30-ans-bateau-marseille", "bal-masque-h9ritage-valmousse"], faq_h="Votre <em>fête</em>",
        faq=[("Organisez-vous des fêtes à domicile ?", "Oui, à domicile comme en domaine ou sur un bateau, selon le nombre d'invités et l'ambiance souhaitée."),
             ("Peut-on reprendre un thème des soirées d'entreprise ?", "Oui : Gatsby, guinguette, casino, kermesse ou opéra se déclinent en version privée."),
             ("Quel budget prévoir ?", "Chaque fête fait l'objet d'un devis détaillé selon le lieu, le nombre d'invités et les animations.")],
        related=[("particuliers/hotes-hotesses/", "Hôtesses pour réceptions"), ("particuliers/mariage/", "Wedding planner")],
        cta_t="Votre <em>fête</em>", cta_p="Date, lieu, nombre d'invités : Mathilde vous propose une idée et un devis."))

    service_page("particuliers/hotes-hotesses/", dict(
        aud="particuliers", crumb="Hôtes & hôtesses", name="Hôtes, hôtesses et serveurs pour mariages et réceptions privées", stype="Personnel de réception privée",
        title="Hôtesses et serveurs pour mariage et réception | MH Event",
        desc="Accueil des invités, vestiaire, bar et service pour votre mariage ou votre réception privée en Provence : une équipe formée, pendant que vous profitez.",
        devis="Hôtesses", hero=("hotesses-hotesses-mh-event-look-t-shirt-flocage", "Équipe MH Event en tee-shirts brodés du logo"),
        h1="Vos invités <em>bien reçus</em>", lead="Une équipe qui accueille, sert et veille, pendant que vous profitez.",
        k2="Pour vos réceptions", h2="Recevoir <em>sans courir</em>",
        intro="Mariage, anniversaire, réception à domicile : les Angelines accueillent vos invités, tiennent le vestiaire, servent au bar et à table, avec la discrétion d'un grand hôtel.",
        incl=["Accueil et placement des invités", "Vestiaire", "Bar et cocktails", "Service à table", "Livre d'or et cadeaux", "Coordination de l'équipe"],
        duo=[("hotesses-img-9366", "Hôtesse MH Event souriante"), ("hotesses-equipe-mh-event-hotesses-animatrices", "Équipe d'hôtesses et animatrices MH Event")],
        band="Réservez l'équipe de votre réception.",
        faq_h="Une équipe <em>pour vos invités</em>",
        faq=[("Combien de personnes prévoir ?", "Cela dépend du nombre d'invités et du service : Mathilde vous conseille l'équipe juste nécessaire."),
             ("Les tenues sont-elles adaptées à la fête ?", "Oui : les tenues sont toujours accordées au thème de votre réception."),
             ("Quel tarif ?", "Dès 26 € HT de l'heure par personne, quatre heures minimum, déplacement en sus.")],
        related=[("particuliers/mariage/", "Wedding planner"), ("particuliers/coordination-jour-j/", "Coordination du jour J"), ("entreprises/hotes-hotesses/", "Conditions détaillées")],
        cta_t="Votre <em>équipe</em>", cta_p="Date, horaires, nombre d'invités : devis sous 48 heures.", price=26,
        area=["Provence", "Gard", "Aix-en-Provence", "Marseille", "Nîmes"]))

# ================================================================ AGENCE
def agence():
    body = hero_photo("mathilde-mathilde-heyral-wedding-planner", "Mathilde Heyral dressant une table", "L'agence · depuis 2023",
                      "Mathilde <em>Heyral</em>", "Fondatrice et présidente de MH Event.", pos="50% 25%", actions=hero_actions("devis/")) + f'''
<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block("Une agence à taille humaine", "Rien n'est <em>standard</em>", "Née fin 2023 en Provence, installée à Nîmes, MH Event suit chaque projet avec la même personne, la même exigence et le même cœur.")}</div>
 {duo("mathilde-mathilde-heyral-protrait-pro-evenement", "Portrait de Mathilde Heyral", "mathilde-img-9513", "Mathilde Heyral prépare une table")}
</div></section>
<section class="sec flush"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Le fil d'une histoire</p><h2 class="t-h2 fade">Un parcours <em>singulier</em></h2></div>
 {rows([
   ("La danse", "Danseuse classique diplômée du Royal Ballet d'Anvers : la rigueur, la scène, le sens du détail."),
   ("Le terrain", "Hôtesse puis cheffe hôtesse : Grand Prix de France de F1, Dior, FDJ, Pasino d'Aix, Grand Théâtre de Provence."),
   ("Le droit", "Master en droit des affaires, puis trois ans à former des juristes aux marchés publics."),
   ("MH Event", "Fin 2023, une agence « 360° » qui réunit organisation, accueil et communication."),
   ("Aujourd'hui", "Partenaire de l'Office de Tourisme de Nîmes, intervenante à l'École Tunon, cofondatrice du cercle H9RITAGE."),
 ])}
</div></section>
<section class="sec bg-cypres on-dark"><div class="wrap">
 <figure class="quote fade"><div class="rule" aria-hidden="true"><i></i></div><blockquote>« Une organisation rigoureuse, un personnel impliqué et une communication efficace : c'est de ce constat qu'est né MH Event. »</blockquote><figcaption class="who">Mathilde Heyral, présidente</figcaption></figure>
</div></section>
<section class="sec"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Trois pôles</p><h2 class="t-h2 fade">Un seul <em>interlocuteur</em></h2></div>
 {rows([
   ("Organisation", "Séminaires, salons, conférences, soirées, inaugurations, afterworks, mariages."),
   ("Service · les Angelines", "Hôtes et hôtesses, animateurs, mixologues, barmans, serveurs, artistes."),
   ("Communication événementielle", "Visuels selon votre charte, stratégie digitale et print, déploiement."),
 ])}
</div></section>
{cta_band("Un projet ? Mathilde vous répond personnellement.", "devis/")}
<section class="sec flush"><div class="strip">{"".join(ph(n, a, "", "(min-width:760px) 28vw, 70vw") for n, a in [
  ("mathilde-mathilde-heyral-mh-event", "Mathilde Heyral lors d'un événement"),
  ("mathilde-conference-table-ronde-evenementiel-marseille", "Mathilde Heyral lors d'une table ronde à Marseille"),
  ("mathilde-img-9084", "Mathilde Heyral en marinière"),
  ("mathilde-mathilde-heyral-ceo", "Mathilde Heyral en réunion"),
  ("mathilde-img-9750", "Mathilde Heyral et son équipe"),
  ("mathilde-portrait-mathilde-heyral-seo-mh-event", "Portrait de Mathilde Heyral"),
])}</div></section>
{cta(devis="devis/")}'''
    page("agence/", "L'agence MH Event et Mathilde Heyral, sa fondatrice",
         "Mathilde Heyral, fondatrice de MH Event : danse classique, terrain, droit des affaires. Une agence événementielle à taille humaine, installée à Nîmes.",
         body, crumbs=[("agence/", "L'agence")], tone="light",
         jsonld=[{"@context": "https://schema.org", "@type": "AboutPage", "url": DOMAIN + "agence/", "about": {"@id": DOMAIN + "#agence"},
                  "mainEntity": {"@type": "Person", "name": "Mathilde Heyral", "jobTitle": "Fondatrice et présidente", "worksFor": {"@id": DOMAIN + "#agence"}}}])

# ================================================================ RÉALISATIONS
def realisations():
    cats = [("all", "Tous"), ("entreprises", "Entreprises"), ("hotels", "Hôtels"), ("particuliers", "Particuliers")]
    times = [("passes", "Passés"), ("avenir", "À venir")]
    fbtn = "".join(f'<button type="button" data-g="cat" data-v="{v}" aria-pressed="{"true" if v=="all" else "false"}">{l}</button>' for v, l in cats)
    fbtn += '<span class="sep" aria-hidden="true"></span>' + '<button type="button" data-g="time" data-v="all" aria-pressed="true" hidden>Tous</button>'
    fbtn += "".join(f'<button type="button" data-g="time" data-v="{v}" aria-pressed="false">{l}</button>' for v, l in times)
    body = f'''<section class="sec" style="padding-top:clamp(190px,20vw,250px)"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(48px,6vw,88px)"><p class="label">Réalisations</p><h1 class="t-xl">Nos <em>événements</em></h1><div class="rule" aria-hidden="true"><i></i></div>
  <p class="lead">Inaugurations, soirées en hôtel, conférences, mariages : des marques, des lieux, des invités.</p></div>
 <div class="filters" role="group" aria-label="Filtrer les événements">{fbtn}</div>
 <p class="sr" id="vign-live" aria-live="polite"></p>
 <div class="vign">{"".join(vignette(e) for e in EVENTS)}</div>
 <p class="vign-empty" hidden>Aucun événement pour ce filtre.</p>
</div></section>
{cta_band("Le prochain événement, c'est le vôtre.", "devis/")}
<section class="sec bg-pierre"><div class="wrap">
 <figure class="quote fade"><div class="rule" aria-hidden="true"><i></i></div><blockquote>« Nous avons eu le plaisir de collaborer à plusieurs reprises avec MH Event et chaque expérience a été tout simplement exceptionnelle. »</blockquote>
 <figcaption class="who">Lucie Lauzel · avis Google · 5,0 sur 35 avis</figcaption></figure>
</div></section>'''
    page("realisations/", "Réalisations événementielles en Provence | MH Event",
         "Inaugurations, soirées en hôtel, séminaires, conférences et mariages organisés par MH Event pour Golden Tulip, ENTENT, Pasino, GEPA et d'autres.",
         body, crumbs=[("realisations/", "Réalisations")], tab="realisations", light=True,
         jsonld=[{"@context": "https://schema.org", "@type": "CollectionPage", "url": DOMAIN + "realisations/", "name": "Réalisations MH Event",
                  "hasPart": [{"@type": "WebPage", "url": DOMAIN + e["file"], "name": e["t"]} for e in EVENTS]}])

def build_all():
    home(); entreprises(); services_entreprises(); team_building(); hotesses()
    hotels(); services_hotels(); particuliers(); services_particuliers()
    agence(); realisations()
