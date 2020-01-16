from django.db import models

from wagtail.images.models import AbstractImage, AbstractRendition, Image


class CustomImage(AbstractImage):
    caption = models.CharField(max_length=255, blank=True)
    credit = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    admin_form_fields = Image.admin_form_fields + ("caption", "credit", "alt_text")


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name="renditions")

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)