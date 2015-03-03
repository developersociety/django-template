from blanc_basic_assets.fields import AssetForeignKey
from blanc_pages.blocks import BaseBlock
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class CarouselBlock(BaseBlock):
    class Meta:
        verbose_name = 'carousel'

    def __str__(self):
        return 'Carousel'


@python_2_unicode_compatible
class CarouselSlide(models.Model):
    carousel = models.ForeignKey(CarouselBlock)
    image = AssetForeignKey('assets.Image')
    title = models.CharField(max_length=100)
    content = models.TextField()
    link = models.URLField(blank=True)
    link_text = models.CharField(max_length=100, blank=True)
    position = models.PositiveSmallIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.title
