from django.contrib import admin

from .models import *
from django.contrib.auth.models import User


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
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Schedule)
admin.site.register(Pits, PitsAdmin)
admin.site.register(Images, ImagesAdmin)

