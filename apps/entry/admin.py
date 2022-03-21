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
    fields = ('team', 'position', 'tutorial_completed')
    readonly_fields = ()

    def get_fields(self, request, obj=None):
        fields = super(TeamMemberInline, self).get_fields(request, obj)
        if not request.user.is_superuser:
            self.readonly_fields = ('team', 'is_superuser', 'user_permissions')
        return fields


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (TeamMemberInline,)
    fieldsets = BaseUserAdmin.fieldsets
    old_fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}))

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_staff=False, is_superuser=False) | qs.filter(id=request.user.id, username=request.user.username)

    def get_form(self, request, obj=None, **kwargs):
        print("hit")
        self.fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'groups')}),
            ('Important dates', {'fields': ('last_login', 'date_joined')}))
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        return form


class MatchAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(MatchAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team_ownership_id=request.user.teammember.team_id)


class PitsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(PitsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team_ownership_id=request.user.teammember.team_id)


class TeamMemberAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)

    def get_queryset(self, request):
        qs = super(TeamMemberAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team=request.user.teammember.team_id)

    def get_fields(self, request, obj=None):
        fields = super(TeamMemberAdmin, self).get_fields(request, obj)
        if not request.user.is_superuser:
            self.readonly_fields = ('user', 'team')
        return fields


# class ImagesAdmin(admin.ModelAdmin):
# def get_queryset(self, request):
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
# admin.site.register(Images, ImagesAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(TeamSettings)
