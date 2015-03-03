from blanc_pages.blocks import BaseBlock
from django.db import models


class TwoColumnTextBlock(BaseBlock):
    left_column = models.TextField(blank=True)
    right_column = models.TextField(blank=True)

    class Meta:
        verbose_name = 'two column text'
