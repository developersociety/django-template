from django.contrib.auth.models import AbstractUser, Group as BaseGroup


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"


# To allow groups to set alongside users in the Django admin - we use a proxy model back to the
# default group model and re-register it this app.
class Group(BaseGroup):
    class Meta:
        proxy = True
