import os
import time
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright


class PlaywrightTestCase(StaticLiveServerTestCase):
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.browser_context = cls.browser.new_context()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def login(self, user):
        """
        Logs the specified Django User object in to the browser and sets the corresponding session cookie
        """
        self.client.force_login(user)
        cookies = []
        for name, cookie in self.client.cookies.items():
            max_age = self.client.session.get_expiry_age()
            expires_time = time.time() + max_age
            cookies.append(
                {
                    'name': name,
                    'value': cookie.value,
                    'max_age': max_age,
                    'expires': int(expires_time),
                    'domain': urlparse(self.live_server_url).netloc,
                    'path': settings.SESSION_COOKIE_PATH or '',
                    'secure': settings.SESSION_COOKIE_SECURE or False,
                    'httponly': settings.SESSION_COOKIE_HTTPONLY or False,
                    'samesite': settings.SESSION_COOKIE_SAMESITE or ''
                }
            )

        self.browser_context.clear_cookies()
        self.browser_context.add_cookies(cookies)
