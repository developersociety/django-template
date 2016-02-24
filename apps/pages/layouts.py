# -*- coding: utf-8 -*-

from glitter import columns
from glitter import templates
from glitter.layouts import PageLayout


@templates.attach('glitter_pages.Page')
class Home(PageLayout):
    content = columns.Column(width=960)
