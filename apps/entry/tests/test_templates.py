from time import sleep

from django.contrib.contenttypes.models import ContentType
from django.test import LiveServerTestCase
from selenium import webdriver

class MatchFormTest(LiveServerTestCase):
    driver = None
    port = 8888

    @classmethod
    def setUpClass(cls):
        ContentType.objects.clear_cache()
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
        super().tearDownClass()

    def test_dsadas(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)
        assert 1 == 1
