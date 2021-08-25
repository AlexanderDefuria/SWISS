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


class MatchAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        print("hit")
        qs = super(MatchAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team_ownership_id=request.user.teammember.team_id)


class PitsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        print("hit")
        qs = super(PitsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team_ownership_id=request.user.teammember.team_id)


#class ImagesAdmin(admin.ModelAdmin):
    #def get_queryset(self, request):
    #    print("hit")
    #    qs = super(ImagesAdmin, self).get_queryset(request)
    #    if request.user.is_superuser:
    #        return qs
    #    return qs.filter(team_ownership_id=request.user.teammember.team_id)



# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Team)
admin.site.register(Event)
admin.site.register(Match, MatchAdmin)
admin.site.register(Schedule)
admin.site.register(Pits, PitsAdmin)
admin.site.register(Images)
#admin.site.register(Images, ImagesAdmin)
admin.site.register(TeamMember)
