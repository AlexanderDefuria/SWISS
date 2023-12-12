from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin

from apps.entry.forms import LoginForm
from apps.organization.forms import RegistrationForm
from apps.organization.models import Organization, OrgMember, Event, OrgSettings


@login_required(login_url='organization:login')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('entry:index'))


class Login(FormMixin, generic.TemplateView):
    template_name = 'entry/login.html'
    form_class = LoginForm
    success_url = 'entry:index'

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                if not OrgMember.objects.filter(user=user).exists():
                    OrgMember.objects.create(user_id=user.id)
            return HttpResponseRedirect(reverse_lazy('entry:index'))

        form.add_error('username', 'Username or password is incorrect')
        form.add_error('password', 'Username or password is incorrect')
        context = {'form': form}
        return render(request, 'entry/login.html', context)


class Registration(FormMixin, generic.TemplateView):
    template_name = 'entry/register.html'
    form_class = RegistrationForm
    success_url = 'entry:index'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('entry:index'))
        else:
            return super(Registration, self).get(request, *args, **kwargs)

    @staticmethod
    def post(request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            if not Event.objects.filter(id=0).exists(): # Settings needs an event to exist
                # This should only happen on the first server run
                event = Event()
                event.save()

            user = User()
            user.orgmember = OrgMember()
            user.set_password(form.cleaned_data['password'])
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            try:
                if form.cleaned_data['create_new_org']:
                    org = Organization()
                    org.settings = OrgSettings()
                    org.settings.current_event = Event.objects.first()
                    org.name = form.cleaned_data['org_name']
                    user.orgmember.position = 'LS'
                    user.orgmember.organization = org
                else:
                    org = Organization.objects.get()
                    if str(org.reg_id)[:6] != form.cleaned_data['org_reg_id']:
                        raise Organization.DoesNotExist
                    user.orgmember.organization = org
            except Organization.DoesNotExist:
                form.add_error('org_name', "Org Name or UUID is incorrect.")
                form.add_error('org_reg_id', "Org Name or UUID is incorrect.")
                context = {'form': form}
                print('org does not exist ' + str(form.cleaned_data))
                return render(request, 'entry/register.html', context)

            user.save()
            user.orgmember.organization.settings.save()
            user.orgmember.organization.save()
            user.orgmember.save()
            user.save()

            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(user)
            auth.login(request, user)
            return HttpResponseRedirect(reverse_lazy('entry:index'))

        return render(request, 'entry/register.html', context)
