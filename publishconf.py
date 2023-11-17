#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

cname = os.path.basename(os.getcwd())
try:
    with open(os.path.join('content', 'CNAME')) as f:
        cname = f.read().strip()
        SITEURL = "https://%s" % cname
except FileNotFoundError:
    pass

SITEURL = "https://%s" % cname
FAVICON = f'{SITEURL}/favicon.svg'
SITELOGO = f'{SITEURL}/{AVATAR}'

PLAUSIBLE_DOMAIN = cname

FEED_ALL_ATOM = 'feeds/all.atom.xml'
TAG_FEED_ATOM = 'feeds/tag/{slug}.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/category/{slug}.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
TAG_FEED_RSS = 'feeds/tag/{slug}.rss.xml'
CATEGORY_FEED_RSS = 'feeds/category/{slug}.rss.xml'

DELETE_OUTPUT_DIRECTORY = True
