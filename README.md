# MH Event — refonte 2026 (V2)

Site statique de présentation du nouveau site de MH Event (mh-event.fr), agence événementielle de Mathilde Heyral.
Copie de travail désindexée (balise noindex sur chaque page + robots.txt).

- Aperçu : https://tpepin74-cpu.github.io/mh-event/
- Charte : pierre #EDE6DA, bordeaux #5A1626, vert cyprès #3B4A32, or #C9A45C, figue noire #2A1A20 ; Cormorant Garamond (titres) et Hanken Grotesk (textes).
- Les pages HTML sont générées par `_build/run.py` (contenus dans `_build/pages.py`, `_build/events.py`, `_build/rest.py`) : `python3 _build/run.py` depuis la racine.
- Styles : `assets/css/mh.css` · Interactions : `assets/js/mh.js` · Concierge : `assets/js/chat.js`.

## Accueil éditorial

La page d'accueil reprend les contenus existants dans une composition ivoire et bordeaux : photographies superposées, titres HTML et portraits détourés. Les autres pages conservent leurs gabarits.

- Source : `_build/home_editorial.py`, appelée par `_build/pages.py::home()`.
- Styles et interactions propres à l'accueil : `assets/css/editorial.css`, `assets/js/editorial.js`.
- Couches photographiques optimisées avec transparence : `assets/img/editorial/`.
- Régénérer seulement l'accueil : `PYTHONPATH=_build python -c 'import pages; pages.home()'`.
- La vidéo d'origine se charge à l'approche de sa section, se met en pause hors écran et respecte la préférence de réduction des animations.
