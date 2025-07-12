import factory

from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Sequence(lambda n: f"person{n}@example.org")
    password = "test123"  # noqa:S105

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            is_superuser = kwargs.pop("is_superuser")
            if is_superuser:
                return manager.create_superuser(*args, **kwargs)
        return manager.create_user(*args, **kwargs)
