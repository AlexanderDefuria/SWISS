from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.organizations.models import OrgMember, Organization, OrgSettings


# Register your models here.
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


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
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


# admin.site.register(User, UserAdmin)
admin.site.register(OrgMember, OrgMemberAdmin)
admin.site.register(OrgSettings)
admin.site.register(Organization)
