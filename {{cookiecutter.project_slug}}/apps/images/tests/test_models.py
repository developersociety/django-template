from django.test import TestCase

from .factories import CustomImageFactory


class CustomImageTestCase(TestCase):

    def test_can_create(self):
        instance = CustomImageFactory.create()
        self.assertIsNotNone(instance.pk)
