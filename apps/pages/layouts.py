# -*- coding: utf-8 -*-

from glitter import columns, templates
from glitter.layouts import PageLayout


@templates.attach('glitter_pages.Page')
class Default(PageLayout):
    content = columns.Column(width=960)
