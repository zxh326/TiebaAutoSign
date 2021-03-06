from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import *

class profile(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
    inlines = (profile, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)