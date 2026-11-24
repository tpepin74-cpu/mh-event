# -*- coding: utf-8 -*-
from build import *
from events import EVENTS, build_events, vignette

# ================================================================ ACCUEIL
def home():
    hero = f'''<section class="hero hero-v" aria-labelledby="h-title">
 <div class="hero-media"><video autoplay muted loop playsinline preload="auto" poster="assets/img/hero-poster.jpg" aria-hidden="true"><source src="assets/video/hero.mp4" type="video/mp4"></video></div>
 <div class="hero-body">
  <h1 class="hero-logo" id="h-title"><img src="assets/img/logo-pierre.webp" width="1000" height="626" alt="MH Event, agence événementielle à Nîmes, Aix, Marseille et Saint-Tropez"></h1>
  <div class="hero-cta">
   <p class="lead">Séminaires, team building, journées bien-être, soirées et mariages.</p>
   <div class="entries"><a class="btn green" href="entreprises.html">Une entreprise</a><a class="btn green" href="particuliers.html">Un particulier</a><a class="btn green" href="hotels.html">Un hôtel</a></div>
  </div>
 </div>
 <button class="v-pause" type="button" aria-pressed="false" aria-label="Mettre la vidéo en pause"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z" fill="currentColor"/></svg></button>
 <a class="hero-down" href="#suite" aria-label="Découvrir la suite">{DOWN}</a>
</section>'''
    body = hero + f'''
<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block("La maison", "Une seule <em>signature</em>", "Corporate ou privé, chaque événement est conçu et piloté par Mathilde Heyral, de la première idée au dernier invité.")}
  <div class="actions fade"><a class="link" href="agence-mathilde-heyral.html">Découvrir l'agence</a></div></div>
 {duo("mariage-mariage-chateau-robe-blanche-bouquet", "Mariée et son bouquet devant un château", "lancement-soiree-inauguration-entreprise-cabries-paca-1", "Soirée d'inauguration à Cabriès")}
</div></section>

<section class="sec flush"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(56px,7vw,110px)"><p class="label fade">Nos univers</p><h2 class="t-h2 fade">Trois façons <em>de recevoir</em></h2></div>
 {doors([
   ("entreprises.html", "afterwork-soiree-entrepeneurs-encheres-pasino-aix", "Dîner de gala au Pasino d'Aix-en-Provence", "Entreprises", "Séminaires, soirées, inaugurations, team building."),
   ("hotels.html", "hotel-pianiste-soiree-opera-hotel-blanc", "Soirée Opéra et champagne en hôtel", "Hôtels", "Soirées vitrines, séminaires, Déjeuner Corpo."),
   ("particuliers.html", "mariage-maries-danse-ouverture-bal-mariage-gard", "Ouverture de bal d'un mariage dans le Gard", "Particuliers", "Mariages, anniversaires, fêtes de famille."),
 ])}
</div></section>

{bleed("tb-team-building-marche-des-senteurs-mh-event-avril-2026", "La Marche des senteurs dans les calanques", "Team building", "Des équipes <em>soudées</em>", ("entreprises-team-building.html", "Le catalogue"))}

<section class="sec"><div class="wrap intro rev">
 <div class="txt">{head_block("Séminaires &amp; bien-être", "Respirer <em>ensemble</em>", "Yoga face à la mer, relaxation sonore, massages, ateliers : des journées qui soudent autant qu'elles reposent.")}
  <div class="actions fade"><a class="link" href="entreprises.html">Les formats</a></div></div>
 {duo("bienetre-cours-yoga-evenement-bien-etre", "Cours de yoga en terrasse face aux collines", "seminaire-mh-event-organisation-seminaire-montpellier", "Séminaire sous chapiteau près de Montpellier", rev=True)}
</div></section>

<section class="sec bg-pierre"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(48px,6vw,88px)"><p class="label fade">Réalisations</p><h2 class="t-h2 fade">Ils nous font <em>confiance</em></h2></div>
 {logos(["golden-tulip","pasino-grand","odalys-euromed","entent","golfe-saint-tropez","reseau-entreprendre","gepa","cci-pays-arles"])}
 <div class="actions center fade" style="margin-top:clamp(48px,6vw,80px);justify-content:center"><a class="btn line" href="realisations.html">Toutes les réalisations</a></div>
</div></section>

<section class="sec"><div class="wrap intro">
 <figure class="fade">{ph("mathilde-portrait-mathilde-heyral-mh-event", "Mathilde Heyral, fondatrice de MH Event", "p")}<figcaption>Mathilde Heyral, fondatrice</figcaption></figure>
 <div class="txt">{head_block("Une seule interlocutrice", "Le sens <em>du détail</em>", "Danseuse classique, cheffe hôtesse au Grand Prix de France de F1, juriste : Mathilde garde de ce parcours une double exigence, l'émotion pour vos invités, la rigueur pour vous.")}
  <p class="sig fade">Mathilde Heyral</p></div>
</div></section>

<section class="sec flush"><div class="wrap">
 <figure class="quote fade"><div class="rule" aria-hidden="true"><i></i></div><blockquote>« Mathilde transforme chaque moment en une expérience unique, fluide et parfaitement orchestrée. »</blockquote>
 <figcaption class="who">Lucie Lauzel · avis Google · <a href="https://share.google/i5QVzxkjr3eyGyZ6x" target="_blank" rel="noopener" style="color:var(--bordeaux)">5,0 sur 35 avis</a></figcaption></figure>
</div></section>
{cta(dark=True)}'''
    page("index.html", "MH Event · Agence événementielle à Nîmes, Aix, Marseille & Saint-Tropez",
         "Agence événementielle haut de gamme en Provence et dans le Gard : séminaires, team building, journées bien-être, soirées en hôtel, hôtesses et mariages.",
         body, tab=None)

# ================================================================ ENTREPRISES
def entreprises():
    body = hero_photo("seminaire-seminaire-groupe-entreprise-sourire-discussion", "Séminaire d'entreprise en plein air", "Entreprises",
                      "Événements <em>d'entreprise</em>", "Vous fixez le cap. MH Event s'occupe de tout le reste.", pos="50% 40%") + f'''
<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block("Séminaires · soirées · inaugurations", "De A <em>à</em> Z", "Lieu, hébergement, plénière, soirée, transport, équipes d'accueil : une seule interlocutrice, des devis clairs, des plannings tenus.")}</div>
 {duo("seminaire-mh-event-organisation-seminaire-montpellier", "Séminaire sous chapiteau près de Montpellier", "lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca", "Inauguration de la machine PULSE chez ENTENT")}
</div></section>

<section class="sec flush"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Les formats</p><h2 class="t-h2 fade">Ce que nous <em>organisons</em></h2></div>
 {rows([
   ("Séminaires & conventions", "Sur un ou deux jours, résidentiel ou non : lieu, plénière, déjeuners, soirée, transport."),
   ("Journées bien-être", "Yoga, relaxation sonore, massages, ateliers : une journée pour souffler ensemble."),
   ("Soirées & galas", "Soirées à thème, dîners-spectacles, cocktails, Christmas party."),
   ("Inaugurations & lancements", "Scénographie, accueil, cadeaux, photographe, musiciens."),
   ("Afterworks & conférences", "Réseaux d'entrepreneurs, conférences, soirées de networking."),
   ("Déjeuners immersifs", "Le Déjeuner Corpo : deux heures pour faire découvrir un lieu ou une marque."),
 ])}
</div></section>

<section class="sec flush"><div class="wrap">{gallery([
  ("lancement-inauguration-machine-industrielle-societe-entent-vitrolles-paca-4", "Inauguration chez ENTENT à Vitrolles"),
  ("bienetre-atelier-sonore-nature-relaxation", "Relaxation sonore en plein air"),
  ("afterwork-conference-wiko-afterwork-aix", "Conférence et afterwork à Aix-en-Provence"),
  ("afterwork-img-8704", "Soirée lyrique avec pianiste"),
  ("seminaire-pique-nique-entreprise-plage-avril-2026", "Pique-nique d'entreprise sur la plage"),
  ("bienetre-cours-pilates-evenement-bien-etre", "Cours de Pilates pendant une journée bien-être"),
])}</div></section>

<section class="sec bg-pierre"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(56px,7vw,110px)"><p class="label fade">Pour vos équipes</p><h2 class="t-h2 fade">Aller plus <em>loin</em></h2></div>
 {doors([
   ("entreprises-team-building.html", "tb-team-building-eveil-corporal-mh-event-cohesion", "Éveil corporel sur la plage", "Team building", "Quinze créations originales, dès 28 € HT par personne."),
   ("entreprises-hotes-hotesses.html", "hotesses-hotesses-mh-event-pasino-aix-tenues-noires", "Hôtesses MH Event en tenue noire au Pasino", "Hôtes & hôtesses", "Les Angelines, formées et coachées, 27 € HT de l'heure."),
 ])}
</div></section>

<section class="sec tight"><div class="wrap">
 <p class="label center fade" style="margin-bottom:40px">Ils nous ont fait confiance</p>
 {logos(["entent","gepa","pasino-grand","reseau-entreprendre","golfe-saint-tropez","cci-pays-arles","alcrys","michel-biet"])}
</div></section>

<section class="sec bg-pierre"><div class="wrap two">
 <div class="stack"><p class="label fade">Questions</p><h2 class="t-h2 fade">Avant de <em>commencer</em></h2></div>
 {faq([("Pouvez-vous gérer un séminaire de A à Z ?", "Oui : conception, recherche du lieu, hébergement, plénière, déjeuners, team building, soirée, transport et hôtesses, avec une seule interlocutrice."),
       ("Quel délai prévoir ?", "Idéalement trois à six mois. Des délais plus courts restent possibles. Pour les fêtes de fin d'année, décembre se réserve en septembre."),
       ("Où intervenez-vous ?", "Surtout à Aix-en-Provence, Marseille, Nîmes, Saint-Tropez, Montpellier, Avignon et Arles, et partout en France sur demande.")])}
</div></section>
{cta("Votre prochain <em>événement</em>", devis="devis.html?type=S%C3%A9minaire")}'''
    page("entreprises.html", "Événements d'entreprise · séminaires, soirées, inaugurations · MH Event",
         "Séminaires, journées bien-être, soirées, inaugurations et afterworks en Provence et dans le Gard, organisés de A à Z par MH Event.", body, tab="entreprises")

# ================================================================ TEAM BUILDING (deux versions)
TB = [
 ("Instant Zen Détente", "Yoga flow, relaxation sonore, moodboard collaboratif. 5 à 80 personnes.", "dès 47 €"),
 ("Instant Zen Active", "Yoga dynamique, ateliers de confiance et de coopération, méditation.", "dès 49 €"),
 ("La Fabrique des couleurs", "Colorimétrie des personnalités et création collective, avec une coach.", "dès 45 €"),
 ("Speed Meeting", "Échanges courts en binômes, animés par une sophrologue.", "dès 28 €"),
 ("Olympiades & défis", "Parcours, tir à la corde, jeux de précision, avec un coach sportif.", "dès 30 €"),
 ("Yoga & énergie collective", "Yoga dynamique puis relaxation, par une professeure diplômée.", "300 € la séance"),
 ("Relaxation sonore", "Une immersion dans les vibrations des bols, allongés.", "dès 30 €"),
 ("Breathwork", "Respiration consciente guidée par une sophrologue.", "dès 39 €"),
 ("Le Circuit des poètes · Nîmes", "Daudet, Bigot, Reboul, Mistral : des Arènes aux Jardins de la Fontaine.", "dès 55 €"),
 ("La route des Crocodiles · Nîmes", "Quatre étapes, quatre compétences, des énigmes au Muséum.", "dès 50 €"),
 ("La Marche des senteurs · Nîmes", "Yoga doux et marche sensorielle aux Jardins de la Fontaine.", "dès 39 €"),
 ("La Marche des senteurs · Pont du Gard", "Garrigue et plantes méditerranéennes, aussi dans les calanques.", "dès 45 €"),
 ("Immersion en manade · Camargue", "Taureaux, chevaux et repas de terroir avec la Manade Aubanel.", "dès 57 €"),
 ("Aix-périence · Aix", "Chasse photo, impro filmée et flash mob autour des fontaines.", "dès 50 €"),
 ("Parcours gourmand · Aix", "Sur les pas du Roi René : tapenade, fougasse, calissons.", "dès 70 €"),
]
def team_building(fname, parent, parent_label, tab, hero_img, hero_alt, lead, intro_t, intro_p, duo_imgs):
    body = hero_photo(hero_img, hero_alt, parent_label + " · Team building", "Des expériences <em>qui soudent</em>", lead,
                      crumbs=[(parent, parent_label), (fname, "Team building")]) + f'''
<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block("Catalogue 2026", intro_t, intro_p)}<div class="actions fade"><a class="btn" href="devis.html?type=Team%20building">Demander un devis</a></div></div>
 {duo(duo_imgs[0][0], duo_imgs[0][1], duo_imgs[1][0], duo_imgs[1][1])}
</div></section>
<section class="sec flush" id="catalogue"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Prix HT par personne</p><h2 class="t-h2 fade">Quinze <em>créations</em></h2></div>
 {rows(TB)}
 <p class="small fade" style="margin-top:28px">Options : accueil café dès 10 €, déjeuner dès 30 €, coordination sur site dès 250 € la demi-journée, hôtesse d'accueil 27 € HT de l'heure.</p>
</div></section>
<section class="sec flush"><div class="strip">{"".join(ph(n, a, "", "(min-width:760px) 28vw, 70vw") for n, a in [
  ("tb-team-building-sport-olympiades-marseille", "Olympiades d'entreprise à Marseille"),
  ("tb-team-building-crocodiles-nimes-mh-event", "Sur la route des Crocodiles à Nîmes"),
  ("tb-img-6306-2", "Yoga sous une voûte de pierre"),
  ("tb-team-building-visite-manade-taureaux-camargue", "Visite de manade en Camargue"),
  ("tb-team-building-fabrique-des-couleurs-marche-consciente-the-camp", "La Fabrique des couleurs à The Camp"),
  ("tb-team-building-yoga-relaxation-sonore", "Yoga et relaxation sonore dans l'herbe"),
  ("tb-team-building-balade-chevaux-equipe", "Balade à cheval en forêt"),
  ("tb-img-8023", "Atelier de cohésion en intérieur"),
])}</div></section>
<section class="sec bg-pierre"><div class="wrap two">
 <div class="stack"><p class="label fade">Questions</p><h2 class="t-h2 fade">Bon à <em>savoir</em></h2></div>
 {faq([("Les activités sont-elles adaptables ?", "Oui. Toutes sont des créations originales de MH Event, clés en main, adaptées au lieu, au nombre de participants et à vos objectifs."),
       ("Pourquoi des activités exclusives à Nîmes ?", "Elles ont été conçues à la demande de l'Office de Tourisme et des Congrès de Nîmes, dont MH Event est partenaire depuis 2026."),
       ("Peut-on les associer à un séminaire ?", "Oui : le team building s'intègre à votre journée, avec accueil, déjeuner et coordination sur site.")])}
</div></section>
{cta("Votre équipe, <em>autrement</em>", devis="devis.html?type=Team%20building")}'''
    page(fname, f"Team building · {parent_label} · MH Event", "Quinze team buildings originaux à Nîmes, Aix, au Pont du Gard et en Camargue, dès 28 € HT par personne.",
         body, cur=fname, tab=tab)

# ================================================================ HÔTES & HÔTESSES (trois versions)
def hotesses(fname, parent, parent_label, tab, hero_img, hero_alt, intro_t, intro_p, missions, duo_imgs, refs):
    body = hero_photo(hero_img, hero_alt, parent_label + " · Les Angelines", "Hôtes &amp; <em>hôtesses</em>", "Le premier sourire de votre événement.",
                      crumbs=[(parent, parent_label), (fname, "Hôtes & hôtesses")], pos="50% 30%") + f'''
<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block("27 € HT de l'heure", intro_t, intro_p)}<div class="actions fade"><a class="btn" href="devis.html?type=H%C3%B4tesses">Réserver une équipe</a></div></div>
 {duo(duo_imgs[0][0], duo_imgs[0][1], duo_imgs[1][0], duo_imgs[1][1])}
</div></section>
<section class="sec flush"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Les missions</p><h2 class="t-h2 fade">À votre <em>service</em></h2></div>
 {rows(missions)}
</div></section>
{bleed("hotesses-hotesses-mh-event-tenue-marin", "Hôtesses MH Event en marinière, Saint-Tropez", "Jamais l'uniforme classique", "Une tenue <em>accordée</em> au thème", pos="50% 30%")}
<section class="sec"><div class="wrap two">
 <div class="stack"><p class="label fade">Références</p><h2 class="t-h2 fade">Ils ont fait appel <em>aux Angelines</em></h2></div>
 <ul class="ev-list fade" style="--ev-fg:var(--ink);--ev-ac:var(--or)">{"".join(f"<li>{r}</li>" for r in refs)}</ul>
</div></section>
{cta("Réservez vos <em>Angelines</em>", "Date, horaires, nombre d'hôtesses, missions et tenue souhaitée : quelques mots suffisent pour un devis.", devis="devis.html?type=H%C3%B4tesses")}'''
    page(fname, f"Hôtes & hôtesses · {parent_label} · MH Event", "Les Angelines : hôtes et hôtesses sélectionnés, formés et coachés par MH Event, 27 € HT de l'heure.",
         body, cur=fname, tab=tab)

# ================================================================ HÔTELS
def hotels():
    body = hero_photo("hotel-evenement-spectacle-peinture-live-hotel-euromed-odalys", "Soirée live painting dans un hôtel de Marseille", "Hôtels",
                      "Faire vivre <em>votre</em> hôtel", "Un bar qui se remplit, une clientèle locale qui revient, des contrats MICE qui suivent.") + f'''
<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block("Dynamisation · MICE", "Une programmation <em>annuelle</em>", "Une à deux soirées vitrines par mois, ouvertes au public, avec planning, descriptif et devis par soirée.")}
  <div class="actions fade"><a class="link" href="realisation-golden-night.html">Le cas Golden Night</a></div></div>
 {duo("hotel-soiree-saxophone-lounge-hotel-marseille-dynamisation", "Soirée saxophone Lounge en hôtel à Marseille", "hotel-pianiste-soiree-opera-hotel-blanc", "Pianiste lors d'une soirée Opéra et champagne")}
</div></section>

<section class="sec flush"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Nos offres</p><h2 class="t-h2 fade">Pour les <em>hôtels</em></h2></div>
 {rows([
   ("Soirées vitrines", "Comedy Club, blind test, casino, piano-bar, guinguette sur le rooftop : le public découvre votre hôtel."),
   ("Soirées séminaires", "Un catalogue de soirées privatisées à glisser dans les propositions de vos commerciaux.", "dès 1 590 € HT"),
   ("Déjeuner Corpo", "Deux heures pour faire découvrir chambres, salles et restauration à 50 professionnels locaux.", "2 400 à 3 900 € HT"),
   ("Séminaires découverte", "Des acheteurs venus de toute la France vivent votre établissement, pour de futurs contrats."),
 ])}
</div></section>

{bleed("hotel-comedy-show-marseille-juin-2026", "Comedy Club au Golden Tulip Marseille Euromed", "Golden Tulip Marseille Euromed", "Golden <em>Night</em>", ("realisation-golden-night.html", "Voir l'événement"), pos="50% 30%")}

<section class="sec bg-figue on-dark" id="soirees"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Prix indicatifs HT</p><h2 class="t-h2 fade">Le catalogue <em>des soirées</em></h2></div>
 {rows([
   ("Nuit andalouse", "Harpe et danseuse de flamenco.", "2 850 €"),
   ("Opéra et champagne", "Chanteurs lyriques et pianiste.", "3 650 €"),
   ("Kermesse", "Puissance 4 géant, Mölkky, chamboule-tout.", "1 590 €"),
   ("Cluedo géant", "Six comédiens, une enquête grandeur nature.", "≈ 2 600 €"),
   ("Gatsby", "Dîner-spectacle années folles.", "≈ 5 000 €"),
   ("Le Vernissage", "Live painting.", "3 100 €"),
   ("Velvet Lounge · Piano Club", "Saxophone ou piano.", "1 850 · 2 400 €"),
   ("Hiver blanc", "Danseuses, chanteur, DJ, environ 100 personnes.", "4 300 €"),
   ("Quiz, blind test, casino", "Jeux et animations.", "dès 1 790 €"),
   ("Comedy Club, cabaret, mentalisme", "Dîners-spectacles.", "sur devis"),
 ])}
</div></section>

<section class="sec"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(56px,7vw,110px)"><p class="label fade">Pour vos clients séminaires</p><h2 class="t-h2 fade">Aller plus <em>loin</em></h2></div>
 {doors([
   ("hotels-team-building.html", "tb-team-building-speed-meeting-hotel-renaissance-aix", "Speed Meeting à l'hôtel Renaissance d'Aix-en-Provence", "Team building", "Une expérience à ajouter à vos offres séminaires."),
   ("hotels-hotes-hotesses.html", "hotesses-1dd14db4-c9e9-425f-9873-2b419e3f39b3", "Hôtesses MH Event à l'accueil d'un événement", "Hôtes & hôtesses", "Accueil, vestiaire, service, 27 € HT de l'heure."),
 ])}
</div></section>

<section class="sec tight bg-pierre"><div class="wrap">
 <p class="label center fade" style="margin-bottom:40px">Ils nous font confiance</p>
 {logos(["golden-tulip","odalys-euromed","odalys-city","sowell","hotels-de-nimes","pasino-grand","nimes-tourisme","cds-groupe"])}
</div></section>
{cta("Parlons de <em>votre</em> hôtel", devis="devis.html?type=Soir%C3%A9e%20en%20h%C3%B4tel")}'''
    page("hotels.html", "Hôtels · soirées de dynamisation, séminaires, Déjeuner Corpo · MH Event",
         "Programmation annuelle de soirées vitrines, catalogue de soirées séminaires et Déjeuner Corpo pour faire vivre votre hôtel.", body, tab="hotels")

# ================================================================ PARTICULIERS
def particuliers():
    body = hero_photo("mariage-organisation-mariage-domaine-aix-juillet-2025", "Mariage dans un domaine près d'Aix-en-Provence", "Particuliers",
                      "Vos plus beaux <em>moments</em>", "Mariages, anniversaires, fêtes de famille, en Provence et dans le Gard.") + f'''
<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block("MH Wedding &amp; privé", "Pensés <em>pour vous</em>", "La même exigence que pour nos clients d'entreprise, dans un univers plus doux : un planning tenu, des prestataires choisis, et vous, présents à chaque instant.")}</div>
 {duo("mariage-photo-mariage-shooting-robe-blanche", "Mariée en robe blanche dans un domaine", "prive-bal-masque-evement-prive", "Bal masqué, couple devant une voiture ancienne")}
</div></section>

<section class="sec flush"><div class="wrap">
 {doors([
   ("particuliers-mariages.html", "mariage-shooting-mariage-couple-sourire-domaine-montpellier", "Mariés souriants dans une allée de domaine", "Mariages &amp; privé", "Coordination du jour J ou organisation complète."),
   ("particuliers-hotes-hotesses.html", "hotesses-f25d5f7f-b901-4e6d-abb2-1578bbd3a3e4-2", "Hôtesses MH Event", "Hôtes &amp; hôtesses", "Accueil des invités, vestiaire, service et bar."),
 ])}
</div></section>

<section class="sec"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Vos célébrations</p><h2 class="t-h2 fade">À chaque <em>occasion</em></h2></div>
 {rows([
   ("Mariages", "Welcome party, cérémonie, brunch du lendemain, souvent sur plusieurs jours.", "dès 3 500 €"),
   ("Anniversaires", "Trente ans en mer, quarante ans en domaine, à domicile ou dans un lieu choisi."),
   ("Fêtes de famille", "Baptêmes, réceptions, food truck dans le jardin."),
   ("Soirées à thème", "Gatsby, guinguette, casino, kermesse ou opéra, en version privée."),
 ])}
</div></section>

<section class="sec flush"><div class="wrap">{gallery([
  ("prive-anniversaire-30-ans-bateau-marseille", "Anniversaire de 30 ans en bateau à Marseille"),
  ("mariage-brasero-mariage-paca-invites", "Braséro et invités pendant un mariage"),
  ("prive-pancarte-accueil-bapteme", "Pancarte d'accueil d'un baptême"),
  ("mariage-dressage-table-blanc-fruits-fleurs-mariage", "Table de mariage dressée en blanc"),
  ("prive-mh-event-evenement-food-truck-2024", "Réception privée avec food truck"),
  ("mariage-ronde-ruban-mariage-mariee-bouquet", "Ronde des rubans autour de la mariée"),
])}</div></section>

{bleed("prive-bal-masque-evement-prive", "Bal masqué au Château de Valmousse", "H9RITAGE · Château de Valmousse", "Le bal <em>masqué</em>", ("realisation-bal-masque-h9ritage.html", "Voir l'événement"), pos="50% 30%")}
{cta("Racontez-nous <em>votre</em> projet", "Une date, un lieu rêvé, un nombre d'invités : quelques mots suffisent pour commencer.", devis="devis.html?type=Mariage")}'''
    page("particuliers.html", "Particuliers · mariages, anniversaires, fêtes privées · MH Event",
         "Mariages, anniversaires et fêtes de famille en Provence et dans le Gard, imaginés et coordonnés par MH Event.", body, tab="particuliers")

def mariages():
    body = hero_photo("mariage-photo-maries-mariage-gruissan-2024", "Mariés face à la mer à Gruissan", "Particuliers · MH Wedding",
                      "Se marier en <em>Provence</em>", "Vous vous dites oui, on s'occupe du reste.",
                      crumbs=[("particuliers.html", "Particuliers"), ("particuliers-mariages.html", "Mariages & privé")]) + f'''
<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block("Welcome party · mariage · brunch", "Un mariage <em>qui vous ressemble</em>", "Ancienne wedding planner du Domaine du Grand Lauron, Mathilde organise des mariages en Provence et dans le Gard, souvent sur plusieurs jours.")}
  <div class="actions fade"><a class="link" href="https://www.instagram.com/mathilde_heyral_wedding/" target="_blank" rel="noopener">@mathilde_heyral_wedding</a></div></div>
 {duo("mariage-mariage-ceremonie-laique-domaine", "Cérémonie laïque dans un domaine", "mariage-bouquet-mariage-domaine-herault-montpellier", "Bouquet de mariée posé sur un muret")}
</div></section>
<section class="sec flush"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Deux façons de vous accompagner</p><h2 class="t-h2 fade">Votre <em>formule</em></h2></div>
 {rows([
   ("Coordination du jour J", "Reprise du planning quelques semaines avant, rencontre des prestataires, présence de l'installation à la fin de soirée.", "sur devis"),
   ("Organisation complète", "Recherche des prestataires, visites, dégustations, essais, suivi du budget.", "dès 3 500 €"),
   ("In English", "For couples living abroad: quotes and planning in English."),
 ])}
</div></section>
<section class="sec flush"><div class="wrap">{gallery([
  ("mariage-mariee-et-demoiselles-dhonneur-noir-et-blanc", "Mariée et demoiselles d'honneur en noir et blanc"),
  ("mariage-maries-noir-et-blanc", "Mariés en noir et blanc"),
  ("mariage-dressage-tables-vaisselles-blanc-mariage", "Tables de mariage dressées en blanc"),
  ("mariage-mariage-chateau-robe-blanche-bouquet", "Mariée devant un château"),
  ("mariage-ronde-rubans-bouquet-mariee", "Ronde des rubans"),
  ("mariage-img-9667", "Pièce montée et feux de table"),
])}</div></section>
{bleed("mariage-maries-danse-ouverture-bal-mariage-gard", "Ouverture de bal d'un mariage dans le Gard", "Les détails qui restent", "Le bal <em>s'ouvre</em>", pos="50% 35%")}
<section class="sec bg-pierre"><div class="wrap two">
 <div class="stack"><p class="label fade">Questions des futurs mariés</p><h2 class="t-h2 fade">Bon à <em>savoir</em></h2></div>
 {faq([("Quelle différence entre coordination et organisation complète ?", "La coordination reprend votre planning quelques semaines avant et assure la présence sur site. L'organisation complète, dès 3 500 €, comprend aussi la recherche des prestataires, les visites, dégustations, essais et le suivi du budget."),
       ("Organisez-vous des mariages pour des couples vivant à l'étranger ?", "Oui, avec devis et planning en anglais."),
       ("Où organisez-vous les mariages ?", "En Provence et dans le Gard, souvent sur plusieurs jours : welcome party, mariage, brunch, pool party.")])}
</div></section>
{cta("Racontez-nous <em>votre</em> mariage", "Date, lieu rêvé, nombre d'invités : quelques mots suffisent pour commencer.", devis="devis.html?type=Mariage")}'''
    page("particuliers-mariages.html", "Mariages & privé · MH Wedding · MH Event", "Mariages en Provence et dans le Gard : coordination du jour J ou organisation complète dès 3 500 €.",
         body, tab="particuliers")

# ================================================================ AGENCE
def agence():
    body = hero_photo("mathilde-mathilde-heyral-wedding-planner", "Mathilde Heyral dressant une table", "L'agence · depuis 2023",
                      "Mathilde <em>Heyral</em>", "Fondatrice et présidente de MH Event.", pos="50% 25%") + f'''
<section class="sec" id="suite"><div class="wrap intro">
 <div class="txt">{head_block("Une agence à taille humaine", "Rien n'est <em>standard</em>", "Née fin 2023 en Provence, MH Event suit chaque projet avec la même personne, la même exigence et le même cœur.")}</div>
 {duo("mathilde-mathilde-heyral-protrait-pro-evenement", "Portrait de Mathilde Heyral", "mathilde-img-9513", "Mathilde Heyral prépare une table", rev=False)}
</div></section>
<section class="sec flush"><div class="wrap">
 <div class="stack" style="margin-bottom:clamp(40px,5vw,72px)"><p class="label fade">Le fil d'une histoire</p><h2 class="t-h2 fade">Un parcours <em>singulier</em></h2></div>
 {rows([
   ("La danse", "Danseuse classique diplômée du Royal Ballet d'Anvers : la rigueur, la scène, le sens du détail."),
   ("Le terrain", "Hôtesse puis cheffe hôtesse : Grand Prix de France de F1, Dior, FDJ, Pasino d'Aix, Grand Théâtre de Provence."),
   ("Le droit", "Master en droit des affaires, puis trois ans à former des juristes aux marchés publics."),
   ("MH Event", "Fin 2023, une agence « 360° » qui réunit organisation, accueil et communication."),
   ("Aujourd'hui", "Partenaire de l'Office de Tourisme de Nîmes, cofondatrice du cercle privé H9RITAGE."),
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
   ("Communication", "Visuels selon votre charte, stratégie digitale et print."),
 ])}
</div></section>
<section class="sec flush"><div class="strip">{"".join(ph(n, a, "", "(min-width:760px) 28vw, 70vw") for n, a in [
  ("mathilde-mathilde-heyral-mh-event", "Mathilde Heyral lors d'un événement"),
  ("mathilde-conference-table-ronde-evenementiel-marseille", "Mathilde Heyral lors d'une table ronde à Marseille"),
  ("mathilde-img-9084", "Mathilde Heyral en marinière"),
  ("mathilde-mathilde-heyral-ceo", "Mathilde Heyral en réunion"),
  ("mathilde-img-9750", "Mathilde Heyral et son équipe"),
  ("mathilde-portrait-mathilde-heyral-seo-mh-event", "Portrait de Mathilde Heyral"),
])}</div></section>
{cta()}'''
    page("agence-mathilde-heyral.html", "L'agence · Mathilde Heyral · MH Event", "Mathilde Heyral, fondatrice de MH Event : danse classique, terrain, droit des affaires. Une agence événementielle à taille humaine.",
         body)

# ================================================================ RÉALISATIONS
def realisations():
    cats = [("all", "Tous"), ("entreprises", "Entreprises"), ("hotels", "Hôtels"), ("particuliers", "Particuliers")]
    times = [("passes", "Passés"), ("avenir", "À venir")]
    fbtn = "".join(f'<button type="button" data-g="cat" data-v="{v}" aria-pressed="{"true" if v=="all" else "false"}">{l}</button>' for v, l in cats)
    fbtn += '<span class="sep" aria-hidden="true"></span>' + '<button type="button" data-g="time" data-v="all" aria-pressed="true" hidden>Tous</button>'
    fbtn += "".join(f'<button type="button" data-g="time" data-v="{v}" aria-pressed="false">{l}</button>' for v, l in times)
    body = f'''<section class="sec" style="padding-top:clamp(170px,20vw,240px)"><div class="wrap">
 <div class="stack center" style="margin-bottom:clamp(48px,6vw,88px)"><p class="label">Réalisations</p><h1 class="t-xl">Nos <em>événements</em></h1><div class="rule" aria-hidden="true"><i></i></div>
  <p class="lead">Des marques, des lieux, des invités. Chaque événement a son histoire&nbsp;: choisissez-en un.</p></div>
 <div class="filters" role="group" aria-label="Filtrer les événements">{fbtn}</div>
 <p class="sr" id="vign-live" aria-live="polite"></p>
 <div class="vign">{"".join(vignette(e) for e in EVENTS)}</div>
 <p class="vign-empty" hidden>Aucun événement pour ce filtre.</p>
</div></section>
<section class="sec bg-pierre"><div class="wrap">
 <figure class="quote fade"><div class="rule" aria-hidden="true"><i></i></div><blockquote>« Nous avons eu le plaisir de collaborer à plusieurs reprises avec MH Event et chaque expérience a été tout simplement exceptionnelle. »</blockquote>
 <figcaption class="who">Lucie Lauzel · avis Google · 5,0 sur 35 avis</figcaption></figure>
</div></section>
{cta("Le prochain, <em>c'est</em> le vôtre")}'''
    page("realisations.html", "Réalisations · MH Event", "Inaugurations, soirées en hôtel, séminaires, conférences et mariages : les événements imaginés et orchestrés par MH Event.",
         body, tab="realisations", light=True)
