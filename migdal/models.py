# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _, ugettext
from markupfield.fields import MarkupField
from migdal.helpers import add_translatable
from migdal import settings


class Category(models.Model):

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('migdal_category', [self.slug])


add_translatable(Category, {
    'title': models.CharField(max_length=64, unique=True, db_index=True),
    'slug': models.SlugField(unique=True, db_index=True),
})


class Entry(models.Model):
    #type = models.CharField(max_length=16,
    #        choices=((t.db, t.slug) for t in settings.TYPES),
    #        db_index=True)
    type = models.CharField(max_length=16,
            choices=((t.db, t.slug) for t in settings.TYPES),
            db_index=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    author = models.CharField(_('author'), max_length=128)
    author_email = models.EmailField(_('author email'), max_length=128, null=True, blank=True)
    image = models.ImageField(_('image'), upload_to='entry/image/', null=True, blank=True)
    promo = models.BooleanField(_('promoted'), default=False)
    categories = models.ManyToManyField(Category, null=True, blank=True)

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        ordering = ['-date']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # convert blank to null for slug uniqueness check to work
        for lc, ln in settings.OPTIONAL_LANGUAGES:
            slug_name = "slug_%s" % lc
            if hasattr(self, slug_name) == u'':
                setattr(self, slug_name, None)
        super(Entry, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('migdal_entry_%s' % self.type, [self.slug])

    def get_type(self):
        return dict(settings.TYPES_DICT)[self.type]


add_translatable(Entry, languages=settings.OBLIGATORY_LANGUAGES, fields={
    'slug': models.SlugField(unique=True, db_index=True),
    'title': models.CharField(_('title'), max_length=255),
    'lead': MarkupField(_('lead'), markup_type='textile_pl'),
})

add_translatable(Entry, languages=settings.OPTIONAL_LANGUAGES, fields={
    'slug': models.SlugField(unique=True, db_index=True, null=True, blank=True),
    'title': models.CharField(_('title'), max_length=255, null=True, blank=True),
    'lead': MarkupField(_('lead'), markup_type='textile_pl', null=True, blank=True),
    'needed': models.CharField(_('needed'), max_length=1, db_index=True, choices=(
                ('n', _('Unneeded')), ('w', _('Needed')), ('y', _('Done'))),
                default='n'),
})

add_translatable(Entry, {
    'body': MarkupField(_('body'), markup_type='textile_pl', null=True, blank=True),
    'published': models.BooleanField(_('published'), default=False),
})



class Attachment(models.Model):
    file = models.FileField(_('file'), upload_to='entry/attach/')
    entry = models.ForeignKey(Entry)

    def url(self):
        return self.file.url if self.file else ''
