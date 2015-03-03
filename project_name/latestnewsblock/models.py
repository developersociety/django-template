from blanc_pages.blocks import BaseBlock
from django.db import models


class LatestNewsBlock(BaseBlock):
    category = models.ForeignKey('news.Category', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'latest news'
