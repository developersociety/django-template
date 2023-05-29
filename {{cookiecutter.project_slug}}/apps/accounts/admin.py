from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BaseGroup

from .models import Group, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


admin.site.unregister(BaseGroup)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass
