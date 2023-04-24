from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

    class Meta:
        db_table = "auth_user"
