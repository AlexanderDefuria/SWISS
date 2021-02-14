from django.contrib import admin

from .models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apps.entry.models import TeamMember


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class TeamMemberInline(admin.StackedInline):
    model = TeamMember
    can_delete = True
    verbose_name_plural = 'Team Info'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (TeamMemberInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Team)
admin.site.register(Event)
admin.site.register(Match)
admin.site.register(Schedule)
admin.site.register(Pits)
admin.site.register(Images)
admin.site.register(TeamMember)
