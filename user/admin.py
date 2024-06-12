from typing import AbstractSet
from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import CustomGroupUser 

from django.db import models

from django.contrib.auth.models import Permission


@admin.register(CustomGroupUser)
class CustomGroupAdmin(GroupAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'permissions')}),
        (_('Description'), {'fields': ('description',)}),
        (_('Date'), {'fields': ('date_of_creation',)}), 
    )



#creating the profile

admin.site.register(Profile)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = UserAdmin.list_display + ('user_profile_is_approved',)
    list_filter = UserAdmin.list_filter + ('userprofile__is_approved',)

    def user_profile_is_approved(self, obj):
        return obj.userprofile.is_approved
        

    user_profile_is_approved.short_description = 'Is Approved'
    user_profile_is_approved.boolean = True


    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)







