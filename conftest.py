import pytest

from playwright.sync_api  import sync_playwright
from settings.browser_setting import BrowserSetting
from settings.project_setting import BROWSER_WIDTH, BROWSER_HEIGHT, PW_PAGE_TIMEOUT, PROJECT_HOST

@pytest.fixture(scope="class", name="browser")
def browser_instance(request):
    with sync_playwright() as playwright:
        new_browser = BrowserSetting().init_desktop_driver(playwright)
        request.cls.browser = new_browser
        yield new_browser
        new_browser.close()

@pytest.fixture(scope="function", name="page")
def page_instance(browser, request):
    # context = browser.new_context(record_video_dir="videos/")
    context = browser.new_context()
    request.cls.context = context
    new_page = context.new_page()
    new_page.set_viewport_size({'width': int(BROWSER_WIDTH), 'height': int(BROWSER_HEIGHT)})
    new_page.set_default_timeout(int(PW_PAGE_TIMEOUT))
    new_page.goto(PROJECT_HOST)
    yield new_page
    context.close()

@pytest.hookimpl()
def pytest_sessionfinish(exitstatus):
    print(f'\n\nProcess finished with exit code {exitstatus}')
    print('https://docs.pytest.org/en/latest/reference/exit-codes.html')
    if exitstatus == 5:
        print('\n[NO_TESTS_COLLECTED] pytest exit code 5')
