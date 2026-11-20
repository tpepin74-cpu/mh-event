# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import *
import pages, events, rest

pages.home(); pages.entreprises(); pages.hotels(); pages.particuliers(); pages.mariages(); pages.agence(); pages.realisations()
pages.team_building("entreprises-team-building.html", "entreprises.html", "Entreprises", "entreprises",
    "tb-team-building-eveil-corporal-mh-event-cohesion", "Éveil corporel sur la plage",
    "Rire ensemble, respirer, se dépasser : quinze créations originales, clés en main.",
    "Le genre de journée <em>dont on reparle</em>", "Animées par des professionnels à Nîmes, à Aix, au Pont du Gard et en Camargue, nos activités s'intègrent à votre séminaire ou se suffisent à elles-mêmes.",
    [("tb-team-building-yoga-relaxation-sonore", "Yoga et relaxation sonore dans l'herbe"), ("tb-team-building-crocodiles-nimes-mh-event", "Sur la route des Crocodiles à Nîmes")])
pages.team_building("hotels-team-building.html", "hotels.html", "Hôtels", "hotels",
    "tb-team-building-speed-meeting-hotel-renaissance-aix", "Speed Meeting à l'hôtel Renaissance d'Aix-en-Provence",
    "Une expérience à ajouter à vos offres séminaires.",
    "Pour vos clients <em>séminaires</em>", "Vos commerciaux proposent un team building clé en main, dans l'hôtel ou à proximité : vos clients repartent avec un souvenir, votre hôtel avec un séminaire réussi.",
    [("tb-img-8004", "Atelier de cohésion en intérieur"), ("tb-team-building-fabrique-des-couleurs-marche-consciente-the-camp", "La Fabrique des couleurs à The Camp")])
M_ENT = [("Accueil & émargement", "Accueil VIP, scan des entrées, orientation des invités."), ("Hôtesses de conférence", "Micros, back-up, gestion des intervenants."),
         ("Vestiaire & cadeaux", "Vestiaire, remise des cadeaux, sacs invités."), ("Bar & service", "Barmans, mixologues, serveurs."),
         ("Vente & animation", "Stands, lancements, opérations de marque."), ("Cheffe hôtesse & régie", "Une responsable sur site pour coordonner l'équipe.")]
M_HOT = [("Accueil des séminaires", "Émargement, orientation, accueil VIP de vos clients."), ("Soirées vitrines", "Accueil du public, vestiaire, service au bar."),
         ("Déjeuners Corpo", "Parcours des invités, collecte des contacts, cadeaux."), ("Bar & service", "Barmans, mixologues, serveurs en renfort."),
         ("Cheffe hôtesse", "Une responsable sur site, en lien avec vos équipes.")]
M_PAR = [("Accueil des invités", "Placement, orientation, livre d'or."), ("Vestiaire", "Un vestiaire tenu du début à la fin."), ("Bar & service", "Barmans, mixologues, serveurs."),
         ("Coordination", "Une cheffe hôtesse pour veiller au bon déroulé.")]
REFS_ENT = ["Rencontres économiques du nautisme · Saint-Tropez", "GEPA · Groupement des Entrepreneurs du Pays d'Aix", "Pasino d'Aix-en-Provence · groupe Partouche", "Enedis",
            "Remise de diplômes ICADEMIE · 350 personnes", "Convention internationale · Renaissance Aix-en-Provence", "Inauguration PULSE · ENTENT"]
REFS_HOT = ["Golden Tulip Marseille Euromed · déjeuners et soirées", "Convention internationale · Renaissance Aix-en-Provence", "Pasino d'Aix-en-Provence · groupe Partouche", "Odalys Euromed · Marseille"]
REFS_PAR = ["Mariages en Provence et dans le Gard", "Anniversaires et réceptions privées", "Bal masqué H9RITAGE · Château de Valmousse"]
pages.hotesses("entreprises-hotes-hotesses.html", "entreprises.html", "Entreprises", "entreprises", "hotesses-hotesses-marinieres-nautique-saint-tropez-rencontres-economiques",
    "Hôtesse MH Event en marinière, Saint-Tropez", "Formées par une <em>cheffe hôtesse</em>",
    "Salons, congrès, conventions, inaugurations, soirées de gala : des professionnelles sélectionnées, formées et coachées par Mathilde, ancienne cheffe hôtesse au Grand Prix de France de F1.",
    M_ENT, [("hotesses-hotesses-mh-event-marche", "Hôtesses MH Event en tailleur noir"), ("hotesses-89fd2f99-4d59-40f7-8307-bdfc0a64e9ea", "Hôtesses préparant l'accueil")], REFS_ENT)
pages.hotesses("hotels-hotes-hotesses.html", "hotels.html", "Hôtels", "hotels", "hotesses-img-9066",
    "Hôtesse MH Event en marinière lors d'un déjeuner en hôtel", "L'accueil <em>de vos clients</em>",
    "Séminaires, soirées vitrines, Déjeuners Corpo : les Angelines renforcent vos équipes, avec l'élégance et la discrétion de votre maison.",
    M_HOT, [("hotesses-1c340331-35d4-48c7-8dc5-86eb8c68496c", "Hôtesse à l'accueil d'un hôtel"), ("hotesses-702fe5a0-dd3e-4cf4-9ede-d07c6874c02f", "Deux hôtesses à l'accueil")], REFS_HOT)
pages.hotesses("particuliers-hotes-hotesses.html", "particuliers.html", "Particuliers", "particuliers", "hotesses-hotesses-mh-event-look-t-shirt-flocage",
    "Équipe MH Event en tee-shirts brodés du logo", "Vos invités <em>bien reçus</em>",
    "Mariage, anniversaire, réception à domicile : une équipe pour accueillir, servir et veiller sur vos invités, pendant que vous profitez.",
    M_PAR, [("hotesses-img-9366", "Hôtesse MH Event souriante"), ("hotesses-equipe-mh-event-hotesses-animatrices", "Équipe d'hôtesses et animatrices MH Event")], REFS_PAR)
events.build_events()
rest.blog(); rest.contact(); rest.devis(); rest.faqpage(); rest.mentions(); rest.notfound(); rest.redirects()
print(len(PAGES), "pages")
