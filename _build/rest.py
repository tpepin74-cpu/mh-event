# -*- coding: utf-8 -*-
import re
from build import *

ARTICLES = [
 dict(f="blog/soirees-dynamisation-hotel/", old="journal-soirees-dynamisation-hotel.html", cat="Hôtels",
      t="Comment un hôtel peut remplir son bar <em>en hiver</em>", plain="Comment un hôtel peut remplir son bar en hiver",
      lead="Soirées de dynamisation : la méthode MH Event, du Golden Tulip Marseille Euromed aux soirées « Golden + concept ».",
      crumb="Remplir son bar en hiver", cta=("Programmer les soirées de votre hôtel ?", "hotels/animation-dynamisation/", "Voir l'offre hôtels"),
      img="hotel-soiree-live-painting-hotel-odalys-euromed-marseille", alt="Soirée live painting à l'hôtel Odalys Euromed"),
 dict(f="blog/team-building-nimes/", old="journal-team-building-nimes.html", cat="Team building",
      t="Team building à Nîmes, au cœur <em>du patrimoine</em>", plain="Team building à Nîmes, au cœur du patrimoine",
      lead="Circuit des poètes, route des Crocodiles, Marche des senteurs : des activités conçues avec l'Office de Tourisme de Nîmes.",
      crumb="Team building à Nîmes", cta=("Un team building à Nîmes pour votre équipe ?", "entreprises/team-building/nimes/", "Voir les parcours"),
      img="tb-team-building-crocodiles-nimes-mh-event", alt="Sur la route des Crocodiles à Nîmes"),
 dict(f="blog/seminaire-pont-du-gard/", old="journal-seminaire-pont-du-gard.html", cat="Séminaires",
      t="Organiser un séminaire au <em>Pont du Gard</em>", plain="Organiser un séminaire au Pont du Gard",
      lead="Un site antique, une marche sensorielle exclusive et la Camargue à proximité.",
      crumb="Séminaire au Pont du Gard", cta=("Un séminaire au Pont du Gard ?", "entreprises/seminaire/", "Organiser mon séminaire"),
      img="seminaire-mh-event-organisation-seminaire-montpellier", alt="Séminaire sous chapiteau dans la garrigue"),
]
LINKMAP = {"hotels.html#catalogue": "hotels/soirees-seminaires/", "hotels.html#soirees": "hotels/soirees-seminaires/",
           "entreprises-team-building.html#catalogue": "entreprises/team-building/"}

def fixlinks(s):
    for a, b in LINKMAP.items():
        s = s.replace(f'href="{a}"', f'href="{b}"')
    return s

def post_card(a):
    return (f'<a class="post fade" href="{a["f"]}">{ph(a["img"], a["alt"], "", "(min-width:860px) 30vw, 100vw")}'
            f'<span class="label">{a["cat"]}</span><h3 class="t-h3">{a["plain"]}</h3></a>')

def blog():
    body = f'''<section class="sec" style="padding-top:clamp(170px,20vw,240px)"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(56px,7vw,110px)"><p class="label">Blog</p><h1 class="t-xl">Conseils <em>&amp; coulisses</em></h1><div class="rule" aria-hidden="true"><i></i></div>
 <p class="lead">Conseils, méthodes et histoires du terrain, par Mathilde Heyral.</p></div>
 <div class="posts">{"".join(post_card(a) for a in ARTICLES)}</div>
</div></section>
{cta(devis="devis/")}'''
    page("blog/", "Blog événementiel : conseils et coulisses | MH Event", "Conseils et retours d'expérience de Mathilde Heyral : animer un hôtel, team building à Nîmes, séminaire au Pont du Gard.", body,
         crumbs=[("blog/", "Blog")], light=True,
         jsonld=[{"@context": "https://schema.org", "@type": "Blog", "name": "Blog MH Event", "url": DOMAIN + "blog/",
                  "blogPost": [{"@type": "BlogPosting", "headline": a["plain"], "url": DOMAIN + a["f"]} for a in ARTICLES]}])
    for a in ARTICLES:
        prose = open("_build/articles/" + a["old"], encoding="utf-8").read()
        prose = fixlinks(prose)
        prose = prose.replace('class="t-lead"', 'class="lead"').replace('class="t-quote"', "")
        others = [x for x in ARTICLES if x is not a]
        body = hero_photo(a["img"], a["alt"], a["cat"], a["t"]) .replace(
            '<a class="hero-down"', '<p class="post-meta" style="position:absolute;left:0;right:0;bottom:calc(var(--tab) + 104px)"><span>Par Mathilde Heyral</span><span>·</span><span>Novembre 2026</span></p><a class="hero-down"') + f'''
<section class="sec" id="suite"><article class="wrap prose">{prose}</article></section>
<section class="sec bg-pierre"><div class="wrap"><div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label">À lire aussi</p><h2 class="t-h2">Sur le <em>blog</em></h2></div>
 <div class="posts" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">{"".join(post_card(x) for x in others)}</div></div></section>
{cta_band(a["cta"][0], a["cta"][1], a["cta"][2])}
{cta(devis="devis/")}'''
        page(a["f"], a["plain"] + " | MH Event", a["lead"], body, crumbs=[("blog/", "Blog"), (a["f"], a["crumb"])], tone="light",
             jsonld=[{"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["plain"], "description": a["lead"], "url": DOMAIN + a["f"],
                      "datePublished": "2026-11-01", "inLanguage": "fr-FR", "author": {"@type": "Person", "name": "Mathilde Heyral"}, "publisher": {"@id": DOMAIN + "#agence"}}])

def contact():
    body = f'''<section class="sec" style="padding-top:clamp(170px,20vw,240px)"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(56px,7vw,100px)"><p class="label">Contact</p><h1 class="t-xl">Parlons de votre <em>projet</em></h1><div class="rule" aria-hidden="true"><i></i></div>
 <p class="lead">Mathilde vous répond sous 24 à 48 h ouvrées. Pour une urgence, appelez directement.</p></div>
 <div class="two">
  <dl class="contact-list">
   <div><dt>Téléphone</dt><dd><a href="{TEL}">{PHONE}</a></dd></div>
   <div><dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
   <div><dt>Adresse</dt><dd>7 rue Tédenat, 30900 Nîmes</dd></div>
   <div><dt>Horaires</dt><dd>Du lundi au vendredi, 9 h – 18 h</dd></div>
   <div><dt>Zone</dt><dd>Provence, Gard, Côte d'Azur, France et international</dd></div>
  </dl>
  <div>
   <form class="form" id="contact-form" novalidate>
    <div class="grid2"><div class="field"><label for="c-nom">Nom et prénom *</label><input class="input" id="c-nom" name="nom" autocomplete="name" required></div>
    <div class="field"><label for="c-mail">E-mail *</label><input class="input" id="c-mail" name="email" type="email" autocomplete="email" required></div></div>
    <div class="grid2"><div class="field"><label for="c-tel">Téléphone</label><input class="input" id="c-tel" name="tel" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="c-suj">Sujet *</label><input class="input" id="c-suj" name="sujet" required></div></div>
    <div class="field"><label for="c-msg">Message *</label><textarea class="input" id="c-msg" name="message" required></textarea></div>
    <label class="check"><input type="checkbox" name="consent" required> <span>J'accepte que mes données soient utilisées pour me recontacter. <a href="mentions-legales.html#donnees" style="border-bottom:1px solid">Confidentialité</a>.</span></label>
    <div><button class="btn" type="submit">Préparer le message</button></div>
   </form>
   <div class="done" hidden><p class="label">Message prêt</p><h2 class="t-h3">Il ne reste qu'à <em>l'envoyer</em></h2><p>Ouvrez-le dans votre messagerie pour l'envoyer à Mathilde.</p><div class="actions"><a class="btn" data-mailto href="mailto:{MAIL}">Envoyer par e-mail</a></div></div>
  </div>
 </div>
</div></section>'''
    page("contact/", "Contact : agence événementielle à Nîmes | MH Event", "Contactez Mathilde Heyral : 06 14 46 61 83, contact@mh-event.fr, 7 rue Tédenat à Nîmes. Réponse sous 24 à 48 h ouvrées.", body,
         crumbs=[("contact/", "Contact")], light=True,
         jsonld=[{"@context": "https://schema.org", "@type": "ContactPage", "url": DOMAIN + "contact/", "about": {"@id": DOMAIN + "#agence"}}])

def devis():
    def opts(name, vals, kind="radio", req=True):
        r = " required" if req else ""
        return '<div class="opts">' + "".join(f'<label class="opt"><input type="{kind}" name="{name}" value="{esc(v)}"{r if (kind=="radio" and i==0) else ""}><span>{v}</span></label>' for i, v in enumerate(vals)) + "</div>"
    body = f'''<section class="sec" style="padding-top:clamp(170px,20vw,240px)"><div class="wrap" style="max-width:calc(900px + 2*var(--gut))">
 <div class="stack center" style="margin-bottom:clamp(56px,7vw,100px)"><p class="label">Devis gratuit · réponse sous 48 h</p><h1 class="t-xl">Votre <em>événement</em></h1><div class="rule" aria-hidden="true"><i></i></div>
 <p class="lead">Deux minutes suffisent. Vous préférez parler&nbsp;? <a href="{TEL}" style="color:var(--bordeaux)">{PHONE}</a></p></div>
 <form class="form" id="devis-form" novalidate style="gap:48px">
  <fieldset class="fs"><legend>Type d'événement *</legend>{opts("type", ["Séminaire", "Journée bien-être", "Soirée d'entreprise", "Soirée en hôtel", "Inauguration", "Team building", "Hôtesses", "Mariage", "Anniversaire / privé", "Autre"])}</fieldset>
  <div class="grid2"><div class="field"><label for="d-date">Date souhaitée *</label><input class="input" id="d-date" name="date" required placeholder="ex. juin 2027"></div>
  <div class="field"><label for="d-lieu">Lieu ou ville *</label><input class="input" id="d-lieu" name="lieu" required></div></div>
  <fieldset class="fs"><legend>Nombre d'invités</legend>{opts("invites", ["Moins de 50", "50 – 100", "100 – 200", "200 – 500", "Plus de 500"], req=False)}</fieldset>
  <fieldset class="fs"><legend>Budget estimatif</legend>{opts("budget", ["Moins de 5 000 €", "5 – 10 k€", "10 – 25 k€", "25 – 50 k€", "Plus de 50 k€", "À définir ensemble"], req=False)}</fieldset>
  <fieldset class="fs"><legend>Prestations souhaitées</legend>{opts("prestations", ["Organisation complète", "Coordination jour J", "Hôtes & hôtesses", "Animations", "Team building", "Communication", "Recherche de lieu", "Traiteur"], kind="checkbox", req=False)}</fieldset>
  <div class="field"><label for="d-det">Votre projet</label><textarea class="input" id="d-det" name="details" placeholder="Quelques mots sur vos envies"></textarea></div>
  <div class="grid2"><div class="field"><label for="d-pre">Prénom *</label><input class="input" id="d-pre" name="prenom" autocomplete="given-name" required></div>
  <div class="field"><label for="d-nom">Nom *</label><input class="input" id="d-nom" name="nom" autocomplete="family-name" required></div></div>
  <div class="grid2"><div class="field"><label for="d-soc">Société</label><input class="input" id="d-soc" name="societe" autocomplete="organization"></div>
  <div class="field"><label for="d-tel">Téléphone *</label><input class="input" id="d-tel" name="tel" type="tel" autocomplete="tel" required></div></div>
  <div class="field"><label for="d-mail">E-mail *</label><input class="input" id="d-mail" name="email" type="email" autocomplete="email" required></div>
  <label class="check"><input type="checkbox" name="consent" required> <span>J'accepte que mes données soient utilisées pour traiter ma demande et me recontacter. <a href="mentions-legales.html#donnees" style="border-bottom:1px solid">Confidentialité</a>.</span></label>
  <div><button class="btn" type="submit">Préparer ma demande</button></div>
 </form>
 <div class="done" hidden><p class="label">Demande prête</p><h2 class="t-h2">Dernière <em>étape</em></h2><p>Envoyez-la à Mathilde : elle vous répond sous 24 à 48 h.</p><pre class="recap"></pre>
  <div class="actions"><a class="btn" data-mailto href="mailto:{MAIL}">Envoyer par e-mail</a><button class="btn line" type="button" data-copy>Copier le texte</button></div></div>
</div></section>'''
    page("devis/", "Demande de devis événementiel gratuit | MH Event", "Devis gratuit pour un séminaire, une soirée, un team building, des hôtesses ou un mariage : deux minutes pour décrire votre projet, réponse sous 48 h.", body,
         crumbs=[("devis/", "Devis")], light=True)

def faqpage():
    qs = [("Dans quelles villes MH Event intervient-elle ?", "Basée à Nîmes, l'agence travaille surtout à Aix-en-Provence, Marseille, Nîmes, Saint-Tropez, Montpellier, Avignon et Arles, et se déplace partout en France et à l'international."),
          ("Comment se déroule une première prise de contact ?", "Après votre demande, Mathilde vous rappelle sous 24 à 48 h ouvrées, puis vous rencontre sur place ou en visio pour détailler le projet."),
          ("Le devis est-il payant ?", "Non. Le devis est gratuit, détaillé poste par poste, et sans engagement."),
          ("Proposez-vous des forfaits ou des prestations à la carte ?", "Les deux : une organisation complète clé en main, ou seulement les prestations dont vous avez besoin (hôtesses, animation, coordination)."),
          ("Où trouver vos tarifs ?", 'Chaque page de service indique ses prix : <a href="entreprises/team-building/">team building</a>, <a href="entreprises/hotes-hotesses/">hôtes et hôtesses</a>, <a href="hotels/soirees-seminaires/">soirées séminaires</a>, <a href="hotels/dejeuner-corpo/">Déjeuner Corpo</a>, <a href="particuliers/mariage/">mariage</a>.'),
          ("Comment choisissez-vous vos prestataires ?", "Mathilde travaille avec un réseau de prestataires locaux qu'elle a vus à l'œuvre : traiteurs, artistes, lieux, techniciens. Chacun est réévalué après chaque événement."),
          ("Travaillez-vous avec les agences et les collectivités ?", "Oui : MH Event intervient aussi en sous-traitance pour des agences, et pour des chambres de commerce, offices de tourisme et collectivités."),
          ("Peut-on vous confier un événement en anglais ?", "Oui. Devis, plannings et échanges peuvent se faire en anglais, notamment pour les mariages de couples étrangers.")]
    body = f'''<section class="sec" style="padding-top:clamp(170px,20vw,240px)"><div class="wrap two">
 <div class="stack"><p class="label">Questions fréquentes</p><h1 class="t-xl">Avant de <em>commencer</em></h1><div class="rule" aria-hidden="true"><i></i></div><p class="lead">Une autre question&nbsp;? Le concierge du site répond tout de suite, et Mathilde sous 24 à 48 h.</p></div>
 {faq(qs)}
</div></section>{cta(devis="devis/")}'''
    page("faq/", "Questions fréquentes sur l'agence | MH Event", "Zones d'intervention, premier contact, devis, prestataires, langues : comment travaille l'agence MH Event.", body,
         crumbs=[("faq/", "Questions fréquentes")], light=True, jsonld=[faq_ld(qs)])

def mentions():
    prose = open("_build/mentions-prose.html", encoding="utf-8").read()
    prose = re.sub(r"<h1[^>]*>.*?</h1>", "", prose, flags=re.S)
    prose = fixlinks(prose).replace('class="t-lead"', 'class="lead"')
    body = f'''<section class="sec" style="padding-top:clamp(170px,20vw,240px)"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(48px,6vw,80px)"><p class="label">Informations</p><h1 class="t-xl">Mentions <em>légales</em></h1><div class="rule" aria-hidden="true"><i></i></div></div>
 <div class="prose">{prose}</div></div></section>'''
    page("mentions-legales/", "Mentions légales et confidentialité | MH Event", "Éditeur, hébergement, données personnelles et cookies du site mh-event.fr.", body,
         crumbs=[("mentions-legales/", "Mentions légales")], light=True)

def notfound():
    body = f'''<section class="nf"><div class="stack center"><p class="label">Page introuvable</p><h1 class="t-xl">Cette page <em>s'est éclipsée</em></h1><div class="rule" aria-hidden="true"><i></i></div>
 <div class="actions"><a class="btn" href="index.html">Retour à l'accueil</a><a class="link" href="realisations/">Les réalisations</a></div></div></section>'''
    page("404.html", "Page introuvable · MH Event", "Cette page n'existe pas ou plus.", body, light=True)

def redirects():
    """Toutes les anciennes adresses .html renvoient vers la nouvelle page : aucun contenu dupliqué."""
    for old, new in ROUTES.items():
        if old == "index.html":
            continue
        tgt = new or "./"
        open(old, "w", encoding="utf-8").write(
            f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex, follow"><title>MH Event</title>'
            f'<link rel="canonical" href="{DOMAIN}{new}"><meta http-equiv="refresh" content="0; url={tgt}"><script>location.replace("{tgt}"+location.hash)</script></head>'
            f'<body style="background:#EDE6DA"><a href="{tgt}">Continuer</a></body></html>\n')

def sitemap(pages):
    urls = "".join(f"<url><loc>{DOMAIN}{p}</loc></url>" for p in pages if not p.endswith(".html"))
    open("sitemap.xml", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n")
