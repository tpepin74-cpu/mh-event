# -*- coding: utf-8 -*-
import re
from build import *

ARTICLES = [
 dict(f="blog-soirees-dynamisation-hotel.html", old="journal-soirees-dynamisation-hotel.html", cat="Hôtels",
      t="Comment un hôtel peut remplir son bar <em>en hiver</em>", plain="Comment un hôtel peut remplir son bar en hiver",
      lead="Soirées de dynamisation : la méthode MH Event, du Golden Tulip Marseille Euromed aux soirées « Golden + concept ».",
      img="hotel-soiree-live-painting-hotel-odalys-euromed-marseille", alt="Soirée live painting à l'hôtel Odalys Euromed"),
 dict(f="blog-team-building-nimes.html", old="journal-team-building-nimes.html", cat="Team building",
      t="Team building à Nîmes, au cœur <em>du patrimoine</em>", plain="Team building à Nîmes : trois expériences au cœur du patrimoine",
      lead="Circuit des poètes, route des Crocodiles, Marche des senteurs : des activités conçues avec l'Office de Tourisme de Nîmes.",
      img="tb-team-building-crocodiles-nimes-mh-event", alt="Sur la route des Crocodiles à Nîmes"),
 dict(f="blog-seminaire-pont-du-gard.html", old="journal-seminaire-pont-du-gard.html", cat="Séminaires",
      t="Organiser un séminaire au <em>Pont du Gard</em>", plain="Organiser un séminaire au Pont du Gard",
      lead="Un site antique, une marche sensorielle exclusive et la Camargue à proximité.",
      img="seminaire-mh-event-organisation-seminaire-montpellier", alt="Séminaire sous chapiteau dans la garrigue"),
]
LINKMAP = {"team-building.html": "entreprises-team-building.html", "hotesses-angelines.html": "entreprises-hotes-hotesses.html",
           "mariages-evenements-prives.html": "particuliers-mariages.html", "journal.html": "blog.html",
           "hotels.html#catalogue": "hotels.html#soirees", "journal-soirees-dynamisation-hotel.html": "blog-soirees-dynamisation-hotel.html",
           "journal-team-building-nimes.html": "blog-team-building-nimes.html", "journal-seminaire-pont-du-gard.html": "blog-seminaire-pont-du-gard.html"}

def fixlinks(s):
    for a, b in LINKMAP.items():
        s = s.replace(f'href="{a}', f'href="{b}')
    return s

def post_card(a):
    return (f'<a class="post fade" href="{a["f"]}">{ph(a["img"], a["alt"], "", "(min-width:860px) 30vw, 100vw")}'
            f'<span class="label">{a["cat"]}</span><h3 class="t-h3">{a["plain"]}</h3></a>')

def blog():
    body = f'''<section class="sec" style="padding-top:clamp(170px,20vw,240px)"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(56px,7vw,110px)"><p class="label">Blog</p><h1 class="t-xl">Les <em>coulisses</em></h1><div class="rule" aria-hidden="true"><i></i></div>
 <p class="lead">Conseils, méthodes et histoires du terrain, par Mathilde Heyral.</p></div>
 <div class="posts">{"".join(post_card(a) for a in ARTICLES)}</div>
</div></section>
{cta()}'''
    page("blog.html", "Blog · MH Event", "Conseils, méthodes et coulisses de l'événementiel par Mathilde Heyral : hôtels, team building, séminaires.", body, light=True)
    for a in ARTICLES:
        prose = open("_build/articles/" + a["old"], encoding="utf-8").read()
        prose = fixlinks(prose)
        prose = prose.replace('class="t-lead"', 'class="lead"').replace('class="t-quote"', "")
        others = [x for x in ARTICLES if x is not a]
        body = hero_photo(a["img"], a["alt"], a["cat"], a["t"], crumbs=[("blog.html", "Blog")]) .replace(
            '<a class="hero-down"', '<p class="post-meta" style="position:absolute;left:0;right:0;bottom:calc(var(--tab) + 104px)"><span>Par Mathilde Heyral</span><span>·</span><span>Novembre 2026</span></p><a class="hero-down"') + f'''
<section class="sec" id="suite"><article class="wrap prose">{prose}</article></section>
<section class="sec bg-pierre"><div class="wrap"><div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label">À lire aussi</p><h2 class="t-h2">Sur le <em>blog</em></h2></div>
 <div class="posts" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">{"".join(post_card(x) for x in others)}</div></div></section>
{cta()}'''
        page(a["f"], a["plain"] + " · Blog MH Event", a["lead"], body, cur="blog.html")

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
    page("contact.html", "Contact · MH Event", "Contactez MH Event : 06 14 46 61 83, contact@mh-event.fr, 7 rue Tédenat à Nîmes. Réponse sous 24 à 48 h.", body, light=True)

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
    page("devis.html", "Demander un devis · MH Event", "Demande de devis gratuite pour votre séminaire, soirée, team building, hôtesses ou mariage. Réponse sous 24 à 48 h.", body, light=True)

def faqpage():
    qs = [("Dans quelles villes MH Event intervient-elle ?", "Partout en France et à l'international. Basés en Provence et dans le Gard, nous travaillons surtout à Aix-en-Provence, Marseille, Nîmes, Saint-Tropez, Montpellier, Avignon et Arles."),
          ("Comment se déroule une première prise de contact ?", "Après votre demande de devis, vous êtes rappelé sous 24 à 48 h pour un premier échange, puis un rendez-vous sur place ou en visio."),
          ("Quel délai prévoir pour organiser un événement ?", "Idéalement trois à six mois pour un événement d'entreprise ou un mariage. Pour les fêtes de fin d'année, décembre se réserve en septembre."),
          ("Proposez-vous des forfaits ou des prestations à la carte ?", "Les deux : des formules clés en main ou des prestations à la carte. Chaque devis est personnalisé."),
          ("Combien coûte un team building ?", "Nos team buildings démarrent à 28 € HT par personne."),
          ("Quel est le tarif d'une hôtesse d'accueil ?", "27 € HT de l'heure, déplacement en sus."),
          ("Combien coûte l'organisation d'un mariage ?", "L'organisation complète démarre à 3 500 €. La coordination du jour J est sur devis."),
          ("Comment garantissez-vous la qualité des prestataires ?", "Nous travaillons avec un réseau de prestataires de confiance, sélectionnés et régulièrement évalués.")]
    body = f'''<section class="sec" style="padding-top:clamp(170px,20vw,240px)"><div class="wrap two">
 <div class="stack"><p class="label">Questions fréquentes</p><h1 class="t-xl">Avant de <em>commencer</em></h1><div class="rule" aria-hidden="true"><i></i></div><p class="lead">Une autre question&nbsp;? Le concierge du site répond tout de suite, et Mathilde sous 24 à 48 h.</p></div>
 {faq(qs)}
</div></section>{cta()}'''
    page("faq.html", "Questions fréquentes · MH Event", "Délais, tarifs, zones d'intervention : les réponses aux questions fréquentes sur MH Event.", body, light=True)

def mentions():
    prose = open("_build/mentions-prose.html", encoding="utf-8").read()
    prose = re.sub(r"<h1[^>]*>.*?</h1>", "", prose, flags=re.S)
    prose = fixlinks(prose).replace('class="t-lead"', 'class="lead"')
    body = f'''<section class="sec" style="padding-top:clamp(170px,20vw,240px)"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(48px,6vw,80px)"><p class="label">Informations</p><h1 class="t-xl">Mentions <em>légales</em></h1><div class="rule" aria-hidden="true"><i></i></div></div>
 <div class="prose">{prose}</div></div></section>'''
    page("mentions-legales.html", "Mentions légales & confidentialité · MH Event", "Mentions légales et politique de confidentialité du site MH Event.", body, light=True)

def notfound():
    body = f'''<section class="nf"><div class="stack center"><p class="label">Page introuvable</p><h1 class="t-xl">Cette page <em>s'est éclipsée</em></h1><div class="rule" aria-hidden="true"><i></i></div>
 <div class="actions"><a class="btn" href="index.html">Retour à l'accueil</a><a class="link" href="realisations.html">Les réalisations</a></div></div></section>'''
    page("404.html", "Page introuvable · MH Event", "Cette page n'existe pas ou plus.", body, light=True)

REDIRECTS = {"team-building.html": "entreprises-team-building.html", "hotesses-angelines.html": "entreprises-hotes-hotesses.html",
             "mariages-evenements-prives.html": "particuliers-mariages.html", "journal.html": "blog.html",
             "journal-soirees-dynamisation-hotel.html": "blog-soirees-dynamisation-hotel.html",
             "journal-team-building-nimes.html": "blog-team-building-nimes.html", "journal-seminaire-pont-du-gard.html": "blog-seminaire-pont-du-gard.html"}
def redirects():
    for a, b in REDIRECTS.items():
        open(a, "w", encoding="utf-8").write(f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><title>MH Event</title>'
            f'<meta http-equiv="refresh" content="0; url={b}"><link rel="canonical" href="{b}"></head><body style="background:#F6F1E8"><a href="{b}">Continuer</a></body></html>\n')
