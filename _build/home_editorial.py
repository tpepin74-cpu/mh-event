# -*- coding: utf-8 -*-
"""MH Event: editorial homepage. All copy and destinations come from the existing homepage."""
from build import page, img, logos, AGENCY, DOMAIN, _v


def cutout(name, alt, cls, eager=False):
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="assets/img/editorial/{name}-cutout.webp" '
            f'alt="{alt}" width="{1012 if name == "bride" else 1060}" height="{1202 if name == "bride" else 1484}" {loading} decoding="async">')


def build_home():
    body = f'''
<section class="signature-stage" aria-labelledby="h-title">
 <div class="ed-wrap signature-inner">
  <p class="eyebrow signature-kicker">Agence événementielle · Provence &amp; Gard</p>
  <div class="signature-garden" aria-hidden="true"><img src="assets/img/editorial/garden-background.webp" alt="" width="1025" height="1535" loading="eager" decoding="async"></div>
  <div class="signature-reception">{img("lancement-soiree-inauguration-entreprise-cabries-paca-1", "Soirée d'inauguration à Cabriès", "(min-width:900px) 19vw, 35vw", eager=True)}</div>
  <svg class="signature-thread thread-back" viewBox="0 0 1000 700" fill="none" aria-hidden="true"><path d="M150 630C-160 420 1000-170 935 130C910 260 766 352 696 405"/></svg>
  <h1 class="signature-title" id="h-title"><span class="sr">MH Event, agence événementielle à Nîmes, Aix-en-Provence, Marseille et Saint-Tropez. </span><span>Une seule</span> <span>signature</span></h1>
  {cutout("bride", "Mariée et son bouquet devant un château", "signature-bride", True)}
  <svg class="signature-thread thread-front" viewBox="0 0 1000 700" fill="none" aria-hidden="true"><path d="M696 405C840 478 925 548 744 602C600 646 383 652 239 699"/></svg>
  <div class="signature-copy">
   <span class="tiny-diamond" aria-hidden="true"></span>
   <p>Corporate ou privé, chaque événement est conçu et piloté par Mathilde Heyral, de la première idée au dernier invité, à Aix-en-Provence, Marseille, Nîmes et Saint-Tropez.</p>
   <a class="ed-link" href="agence/">Découvrir l'agence</a>
  </div>
  <a class="signature-scroll" href="#suite" aria-label="Découvrir la suite">Découvrir la suite<span aria-hidden="true"></span></a>
 </div>
</section>

<section class="event-film hero" id="suite" aria-label="Les événements MH Event">
 <div class="ed-wrap film-layout">
  <div class="film-frame">
   <video muted loop playsinline preload="none" poster="assets/img/hero-poster.jpg" aria-label="Les événements organisés par MH Event"><source data-film-src="assets/video/hero.mp4" type="video/mp4"></video>
   <button class="v-pause film-pause" type="button" aria-pressed="true" aria-label="Lire la vidéo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z" fill="currentColor"/></svg></button>
   <img class="film-logo" src="assets/img/logo-pierre.webp" width="1000" height="626" alt="MH Event">
  </div>
  <div class="film-copy">
   <p class="film-lead">Séminaires, team building, journées bien-être, soirées et mariages.</p>
   <div class="film-entries"><a href="entreprises/">Une entreprise</a><a href="particuliers/">Un particulier</a><a href="hotels/">Un hôtel</a></div>
  </div>
 </div>
</section>

<section class="audiences ed-section" aria-labelledby="audiences-title">
 <div class="ed-wrap">
  <div class="section-heading"><p class="eyebrow">Vous êtes</p><h2 class="ed-title" id="audiences-title">Trois façons<br><em>de recevoir</em></h2><span class="heading-flourish" aria-hidden="true">&amp;</span></div>
  <div class="audience-grid">
   <a class="audience audience-business" href="entreprises/">
    <div class="audience-image">{img("afterwork-soiree-entrepeneurs-encheres-pasino-aix", "Dîner de gala au Pasino d'Aix-en-Provence", "(min-width:800px) 33vw, 100vw")}</div>
    <div class="audience-caption"><h3>Une entreprise</h3><p>Séminaires, soirées, inaugurations, team building.</p><span class="ed-link">Découvrir</span></div>
   </a>
   <a class="audience audience-hotel" href="hotels/">
    <div class="audience-image">{img("hotel-pianiste-soiree-opera-hotel-blanc", "Soirée Opéra et champagne en hôtel", "(min-width:800px) 27vw, 100vw")}</div>
    <div class="audience-caption"><h3>Un hôtel</h3><p>Soirées vitrines, soirées séminaires, Déjeuner Corpo.</p><span class="ed-link">Découvrir</span></div>
   </a>
   <a class="audience audience-private" href="particuliers/">
    <div class="audience-image">{img("mariage-maries-danse-ouverture-bal-mariage-gard", "Ouverture de bal d'un mariage dans le Gard", "(min-width:800px) 33vw, 100vw")}</div>
    <div class="audience-caption"><h3>Un particulier</h3><p>Mariage, coordination du jour J, anniversaires.</p><span class="ed-link">Découvrir</span></div>
   </a>
  </div>
 </div>
</section>

<section class="together" aria-labelledby="together-title">
 <div class="ed-wrap together-inner">
  <p class="eyebrow">Team building</p>
  <h2 id="together-title">Des équipes<br><em>soudées</em></h2>
  <figure class="together-photo">{img("tb-team-building-marche-des-senteurs-mh-event-avril-2026", "La Marche des senteurs dans les calanques", "(min-width:900px) 76vw, 100vw")}</figure>
  <div class="together-caption"><span class="tiny-diamond" aria-hidden="true"></span><a class="ed-link" href="entreprises/team-building/">Voir les quinze activités</a></div>
  <span class="together-circle" aria-hidden="true"></span>
 </div>
</section>

<section class="wellness ed-section" aria-labelledby="wellness-title">
 <div class="ed-wrap wellness-inner">
  <div class="wellness-art">
   <div class="wellness-main">{img("bienetre-cours-yoga-evenement-bien-etre", "Cours de yoga en terrasse face aux collines", "(min-width:900px) 36vw, 78vw")}</div>
   <div class="wellness-detail">{img("seminaire-mh-event-organisation-seminaire-montpellier", "Séminaire sous chapiteau près de Montpellier", "(min-width:900px) 23vw, 45vw")}</div>
   <svg class="wellness-thread" viewBox="0 0 600 700" fill="none" aria-hidden="true"><path d="M110 670C-160 500 340-150 510 30C660 200 420 540 230 570"/></svg>
  </div>
  <div class="wellness-copy">
   <p class="eyebrow">Séminaires &amp; bien-être</p><h2 class="ed-title" id="wellness-title">Respirer <br><em>ensemble</em></h2>
   <p class="ed-body">Yoga face à la mer, relaxation sonore, massages : des journées qui soudent autant qu'elles reposent.</p>
   <div class="wellness-links"><a class="ed-link" href="entreprises/journee-bien-etre/">Les journées bien-être</a><a class="ed-link" href="entreprises/seminaire/">Organiser un séminaire</a></div>
  </div>
 </div>
</section>

<section class="quote-ribbon"><div class="ed-wrap ribbon-inner"><p>Un devis gratuit,<br>une réponse sous <em>48 heures.</em></p><div><a class="ed-button" href="devis/">Demander un devis</a><a class="ribbon-tel" href="tel:+33614466183">ou appelez le 06 14 46 61 83</a></div></div></section>

<section class="client-section ed-section" aria-labelledby="clients-title"><div class="ed-wrap">
 <div class="clients-heading"><div><p class="eyebrow">Réalisations</p><h2 class="ed-title" id="clients-title">Ils nous font<br><em>confiance</em></h2></div><a class="ed-link" href="realisations/">Toutes les réalisations</a></div>
 {logos(["golden-tulip", "pasino-grand", "odalys-euromed", "entent", "golfe-saint-tropez", "reseau-entreprendre", "gepa", "cci-pays-arles"])}
</div></section>

<section class="founder ed-section" aria-labelledby="founder-title"><div class="ed-wrap founder-inner">
 <figure class="founder-art"><span class="founder-monogram" aria-hidden="true">M</span><span class="founder-panel" aria-hidden="true"></span>
  {cutout("mathilde", "Mathilde Heyral, fondatrice de MH Event", "founder-cutout")}
  <span class="founder-outline" aria-hidden="true"></span><figcaption>Mathilde Heyral, fondatrice</figcaption>
 </figure>
 <div class="founder-copy"><p class="eyebrow">Une seule interlocutrice</p><h2 class="ed-title" id="founder-title">Le sens<br><em>du détail</em></h2><p class="ed-body">Danseuse classique, cheffe hôtesse au Grand Prix de France de F1, juriste : Mathilde garde de ce parcours une double exigence, l'émotion pour vos invités, la rigueur pour vous.</p><p class="founder-signature">Mathilde Heyral</p></div>
</div></section>

<section class="testimonial"><div class="ed-wrap"><figure><span class="quote-mark" aria-hidden="true">“</span><blockquote>« Mathilde transforme chaque moment en une expérience unique, fluide et parfaitement orchestrée. »</blockquote><figcaption>Lucie Lauzel · avis Google · <a href="https://share.google/i5QVzxkjr3eyGyZ6x" target="_blank" rel="noopener">5,0 sur 35 avis</a></figcaption></figure></div></section>

<section class="contact-editorial ed-section" aria-labelledby="contact-title"><div class="ed-wrap contact-inner">
 <p class="eyebrow">Devis gratuit · réponse sous 48 h</p><h2 id="contact-title">Et si on en<br><em>parlait</em>&nbsp;?</h2>
 <span class="contact-loop" aria-hidden="true"></span>
 <p class="ed-body">Une idée précise ou une envie encore floue : racontez-la. Mathilde vous rappelle sous 24 à 48 h.</p>
 <div class="contact-actions"><a class="ed-button" href="devis/">Demander un devis</a><a class="ed-link" href="tel:+33614466183">06 14 46 61 83</a></div>
 <p class="contact-address"><a href="mailto:contact@mh-event.fr">contact@mh-event.fr</a><span> · 7 rue Tédenat, Nîmes</span></p>
</div></section>'''
    extra = (f'<link rel="stylesheet" href="assets/css/editorial.css?v={_v("assets/css/editorial.css")}">'
             f'<script src="assets/js/editorial.js?v={_v("assets/js/editorial.js")}" defer></script>')
    page("", "MH Event · Agence événementielle à Aix, Marseille, Nîmes",
         "Agence événementielle haut de gamme à Aix-en-Provence, Marseille, Nîmes et Saint-Tropez : séminaires, team building, soirées en hôtel, hôtesses et mariages.",
         body, light=True, bodycls="home-editorial", extra_head=extra,
         jsonld=[AGENCY, {"@context": "https://schema.org", "@type": "WebSite", "name": "MH Event", "url": DOMAIN}])
