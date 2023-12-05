## ADACS Playwright Class

#### Usage
Use this class instead of the django StaticLiveServerTestCase.

It adds 2 useful class properties:

self.browser = A browser object from playwright used for accessing the page.
self.playwright = The return from sync_playwright().start()

This class only supports chronium and synchronous tests.

#### Example

```
from adacs_django_playwright.adacs_django_playwright import PlaywrightTestCase

class MyTestCase(PlaywrightTestCase):

  def awesome_test(self):
    page = self.browser.new_page()
    page.goto(f"{self.live_server_url}")
```
