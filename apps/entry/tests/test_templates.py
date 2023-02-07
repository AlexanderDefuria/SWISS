import pytest
from django.contrib.auth.models import User
from django.test import LiveServerTestCase, override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By

from apps.entry.tests.common import *
from apps.entry.urls import urlpatterns
from apps.entry.tests.test_common import test_should_create_organization


@pytest.mark.django_db
@pytest.mark.usefixtures("firefox_driver_init")
@override_settings(DEBUG=True)
class MatchFormTest(LiveServerTestCase):
    browser = None
    port = 8888
    user:User = None
    base_url:str = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.base_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self) -> None:
        self.user = create_user()
        self.org = create_organization(create_org_settings(create_event()), create_team())
        self.org_member = create_org_member(self.user, self.org)
        self.assertTrue(self.client.login(username=username, password=password))
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url) # visit page in the site domain so the page accepts the cookie
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': True, 'path': '/'})

    def test_login(self):
        self.live_server_url += '/entry/login/'
        self.browser.get(self.live_server_url)
        username_elem = self.browser.find_element(value='username')
        username_elem.clear()
        username_elem.send_keys(username)
        password_elem = self.browser.find_element(value='password')
        password_elem.clear()
        password_elem.send_keys(password)
        self.browser.find_element(by=By.CLASS_NAME, value='loginButton').click()

        self.assertEqual(self.browser.current_url, f'http://localhost:{self.port}/entry/')

    def test_static_pages_load(self):
        urls = ['matchscout', 'pitscout', 'visual', 'glance',
                'teams', 'stats', 'matchdata', 'pitdata', 'about']

        for url in urls:
            browser = self.browser
            browser.get(self.base_url + '/entry/' + url)
            self.assertIsNotNone(browser.find_element(by=By.TAG_NAME, value='title'))
            self.assertIn(url, self.browser.current_url)
