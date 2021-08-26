from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from apps.entry.models import TeamMember
from django.http import HttpResponse
from django.conf import settings
import traceback

from apps.entry.urls import urlpatterns
from apps import config
from apps import importFRC


class ValidateUser:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        config.update_permissions()
        self.permissions = config.permissions
        self.update_permissions()
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)

        if str(request.path).__contains__('media') or str(request.path).__contains__('static') or str(request.path).__contains__('admin'):
            return response

        try:
            if str(request.path) == "/":
                return HttpResponseRedirect(reverse_lazy('entry:index'))
        except IndexError:
            print("INDEX ERROR")
            return response
        try:
            view = str(request.path).split('/')[2]
            app = str(request.path).split('/')[1]
        except IndexError:
            print("\nINDEX ERROR FROM PATH SPLITTING IN MIDDLEWARE:")
            print(request.path)
            print("\n")
            return HttpResponseRedirect(reverse_lazy('entry:index'))

        if view == "logout" or view == "login" or app == "media" or view == "register":
            return response

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('entry:login'))

        if request.user.teammember.position == "NA":
            return HttpResponseRedirect(reverse_lazy('entry:logout'))

        if view == 'entry':
            if self.valid_perms(view, request.user):
                return response
            else:
                return HttpResponseRedirect(reverse_lazy('entry:index'))

        return response

    def update_permissions(self):
        self.permissions = {}

        for each in config.permissions:
            self.permissions[each] = config.permissions[each]['minimum']

    def valid_perms(self, view, user):
        if view == '':
            view = 'index'

        # if 'matchscout' in view:


        reqlevel = 0
        for each in TeamMember.AVAILABLE_POSITIONS:
            if each[0] == self.permissions[view]:
                break
            else:
                reqlevel += 1

        actlevel = 0
        for each in TeamMember.AVAILABLE_POSITIONS:
            if each[0] == user.teammember.position:
                break
            else:
                actlevel += 1

        return actlevel >= reqlevel


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
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
                # TODO Put discord thingy here @Nick

            return HttpResponse("Error processing the request.", status=500)