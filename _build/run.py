# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import *
import pages, events, rest

pages.build_all()
events.build_events()
rest.blog(); rest.contact(); rest.devis(); rest.faqpage(); rest.mentions(); rest.notfound()
rest.redirects()
rest.sitemap(PAGES)
print(len(PAGES), "pages")
