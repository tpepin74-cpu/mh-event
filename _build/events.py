# -*- coding: utf-8 -*-
"""Réalisations : une vignette par événement, une page par événement avec son propre style."""
from build import *

# Palettes issues de la charte (fond, titres, accent, texte)
TH = {
 "ivoire":   ("#F6F1E8", "#2A1A20", "#5A1626", "#5E5054"),
 "pierre":   ("#EDE6DA", "#2A1A20", "#3B4A32", "#5E5054"),
 "figue":    ("#2A1A20", "#EDE6DA", "#C9A45C", "rgba(237,230,218,.78)"),
 "bordeaux": ("#5A1626", "#EDE6DA", "#C9A45C", "rgba(237,230,218,.8)"),
 "cypres":   ("#3B4A32", "#F6F1E8", "#C9A45C", "rgba(246,241,232,.8)"),
 "or":       ("#F6F1E8", "#2A1A20", "#9C7A36", "#5E5054"),
}

# slug, titre, ligne, catégorie, temps, date, lieu, logo, marque (texte), photos [(nom, alt)], contexte, dispositif, chiffres, citation, thème, variante
EVENTS = [
 dict(slug="golden-night-golden-tulip-marseille", t="Golden Night", wm=None, logo="golden-tulip", cat="hotels", time="passes", date="Depuis le 4 juin 2026", lieu="Golden Tulip Marseille Euromed",
      ph=[("hotel-comedy-show-marseille-juin-2026", "Comedy Club de la première Golden Night"), ("hotel-comedy-club-malik-fares", "Humoriste sur scène lors d'une Golden Night"),
          ("hotel-applaudissement-rires-groupe-soiree-evenement", "Public qui rit et applaudit"), ("hotel-groupement-personnes-soiree-evenement-hotel-marseille", "Public réuni dans les salons de l'hôtel")],
      ctx="Redynamiser l'hôtel, créer du passage, faire revenir une clientèle locale. La réponse&nbsp;: une soirée gratuite, ouverte au public, chaque mois sur un thème différent.",
      dis=["Programmation mensuelle", "Comedy Club, murder party, soirée jazz, blind test", "Dîner bien-être « Green &amp; Care »", "Artistes, régie et accueil"],
      facts=[("4 juin 2026", "Première soirée"), ("1 / mois", "Ouverte au public"), ("4", "Humoristes sur scène")],
      quote=("Hier c'était top.", "La cliente, le lendemain de la première"), th="figue", v="a"),
 dict(slug="golden-plus-concept", t="Golden + concept", wm=None, logo="golden-tulip", cat="hotels", time="avenir", date="Décembre 2026 – juin 2027", lieu="Golden Tulip Marseille Euromed",
      ph=[("hotel-soiree-guinguette-terrasse-hotel-marseille-dynamisation", "Guinguette en terrasse d'hôtel à Marseille"), ("hotel-soiree-saxophone-lounge-hotel-marseille-dynamisation-1", "Soirée saxophone Lounge")],
      ctx="Après les Golden Night, la programmation de l'hiver passe sous une marque propre à l'hôtel.",
      dis=["Golden Ski", "Golden Casino", "Golden Gatsby", "Golden Piano-bar", "Golden Guinguette"], facts=[], quote=None, th="or", v="c"),
 dict(slug="escale-mediterraneenne-golden-tulip", t="Escale Méditerranéenne", wm=None, logo="golden-tulip", cat="hotels", time="passes", date="Déjeuner Corpo", lieu="Golden Tulip Marseille Euromed",
      ph=[("dejeuner-img-9036", "Invités réunis lors de l'Escale Méditerranéenne"), ("dejeuner-img-9064", "Invitées souriantes en marinière"), ("dejeuner-img-9052", "Buffet en terrasse"),
          ("dejeuner-img-9067", "Accueil des invités avec un sac cadeau"), ("dejeuner-img-9076", "Salle de séminaire de l'hôtel"), ("dejeuner-img-9081", "Échanges en terrasse")],
      ctx="Un déjeuner-parcours pour faire découvrir l'hôtel à des professionnels locaux&nbsp;: un passeport, quatre escales et un jeu concours.",
      dis=["Passeport et quatre escales", "Jeu concours", "Tout le staff en marinière", "Collecte des contacts, avec accord RGPD"],
      facts=[("4", "Escales"), ("2 h", "De parcours")], quote=None, th="pierre", v="b"),
 dict(slug="odalys-euromed-marseille", t="Odalys Euromed", wm=None, logo="odalys-euromed", cat="hotels", time="passes", date="Depuis janvier 2025", lieu="Marseille",
      ph=[("hotel-soiree-inauguration-hotel-odalys-euromed-janvier-2025", "Inauguration de l'hôtel Odalys Euromed"), ("hotel-soiree-live-painting-hotel-odalys-euromed-marseille", "Soirée live painting"),
          ("hotel-discussion-invites-evenements-hotel-odalys-euromed", "Invités en conversation"), ("dejeuner-dejeuner-corporate-kermesse-odalys-avril-2025", "Kermesse avec CDS Groupe"),
          ("hotel-live-painting-raphael-federici-saxophoniste", "Live painting et saxophoniste")],
      ctx="De l'inauguration de l'hôtel en janvier 2025 aux soirées qui le font vivre&nbsp;: live painting, lobby transformé en station de ski, Kermesse avec CDS Groupe.",
      dis=["Soirée d'inauguration", "Live painting et saxophone", "Lobby en station de ski, soirée raclette", "Kermesse avec CDS Groupe"],
      facts=[], quote=None, th="bordeaux", v="b"),
 dict(slug="soiree-feria-sowell-nimes", t="Soirée Feria au SoWell", wm=None, logo="sowell", cat="hotels", time="passes", date="Soirée en hôtel", lieu="Hôtel SoWell · Nîmes",
      ph=[("hotel-soiree-feria-groupe-live-hotel-sowell-nimes", "Groupe live devant l'hôtel SoWell à Nîmes")],
      ctx="Une soirée aux couleurs de la feria, avec un groupe live, pour ouvrir l'hôtel aux Nîmois.",
      dis=["Groupe live", "Ambiance feria", "Soirée ouverte au public"], facts=[], quote=None, th="bordeaux", v="a"),
 dict(slug="dejeuner-corporate-odalys-aix", t="Déjeuner corporate Odalys", wm=None, logo="odalys-city", cat="hotels", time="passes", date="Juin 2026", lieu="Odalys · Aix-en-Provence",
      ph=[("dejeuner-dejeuner-corporate-hotel-odalys-aix-juin-2026", "Patio dressé pour le déjeuner corporate"), ("dejeuner-dejeuner-affaire-discussions-hotel-juin-2026", "Invités en discussion"),
          ("dejeuner-animation-molkky-exterieur-hotesse-evenement", "Mölkky dans la cour de l'hôtel")],
      ctx="Un déjeuner pour faire découvrir l'hôtel à des professionnels d'Aix-en-Provence, entre patio, salles et jeux en extérieur.",
      dis=["Déjeuner dans le patio", "Animation Mölkky", "Accueil et hôtesses"], facts=[], quote=None, th="ivoire", v="c"),
 dict(slug="golden-tulip-festival", t="Golden Tulip Festival", wm=None, logo="golden-tulip", cat="hotels", time="avenir", date="Avril 2027", lieu="Golden Tulip Marseille Euromed",
      ph=[("dejeuner-img-9081", "Terrasse du Golden Tulip Marseille Euromed")],
      ctx="Un Déjeuner Corpo printanier&nbsp;: une cueillette de tulipes au cœur de l'hôtel.",
      dis=["Cueillette de tulipes dans l'hôtel", "Format Déjeuner Corpo"], facts=[], quote=None, th="pierre", v="c"),
 dict(slug="soiree-o-delice-ligue-football", t="Soirée Ô Délice", wm="Ligue de la Méditerranée|de Football", logo=None, cat="entreprises", time="passes", date="Septembre 2026", lieu="Odalys City Centre Euromed · Marseille",
      ph=[("hotel-pianiste-soiree-opera-hotel-blanc", "Soprano et pianiste en soirée"), ("hotel-chanteur-opera-soiree-hotel-mh-event", "Chanteur lyrique en soirée")],
      ctx="La première soirée de la saison du Club des partenaires de la Ligue&nbsp;: une quarantaine de convives et un mini-concert lyrique.",
      dis=["Mini-concert de la soprano Barbara Bourdarel", "Au piano, Alain Pietka", "Cocktail signé Maison Nans Traiteur"],
      facts=[("≈ 40", "Convives")], quote=None, th="cypres", v="c"),
 dict(slug="inauguration-pulse-entent", t="Inauguration PULSE", wm=None, logo="entent", cat="entreprises", time="passes", date="9 octobre 2026", lieu="ENTENT · Vitrolles",
      ph=[("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-4", "L'équipe ENTENT réunie devant la machine"), ("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca", "Prise de parole lors de l'inauguration"),
          ("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-2", "Invités découvrant la machine PULSE"), ("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-1", "Remise d'un cadeau"),
          ("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-3", "Les invités dans l'atelier"), ("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-6", "Invités en noir et blanc"),
          ("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-7", "Une invitée devant le mur de photos")],
      ctx="ENTENT inaugure PULSE, sa nouvelle machine industrielle, au cœur de son site de Vitrolles. Un atelier transformé en lieu de réception.",
      dis=["Scénographie de l'atelier", "Accueil des invités", "Cadeaux", "Coordination le jour J"], facts=[], quote=None, th="figue", v="a"),
 dict(slug="inauguration-maison-elise-p-cabries", t="Inauguration Maison Elise P", wm="Maison|Elise P", logo=None, cat="entreprises", time="passes", date="Nouveaux locaux", lieu="Cabriès · Bouches-du-Rhône",
      ph=[("lancement-soiree-inauguration-entreprise-cabries-paca-3", "Invités en blanc dans la cour"), ("lancement-soiree-inauguration-entreprise-cabries-paca-1", "Invités réunis devant la maison"),
          ("lancement-soiree-inauguration-entreprise-cabries-paca", "Invités dans les nouveaux locaux"), ("lancement-soiree-inauguration-entreprise-cabries-paca-4", "Embrassades entre invitées"),
          ("lancement-soiree-inauguration-entreprise-cabries-paca-5", "La cour pendant la soirée"), ("lancement-soiree-inauguration-entreprise-cabries-paca-2", "Invitées en conversation")],
      ctx="La Maison Elise P ouvre ses nouveaux locaux à Cabriès&nbsp;: une soirée en blanc, entre la boutique et la cour provençale.",
      dis=["Soirée d'inauguration", "Accueil des invités", "Coordination le jour J"], facts=[], quote=None, th="ivoire", v="c"),
 dict(slug="evenement-gepa-aix-en-provence", t="Événement GEPA", wm=None, logo="gepa", cat="entreprises", time="passes", date="Mars 2026", lieu="Aix-en-Provence",
      ph=[("afterwork-evenement-gepa-aix-mars-2026-accueil", "Entrée de l'événement GEPA à Aix-en-Provence"), ("hotesses-hote-hotesse-evenement-gepa-aix-mars-2026", "Hôte et hôtesse à l'accueil")],
      ctx="Le Groupement des Entrepreneurs du Pays d'Aix réunit ses membres&nbsp;: MH Event signe l'accueil.",
      dis=["Accueil et émargement", "Hôtes et hôtesses", "Orientation des invités"], facts=[], quote=None, th="bordeaux", v="b"),
 dict(slug="diner-gala-pasino-aix-en-provence", t="Dîner de gala au Pasino", wm=None, logo="pasino-grand", cat="entreprises", time="passes", date="Gala et vente aux enchères", lieu="Pasino · Aix-en-Provence",
      ph=[("afterwork-soiree-entrepeneurs-encheres-pasino-aix", "Dîner de gala et vente aux enchères au Pasino"), ("hotesses-hotesses-mh-event-pasino-aix-tenues-noires", "Hôtesses en tenue noire au Pasino")],
      ctx="Un dîner de gala d'entrepreneurs suivi d'une vente aux enchères, dans la grande salle du Pasino d'Aix-en-Provence.",
      dis=["Hôtesses en tenue noire", "Accueil et placement", "Coordination de la soirée"], facts=[], quote=None, th="figue", v="c"),
 dict(slug="conference-afterwork-wiko-aix", t="Conférence et afterwork Wiko", wm="Wiko|conférence", logo=None, cat="entreprises", time="passes", date="Conférence et afterwork", lieu="Aix-en-Provence",
      ph=[("afterwork-conference-wiko-afterwork-aix", "Conférence devant le public à Aix-en-Provence"), ("afterwork-intervention-fondateur-wiko-conference-image-de-marque", "Intervention sur l'image de marque")],
      ctx="Une conférence sur l'image de marque, prolongée par un afterwork entre les invités.",
      dis=["Conférence", "Afterwork", "Accueil des invités"], facts=[], quote=None, th="ivoire", v="a"),
 dict(slug="conference-michel-biet-avignon", t="Conférence Michel Biet", wm=None, logo="michel-biet", cat="entreprises", time="passes", date="Conférence", lieu="Avignon",
      ph=[("afterwork-conference-michel-biet-avignon", "Michel Biet sur scène à Avignon")],
      ctx="Une conférence de Michel Biet à Avignon, de l'accueil à la scène.",
      dis=["Accueil des invités", "Régie de la conférence"], facts=[], quote=None, th="pierre", v="b"),
 dict(slug="soiree-reseau-entreprendre-marseille", t="Soirée Réseau Entreprendre", wm=None, logo="reseau-entreprendre", cat="entreprises", time="passes", date="Soirée", lieu="Marseille",
      ph=[("hotesses-hotesses-soiree-reseau-entreprendre-marseille", "Hôtesses MH Event à la soirée Réseau Entreprendre")],
      ctx="Une soirée du Réseau Entreprendre à Marseille, avec l'accueil des Angelines.",
      dis=["Hôtesses d'accueil", "Accueil et vestiaire"], facts=[], quote=None, th="cypres", v="a"),
 dict(slug="soiree-fin-annee-alcrys", t="Soirée de fin d'année Alcrys", wm=None, logo="alcrys", cat="entreprises", time="passes", date="Décembre 2025", lieu="Soirée d'entreprise",
      ph=[("hotel-soiree-fin-annee-entreprise-alcrys-decembre-2025", "Soirée de fin d'année Alcrys")],
      ctx="La soirée de fin d'année des équipes Alcrys, pour clore 2025 ensemble.",
      dis=["Soirée de fin d'année", "Coordination de la soirée"], facts=[], quote=None, th="bordeaux", v="c"),
 dict(slug="rencontres-economiques-nautisme-saint-tropez", t="Rencontres économiques du nautisme", wm=None, logo="golfe-saint-tropez", cat="entreprises", time="passes", date="2025", lieu="Golfe de Saint-Tropez",
      ph=[("institution-discours-scene-scenographie-golfe-saint-tropez", "Scène et scénographie des Rencontres"), ("hotesses-hotesses-mh-event-tenue-marin", "Hôtesses en marinière"),
          ("hotesses-hotesses-marinieres-nautique-saint-tropez-rencontres-economiques", "Hôtesse en marinière à l'accueil")],
      ctx="« Moment historique pour le golfe de Saint-Tropez »&nbsp;: seize intervenants et cinq heures de débats autour de la filière nautique.",
      dis=["Scénographie de la scène", "Hôtesses en marinière", "Accueil des intervenants et du public"],
      facts=[("16", "Intervenants"), ("5 h", "De débats")], quote=None, th="ivoire", v="c"),
 dict(slug="salon-li-rescountre-d-aqui-arles", t="Li Rescountre d'Aqui", wm=None, logo="cci-pays-arles", cat="entreprises", time="passes", date="Salon", lieu="Arles",
      ph=[("institution-evenement-institutionnel-salon-arles-li-rescountre-dacqui", "Exposants et visiteurs du salon à Arles"), ("institution-salon-arles-atelier-culinaire", "Atelier culinaire du salon"),
          ("institution-mh-event-article-journal-presse-organisation", "Article de presse sur le salon")],
      ctx="Un salon dédié au circuit court en pays d'Arles, avec la CCI&nbsp;: producteurs, acheteurs, ateliers culinaires.",
      dis=["Organisation du salon", "Atelier culinaire", "Accueil des exposants et visiteurs"], facts=[], quote=None, th="pierre", v="b"),
 dict(slug="salon-gastronomie-chateauneuf", t="Salon de la gastronomie", wm=None, logo="festival-gastronomie", cat="entreprises", time="passes", date="Inauguration", lieu="Châteauneuf",
      ph=[("institution-inauguration-ouverture-salon-gastronomie-chateauneuf", "Inauguration du salon de la gastronomie")],
      ctx="L'ouverture officielle du salon de la gastronomie, ruban et élus réunis.",
      dis=["Cérémonie d'inauguration", "Accueil des officiels"], facts=[], quote=None, th="cypres", v="a"),
 dict(slug="mariage-domaine-aix-en-provence", t="Mariage dans un domaine à Aix", wm="Mariage|à Aix", logo=None, cat="particuliers", time="passes", date="Juillet 2025", lieu="Domaine près d'Aix-en-Provence",
      ph=[("mariage-organisation-mariage-domaine-aix-juillet-2025", "Tables dressées dans la cour du domaine"), ("mariage-ceremonie-mariage-juillet-2025", "Cérémonie de mariage"),
          ("mariage-mariee-et-demoiselles-dhonneur-noir-et-blanc", "La mariée et ses demoiselles d'honneur"), ("mariage-dressage-table-blanc-fruits-fleurs-mariage", "Table dressée en blanc")],
      ctx="Un mariage d'été dans un domaine provençal&nbsp;: cérémonie à l'ombre, dîner dans la cour.",
      dis=["Organisation complète", "Cérémonie", "Dîner dans la cour", "Coordination le jour J"], facts=[], quote=None, th="ivoire", v="b"),
 dict(slug="mariage-gruissan", t="Mariage à Gruissan", wm="Mariage|à Gruissan", logo=None, cat="particuliers", time="passes", date="2024", lieu="Gruissan",
      ph=[("mariage-photo-maries-mariage-gruissan-2024", "Les mariés face à la mer"), ("mariage-installation-tables-mariage-gruissan", "Installation des tables"), ("mariage-mariage-vin-honneur-gruissan", "Vin d'honneur")],
      ctx="Un mariage les pieds presque dans l'eau, du vin d'honneur au dîner.",
      dis=["Installation des tables", "Vin d'honneur", "Coordination le jour J"], facts=[], quote=None, th="pierre", v="a"),
 dict(slug="bal-masque-h9ritage-valmousse", t="Bal masqué H9RITAGE", wm="H9RITAGE|bal masqué", logo=None, cat="particuliers", time="passes", date="10 septembre 2026", lieu="Château de Valmousse · Lambesc",
      ph=[("prive-bal-masque-evement-prive", "Couple masqué devant une voiture ancienne")],
      ctx="H9RITAGE, le cercle privé cofondé par Mathilde avec la créatrice Margaux Avila, fait revivre l'art de recevoir à la française.",
      dis=["Bal masqué", "Défilé", "Partenariats joaillerie et automobile"], facts=[], quote=None, th="figue", v="b"),
 dict(slug="anniversaire-30-ans-bateau-marseille", t="Anniversaire 30 ans en bateau", wm="Anniversaire|30 ans", logo=None, cat="particuliers", time="passes", date="Anniversaire", lieu="Marseille",
      ph=[("prive-anniversaire-30-ans-bateau-marseille", "Anniversaire de 30 ans en bateau au large de Marseille")],
      ctx="Un anniversaire en bateau, au large de Marseille.",
      dis=["Privatisation du bateau", "Organisation de la journée"], facts=[], quote=None, th="cypres", v="c"),
]
SVC_LABEL = {h: l for k in SVC for h, l in SVC[k]}
SVC_OF = {'golden-night-golden-tulip-marseille': 'hotels/animation-dynamisation/', 'golden-plus-concept': 'hotels/animation-dynamisation/', 'escale-mediterraneenne-golden-tulip': 'hotels/dejeuner-corpo/', 'odalys-euromed-marseille': 'hotels/animation-dynamisation/', 'soiree-feria-sowell-nimes': 'hotels/animation-dynamisation/', 'dejeuner-corporate-odalys-aix': 'hotels/dejeuner-corpo/', 'golden-tulip-festival': 'hotels/dejeuner-corpo/', 'soiree-o-delice-ligue-football': 'entreprises/soiree-entreprise/', 'inauguration-pulse-entent': 'entreprises/inauguration/', 'inauguration-maison-elise-p-cabries': 'entreprises/inauguration/', 'evenement-gepa-aix-en-provence': 'entreprises/hotes-hotesses/', 'diner-gala-pasino-aix-en-provence': 'entreprises/soiree-entreprise/', 'conference-afterwork-wiko-aix': 'entreprises/conference-salon-afterwork/', 'conference-michel-biet-avignon': 'entreprises/conference-salon-afterwork/', 'soiree-reseau-entreprendre-marseille': 'entreprises/hotes-hotesses/', 'soiree-fin-annee-alcrys': 'entreprises/christmas-party/', 'rencontres-economiques-nautisme-saint-tropez': 'entreprises/conference-salon-afterwork/', 'salon-li-rescountre-d-aqui-arles': 'entreprises/conference-salon-afterwork/', 'salon-gastronomie-chateauneuf': 'entreprises/conference-salon-afterwork/', 'mariage-domaine-aix-en-provence': 'particuliers/mariage/', 'mariage-gruissan': 'particuliers/coordination-jour-j/', 'bal-masque-h9ritage-valmousse': 'particuliers/anniversaire-fete-privee/', 'anniversaire-30-ans-bateau-marseille': 'particuliers/anniversaire-fete-privee/'}
for e in EVENTS:
    e["file"] = f'realisations/{e["slug"]}/'
    e["svc"] = SVC_OF[e["slug"]]

def plate(e):
    if e["logo"]:
        w, hh = Image.open(f"{IMG}/clients/{e['logo']}.webp").size
        return f'<img src="{IMG}/clients/{e["logo"]}.webp" width="{w}" height="{hh}" alt="{esc(e["t"])}" loading="lazy">'
    a, b = e["wm"].split("|")
    return f'<span class="wm">{a}<em>{b}</em></span>'

def vignette(e):
    bg, fg, ac, tx = TH[e["th"]]
    bg = {"ivoire": "#DCCDB3", "or": "#C9A45C"}.get(e["th"], bg)
    st = '<span class="st">À venir</span>' if e["time"] == "avenir" else ""
    cat = {"entreprises": "Entreprise", "hotels": "Hôtel", "particuliers": "Particulier"}[e["cat"]]
    p = e["ph"][0][0]
    return (f'<a class="vg fade" href="{e["file"]}" data-cat="{e["cat"]}" data-time="{e["time"]}" style="--vg-bg:{bg};--vg-fg:{fg}">'
            f'<div class="tile">{img(p, "", "(min-width:960px) 30vw, 100vw")}<div class="plate">{plate(e)}</div>{st}</div>'
            f'<div class="meta"><span>{cat} · {e["lieu"]}</span><h3>{e["t"]}</h3><span>{e["date"]}</span></div></a>')

def build_events():
    n = len(EVENTS)
    for i, e in enumerate(EVENTS):
        bg, fg, ac, tx = TH[e["th"]]
        prev, nxt = EVENTS[(i - 1) % n], EVENTS[(i + 1) % n]
        photos = e["ph"]
        first = photos[0]
        dark = e["th"] in ("figue", "bordeaux", "cypres")
        brand = f'<div class="brand">{plate(e)}</div>' if e["logo"] else ""
        wm = ""
        if not e["logo"]:
            a, b = e["wm"].split("|")
            wm = f'<p class="label">{a} {b}</p>'
        title = e["t"]
        words = title.split(" ")
        if len(words) > 1:
            title_html = " ".join(words[:-1]) + f" <em>{words[-1]}</em>"
        else:
            title_html = f"<em>{title}</em>"
        hero_img = img(first[0], first[1], "100vw" if e["v"] != "b" else "(min-width:960px) 50vw, 100vw", eager=True)
        when = f'<p class="when">{e["date"]} · {e["lieu"]}</p>'
        status = '<p class="label">À venir</p>' if e["time"] == "avenir" else ""
        hero = f'''<section class="ev-hero"><div class="ph">{hero_img}</div>
 <div class="body">{brand}{wm}{status}<h1 class="t-xl">{title_html}</h1>{when}</div></section>'''
        # chapitres
        facts = ""
        if e["facts"]:
            facts = '<div class="facts fade" style="margin-top:48px">' + "".join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in e["facts"]) + "</div>"
        chap1 = f'''<section class="ev-chap" id="contexte"><div class="wrap ev-brief">
 <p class="num fade">01</p>
 <div class="txt"><p class="label fade">Le contexte</p><p class="fade">{e["ctx"]}</p>{facts}</div>
</div></section>'''
        rest = photos[1:]
        if len(rest) >= 2:
            visual = duo(rest[0][0], rest[0][1], rest[1][0], rest[1][1])
            rest2 = rest[2:]
        elif len(rest) == 1:
            visual = ph(rest[0][0], rest[0][1], "p")
            rest2 = []
        else:
            visual = ph(first[0], first[1], "p")
            rest2 = []
        chap2 = f'''<section class="ev-chap" id="dispositif" style="padding-top:0"><div class="wrap ev-pin">
 <div class="sticky stack"><p class="num fade">02</p><p class="label fade">Le dispositif</p><h2 class="t-h2 fade">Signé <em>MH Event</em></h2>
  <ul class="ev-list fade">{"".join(f"<li>{x}</li>" for x in e["dis"])}</ul></div>
 <div class="ev-photos">{visual}</div>
</div></section>'''
        chap3 = ""
        idx = [("contexte", "Le contexte"), ("dispositif", "Le dispositif")]
        if rest2:
            if len(rest2) == 1:
                g = bleed(rest2[0][0], rest2[0][1])
                chap3 = f'<section id="images">{g}</section>'
            else:
                chap3 = f'<section class="ev-chap" id="images" style="padding-top:0"><div class="wrap">{gallery(rest2)}</div></section>'
            idx.append(("images", "En images"))
        q = ""
        if e["quote"]:
            q = f'''<section class="ev-chap" id="paroles" style="padding-top:0"><div class="wrap"><figure class="quote fade"><div class="rule" aria-hidden="true"><i></i></div>
 <blockquote>« {e["quote"][0]} »</blockquote><figcaption class="who">{e["quote"][1]}</figcaption></figure></div></section>'''
            idx.append(("paroles", "Ils en parlent"))
        index = '<nav class="ev-index" aria-label="Chapitres">' + "".join(f'<a href="#{a}">{b}</a>' for a, b in idx) + "</nav>"
        nav = f'''<nav class="ev-next" aria-label="Autres événements">
 <a href="{prev["file"]}"><span class="label">Précédent</span><span class="t-h3">{prev["t"]}</span></a>
 <a href="{nxt["file"]}"><span class="label">Suivant</span><span class="t-h3">{nxt["t"]}</span></a>
</nav>'''
        end = f'''<section class="ev-chap"><div class="wrap cta"><p class="label fade">Réalisations</p><h2 class="t-h2 fade">Le prochain, <em>c'est</em> le vôtre</h2>
 <div class="actions fade" style="justify-content:center"><a class="btn" href="devis.html">Demander un devis</a><a class="link" href="realisations.html">Tous les événements</a></div>
 <p class="fade" style="margin-top:8px">Le service : <a class="link" href="{e["svc"]}">{SVC_LABEL[e["svc"]]}</a></p></div></section>'''
        style = f'<style>body.ev{{--ev-bg:{bg};--ev-fg:{fg};--ev-ac:{ac};--ev-tx:{tx}}}</style>\n'
        body = hero + chap1 + chap2 + chap3 + q + end + nav
        after = '<div class="ev-progress" aria-hidden="true"></div>\n' + index + "\n"
        cls = f"ev ev-{e['v']}" + (" ev-dark" if dark else "")
        import re as _re
        desc = _re.sub(r"<[^>]+>|&nbsp;", " ", e["ctx"]).replace("  ", " ").strip()
        desc = f'{e["t"]}, {e["lieu"]} ({e["date"]}). ' + desc
        if len(desc) > 158:
            desc = desc[:155].rsplit(" ", 1)[0] + "…"
        _tt = f'{e["t"]} · {e["lieu"]} | MH Event'
        page(e["file"], _tt if len(_tt) <= 62 else f'{e["t"]} | Réalisation MH Event', desc,
             body, crumbs=[("realisations/", "Réalisations"), (e["file"], e["t"])], tab="realisations", light=(e["v"] != "a"),
             bodycls=cls, extra_head=style, after=after, tone=("light" if e["v"] == "a" else "dark"))
