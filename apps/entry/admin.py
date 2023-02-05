from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class OrgMemberInline(admin.StackedInline):
    model = OrgMember
    can_delete = True
    verbose_name_plural = 'Team Info'
    fields = ('team', 'position', 'tutorial_completed')
    readonly_fields = ()

    def get_fields(self, request, obj=None):
        fields = super(OrgMemberInline, self).get_fields(request, obj)
        if not request.user.is_superuser:
            self.readonly_fields = ('team', 'is_superuser', 'user_permissions')
        return fields


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (OrgMemberInline,)
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
        return qs.filter(is_staff=False, is_superuser=False) | qs.filter(id=request.user.id,
                                                                         username=request.user.username)

    def get_form(self, request, obj=None, **kwargs):
        print("hit")
        self.fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'groups')}),
            ('Important dates', {'fields': ('last_login', 'date_joined')}))
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        return form


class MatchFilter(admin.SimpleListFilter):
    template = 'admin/integer_filter.html'  # templates/admin/integer_filter.html
    title = 'Match Number'
    parameter_name = 'match_number'

    def lookups(self, request, model_admin):
        return [('', ''), ('', '')]

    def queryset(self, request, queryset):
        if self.value() is not None:
            match = self.value()
            return queryset.filter(match_number=match)
        return queryset


class EventFilter(admin.ChoicesFieldListFilter):

    def lookups(self, request, model_admin):
        pass

    def queryset(self, request, queryset):
        pass


class OwnershipFilter(admin.SimpleListFilter):
    template = 'admin/integer_filter.html'  # templates/admin/integer_filter.html
    title = 'Ownership'
    parameter_name = 'ownership'

    def lookups(self, request, model_admin):
        return [('', ''), ('', '')]

    def queryset(self, request, queryset):
        if not request.user.is_superuser:
            return queryset.filter(ownership=request.user.orgmember.organization)
        if self.value() is not None:
            return queryset.filter(ownership=request.user.orgmember.organization)
        return queryset


class MatchAdmin(admin.ModelAdmin):
    list_filter = [MatchFilter, OwnershipFilter]
    autocomplete_fields = ['team', 'event']
    search_fields = ['team__name', 'event__name']

    def get_queryset(self, request):
        qs = super(MatchAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(townership=request.user.orgmember.organization)


class PitsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(PitsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ownership=request.user.orgmember.organization)


class OrgMemberAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)

    def get_queryset(self, request):
        qs = super(OrgMemberAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.orgmember.organization)  # get org members from same org

    def get_fields(self, request, obj=None):
        fields = super(OrgMemberAdmin, self).get_fields(request, obj)
        if not request.user.is_superuser:
            self.readonly_fields = ('user', 'organization')
        return fields


class TeamAdmin(admin.ModelAdmin):
    search_fields = ['name', 'number']


class EventAdmin(admin.ModelAdmin):
    search_fields = ['name', 'number']


class ImagesAdmin(admin.ModelAdmin):
    search_fields = ['name', 'image']

    def get_queryset(self, request):
        qs = super(ImagesAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(ownership=request.user.orgmember.organization)


# REGISTRATIONS
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Schedule)
admin.site.register(Pits, PitsAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(OrgMember, OrgMemberAdmin)
admin.site.register(OrgSettings)
admin.site.register(Organization)
