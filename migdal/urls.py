# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from migdal import feeds, settings
from migdal.helpers import i18n_patterns

pats = []
for t in settings.TYPES:
    pats += [
        # entry list
        url(string_concat(r'^', t.slug, r'/$'),
            'migdal.views.entry_list', {'type_db': t.db},
            name='migdal_entry_list_%s' % t.db),
        url(string_concat(r'^', t.slug, r'/rss.xml$'),
            feeds.EntriesFeed(), {'type_db': t.db},
            name='migdal_entry_list_%s_feed' % t.db),
        # single entry
        url(string_concat(r'^', t.slug, r'/(?P<slug>[^/]+)/$'),
            'migdal.views.entry', {'type_db': t.db},
            name='migdal_entry_%s' % t.db),
    ]

urlpatterns = i18n_patterns('',
    # main page
    url(r'^$', 'migdal.views.entry_list', name='migdal_main'),
    url(r'^rss.xml$', feeds.EntriesFeed(), name='migdal_main_feed'),
    # category
    url(string_concat(r'^', _('categories'), r'/(?P<category_slug>[^/]*)/$'),
        'migdal.views.entry_list', name='migdal_category'),
    url(string_concat(r'^', _('categories'), r'/(?P<category_slug>[^/]*)/rss.xml$'),
        feeds.EntriesFeed(), name='migdal_category_feed'),
    # type-specific views
    *pats
)
