import factory

from images.models import CustomImage


class CustomImageFactory(factory.django.DjangoModelFactory):
    width = 100
    height = 100
    title = 'test'

    class Meta:
        model = CustomImage
