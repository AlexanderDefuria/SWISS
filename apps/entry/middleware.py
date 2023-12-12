from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from apps.organization.models import OrgMember, OrgSettings
from django.http import HttpResponse
from django.conf import settings
import traceback
import json
import os

jpath = os.path.join(settings.BASE_DIR, './apps/permissions.json')
permissions_global = []
logged_in_users = []

# Note, update_permissions_from_file() runs at start.


class ValidateUser:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        update_permissions_from_file()
        self.permissions = permissions_global
        self.update_permissions()
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)

        if str(request.path).__contains__('media') or str(request.path).__contains__('static') or str(request.path).__contains__('admin') or str(request.path).__contains__('promotional'):
            return response

        try:
            if str(request.path) == "/":
                return HttpResponseRedirect(reverse_lazy('promotional:index'))
        except IndexError:
            print("INDEX ERROR")
            return response
        try:
            view = str(request.path).split('/')[2]
            app = str(request.path).split('/')[1]
        except IndexError:
            if str(request.path).__contains__("favicon.ico"):
                return response
            if str(request.path).__contains__("logout"):
                return response

            print("\nINDEX ERROR FROM PATH SPLITTING IN MIDDLEWARE:")
            print(request.path)
            print("\n")
            return HttpResponseRedirect(reverse_lazy('entry:index'))

        if app == "hours" and view in ["view", "card"]:
            return response

        if view == "login" and request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('entry:index'))

        if view == "logout" or view == "login" or app == "media" or view == "register":
            return response

        if not request.user.is_authenticated:
            print("\n" + str(request.user) + " IS REQUESTING " + request.path + " WITHOUT AUTHENTICATION!\n")
            return HttpResponseRedirect(reverse_lazy('organization:login'))

        if request.user.orgmember.position == "NA":
            return HttpResponseRedirect(reverse_lazy('organization:logout'))

        print(request.user.orgmember)

        if app == 'entry':
            if self.valid_perms(view, request.user):
                return response
            else:
                print(view)
                print("\n" + str(request.user) + " [" + str(request.user.orgmember.position)
                      + "] IS REQUESTING " + request.path + " WITH INVALID PERMS!\n")
                return HttpResponseRedirect(reverse_lazy('entry:index'))

        return response

    def update_permissions(self):
        self.permissions = {}

        for each in permissions_global:
            self.permissions[each] = permissions_global[each]['minimum']

    def valid_perms(self, view, user):
        if view == '':
            view = 'index'

        reqlevel = 0
        for each in OrgSettings.AVAILABLE_POSITIONS:
            try:
                if each[0] == self.permissions[view]:
                    break
                reqlevel += 1
            except KeyError:
                return False

        actlevel = 0
        for each in OrgSettings.AVAILABLE_POSITIONS:
            if each[0] == user.orgmember.position:
                break
            else:
                actlevel += 1

        return actlevel >= reqlevel


def process_exception(request, exception):
    if not settings.DEBUG:
        if exception:
            # Format your message here
            message = "**{url}**\n\n{error}\n\n````{tb}````".format(
                url=request.build_absolute_uri(),
                error=repr(exception),
                tb=traceback.format_exc()
            )
            # Do now whatever with this message
            # e.g. requests.post(<slack channel/teams channel>, data=message)
            # TODO Integrate into other comm medium slack discord etc...

        return HttpResponse("Error processing the request.", status=500)


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


def update_permissions_from_file():
    global permissions_global
    with open(jpath) as f:
        permissions_global = json.load(f)


update_permissions_from_file()
