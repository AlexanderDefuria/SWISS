from time import sleep

from django.contrib.contenttypes.models import ContentType
from django.test import LiveServerTestCase
from selenium import webdriver

from entry.tests.common import create_user


class MatchFormTest(LiveServerTestCase):
    driver = None
    port = 8888
    user = None

    @classmethod
    def setUpClass(cls):
        ContentType.objects.clear_cache()
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self):
        user = create_user()
        driver = self.driver
        url = self.live_server_url
        print(url)
        driver.get(url)
        sleep(100)
        assert 1 == 1
