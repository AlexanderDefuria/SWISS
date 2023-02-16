import pytest

from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.test import Client
from django.contrib.auth.models import User
from apps.entry.tests.common import *


@pytest.mark.django_db
def test_user_detail(client, django_user_model):
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()
    c = Client()
    logged_in = c.login(username='testuser', password='12345')
    url = reverse('entry:index')
    response = client.get(url)
    # assert response.status_code == 200
    # assert 'someone' in response.content


@pytest.mark.django_db
def test_unauthorized(client):
    url = reverse('admin:app_list', kwargs={'app_label':'entry'})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/admin/login/?next=/admin/entry/'


@pytest.mark.django_db
def test_superuser_view(admin_client):
    url = reverse('admin:app_list', kwargs={'app_label':'entry'})
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_page_load(client):
    url = reverse('entry:login')
    response = client.get(url)
    assert response.status_code == 200

