#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime

AUTHOR = 'Florian Haas'
SITENAME = 'xahteiwi.eu'

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'http://localhost:8000'
AVATAR = 'images/avatar.jpg'
SITELOGO = SITEURL + '/' + AVATAR
COPYRIGHT_YEAR = datetime.now().year

THEME = 'themes/Flex'
THEME_COLOR = 'light'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

MAIN_MENU = True

ROBOTS = 'index,follow'

OUTPUT_RETENTION = ['.git',
                    '.nojekyll',
                    'LICENSE']

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

STATIC_PATHS = [
    'CNAME',
    'css',
    'favicon.ico',
    'fonts',
    'images',
    'keybase.txt',
    'robots.txt',
    ]

PLUGIN_PATHS = [
    'plugins',
    'plugins/bootstrapify',
    'plugins/custom_article_urls',
    'plugins/pelican-page-hierarchy',
    'plugins/series',
    'plugins/sitemap',
    'plugins/summary',
]
PLUGINS = [
    'bootstrapify',
    'custom_article_urls',
    'i18n_subsites',
    'page_hierarchy',
    'render_math',
    'series',
    'sitemap',
    'summary',
]

PATH = 'content'

# Page sources go into content/pages, and they get rendered according
# to their slug, unless overridden by Save_as metadata.
PAGE_PATHS = ["pages"]
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

# Article sources go into content/articles, and they get rendered
# according to category, or if a matching category is given in
# CUSTOM_ARTICLE_URLS, to whatever is specified there. In addition, an
# article's output path can also be overridden by Save_as metadata.
ARTICLE_PATHS = ["articles"]
ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = "{category}/{slug}/index.html"
CUSTOM_ARTICLE_URLS = {
    'blog': {'URL': 'blog/{date:%Y/%m/%d}/{slug}/',
             'SAVE_AS': 'blog/{date:%Y/%m/%d}/{slug}/index.html'},
    'hints-and-kinks': {'URL': 'resources/{category}/{slug}/',
                        'SAVE_AS': 'resources/{category}/{slug}/index.html'},
    'news-releases': {'URL': 'resources/{category}/{slug}/',
                        'SAVE_AS': 'resources/{category}/{slug}/index.html'},
    'presentations': {'URL': 'resources/{category}/{slug}/',
                        'SAVE_AS': 'resources/{category}/{slug}/index.html'},
    'case-studies': {'URL': 'testimonials/{category}/{slug}/',
                     'SAVE_AS': 'testimonials/{category}/{slug}/index.html'},
    }

# Direct templates are those that don't have a source document, but
# are generated from an aggregate of multiple source
# documents. Normally 'index' is included in this list. We generate
# our index.html from a page, so we can leave it off this list.
DIRECT_TEMPLATES = ('categories', 'tags', 'authors', 'archives', 'search')

TIMEZONE = 'Etc/UTC'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = [
    ('Tech', '/category/hints-and-kinks.html'),
    ('Talks', '/category/presentations.html'),
    ('Thoughts', '/category/blog.html'),
    ('\u200b', ''),
    ('About', '/about/'),
    ('Comments', '/comments/'),
    ('Legal', '/legal/'),
    ('Privacy', '/privacy/'),
    ('\u200b', ''),
    ('Categories', '/categories.html'),
    ('Tags', '/tags.html'),
    ('\u200b', ''),
]

# Blogroll
LINKS = []

# Social links, also displayed on the sidebar.
SOCIAL = (('twitter', 'https://twitter.com/xahteiwi'),
          ('mastodon', 'https://mastodon.social/@xahteiwi'),
          ('linkedin', 'https://www.linkedin.com/in/fghaas'),
          ('github', 'https://github.com/fghaas'))

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Generate an XML sitemap (provided by the sitemap module).
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# The Series plugin displays this message for any article that is part
# of a series
SERIES_TEXT = 'Part %(index)s of "%(name)s"'

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
HIDE_SITENAME = False

CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike License",
    "version": "4.0",
    "slug": "by-sa",
    "icon": True,
    "language": "en_US",
}

TWITTER_USERNAME = 'xahteiwi'
TWITTER_CARDS = True

SUMMARY_END_MARKER = '<!--break-->'

CUSTOM_CSS = 'css/override.css'
