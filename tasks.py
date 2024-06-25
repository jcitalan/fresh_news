from robocorp.tasks import task

from scrapers import BROWSER_OPTIONS, AngelesTimesScraper
from utils.browsers import SeleniumBrowser


@task
def Scraping():
    """
    Main task function to perform the scraping operation.

    TODO: Implement the logic for the task.
    """
    try:
        with SeleniumBrowser(
            browser_settings={
                "headless": True,
                "options": BROWSER_OPTIONS,
                "maximized": True,
            }
        ) as browser:
            scraper = AngelesTimesScraper(browser=browser)
            scraper.extract()
    except Exception as e:
        print(f"Error during scraping task: {e}")
        raise
