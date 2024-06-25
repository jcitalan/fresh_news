from robocorp.tasks import task

from scrapers import BROWSER_OPTIONS, AngelesTimesScraper
from utils.browsers import SeleniumBrowser


@task
def Scraping():
    """
    TODO: Implement the logic for the task.
    """

    with SeleniumBrowser(
        browser_settings={
            "headless": False,
            "options": BROWSER_OPTIONS,
            "maximized": True,
        }
    ) as browser:
        _ = AngelesTimesScraper(browser=browser).extract()
